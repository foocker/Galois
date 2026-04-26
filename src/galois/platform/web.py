"""FastAPI workbench for launching and inspecting Galois research runs."""

from __future__ import annotations

import json
import re
import threading
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .cli import (
    _feature_payload,
    _prepare_reasoning_workspace,
    _prepare_verification_workspace,
    _resolve_run_feature_flags,
    _stage_problem_for_reasoning_workspace,
    execute_run_workflows,
)
from .config import DEFAULT_MODEL, SUPPORTED_MODELS, load_config, model_is_configured
from .contracts import PipelinePreset, ProblemInput, WorkflowKind
from .paths import ensure_run_layout, resolve_paths
from .run_registry import append_event, create_run_manifest, write_manifest
from .workflows import build_workflow_plan


ASSET_DIR = Path(__file__).with_name("web_assets")


class RunCreateRequest(BaseModel):
    title: str | None = None
    problem_markdown: str
    pipeline: str = "reasoning-verification"
    model: str = DEFAULT_MODEL


def _slug(text: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return normalized[:48] or "problem"


def _write_web_problem(run_dir: Path, problem_markdown: str) -> Path:
    problem_dir = run_dir / "problem"
    problem_dir.mkdir(parents=True, exist_ok=True)
    source_path = problem_dir / "source_statement.md"
    statement_path = problem_dir / "statement.md"
    content = problem_markdown.strip() + "\n"
    source_path.write_text(content, encoding="utf-8")
    statement_path.write_text(content, encoding="utf-8")
    return statement_path


def _safe_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


def _latest_revision(path: Path) -> int:
    match = re.search(r"_r(\d+)\.md$", path.name)
    return int(match.group(1)) if match else 0


def _latest_blueprint(run_dir: Path) -> Path | None:
    blueprints = sorted(
        (run_dir / "reasoning").glob("blueprint_r*.md"),
        key=lambda candidate: (_latest_revision(candidate), candidate.name),
    )
    return blueprints[-1] if blueprints else None


def _final_workspace_blueprint(run_dir: Path) -> Path | None:
    result_root = run_dir / "reasoning" / "workspace" / "results"
    if not result_root.exists():
        return None
    blueprints = sorted(
        result_root.glob("*/blueprint.md"),
        key=lambda candidate: (candidate.stat().st_mtime, str(candidate)),
    )
    return blueprints[-1] if blueprints else None


def _read_events(run_dir: Path, limit: int = 40) -> list[dict[str, Any]]:
    events_path = run_dir / "events.jsonl"
    if not events_path.exists():
        return []
    events: list[dict[str, Any]] = []
    for line in events_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events[-limit:]


def _output_payload(run_dir: Path) -> dict[str, Any] | None:
    final_blueprint_path = _final_workspace_blueprint(run_dir)
    if final_blueprint_path is not None:
        return {
            "kind": "final_blueprint",
            "path": str(final_blueprint_path),
            "content": final_blueprint_path.read_text(encoding="utf-8"),
        }

    blueprint_path = _latest_blueprint(run_dir)
    if blueprint_path is not None:
        return {
            "kind": "reasoning_blueprint",
            "path": str(blueprint_path),
            "content": blueprint_path.read_text(encoding="utf-8"),
        }

    summary_path = run_dir / "summary.md"
    if summary_path.exists():
        return {
            "kind": "summary",
            "path": str(summary_path),
            "content": summary_path.read_text(encoding="utf-8"),
        }
    return None


def _problem_payload(run_dir: Path) -> dict[str, Any] | None:
    for problem_path in (run_dir / "problem" / "source_statement.md", run_dir / "problem" / "statement.md"):
        if problem_path.exists():
            return {
                "kind": problem_path.stem,
                "path": str(problem_path),
                "content": problem_path.read_text(encoding="utf-8"),
            }
    return None


def read_run_snapshot(run_root: Path, run_id: str, project_root: Path | None = None) -> dict[str, Any]:
    resolved_run_root = run_root.resolve()
    run_dir = (resolved_run_root / run_id).resolve()
    if run_dir.parent != resolved_run_root or not run_dir.exists() or not run_dir.is_dir():
        raise FileNotFoundError(run_id)

    manifest = _safe_json(run_dir / "manifest.json", {})
    subagents = _safe_json(run_dir / "subagents.json", [])
    events = _read_events(run_dir)
    output = _output_payload(run_dir)
    problem_input = _problem_payload(run_dir)

    return {
        "run_id": manifest.get("run_id", run_dir.name),
        "run_dir": str(run_dir),
        "status": manifest.get("status", "unknown"),
        "pipeline": manifest.get("pipeline"),
        "model": manifest.get("model"),
        "problem": manifest.get("problem", {}),
        "workflows": manifest.get("workflows", []),
        "features": manifest.get("features", {}),
        "events": events,
        "subagents": subagents,
        "problem_input": problem_input,
        "output": output,
    }


def _create_prepared_run(
    *,
    config_path: Path | None,
    payload: RunCreateRequest,
) -> tuple[str, str, str, str]:
    run_config = load_config(config_path)
    run_config.model = payload.model
    run_paths = resolve_paths(run_config)
    ensure_run_layout(run_paths)
    feature_flags = _resolve_run_feature_flags(
        verification_default=run_config.verification.enabled,
        max_repair_rounds_default=run_config.max_repair_rounds,
        pipeline=payload.pipeline,
        reasoning_only=False,
        verification_override=None,
    )
    problem = ProblemInput(
        problem_id=_slug(payload.title or "problem"),
        problem_path="problem/statement.md",
        title=payload.title,
    )
    run_dir, manifest = create_run_manifest(config=run_config, paths=run_paths, problem=problem)
    statement_path = _write_web_problem(run_dir, payload.problem_markdown)
    problem.problem_path = str(statement_path)
    manifest.problem = problem
    launches = build_workflow_plan(
        config=run_config,
        paths=run_paths,
        problem=problem,
        run_dir=run_dir,
        verification_enabled=feature_flags.verification_enabled,
    )
    if any(launch.kind == WorkflowKind.REASONING for launch in launches):
        _prepare_reasoning_workspace(run_dir, run_paths.repo_root)
        _stage_problem_for_reasoning_workspace(run_dir=run_dir, repo_root=run_paths.repo_root, problem=problem)
    if any(launch.kind == WorkflowKind.VERIFICATION for launch in launches):
        _prepare_verification_workspace(run_dir, run_paths.repo_root)
    manifest.pipeline = feature_flags.pipeline
    manifest.features = _feature_payload(feature_flags)
    manifest.workflows = [launch.kind for launch in launches]
    write_manifest(run_dir, manifest)
    append_event(
        run_dir,
        run_id=manifest.run_id,
        event_type="run_created",
        payload={
            "problem": {
                "problem_id": problem.problem_id,
                "problem_path": problem.problem_path,
                "title": problem.title,
                "tags": problem.tags,
            },
            "run_dir": str(run_dir),
            "workflow_count": len(launches),
            "skip_services": False,
            **_feature_payload(feature_flags),
        },
    )
    _start_run_thread(
        run_id=manifest.run_id,
        config=run_config,
        paths=run_paths,
        run_dir=run_dir,
        manifest=manifest,
        problem=problem,
        launches=launches,
        feature_flags=feature_flags,
    )
    return manifest.run_id, problem.problem_id, str(statement_path), feature_flags.pipeline.value


def _start_run_thread(**kwargs: Any) -> None:
    thread = threading.Thread(
        target=execute_run_workflows,
        kwargs={key: value for key, value in kwargs.items() if key != "run_id"},
        name=f"galois-run-{kwargs['run_id']}",
        daemon=True,
    )
    thread.start()


def create_app(config_path: Path | None = None) -> FastAPI:
    config = load_config(config_path)
    paths = resolve_paths(config)
    app = FastAPI(title="Galois Research Workbench")

    if ASSET_DIR.exists():
        app.mount("/assets", StaticFiles(directory=ASSET_DIR), name="assets")

    @app.get("/", response_class=HTMLResponse)
    def index() -> str:
        index_path = ASSET_DIR / "index.html"
        return index_path.read_text(encoding="utf-8")

    @app.get("/api/runs")
    def list_runs() -> dict[str, Any]:
        run_root = config.run_root_path
        runs = []
        if run_root.exists():
            for run_dir in sorted((candidate for candidate in run_root.iterdir() if candidate.is_dir()), reverse=True):
                manifest = _safe_json(run_dir / "manifest.json", {})
                runs.append(
                    {
                        "run_id": manifest.get("run_id", run_dir.name),
                        "status": manifest.get("status", "unknown"),
                        "pipeline": manifest.get("pipeline"),
                        "model": manifest.get("model"),
                        "problem": manifest.get("problem", {}),
                    }
                )
        return {"runs": runs[:20]}

    @app.post("/api/runs")
    def create_run(payload: RunCreateRequest) -> dict[str, Any]:
        if not payload.problem_markdown.strip():
            raise HTTPException(status_code=400, detail="problem_markdown must not be blank")
        if payload.pipeline not in {pipeline.value for pipeline in PipelinePreset}:
            raise HTTPException(status_code=400, detail="unsupported pipeline")
        if payload.model not in SUPPORTED_MODELS:
            raise HTTPException(status_code=400, detail="unsupported model")
        if payload.model not in config.model_connections:
            raise HTTPException(status_code=400, detail="model is not configured")
        if not model_is_configured(config, payload.model):
            raise HTTPException(status_code=400, detail="model credentials are not configured")

        run_id, problem_id, problem_path, pipeline = _create_prepared_run(config_path=config_path, payload=payload)
        return JSONResponse(
            status_code=202,
            content={
                "run_id": run_id,
                "problem_id": problem_id,
                "problem_path": problem_path,
                "status": "queued",
                "pipeline": pipeline,
                "model": payload.model,
            },
        )

    @app.get("/api/runs/{run_id}")
    def get_run(run_id: str) -> dict[str, Any]:
        try:
            return read_run_snapshot(config.run_root_path, run_id)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail="run not found") from exc

    return app


app = create_app()
