"""FastAPI workbench for launching and inspecting Galois research runs."""

from __future__ import annotations

import json
import re
import threading
from pathlib import Path
from typing import Any

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .cli import (
    _feature_payload,
    _prepare_reasoning_workspace,
    _prepare_verification_workspace,
    _prepare_writing_workspace,
    _resolve_run_feature_flags,
    _stage_input_for_writing_workspace,
    _stage_problem_for_reasoning_workspace,
    execute_run_workflows,
)
from .config import DEFAULT_MODEL, SUPPORTED_MODELS, load_config, model_is_configured
from .contracts import PipelinePreset, ProblemInput, WorkflowKind
from .paths import ensure_run_layout, resolve_paths
from .run_registry import append_event, create_run_manifest, write_manifest
from .workflows import build_workflow_plan, build_writing_workflow_plan
from galois.writing.citation_lookup import CitationLookupService


ASSET_DIR = Path(__file__).with_name("web_assets")
MATLAS_BASE_URL = "https://matlas.ai"


class RunCreateRequest(BaseModel):
    title: str | None = None
    problem_markdown: str
    pipeline: str = "reasoning-verification"
    model: str = DEFAULT_MODEL


class MatlasSearchRequest(BaseModel):
    query: str = Field(min_length=1)
    num_results: int = Field(default=10, ge=10, le=200)


class MatlasFeedbackRequest(BaseModel):
    query: str = Field(min_length=1)
    candidate_id: str = Field(min_length=1)
    label: str


class CitationResolveRequest(BaseModel):
    identifier: str = Field(min_length=1)
    sources: list[str] | None = None


class CitationSearchRequest(BaseModel):
    query: str = Field(min_length=1)
    sources: list[str] | None = None
    limit: int = Field(default=10, ge=1, le=50)


class CitationValidateRequest(BaseModel):
    bibtex: str = Field(min_length=1)
    sources: list[str] | None = None


class WritingProjectCreateRequest(BaseModel):
    title: str | None = None
    project_type: str = "paper"
    draft_markdown: str = ""
    references_markdown: str = ""
    manuscript_markdown: str = ""
    theorem_statement: str = ""
    proof_draft: str = ""
    bibliography: str = ""
    reviewer_comments: str = ""
    target_journal: str = ""
    requested_work: str = "Review and improve this mathematical manuscript."
    min_references: int | None = Field(default=None, ge=0, le=200)
    max_references: int | None = Field(default=None, ge=0, le=200)
    min_pages: int | None = Field(default=None, ge=1, le=300)
    max_pages: int | None = Field(default=None, ge=1, le=300)
    review_rounds: int = Field(default=1, ge=0, le=5)
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


def _write_web_writing_input(run_dir: Path, payload: WritingProjectCreateRequest) -> Path:
    writing_dir = run_dir / "writing"
    writing_dir.mkdir(parents=True, exist_ok=True)
    input_path = writing_dir / "input.md"
    draft = payload.draft_markdown.strip()
    if not draft:
        legacy_parts = []
        if payload.theorem_statement.strip():
            legacy_parts.extend(["### Theorem Statement", "", payload.theorem_statement.strip(), ""])
        if payload.proof_draft.strip():
            legacy_parts.extend(["### Proof Draft", "", payload.proof_draft.strip(), ""])
        if payload.manuscript_markdown.strip():
            legacy_parts.extend(["### Manuscript Draft", "", payload.manuscript_markdown.strip(), ""])
        draft = "\n".join(legacy_parts).strip()
    references = payload.references_markdown.strip() or payload.bibliography.strip()
    sections = [
        "# Galois Paper Writing Request",
        "",
        f"project_type: {payload.project_type.strip() or 'paper'}",
        "",
        "## Writing Parameters",
        "",
        f"min_references: {payload.min_references if payload.min_references is not None else 'Not specified.'}",
        f"max_references: {payload.max_references if payload.max_references is not None else 'Not specified.'}",
        f"min_pages: {payload.min_pages if payload.min_pages is not None else 'Not specified.'}",
        f"max_pages: {payload.max_pages if payload.max_pages is not None else 'Not specified.'}",
        f"review_rounds: {payload.review_rounds}",
        "",
        "## Title",
        "",
        (payload.title or "Untitled mathematical manuscript").strip(),
        "",
        "## Target Journal",
        "",
        payload.target_journal.strip() or "Not specified.",
        "",
        "## Requested Work",
        "",
        payload.requested_work.strip() or "Review and improve this mathematical manuscript.",
        "",
        "## Draft",
        "",
        draft or "Not provided.",
        "",
        "## References",
        "",
        references or "Not provided.",
        "",
        "## Reviewer Comments",
        "",
        payload.reviewer_comments.strip() or "Not provided.",
        "",
    ]
    input_path.write_text("\n".join(sections), encoding="utf-8")
    return input_path


def _safe_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


def _latest_revision(path: Path) -> int:
    match = re.search(r"_r(\d+)\.[^.]+$", path.name)
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
    writing_payload = _writing_output_payload(run_dir)
    if writing_payload is not None:
        return writing_payload

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


def _latest_revisioned_file(directory: Path, pattern: str) -> Path | None:
    files = sorted(
        directory.glob(pattern),
        key=lambda candidate: (_latest_revision(candidate), candidate.name),
    )
    return files[-1] if files else None


def _writing_output_payload(run_dir: Path) -> dict[str, Any] | None:
    writing_dir = run_dir / "writing"
    if not writing_dir.exists():
        return None

    manuscript = _latest_revisioned_file(writing_dir, "manuscript_draft_r*.md")
    review = _latest_revisioned_file(writing_dir, "review_report_r*.md")
    citation = _latest_revisioned_file(writing_dir, "citation_report_r*.md")
    tasks = _latest_revisioned_file(writing_dir, "revision_tasks_r*.json")
    bundle = _latest_revisioned_file(writing_dir, "export_bundle_r*.json")
    paper_project = _latest_revisioned_file(writing_dir, "paper_project_r*.json")

    if not any((manuscript, review, citation, tasks, bundle, paper_project)):
        return None

    artifacts: dict[str, Any] = {}
    for key, path in {
        "manuscript_draft": manuscript,
        "review_report": review,
        "citation_report": citation,
    }.items():
        if path is not None:
            artifacts[key] = {
                "path": str(path),
                "content": path.read_text(encoding="utf-8"),
            }
    for key, path in {
        "revision_tasks": tasks,
        "export_bundle": bundle,
        "paper_project": paper_project,
    }.items():
        if path is not None:
            artifacts[key] = {
                "path": str(path),
                "content": _safe_json(path, {}),
            }
    return {
        "kind": "paper_project",
        "path": str(paper_project or manuscript or review or citation),
        "content": artifacts.get("manuscript_draft", {}).get("content", ""),
        "artifacts": artifacts,
    }


def _post_matlas_json(endpoint: str, payload: dict[str, object]) -> Any:
    url = f"{MATLAS_BASE_URL}{endpoint}"
    try:
        with httpx.Client(timeout=20.0, follow_redirects=True) as client:
            response = client.post(url, json=payload)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as exc:
        detail: Any
        try:
            detail = exc.response.json()
        except ValueError:
            detail = exc.response.text or "Matlas request failed"
        raise HTTPException(status_code=exc.response.status_code, detail=detail) from exc
    except (httpx.RequestError, ValueError) as exc:
        raise HTTPException(status_code=502, detail=f"Matlas service unavailable: {exc}") from exc


def _citation_lookup_service(cache_dir: Path) -> CitationLookupService:
    return CitationLookupService(cache_dir=cache_dir)


def _problem_payload(run_dir: Path) -> dict[str, Any] | None:
    for problem_path in (run_dir / "problem" / "source_statement.md", run_dir / "problem" / "statement.md"):
        if problem_path.exists():
            return {
                "kind": problem_path.stem,
                "path": str(problem_path),
                "content": problem_path.read_text(encoding="utf-8"),
            }
    writing_input = run_dir / "writing" / "input.md"
    if writing_input.exists():
        return {
            "kind": "writing_input",
            "path": str(writing_input),
            "content": writing_input.read_text(encoding="utf-8"),
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


def _create_prepared_writing_run(
    *,
    config_path: Path | None,
    payload: WritingProjectCreateRequest,
) -> tuple[str, str, str]:
    run_config = load_config(config_path)
    run_config.model = payload.model
    run_paths = resolve_paths(run_config)
    ensure_run_layout(run_paths)
    feature_flags = _resolve_run_feature_flags(
        verification_default=run_config.verification.enabled,
        max_repair_rounds_default=run_config.max_repair_rounds,
        pipeline=PipelinePreset.WRITING_ONLY,
        reasoning_only=False,
        verification_override=False,
        repair_loop_override=False,
        max_repair_rounds_override=0,
    )
    problem = ProblemInput(
        problem_id=_slug(payload.title or "paper-project"),
        problem_path="writing/input.md",
        title=payload.title,
        tags=["paper-writing", payload.project_type],
    )
    run_dir, manifest = create_run_manifest(config=run_config, paths=run_paths, problem=problem)
    input_path = _write_web_writing_input(run_dir, payload)
    problem.problem_path = str(input_path)
    manifest.problem = problem
    launches = build_writing_workflow_plan(
        config=run_config,
        paths=run_paths,
        problem=problem,
        run_dir=run_dir,
    )
    _prepare_writing_workspace(run_dir, run_paths.repo_root)
    _stage_input_for_writing_workspace(run_dir=run_dir, repo_root=run_paths.repo_root, problem=problem)
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
    return manifest.run_id, problem.problem_id, str(input_path)


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
        problem_pipelines = {PipelinePreset.REASONING_ONLY.value, PipelinePreset.REASONING_VERIFICATION.value}
        if payload.pipeline not in problem_pipelines:
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

    @app.post("/api/writing/projects")
    def create_writing_project(payload: WritingProjectCreateRequest) -> dict[str, Any]:
        if payload.model not in SUPPORTED_MODELS:
            raise HTTPException(status_code=400, detail="unsupported model")
        if payload.model not in config.model_connections:
            raise HTTPException(status_code=400, detail="model is not configured")
        if not model_is_configured(config, payload.model):
            raise HTTPException(status_code=400, detail="model credentials are not configured")
        if not any(
            value.strip()
            for value in (
                payload.manuscript_markdown,
                payload.draft_markdown,
                payload.theorem_statement,
                payload.proof_draft,
                payload.bibliography,
                payload.references_markdown,
                payload.reviewer_comments,
            )
        ):
            raise HTTPException(status_code=400, detail="writing project content must not be blank")
        if (
            payload.min_references is not None
            and payload.max_references is not None
            and payload.min_references > payload.max_references
        ):
            raise HTTPException(status_code=400, detail="min_references must be <= max_references")
        if payload.min_pages is not None and payload.max_pages is not None and payload.min_pages > payload.max_pages:
            raise HTTPException(status_code=400, detail="min_pages must be <= max_pages")

        run_id, project_id, input_path = _create_prepared_writing_run(config_path=config_path, payload=payload)
        return JSONResponse(
            status_code=202,
            content={
                "run_id": run_id,
                "project_id": project_id,
                "input_path": input_path,
                "status": "queued",
                "pipeline": PipelinePreset.WRITING_ONLY.value,
                "model": payload.model,
            },
        )

    @app.post("/api/matlas/search")
    def search_matlas(payload: MatlasSearchRequest) -> dict[str, Any]:
        query = payload.query.strip()
        if not query:
            raise HTTPException(status_code=400, detail="query must not be blank")
        results = _post_matlas_json("/api/search", {"query": query, "num_results": payload.num_results})
        if not isinstance(results, list):
            raise HTTPException(status_code=502, detail="Matlas search returned an unexpected response")
        return {"results": results}

    @app.post("/api/matlas/feedback")
    def send_matlas_feedback(payload: MatlasFeedbackRequest) -> dict[str, Any]:
        query = payload.query.strip()
        candidate_id = payload.candidate_id.strip()
        if not query:
            raise HTTPException(status_code=400, detail="query must not be blank")
        if not candidate_id:
            raise HTTPException(status_code=400, detail="candidate_id must not be blank")
        if payload.label not in {"relevant", "irrelevant"}:
            raise HTTPException(status_code=400, detail="unsupported feedback label")
        result = _post_matlas_json(
            "/api/feedback",
            {"query": query, "candidate_id": candidate_id, "label": payload.label},
        )
        if not isinstance(result, dict):
            raise HTTPException(status_code=502, detail="Matlas feedback returned an unexpected response")
        return result

    @app.post("/api/citations/resolve")
    def resolve_citation(payload: CitationResolveRequest) -> dict[str, Any]:
        identifier = payload.identifier.strip()
        if not identifier:
            raise HTTPException(status_code=400, detail="identifier must not be blank")
        with _citation_lookup_service(config.run_root_path / "citation_cache") as service:
            return service.resolve(identifier, sources=payload.sources)

    @app.post("/api/citations/search")
    def search_citations(payload: CitationSearchRequest) -> dict[str, Any]:
        query = payload.query.strip()
        if not query:
            raise HTTPException(status_code=400, detail="query must not be blank")
        with _citation_lookup_service(config.run_root_path / "citation_cache") as service:
            return service.search(query, sources=payload.sources, limit=payload.limit)

    @app.post("/api/citations/validate")
    def validate_citations(payload: CitationValidateRequest) -> dict[str, Any]:
        bibtex = payload.bibtex.strip()
        if not bibtex:
            raise HTTPException(status_code=400, detail="bibtex must not be blank")
        with _citation_lookup_service(config.run_root_path / "citation_cache") as service:
            return service.validate_bibtex(bibtex, sources=payload.sources)

    @app.get("/api/runs/{run_id}")
    def get_run(run_id: str) -> dict[str, Any]:
        try:
            return read_run_snapshot(config.run_root_path, run_id)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail="run not found") from exc

    return app


app = create_app()
