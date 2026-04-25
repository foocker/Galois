"""Threaded subagent task registry for workflow processes.

This is the Galois equivalent of the useful core in OpenGauss'
``swarm_manager.py``: a thread-safe task registry where each task owns a
background thread and, when launched, a child process.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from collections import deque
from datetime import UTC, datetime
import json
import os
from pathlib import Path
import signal
import subprocess
import threading
import time
import uuid
from typing import Callable

from .serialization import sanitize_for_run_artifact


_RECENT_OUTPUT_LIMIT = 256 * 1024


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


@dataclass(slots=True)
class SubagentTask:
    task_id: str
    description: str
    workflow_kind: str = ""
    workflow_command: str = ""
    working_dir: str = ""
    backend_name: str = ""
    status: str = "queued"
    session_id: str | None = None
    thread: threading.Thread | None = field(default=None, repr=False)
    process: subprocess.Popen[str] | None = field(default=None, repr=False)
    pid: int | None = None
    process_group: bool = False
    start_time: float | None = None
    end_time: float | None = None
    progress: str = "Waiting"
    result: str | None = None
    error: str | None = None
    returncode: int | None = None
    stdout_path: str = ""
    stderr_path: str = ""
    created_at: str = field(default_factory=_utc_now)
    recent_output: str = field(default="", repr=False)
    output_tail_lines: deque[str] = field(default_factory=lambda: deque(maxlen=200), repr=False)

    def snapshot(self) -> dict:
        return {
            "task_id": self.task_id,
            "description": self.description,
            "workflow_kind": self.workflow_kind,
            "workflow_command": self.workflow_command,
            "working_dir": self.working_dir,
            "backend_name": self.backend_name,
            "status": self.status,
            "session_id": self.session_id,
            "pid": self.pid,
            "process_group": self.process_group,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "progress": self.progress,
            "result": self.result,
            "error": self.error,
            "returncode": self.returncode,
            "stdout_path": self.stdout_path,
            "stderr_path": self.stderr_path,
            "created_at": self.created_at,
            "recent_output": self.recent_output,
            "output_tail_lines": list(self.output_tail_lines),
            "thread_alive": self.thread.is_alive() if self.thread is not None else False,
            "process_alive": self.process.poll() is None if self.process is not None else False,
        }


class SubagentManager:
    """Thread-safe registry for background workflow subagents."""

    def __init__(self) -> None:
        self.tasks: dict[str, SubagentTask] = {}
        self._counter = 0
        self._lock = threading.Lock()
        self._on_complete: Callable[[SubagentTask], None] | None = None

    def set_on_complete(self, callback: Callable[[SubagentTask], None] | None) -> None:
        self._on_complete = callback

    def spawn(
        self,
        description: str,
        *,
        workflow_kind: str = "",
        workflow_command: str = "",
        working_dir: str = "",
        backend_name: str = "",
        run_fn: Callable[..., None] | None = None,
        run_kwargs: dict | None = None,
    ) -> SubagentTask:
        with self._lock:
            self._counter += 1
            task_id = f"ga-{self._counter:03d}"
            task = SubagentTask(
                task_id=task_id,
                description=description,
                workflow_kind=workflow_kind,
                workflow_command=workflow_command,
                working_dir=working_dir,
                backend_name=backend_name,
                session_id=f"ga_{uuid.uuid4().hex[:8]}",
            )
            self.tasks[task_id] = task

        if run_fn is not None:

            def _target() -> None:
                task.status = "running"
                task.start_time = time.time()
                try:
                    run_fn(task, **(run_kwargs or {}))
                    with self._lock:
                        if task.status == "running":
                            task.status = "complete"
                except Exception as exc:
                    with self._lock:
                        task.status = "failed"
                        task.error = str(exc)
                finally:
                    with self._lock:
                        if task.end_time is None:
                            task.end_time = time.time()
                    if self._on_complete is not None:
                        try:
                            self._on_complete(task)
                        except Exception:
                            pass

            thread = threading.Thread(target=_target, daemon=True, name=f"galois-subagent-{task_id}")
            task.thread = thread
            thread.start()

        return task

    def spawn_process(
        self,
        description: str,
        *,
        argv: list[str],
        cwd: str,
        env: dict[str, str],
        stdout_path: Path,
        stderr_path: Path,
        workflow_kind: str = "",
        backend_name: str = "",
        start_new_session: bool = False,
    ) -> SubagentTask:
        return self.spawn(
            description,
            workflow_kind=workflow_kind,
            workflow_command=" ".join(argv),
            working_dir=cwd,
            backend_name=backend_name,
            run_fn=_run_process_task,
            run_kwargs={
                "argv": argv,
                "cwd": cwd,
                "env": env,
                "stdout_path": stdout_path,
                "stderr_path": stderr_path,
                "start_new_session": start_new_session,
            },
        )

    def wait(self, task_id: str, timeout: float | None = None) -> SubagentTask:
        task = self.get_task(task_id)
        if task is None:
            raise KeyError(task_id)
        if task.thread is not None:
            task.thread.join(timeout)
        return task

    def wait_all(self, timeout: float | None = None) -> list[SubagentTask]:
        with self._lock:
            task_ids = list(self.tasks)
        return [self.wait(task_id, timeout=timeout) for task_id in task_ids]

    def get_task(self, task_id: str) -> SubagentTask | None:
        with self._lock:
            return self.tasks.get(task_id)

    def list_tasks(self, status: str | None = None) -> list[SubagentTask]:
        with self._lock:
            tasks = list(self.tasks.values())
        if status is not None:
            return [task for task in tasks if task.status == status]
        return tasks

    def cancel(self, task_id: str) -> bool:
        return self._terminate(task_id, status="cancelled")

    def stop(self, task_id: str) -> bool:
        return self._terminate(task_id, status="stopping")

    def _terminate(self, task_id: str, *, status: str) -> bool:
        with self._lock:
            task = self.tasks.get(task_id)
            if task is None or task.status in {"complete", "failed", "cancelled", "stopped"}:
                return False
            task.status = status
            task.end_time = time.time()
        if task.process is not None:
            try:
                if task.process.poll() is None:
                    if task.process_group:
                        os.killpg(task.process.pid, signal.SIGTERM)
                    else:
                        task.process.terminate()
            except OSError:
                pass
        return True

    def counts(self) -> dict[str, int]:
        out: dict[str, int] = {}
        with self._lock:
            for task in self.tasks.values():
                out[task.status] = out.get(task.status, 0) + 1
        return out

    def snapshots(self) -> list[dict]:
        with self._lock:
            return [task.snapshot() for task in self.tasks.values()]

    def write_snapshots(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(sanitize_for_run_artifact(self.snapshots(), run_dir=path.parent), ensure_ascii=False, indent=2)
            + "\n",
            encoding="utf-8",
        )


def _run_process_task(
    task: SubagentTask,
    *,
    argv: list[str],
    cwd: str,
    env: dict[str, str],
    stdout_path: Path,
    stderr_path: Path,
    start_new_session: bool = False,
) -> None:
    stdout_path.parent.mkdir(parents=True, exist_ok=True)
    stderr_path.parent.mkdir(parents=True, exist_ok=True)
    task.stdout_path = str(stdout_path)
    task.stderr_path = str(stderr_path)
    task.process_group = start_new_session
    task.progress = "Launching process"

    try:
        proc = subprocess.Popen(
            argv,
            cwd=cwd,
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=False,
            bufsize=1,
            start_new_session=start_new_session,
        )
        task.process = proc
        task.pid = proc.pid
        task.progress = "Process running"

        pump_threads = [
            threading.Thread(
                target=_pump_stream,
                args=(task, proc.stdout, stdout_path, "stdout"),
                daemon=True,
                name=f"galois-subagent-{task.task_id}-stdout",
            ),
            threading.Thread(
                target=_pump_stream,
                args=(task, proc.stderr, stderr_path, "stderr"),
                daemon=True,
                name=f"galois-subagent-{task.task_id}-stderr",
            ),
        ]
        for pump_thread in pump_threads:
            pump_thread.start()

        task.returncode = proc.wait()
        for pump_thread in pump_threads:
            pump_thread.join(timeout=2)

        if task.status == "cancelled":
            task.progress = "Cancelled"
        elif task.status == "stopping":
            task.status = "stopped"
            task.progress = "Stopped"
        elif task.returncode == 0:
            task.progress = "Process completed"
        else:
            task.status = "failed"
            task.error = f"exit {task.returncode}"
            task.progress = "Process failed"
    except FileNotFoundError as exc:
        task.returncode = 127
        task.status = "failed"
        task.error = f"entrypoint not found: {argv[0]}"
        stderr_path.write_text(f"{task.error}\n{exc}\n", encoding="utf-8")
        task.progress = "Launch failed"
    except Exception as exc:
        task.returncode = 1
        task.status = "failed"
        task.error = str(exc)
        stderr_path.write_text(f"{task.error}\n", encoding="utf-8")
        task.progress = "Unexpected error"
    finally:
        task.process = None


def _remember_output(task: SubagentTask, stream_name: str, text: str) -> None:
    if not text:
        return
    chunk = f"[{stream_name}] {text}"
    task.recent_output += chunk
    if len(task.recent_output) > _RECENT_OUTPUT_LIMIT:
        task.recent_output = task.recent_output[-_RECENT_OUTPUT_LIMIT:]
    for line in text.splitlines():
        if line:
            task.output_tail_lines.append(f"{stream_name}: {line}")


def _pump_stream(
    task: SubagentTask,
    stream,
    destination: Path,
    stream_name: str,
) -> None:
    if stream is None:
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as handle:
        while True:
            chunk = stream.readline()
            if chunk == "":
                break
            handle.write(chunk)
            handle.flush()
            _remember_output(task, stream_name, chunk)


def terminate_process_group(proc: subprocess.Popen[str], timeout: float = 5) -> None:
    if proc.poll() is not None:
        return
    try:
        os.killpg(proc.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    except OSError:
        proc.terminate()
    try:
        proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=timeout)
