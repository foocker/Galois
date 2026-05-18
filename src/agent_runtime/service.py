"""Backend-neutral HTTP API for a vendored mathematical research runtime."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import json
import os
from pathlib import Path
import queue
import re
import shutil
import subprocess
import threading
from typing import Any, Callable
import uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


CAPABILITY = "math_research"
SUPPORTED_PROMPT_SUFFIXES = {".md", ".markdown", ".txt", ".tex"}
STATIC_WORKSPACE_ENTRIES = ("AGENTS.md", ".agents", ".codex", "tests")
WRITABLE_WORKSPACE_DIRS = ("data", "input", "memory", "results", "downloads", "scripts", "logs")
RUN_SHARED_ENTRIES = ("memory", "results", "downloads", "scripts")


class RuntimeFile(BaseModel):
    name: str = Field(..., min_length=1)
    content: str = ""


class ProblemInput(BaseModel):
    content: str = Field(..., min_length=1)
    format: str = "markdown"


class ExecutionOptions(BaseModel):
    verification: bool = True
    model: str | None = None
    reasoning_effort: str | None = None


class ProjectCreateRequest(BaseModel):
    title: str | None = None
    problem: ProblemInput
    instructions: list[RuntimeFile] = Field(default_factory=list)
    references: list[RuntimeFile] = Field(default_factory=list)
    execution: ExecutionOptions = Field(default_factory=ExecutionOptions)


class ProjectContinueRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    instructions: list[RuntimeFile] = Field(default_factory=list)
    references: list[RuntimeFile] = Field(default_factory=list)
    execution: ExecutionOptions | None = None


@dataclass(slots=True)
class ResearchRunContext:
    project_id: str
    run_id: str
    run_dir: Path
    workspace_dir: Path
    problem_id: str
    problem_file: Path
    prompt_dir: Path
    reference_dir: Path
    results_dir: Path
    memory_dir: Path
    downloads_dir: Path
    scripts_dir: Path
    logs_dir: Path
    agent_state_file: Path
    verification_enabled: bool
    model: str | None = None
    reasoning_effort: str | None = None
    previous_run_id: str | None = None
    continuation_prompt: str | None = None


Launcher = Callable[[ResearchRunContext], None]


@dataclass(slots=True)
class RuntimeJob:
    context: ResearchRunContext
    launcher: Launcher


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _runtime_asset_dir() -> Path:
    return _repo_root() / "references" / "Lumen" / "agents" / "generation"


def _utc_stamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")


def _slug(value: str | None, fallback: str = "project") -> str:
    text = value or fallback
    normalized = re.sub(r"[^a-zA-Z0-9_-]+", "-", text.lower()).strip("-")
    return normalized[:72] or fallback


def _allocate_project_id(runtime_root: Path, title: str | None) -> str:
    base = _slug(title, "project")
    candidate = base
    suffix = 2
    while (runtime_root / "projects" / candidate).exists():
        candidate = f"{base}-{suffix}"
        suffix += 1
    return candidate


def _safe_relative_path(raw: str) -> Path:
    candidate = Path(raw.replace("\\", "/"))
    if candidate.is_absolute() or any(part in {"", ".", ".."} for part in candidate.parts):
        raise HTTPException(status_code=400, detail="invalid file name")
    return candidate


def _write_runtime_files(base_dir: Path, files: list[RuntimeFile]) -> None:
    base_dir.mkdir(parents=True, exist_ok=True)
    resolved_base = base_dir.resolve()
    for item in files:
        relative = _safe_relative_path(item.name)
        target = (base_dir / relative).resolve()
        if not target.is_relative_to(resolved_base):
            raise HTTPException(status_code=400, detail="invalid file name")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(item.content, encoding="utf-8")


def _serialize_files(files: list[RuntimeFile]) -> list[dict[str, str]]:
    return [{"name": item.name, "content": item.content} for item in files]


def _load_runtime_files(raw: Any) -> list[RuntimeFile]:
    if not isinstance(raw, list):
        return []
    files: list[RuntimeFile] = []
    for item in raw:
        if isinstance(item, dict):
            files.append(RuntimeFile(name=str(item.get("name", "")), content=str(item.get("content", ""))))
    return files


def _merge_runtime_files(base: list[RuntimeFile], extra: list[RuntimeFile]) -> list[RuntimeFile]:
    merged: dict[str, RuntimeFile] = {}
    for item in [*base, *extra]:
        _safe_relative_path(item.name)
        merged[item.name] = item
    return list(merged.values())


def _read_text(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    return path.read_text(encoding="utf-8")


def _project_state_path(project_dir: Path) -> Path:
    return project_dir / "project.json"


def _run_state_path(run_dir: Path) -> Path:
    return run_dir / "run.json"


def _run_dir_from_id(runtime_root: Path, run_id: str) -> Path:
    legacy_run_dir = runtime_root / "runs" / run_id
    if _run_state_path(legacy_run_dir).exists():
        return legacy_run_dir
    projects_dir = runtime_root / "projects"
    if projects_dir.exists():
        for candidate in projects_dir.glob(f"*/runs/{run_id}"):
            if _run_state_path(candidate).exists():
                return candidate
    raise FileNotFoundError(run_id)


def _events_path(run_dir: Path) -> Path:
    return run_dir / "events.jsonl"


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _append_event(run_dir: Path, event_type: str, status: str, message: str | None = None) -> None:
    payload: dict[str, Any] = {
        "type": event_type,
        "status": status,
        "created_at": datetime.now(UTC).isoformat(),
    }
    if message:
        payload["message"] = message
    path = _events_path(run_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _read_events(run_dir: Path) -> list[dict[str, Any]]:
    path = _events_path(run_dir)
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        payload = json.loads(line)
        if isinstance(payload, dict):
            events.append(payload)
    return events


def _ensure_symlink(target: Path, source: Path) -> None:
    if target.exists() or target.is_symlink():
        return
    target.symlink_to(source, target_is_directory=source.is_dir())


def _mcp_server_wrapper(source_server: Path) -> str:
    source_literal = json.dumps(str(source_server))
    return f'''from __future__ import annotations

from importlib import util as _importlib_util
from pathlib import Path as _Path
import sys as _sys

_WORKSPACE_ROOT = _Path(__file__).resolve().parents[1]
_SOURCE_SERVER = _Path({source_literal})
_SPEC = _importlib_util.spec_from_file_location("_agent_runtime_mcp_source", _SOURCE_SERVER)
if _SPEC is None or _SPEC.loader is None:
    raise ImportError(f"Could not load MCP server from {{_SOURCE_SERVER}}")
_SOURCE = _importlib_util.module_from_spec(_SPEC)
_WRITE_BYTECODE = _sys.dont_write_bytecode
_sys.dont_write_bytecode = True
try:
    _SPEC.loader.exec_module(_SOURCE)
finally:
    _sys.dont_write_bytecode = _WRITE_BYTECODE

REPO_ROOT = _WORKSPACE_ROOT
MEMORY_ROOT = REPO_ROOT / "memory"
_SOURCE.REPO_ROOT = REPO_ROOT
_SOURCE.MEMORY_ROOT = MEMORY_ROOT

CHANNEL_FILES = _SOURCE.CHANNEL_FILES
search_arxiv_theorems = _SOURCE.search_arxiv_theorems
verify_proof_service = _SOURCE.verify_proof_service
sanitize_problem_id = _SOURCE.sanitize_problem_id
build_problem_id = _SOURCE.build_problem_id
memory_init = _SOURCE.memory_init
memory_append = _SOURCE.memory_append
memory_search = _SOURCE.memory_search
branch_update = _SOURCE.branch_update


def build_mcp_app():
    return _SOURCE.build_mcp_app()


APP = build_mcp_app()


def main() -> None:
    if APP is None:
        raise SystemExit("fastmcp is not installed. Install requirements from mcp/requirements.txt first.")
    APP.run()


if __name__ == "__main__":
    main()
'''


def _mcp_init_wrapper() -> str:
    return '''from .server import (
    APP,
    branch_update,
    build_problem_id,
    memory_append,
    memory_init,
    memory_search,
    sanitize_problem_id,
    search_arxiv_theorems,
    verify_proof_service,
)

__all__ = [
    "APP",
    "branch_update",
    "build_problem_id",
    "memory_append",
    "memory_init",
    "memory_search",
    "sanitize_problem_id",
    "search_arxiv_theorems",
    "verify_proof_service",
]
'''


def _prepare_mcp_workspace(workspace_dir: Path, source: Path) -> None:
    target = workspace_dir / "mcp"
    if target.exists() and not target.is_dir():
        return
    target.mkdir(parents=True, exist_ok=True)
    server_file = target / "server.py"
    init_file = target / "__init__.py"
    requirements_file = target / "requirements.txt"
    if not server_file.exists():
        server_file.write_text(_mcp_server_wrapper(source / "mcp" / "server.py"), encoding="utf-8")
    if not init_file.exists():
        init_file.write_text(_mcp_init_wrapper(), encoding="utf-8")
    _ensure_symlink(requirements_file, source / "mcp" / "requirements.txt")


def _prepare_runtime_workspace(workspace_dir: Path) -> None:
    source = _runtime_asset_dir()
    if not source.exists():
        raise RuntimeError("research runtime assets are missing")

    workspace_dir.mkdir(parents=True, exist_ok=True)
    for name in STATIC_WORKSPACE_ENTRIES:
        _ensure_symlink(workspace_dir / name, source / name)
    _prepare_mcp_workspace(workspace_dir, source)
    for name in WRITABLE_WORKSPACE_DIRS:
        (workspace_dir / name).mkdir(parents=True, exist_ok=True)


def _extract_session_id(output: str) -> str:
    matches = re.findall(r"session id: ([0-9a-f-]+)", output, flags=re.IGNORECASE)
    return matches[-1] if matches else ""


def _read_prompt_files(prompt_dir: Path) -> str:
    if not prompt_dir.exists() or not prompt_dir.is_dir():
        return ""
    chunks: list[str] = []
    for path in sorted(prompt_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_PROMPT_SUFFIXES:
            continue
        content = path.read_text(encoding="utf-8").strip()
        if content:
            chunks.append(f"### {path.relative_to(prompt_dir).as_posix()}\n{content}")
    if not chunks:
        return ""
    return "\n\nAdditional user instructions:\n\n" + "\n\n".join(chunks)


def _artifact_dir(run_dir: Path) -> Path:
    return run_dir / "artifacts"


def _public_artifacts(context: ResearchRunContext) -> dict[str, Any]:
    artifact_dir = _artifact_dir(context.run_dir)
    solution = _read_text(artifact_dir / "solution.md")
    verified_solution = _read_text(artifact_dir / "verified_solution.md")
    if solution is None and verified_solution is None and not _run_state_path(context.run_dir).exists():
        result_dir = context.results_dir / context.problem_id
        solution = _read_text(result_dir / "blueprint.md")
        verified_solution = _read_text(result_dir / "blueprint_verified.md")
    return {
        "solution": {"content": solution} if solution is not None else None,
        "verified_solution": {"content": verified_solution} if verified_solution is not None else None,
    }


def _snapshot_artifacts(context: ResearchRunContext) -> None:
    result_dir = context.results_dir / context.problem_id
    artifact_dir = _artifact_dir(context.run_dir)
    artifact_dir.mkdir(parents=True, exist_ok=True)
    for source_name, target_name in (
        ("blueprint.md", "solution.md"),
        ("blueprint_verified.md", "verified_solution.md"),
    ):
        source = result_dir / source_name
        if source.exists() and source.is_file():
            shutil.copy2(source, artifact_dir / target_name)


def _prepare_run_directory(context: ResearchRunContext) -> None:
    context.logs_dir.mkdir(parents=True, exist_ok=True)
    _artifact_dir(context.run_dir).mkdir(parents=True, exist_ok=True)
    for name in RUN_SHARED_ENTRIES:
        _ensure_symlink(context.run_dir / name, context.workspace_dir / name)


def _public_run_payload(context: ResearchRunContext, *, status: str, continued_from: str | None = None) -> dict[str, Any]:
    return {
        "project_id": context.project_id,
        "run_id": context.run_id,
        "status": status,
        "capability": CAPABILITY,
        "continued_from": continued_from,
        "artifacts": _public_artifacts(context),
    }


def _public_project_payload(
    *,
    project_id: str,
    latest_run_id: str,
    status: str,
    title: str | None,
    continued_from: str | None = None,
) -> dict[str, Any]:
    links = {
        "run": f"/v1/runs/{latest_run_id}",
        "artifacts": f"/v1/runs/{latest_run_id}/artifacts",
        "events": f"/v1/runs/{latest_run_id}/events",
    }
    return {
        "project_id": project_id,
        "latest_run_id": latest_run_id,
        "status": status,
        "capability": CAPABILITY,
        "title": title,
        "continued_from": continued_from,
        "links": links,
    }


def _context_from_state(runtime_root: Path, run_id: str) -> ResearchRunContext:
    run_dir = _run_dir_from_id(runtime_root, run_id)
    state = _load_json(_run_state_path(run_dir))
    workspace_dir = Path(state.get("workspace_dir", run_dir / "workspace" / "generation"))
    context = ResearchRunContext(
        project_id=str(state["project_id"]),
        run_id=run_id,
        run_dir=run_dir,
        workspace_dir=workspace_dir,
        problem_id=str(state["problem_id"]),
        problem_file=Path(state["problem_file"]),
        prompt_dir=Path(state["prompt_dir"]),
        reference_dir=Path(state["reference_dir"]),
        results_dir=Path(state["results_dir"]),
        memory_dir=Path(state["memory_dir"]),
        downloads_dir=Path(state["downloads_dir"]),
        scripts_dir=Path(state["scripts_dir"]),
        logs_dir=Path(state["logs_dir"]),
        agent_state_file=Path(state.get("agent_state_file", run_dir / "state" / "agent_state.txt")),
        verification_enabled=bool(state["verification_enabled"]),
        model=state.get("model"),
        reasoning_effort=state.get("reasoning_effort"),
        previous_run_id=state.get("previous_run_id"),
        continuation_prompt=state.get("continuation_prompt"),
    )
    _prepare_run_directory(context)
    return context


def _write_context_state(context: ResearchRunContext) -> None:
    _write_json(
        _run_state_path(context.run_dir),
        {
            "project_id": context.project_id,
            "run_id": context.run_id,
            "workspace_dir": str(context.workspace_dir),
            "problem_id": context.problem_id,
            "problem_file": str(context.problem_file),
            "prompt_dir": str(context.prompt_dir),
            "reference_dir": str(context.reference_dir),
            "results_dir": str(context.results_dir),
            "memory_dir": str(context.memory_dir),
            "downloads_dir": str(context.downloads_dir),
            "scripts_dir": str(context.scripts_dir),
            "logs_dir": str(context.logs_dir),
            "agent_state_file": str(context.agent_state_file),
            "verification_enabled": context.verification_enabled,
            "model": context.model,
            "reasoning_effort": context.reasoning_effort,
            "previous_run_id": context.previous_run_id,
            "continuation_prompt": context.continuation_prompt,
        },
    )


def _new_context(
    *,
    project_dir: Path,
    project_id: str,
    problem_markdown: str,
    prompt_files: list[RuntimeFile],
    references: list[RuntimeFile],
    verification_enabled: bool,
    model: str | None,
    reasoning_effort: str | None,
    previous_run_id: str | None = None,
    continuation_prompt: str | None = None,
) -> ResearchRunContext:
    run_id = f"{_utc_stamp()}_{uuid.uuid4().hex[:8]}"
    run_dir = project_dir / "runs" / run_id
    workspace_dir = project_dir / "workspace" / "generation"
    _prepare_runtime_workspace(workspace_dir)

    problem_id = project_id
    problem_file = workspace_dir / "data" / f"{problem_id}.md"
    prompt_dir = workspace_dir / "input" / "prompts"
    reference_dir = workspace_dir / "data" / f"{problem_id}.refs"
    problem_file.parent.mkdir(parents=True, exist_ok=True)
    problem_file.write_text(problem_markdown, encoding="utf-8")
    _write_runtime_files(prompt_dir, prompt_files)
    _write_runtime_files(reference_dir, references)
    _snapshot_run_input(
        run_dir=run_dir,
        problem_markdown=problem_markdown,
        prompt_files=prompt_files,
        references=references,
        continuation_prompt=continuation_prompt,
    )

    return ResearchRunContext(
        project_id=project_id,
        run_id=run_id,
        run_dir=run_dir,
        workspace_dir=workspace_dir,
        problem_id=problem_id,
        problem_file=problem_file,
        prompt_dir=prompt_dir,
        reference_dir=reference_dir,
        results_dir=workspace_dir / "results",
        memory_dir=workspace_dir / "memory",
        downloads_dir=workspace_dir / "downloads",
        scripts_dir=workspace_dir / "scripts",
        logs_dir=run_dir / "logs",
        agent_state_file=run_dir / "state" / "agent_state.txt",
        verification_enabled=verification_enabled,
        model=model,
        reasoning_effort=reasoning_effort,
        previous_run_id=previous_run_id,
        continuation_prompt=continuation_prompt,
    )


def _snapshot_run_input(
    *,
    run_dir: Path,
    problem_markdown: str,
    prompt_files: list[RuntimeFile],
    references: list[RuntimeFile],
    continuation_prompt: str | None,
) -> None:
    input_dir = run_dir / "input"
    input_dir.mkdir(parents=True, exist_ok=True)
    (input_dir / "problem.md").write_text(problem_markdown, encoding="utf-8")
    if continuation_prompt:
        (input_dir / "continuation.md").write_text(continuation_prompt, encoding="utf-8")
    _write_runtime_files(input_dir / "prompts", prompt_files)
    _write_runtime_files(input_dir / "references", references)


def _build_agent_prompt(context: ResearchRunContext) -> str:
    problem_path = context.problem_file.relative_to(context.workspace_dir).as_posix()
    reference_path = context.reference_dir.relative_to(context.workspace_dir).as_posix()
    prompt = (
        f"Use AGENTS.md exactly to solve the math problem in {problem_path}. "
        f"Use problem_id={context.problem_id}. "
        f"Use reference_dir={reference_path} if it exists."
    )
    if not context.verification_enabled:
        prompt += " Verification is disabled for this run; produce the best complete blueprint.md without requiring verifier success."
    if context.previous_run_id:
        prompt += (
            " Continue this existing research project from the existing results, memory, downloads, and scripts in this workspace. "
            "Do not restart from scratch unless the prior artifacts are unusable."
        )
    if context.continuation_prompt:
        prompt += f"\n\nContinuation request:\n{context.continuation_prompt.strip()}"
    prompt += _read_prompt_files(context.prompt_dir)
    return prompt


def _default_launcher(context: ResearchRunContext) -> None:
    codex_bin = os.getenv("CODEX_BIN", "codex")
    model = context.model or os.getenv("CODEX_MODEL", "gpt-5.4")
    reasoning_effort = context.reasoning_effort or os.getenv("CODEX_REASONING_EFFORT", "xhigh")
    command = [
        codex_bin,
        "exec",
        "-C",
        str(context.workspace_dir),
        "-m",
        model,
        "--config",
        f'model_reasoning_effort="{reasoning_effort}"',
        "--dangerously-bypass-approvals-and-sandbox",
        _build_agent_prompt(context),
    ]

    context.logs_dir.mkdir(parents=True, exist_ok=True)
    log_path = context.logs_dir / context.problem_id / "run.md"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(
        command,
        cwd=context.workspace_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    log_path.write_text(completed.stdout or "", encoding="utf-8")
    session_id = _extract_session_id(completed.stdout or "")
    if session_id:
        context.agent_state_file.parent.mkdir(parents=True, exist_ok=True)
        context.agent_state_file.write_text(f"{session_id}\n", encoding="utf-8")
    if completed.returncode != 0:
        raise RuntimeError(f"research runtime command failed with exit code {completed.returncode}")


def _run_context(context: ResearchRunContext, launcher: Launcher) -> None:
    try:
        _set_run_status(context.run_dir, "running")
        _append_event(context.run_dir, "running", "running")
        launcher(context)
        _snapshot_artifacts(context)
        _set_run_status(context.run_dir, "succeeded")
        _append_event(context.run_dir, "succeeded", "succeeded")
    except Exception as exc:  # pragma: no cover - async failures are inspected through run state
        _set_run_status(context.run_dir, "failed", error=str(exc))
        _append_event(context.run_dir, "failed", "failed", message="runtime execution failed")


class RuntimeScheduler:
    def __init__(self, *, max_concurrency: int) -> None:
        self.max_concurrency = max(1, max_concurrency)
        self._jobs: queue.Queue[RuntimeJob] = queue.Queue()
        self._project_locks: dict[str, threading.Lock] = {}
        self._project_locks_guard = threading.Lock()
        for index in range(self.max_concurrency):
            thread = threading.Thread(target=self._worker, name=f"research-runtime-worker-{index + 1}", daemon=True)
            thread.start()

    def submit(self, context: ResearchRunContext, launcher: Launcher) -> str:
        _write_context_state(context)
        _prepare_run_directory(context)
        _set_run_status(context.run_dir, "queued")
        _append_event(context.run_dir, "created", "queued")
        self._jobs.put(RuntimeJob(context=context, launcher=launcher))
        return "queued"

    def _project_lock(self, project_id: str) -> threading.Lock:
        with self._project_locks_guard:
            lock = self._project_locks.get(project_id)
            if lock is None:
                lock = threading.Lock()
                self._project_locks[project_id] = lock
            return lock

    def _worker(self) -> None:
        while True:
            job = self._jobs.get()
            try:
                with self._project_lock(job.context.project_id):
                    _run_context(job.context, job.launcher)
            finally:
                self._jobs.task_done()


def _launch_context(
    *,
    context: ResearchRunContext,
    launcher: Launcher,
    run_async: bool,
    scheduler: RuntimeScheduler | None = None,
) -> str:
    if run_async:
        if scheduler is None:
            raise RuntimeError("runtime scheduler is required for async runs")
        return scheduler.submit(context, launcher)
    _write_context_state(context)
    _prepare_run_directory(context)
    _set_run_status(context.run_dir, "queued")
    _append_event(context.run_dir, "created", "queued")
    _run_context(context, launcher)
    return str(_load_json(_run_state_path(context.run_dir)).get("status", "unknown"))


def _set_run_status(run_dir: Path, status: str, error: str | None = None) -> None:
    state = _load_json(_run_state_path(run_dir))
    state["status"] = status
    if error is None:
        state.pop("error", None)
    if error:
        state["error"] = error
    _write_json(_run_state_path(run_dir), state)


def create_app(
    *,
    runtime_root: Path,
    launcher: Launcher | None = None,
    run_async: bool = True,
    max_concurrency: int | None = None,
) -> FastAPI:
    runtime_root = runtime_root.resolve()
    runtime_root.mkdir(parents=True, exist_ok=True)
    launcher = launcher or _default_launcher
    if max_concurrency is None:
        max_concurrency = int(os.getenv("AGENT_RUNTIME_MAX_CONCURRENCY", "2"))
    scheduler = RuntimeScheduler(max_concurrency=max_concurrency) if run_async else None
    app = FastAPI(title="Research Runtime API", version="0.1.0")

    @app.get("/v1/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "capability": CAPABILITY}

    @app.post("/v1/projects", status_code=202)
    def create_project(request: ProjectCreateRequest) -> dict[str, Any]:
        project_id = _allocate_project_id(runtime_root, request.title)
        project_dir = runtime_root / "projects" / project_id
        project_dir.mkdir(parents=True, exist_ok=True)
        context = _new_context(
            project_dir=project_dir,
            project_id=project_id,
            problem_markdown=request.problem.content,
            prompt_files=request.instructions,
            references=request.references,
            verification_enabled=request.execution.verification,
            model=request.execution.model,
            reasoning_effort=request.execution.reasoning_effort,
        )
        status = _launch_context(context=context, launcher=launcher, run_async=run_async, scheduler=scheduler)
        _write_json(
            _project_state_path(project_dir),
            {
                "project_id": project_id,
                "title": request.title,
                "problem": request.problem.model_dump(),
                "instructions": _serialize_files(request.instructions),
                "references": _serialize_files(request.references),
                "execution": request.execution.model_dump(),
                "latest_run_id": context.run_id,
            },
        )
        return _public_project_payload(
            project_id=project_id,
            latest_run_id=context.run_id,
            status=status,
            title=request.title,
        )

    @app.post("/v1/projects/{project_id}/runs", status_code=202)
    def continue_project(project_id: str, request: ProjectContinueRequest) -> dict[str, Any]:
        project_dir = runtime_root / "projects" / project_id
        try:
            project = _load_json(_project_state_path(project_dir))
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail="project not found") from exc
        previous_run_id = str(project["latest_run_id"])
        prompt_files = _merge_runtime_files(_load_runtime_files(project.get("instructions")), request.instructions)
        references = _merge_runtime_files(_load_runtime_files(project.get("references")), request.references)
        prior_execution = project.get("execution") if isinstance(project.get("execution"), dict) else {}
        execution = request.execution or ExecutionOptions(
            verification=bool(prior_execution.get("verification", True)),
            model=prior_execution.get("model"),
            reasoning_effort=prior_execution.get("reasoning_effort"),
        )
        context = _new_context(
            project_dir=project_dir,
            project_id=project_id,
            problem_markdown=str(project.get("problem", {}).get("content", "")),
            prompt_files=prompt_files,
            references=references,
            verification_enabled=execution.verification,
            model=execution.model,
            reasoning_effort=execution.reasoning_effort,
            previous_run_id=previous_run_id,
            continuation_prompt=request.prompt,
        )
        status = _launch_context(context=context, launcher=launcher, run_async=run_async, scheduler=scheduler)
        project["latest_run_id"] = context.run_id
        project["instructions"] = _serialize_files(prompt_files)
        project["references"] = _serialize_files(references)
        project["execution"] = execution.model_dump()
        _write_json(_project_state_path(project_dir), project)
        return _public_project_payload(
            project_id=project_id,
            latest_run_id=context.run_id,
            status=status,
            title=project.get("title"),
            continued_from=previous_run_id,
        )

    @app.get("/v1/runs/{run_id}")
    def get_run(run_id: str) -> dict[str, Any]:
        try:
            context = _context_from_state(runtime_root, run_id)
            state = _load_json(_run_state_path(context.run_dir))
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail="run not found") from exc
        return _public_run_payload(
            context,
            status=str(state.get("status", "unknown")),
            continued_from=context.previous_run_id,
        )

    @app.get("/v1/runs/{run_id}/artifacts")
    def get_run_artifacts(run_id: str) -> dict[str, Any]:
        try:
            context = _context_from_state(runtime_root, run_id)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail="run not found") from exc
        return {
            "run_id": run_id,
            "capability": CAPABILITY,
            "artifacts": _public_artifacts(context),
        }

    @app.get("/v1/runs/{run_id}/events")
    def get_run_events(run_id: str) -> dict[str, Any]:
        try:
            context = _context_from_state(runtime_root, run_id)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail="run not found")
        if not context.run_dir.exists():
            raise HTTPException(status_code=404, detail="run not found")
        return {
            "run_id": run_id,
            "capability": CAPABILITY,
            "events": _read_events(context.run_dir),
        }

    return app


def serve(
    runtime_root: Path,
    host: str = "127.0.0.1",
    port: int = 8765,
    max_concurrency: int | None = None,
) -> None:
    import uvicorn

    uvicorn.run(create_app(runtime_root=runtime_root, max_concurrency=max_concurrency), host=host, port=port)


def launch_subprocess(context: ResearchRunContext, *, command: list[str]) -> None:
    completed = subprocess.run(command, cwd=context.workspace_dir, text=True, check=False)
    if completed.returncode != 0:
        raise RuntimeError(f"research runtime command failed with exit code {completed.returncode}")
