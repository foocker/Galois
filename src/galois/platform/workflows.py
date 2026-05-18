"""Workflow inventory and launch-plan helpers."""

from __future__ import annotations

import os
from pathlib import Path
import sys

from .artifacts import reasoning_workspace_dir
from .config import PlatformConfig, model_runtime_environment
from .contracts import LaunchMode, ProblemInput, WorkflowKind, WorkflowLaunch
from .paths import RepoPaths


def _venv_path_prefix_env() -> dict[str, str]:
    python_bin = Path(sys.executable)
    if not python_bin.is_absolute():
        python_bin = (Path.cwd() / python_bin).resolve()
    venv_bin = str(python_bin.parent)
    existing_path = os.environ.get("PATH", "")
    if existing_path:
        path_parts = [venv_bin] + [
            segment for segment in existing_path.split(os.pathsep) if segment and segment != venv_bin
        ]
        new_path = os.pathsep.join(path_parts)
    else:
        new_path = venv_bin
    return {
        "PATH": new_path,
        "GALOIS_PYTHON_BIN": str(python_bin),
    }


def _resolve_problem_path(problem: ProblemInput, paths: RepoPaths) -> Path:
    candidate = Path(problem.problem_path)
    if not candidate.is_absolute():
        candidate = paths.repo_root / candidate
    return candidate.resolve()


def _reasoning_problem_path(problem: ProblemInput, paths: RepoPaths, run_dir: Path | None = None) -> str:
    problem_path = _resolve_problem_path(problem, paths)
    if not problem_path.exists():
        raise FileNotFoundError(f"problem file not found: {problem_path}")
    if run_dir is not None:
        return str(run_dir / "problem" / "statement.md")
    try:
        relative = problem_path.relative_to(paths.reasoning_dir)
    except ValueError as exc:
        raise ValueError(
            f"reasoning problem path must live under {paths.reasoning_dir}: {problem_path}"
        ) from exc
    return relative.as_posix()


def build_reasoning_launch(
    *,
    config: PlatformConfig,
    paths: RepoPaths,
    problem: ProblemInput,
    run_dir: Path | None = None,
    verification_enabled: bool = True,
) -> WorkflowLaunch:
    cwd = paths.reasoning_dir
    environment = {
        "CODEX_BIN": config.codex.bin,
        "MODEL": config.model,
        "REASONING_EFFORT": config.model_reasoning_effort,
        "PROBLEM_FILE": _reasoning_problem_path(problem, paths, run_dir=run_dir),
        "GALOIS_REASONING_PROBLEM_ID": problem.problem_id,
        "GALOIS_REASONING_VERIFICATION_ENABLED": "1" if verification_enabled else "0",
        "GALOIS_REASONING_VERIFICATION_MODE": "external" if verification_enabled else "disabled",
        "RESUME": "auto" if config.resume_enabled else "0",
        **_venv_path_prefix_env(),
        **model_runtime_environment(config),
    }
    if run_dir is not None:
        runtime_dir = reasoning_workspace_dir(run_dir)
        environment.update(
            {
                "GALOIS_REASONING_RUNTIME_DIR": str(runtime_dir),
                "LOG_DIR": str(run_dir / "reasoning" / "logs"),
                "RESULTS_DIR": str(runtime_dir / "results"),
                "MEMORY_DIR": str(runtime_dir / "memory"),
                "DOWNLOADS_DIR": str(runtime_dir / "downloads"),
                "SCRIPTS_DIR": str(runtime_dir / "scripts"),
                "SESSION_FILE": str(run_dir / "reasoning" / "session.txt"),
            }
        )
    return WorkflowLaunch(
        kind=WorkflowKind.REASONING,
        cwd=str(cwd),
        entrypoint=sys.executable,
        arguments=[
            "-m",
            "galois.reasoning.runner",
            "--repo-root",
            str(paths.repo_root),
            "--workdir",
            str(cwd),
        ],
        environment=environment,
    )


def build_verification_launch(
    *,
    config: PlatformConfig,
    paths: RepoPaths,
    run_dir: Path | None = None,
) -> WorkflowLaunch:
    agent_dir = paths.verification_dir
    runtime_dir = paths.verification_dir if run_dir is None else run_dir / "verification" / "workspace"
    results_dir = runtime_dir / "results"
    return WorkflowLaunch(
        kind=WorkflowKind.VERIFICATION,
        cwd=str(paths.repo_root),
        entrypoint=sys.executable,
        arguments=["-m", "uvicorn", "galois.verification.service:app", "--host", "127.0.0.1", "--port", "8091"],
        environment={
            "CODEX_BIN": config.codex.bin,
            "CODEX_MODEL": config.model,
            "CODEX_REASONING_EFFORT": config.model_reasoning_effort,
            **_venv_path_prefix_env(),
            **model_runtime_environment(config),
            "GALOIS_VERIFICATION_AGENT_DIR": str(agent_dir),
            "GALOIS_VERIFICATION_RUNTIME_DIR": str(runtime_dir),
            "GALOIS_VERIFICATION_WORKDIR": str(agent_dir),
            "GALOIS_VERIFICATION_RESULTS_DIR": str(results_dir),
            "PYTHONUNBUFFERED": "1",
        },
        mode=LaunchMode.SERVICE,
        healthcheck_url="http://127.0.0.1:8091/health",
    )


def _writing_input_path(problem: ProblemInput, paths: RepoPaths, run_dir: Path | None = None) -> str:
    if run_dir is not None:
        return str(run_dir / "writing" / "input.md")
    return _resolve_problem_path(problem, paths).as_posix()


def build_writing_launch(
    *,
    config: PlatformConfig,
    paths: RepoPaths,
    problem: ProblemInput,
    run_dir: Path | None = None,
) -> WorkflowLaunch:
    cwd = paths.writing_dir
    runtime_dir = cwd if run_dir is None else run_dir / "writing" / "workspace"
    environment = {
        "CODEX_BIN": config.codex.bin,
        "MODEL": config.model,
        "REASONING_EFFORT": config.model_reasoning_effort,
        "WRITING_FILE": _writing_input_path(problem, paths, run_dir=run_dir),
        "GALOIS_WRITING_PROJECT_ID": problem.problem_id,
        "RESUME": "auto" if config.resume_enabled else "0",
        **_venv_path_prefix_env(),
        **model_runtime_environment(config),
    }
    if run_dir is not None:
        environment.update(
            {
                "GALOIS_WRITING_RUNTIME_DIR": str(runtime_dir),
                "LOG_DIR": str(run_dir / "writing" / "logs"),
                "RESULTS_DIR": str(runtime_dir / "results"),
                "MEMORY_DIR": str(runtime_dir / "memory"),
                "CITATIONS_DIR": str(runtime_dir / "citations"),
                "DOWNLOADS_DIR": str(runtime_dir / "downloads"),
                "SESSION_FILE": str(run_dir / "writing" / "session.txt"),
            }
        )
    return WorkflowLaunch(
        kind=WorkflowKind.WRITING,
        cwd=str(cwd),
        entrypoint=sys.executable,
        arguments=[
            "-m",
            "galois.writing.runner",
            "--repo-root",
            str(paths.repo_root),
            "--workdir",
            str(cwd),
        ],
        environment=environment,
    )


def build_workflow_plan(
    *,
    config: PlatformConfig,
    paths: RepoPaths,
    problem: ProblemInput,
    run_dir: Path | None = None,
    verification_enabled: bool | None = None,
) -> list[WorkflowLaunch]:
    launches: list[WorkflowLaunch] = []
    effective_verification_enabled = config.verification.enabled if verification_enabled is None else verification_enabled
    if config.reasoning.enabled:
        launches.append(
            build_reasoning_launch(
                config=config,
                paths=paths,
                problem=problem,
                run_dir=run_dir,
                verification_enabled=effective_verification_enabled,
            )
        )
    if effective_verification_enabled:
        launches.append(build_verification_launch(config=config, paths=paths, run_dir=run_dir))
    return launches


def build_writing_workflow_plan(
    *,
    config: PlatformConfig,
    paths: RepoPaths,
    problem: ProblemInput,
    run_dir: Path | None = None,
) -> list[WorkflowLaunch]:
    if not config.writing.enabled:
        return []
    return [build_writing_launch(config=config, paths=paths, problem=problem, run_dir=run_dir)]
