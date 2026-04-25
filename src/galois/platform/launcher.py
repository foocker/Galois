"""Workflow launching and run-directory logging.

The launcher uses the OpenGauss-style subagent core in ``subagents.py``:
each workflow is represented by a registered task, a background thread, and
when active, a child process.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import shlex
import time
from urllib import error, request

from .contracts import LaunchMode, WorkflowLaunch
from .run_registry import append_event, utc_now_iso
from .serialization import sanitize_for_run_artifact
from .subagents import SubagentManager, SubagentTask


@dataclass(slots=True)
class WorkflowResult:
    workflow: str
    mode: LaunchMode
    command: list[str]
    cwd: str
    started_at: str
    finished_at: str
    pid: int | None
    exit_code: int | None
    stdout_path: str
    stderr_path: str
    status: str
    error: str | None = None
    subagent_task_id: str | None = None
    subagent_session_id: str | None = None


@dataclass(slots=True)
class RunningService:
    launch: WorkflowLaunch
    manager: SubagentManager
    task_id: str
    started_at: str
    stdout_path: str
    stderr_path: str


def _command(launch: WorkflowLaunch) -> list[str]:
    return [launch.entrypoint, *launch.arguments]


def _merged_env(launch: WorkflowLaunch) -> dict[str, str]:
    env = os.environ.copy()
    env.update(launch.environment)
    return env


def _workflow_dir(run_dir: Path, launch: WorkflowLaunch) -> Path:
    return run_dir / launch.kind.value


def _write_launch_metadata(run_dir: Path, workflow_dir: Path, launch: WorkflowLaunch, argv: list[str]) -> None:
    payload = {
        "kind": launch.kind.value,
        "mode": launch.mode.value,
        "cwd": launch.cwd,
        "entrypoint": launch.entrypoint,
        "arguments": launch.arguments,
        "command": argv,
        "command_string": shlex.join(argv),
        "environment": launch.environment,
        "healthcheck_url": launch.healthcheck_url,
        "startup_timeout_seconds": launch.startup_timeout_seconds,
    }
    (workflow_dir / "launch.json").write_text(
        json.dumps(sanitize_for_run_artifact(payload, run_dir=run_dir), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _prepare_workflow(run_dir: Path, launch: WorkflowLaunch) -> tuple[Path, Path, list[str]]:
    workflow_dir = _workflow_dir(run_dir, launch)
    log_dir = workflow_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    attempt = 1
    while (log_dir / f"stdout_r{attempt}.log").exists() or (log_dir / f"stderr_r{attempt}.log").exists():
        attempt += 1

    stdout_path = log_dir / f"stdout_r{attempt}.log"
    stderr_path = log_dir / f"stderr_r{attempt}.log"
    argv = _command(launch)
    _write_launch_metadata(run_dir, workflow_dir, launch, argv)
    return stdout_path, stderr_path, argv


def _wait_for_health(url: str, timeout_seconds: int) -> bool:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        try:
            with request.urlopen(url, timeout=1) as response:
                if 200 <= response.status < 300:
                    return True
        except (OSError, error.URLError):
            time.sleep(0.25)
    return False


def _wait_for_process(task: SubagentTask, timeout_seconds: int) -> bool:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if task.process is not None:
            return True
        if task.thread is not None and not task.thread.is_alive():
            return False
        time.sleep(0.01)
    return task.process is not None


def _append_started_event(
    *,
    run_dir: Path,
    run_id: str,
    launch: WorkflowLaunch,
    argv: list[str],
    stdout_path: Path,
    stderr_path: Path,
) -> str:
    started_at = utc_now_iso()
    append_event(
        run_dir,
        run_id=run_id,
        workflow=launch.kind.value,
        event_type="workflow_started",
        payload={
            "mode": launch.mode.value,
            "cwd": launch.cwd,
            "command": argv,
            "stdout_path": str(stdout_path),
            "stderr_path": str(stderr_path),
            "healthcheck_url": launch.healthcheck_url,
        },
    )
    return started_at


def _append_finished_event(
    *,
    run_dir: Path,
    run_id: str,
    result: WorkflowResult,
) -> None:
    append_event(
        run_dir,
        run_id=run_id,
        workflow=result.workflow,
        event_type="workflow_finished",
        payload={
            "mode": result.mode.value,
            "pid": result.pid,
            "exit_code": result.exit_code,
            "status": result.status,
            "stdout_path": result.stdout_path,
            "stderr_path": result.stderr_path,
            "error": result.error,
            "subagent_task_id": result.subagent_task_id,
            "subagent_session_id": result.subagent_session_id,
        },
    )


def _result_from_task(
    *,
    launch: WorkflowLaunch,
    argv: list[str],
    started_at: str,
    stdout_path: Path | str,
    stderr_path: Path | str,
    task: SubagentTask,
    status: str | None = None,
    error_message: str | None = None,
) -> WorkflowResult:
    task_status = status or ("succeeded" if task.status == "complete" and task.returncode == 0 else "failed")
    return WorkflowResult(
        workflow=launch.kind.value,
        mode=launch.mode,
        command=argv,
        cwd=launch.cwd,
        started_at=started_at,
        finished_at=utc_now_iso(),
        pid=task.pid,
        exit_code=task.returncode,
        stdout_path=str(stdout_path),
        stderr_path=str(stderr_path),
        status=task_status,
        error=error_message if error_message is not None else task.error,
        subagent_task_id=task.task_id,
        subagent_session_id=task.session_id,
    )


def run_oneshot_workflow(
    *,
    run_dir: Path,
    run_id: str,
    launch: WorkflowLaunch,
    manager: SubagentManager | None = None,
) -> WorkflowResult:
    stdout_path, stderr_path, argv = _prepare_workflow(run_dir, launch)
    started_at = _append_started_event(
        run_dir=run_dir,
        run_id=run_id,
        launch=launch,
        argv=argv,
        stdout_path=stdout_path,
        stderr_path=stderr_path,
    )

    manager = manager or SubagentManager()
    task = manager.spawn_process(
        f"{launch.kind.value} workflow",
        argv=argv,
        cwd=launch.cwd,
        env=_merged_env(launch),
        stdout_path=stdout_path,
        stderr_path=stderr_path,
        workflow_kind=launch.kind.value,
        backend_name=launch.entrypoint,
    )
    task = manager.wait(task.task_id)
    result = _result_from_task(
        launch=launch,
        argv=argv,
        started_at=started_at,
        stdout_path=stdout_path,
        stderr_path=stderr_path,
        task=task,
    )
    _append_finished_event(run_dir=run_dir, run_id=run_id, result=result)
    return result


def start_service_workflow(
    *,
    run_dir: Path,
    run_id: str,
    launch: WorkflowLaunch,
    manager: SubagentManager | None = None,
) -> RunningService:
    stdout_path, stderr_path, argv = _prepare_workflow(run_dir, launch)
    started_at = _append_started_event(
        run_dir=run_dir,
        run_id=run_id,
        launch=launch,
        argv=argv,
        stdout_path=stdout_path,
        stderr_path=stderr_path,
    )

    manager = manager or SubagentManager()
    task = manager.spawn_process(
        f"{launch.kind.value} service",
        argv=argv,
        cwd=launch.cwd,
        env=_merged_env(launch),
        stdout_path=stdout_path,
        stderr_path=stderr_path,
        workflow_kind=launch.kind.value,
        backend_name=launch.entrypoint,
        start_new_session=True,
    )

    error_message: str | None = None
    try:
        if not _wait_for_process(task, launch.startup_timeout_seconds):
            raise RuntimeError("service process did not start")
        if launch.healthcheck_url and not _wait_for_health(
            launch.healthcheck_url, launch.startup_timeout_seconds
        ):
            raise RuntimeError(f"healthcheck failed: {launch.healthcheck_url}")
        if task.process is None or task.process.poll() is not None:
            raise RuntimeError(f"service exited during startup with exit code {task.returncode}")

        append_event(
            run_dir,
            run_id=run_id,
            workflow=launch.kind.value,
            event_type="workflow_healthy",
            payload={
                "pid": task.pid,
                "healthcheck_url": launch.healthcheck_url,
                "subagent_task_id": task.task_id,
                "subagent_session_id": task.session_id,
            },
        )
        return RunningService(
            launch=launch,
            manager=manager,
            task_id=task.task_id,
            started_at=started_at,
            stdout_path=str(stdout_path),
            stderr_path=str(stderr_path),
        )
    except Exception as exc:
        error_message = str(exc)
        manager.cancel(task.task_id)
        task = manager.wait(task.task_id, timeout=5)
        with stderr_path.open("a", encoding="utf-8") as handle:
            handle.write(f"{error_message}\n")
        result = _result_from_task(
            launch=launch,
            argv=argv,
            started_at=started_at,
            stdout_path=stdout_path,
            stderr_path=stderr_path,
            task=task,
            status="failed",
            error_message=error_message,
        )
        _append_finished_event(run_dir=run_dir, run_id=run_id, result=result)
        raise


def stop_service_workflow(
    *,
    run_dir: Path,
    run_id: str,
    service: RunningService,
    failed_error: str | None = None,
) -> WorkflowResult:
    task = service.manager.get_task(service.task_id)
    if task is None:
        raise RuntimeError(f"service task not found: {service.task_id}")

    launch = service.launch
    argv = _command(launch)
    service_was_running = task.process is not None and task.process.poll() is None
    if service_was_running:
        service.manager.stop(task.task_id)
    task = service.manager.wait(task.task_id, timeout=5)

    status = "failed" if failed_error else "succeeded"
    error_message = failed_error
    if not service_was_running and failed_error is None:
        status = "failed"
        error_message = f"service exited before cleanup with exit code {task.returncode}"

    result = _result_from_task(
        launch=launch,
        argv=argv,
        started_at=service.started_at,
        stdout_path=service.stdout_path,
        stderr_path=service.stderr_path,
        task=task,
        status=status,
        error_message=error_message,
    )
    _append_finished_event(run_dir=run_dir, run_id=run_id, result=result)
    return result


def run_service_workflow(
    *,
    run_dir: Path,
    run_id: str,
    launch: WorkflowLaunch,
    manager: SubagentManager | None = None,
) -> WorkflowResult:
    service = start_service_workflow(run_dir=run_dir, run_id=run_id, launch=launch, manager=manager)
    return stop_service_workflow(run_dir=run_dir, run_id=run_id, service=service)


def run_workflow(
    *,
    run_dir: Path,
    run_id: str,
    launch: WorkflowLaunch,
    manager: SubagentManager | None = None,
) -> WorkflowResult:
    if launch.mode == LaunchMode.SERVICE:
        return run_service_workflow(run_dir=run_dir, run_id=run_id, launch=launch, manager=manager)
    return run_oneshot_workflow(run_dir=run_dir, run_id=run_id, launch=launch, manager=manager)
