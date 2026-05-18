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
    _copy_problem_artifacts,
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
from .problem_garden import ProblemGardenStore
from .routes.problem_garden import create_problem_garden_router
from .run_index import RunIndexStore, manifest_run_record
from .run_registry import append_event, create_run_manifest, write_manifest
from .workflows import build_workflow_plan, build_writing_workflow_plan
from galois.writing.citation_lookup import CitationLookupService


ASSET_DIR = Path(__file__).with_name("web_assets")
MATLAS_BASE_URL = "https://matlas.ai"


class ReferenceFile(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)


class RunCreateRequest(BaseModel):
    title: str | None = None
    problem_markdown: str
    pipeline: str = "reasoning-verification"
    model: str = DEFAULT_MODEL
    references: list[ReferenceFile] = Field(default_factory=list)


class RunContinueRequest(BaseModel):
    feedback: str = Field(min_length=1)
    pipeline: str | None = None
    model: str | None = None


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
    authors: str = ""
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


class WritingProjectContinueRequest(BaseModel):
    feedback: str = Field(min_length=1)
    manuscript_markdown: str = ""
    model: str | None = None


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


def _write_web_references(run_dir: Path, references: list[ReferenceFile]) -> Path | None:
    """Stage user-uploaded reference files into a run-local refs directory.

    Mirrors Rethlas's `<problem>.refs/` convention. The CLI's
    `_prepare_reference_dir` will pick these up because the staged problem
    file at `run_dir/problem/statement.md` has a sibling `statement.refs/`
    directory once we drop files there.
    """
    if not references:
        return None
    refs_dir = run_dir / "problem" / "statement.refs"
    refs_dir.mkdir(parents=True, exist_ok=True)
    for ref in references:
        sanitized = re.sub(r"[^A-Za-z0-9._/\-]+", "_", ref.name).strip("/.")
        if not sanitized:
            sanitized = "reference.md"
        target = (refs_dir / sanitized).resolve()
        try:
            target.relative_to(refs_dir.resolve())
        except ValueError:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(ref.content, encoding="utf-8")
    return refs_dir


def _finalize_web_problem_artifacts(
    *,
    run_dir: Path,
    problem: ProblemInput,
    repo_root: Path,
    config,
) -> None:
    """Run the canonical-English translation pass and write meta.json.

    The web entrypoint only stages the raw user markdown into source_statement.md
    and statement.md. Without this finalize pass, non-English statements never
    get translated and meta.json is missing — the CLI does this via
    _copy_problem_artifacts before launching workflows.
    """
    _copy_problem_artifacts(run_dir, problem, repo_root, config)


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
        "## Authors",
        "",
        payload.authors.strip() or "Not provided.",
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


def _markdown_section(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*$\n(?P<body>.*?)(?=^##\s+|\Z)",
        flags=re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    return match.group("body").strip() if match else ""


def _read_text_if_exists(path: Path | None) -> str:
    if path is None or not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()


def _write_web_writing_continuation_input(
    run_dir: Path,
    *,
    previous_run_dir: Path,
    previous_input: str,
    previous_manuscript: str,
    previous_citation_report: str,
    previous_review_report: str,
    previous_revision_tasks: str,
    feedback: str,
    current_manuscript: str,
) -> Path:
    writing_dir = run_dir / "writing"
    writing_dir.mkdir(parents=True, exist_ok=True)
    input_path = writing_dir / "input.md"
    sections = [
        "# Galois Paper Writing Continuation Request",
        "",
        f"continued_from: {previous_run_dir.name}",
        "",
        "## Authors",
        "",
        _markdown_section(previous_input, "Authors") or "Not provided.",
        "",
        "## Continuation Feedback",
        "",
        feedback.strip(),
        "",
        "## Current Edited Manuscript",
        "",
        current_manuscript.strip() or "Not provided.",
        "",
        "## Previous Manuscript",
        "",
        previous_manuscript or "Not provided.",
        "",
        "## Previous Citation Report",
        "",
        previous_citation_report or "Not provided.",
        "",
        "## Previous Review Report",
        "",
        previous_review_report or "Not provided.",
        "",
        "## Previous Revision Tasks",
        "",
        previous_revision_tasks or "Not provided.",
        "",
        "## Previous Input",
        "",
        previous_input.strip() or "Not provided.",
        "",
        "## Requested Work",
        "",
        "Revise and polish the current manuscript using the continuation feedback. Preserve valid mathematical content, keep or repair inline citations, and update the writing artifacts.",
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
    verified = sorted(
        result_root.glob("*/blueprint_verified.md"),
        key=lambda candidate: (candidate.stat().st_mtime, str(candidate)),
    )
    if verified:
        return verified[-1]
    blueprints = sorted(
        result_root.glob("*/blueprint.md"),
        key=lambda candidate: (candidate.stat().st_mtime, str(candidate)),
    )
    return blueprints[-1] if blueprints else None


def _latest_verification_decision(run_dir: Path) -> dict[str, Any] | None:
    verification_dir = run_dir / "verification"
    if not verification_dir.exists():
        return None
    decision_files = sorted(
        verification_dir.glob("verification_decision_r*.json"),
        key=lambda candidate: _latest_revision(candidate),
    )
    if not decision_files:
        return None
    decision_path = decision_files[-1]
    decision_payload = _safe_json(decision_path, {})
    if not isinstance(decision_payload, dict):
        return None

    normalized_path_value = decision_payload.get("normalized_path")
    normalized_payload: dict[str, Any] = {}
    if isinstance(normalized_path_value, str) and normalized_path_value:
        normalized_path = Path(normalized_path_value)
        if not normalized_path.is_absolute():
            normalized_path = run_dir / normalized_path
        if normalized_path.exists():
            loaded = _safe_json(normalized_path, {})
            if isinstance(loaded, dict):
                normalized_payload = loaded

    return {
        "path": str(decision_path),
        "decision": decision_payload,
        "normalized": normalized_payload,
    }


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

    verification = _latest_verification_decision(run_dir)

    final_blueprint_path = _final_workspace_blueprint(run_dir)
    if final_blueprint_path is not None:
        is_verified = final_blueprint_path.name == "blueprint_verified.md"
        payload: dict[str, Any] = {
            "kind": "verified_blueprint" if is_verified else "final_blueprint",
            "path": str(final_blueprint_path),
            "content": final_blueprint_path.read_text(encoding="utf-8"),
            "verified": is_verified,
        }
        if verification is not None:
            payload["verification"] = verification
        return payload

    blueprint_path = _latest_blueprint(run_dir)
    if blueprint_path is not None:
        payload = {
            "kind": "reasoning_blueprint",
            "path": str(blueprint_path),
            "content": blueprint_path.read_text(encoding="utf-8"),
            "verified": False,
        }
        if verification is not None:
            payload["verification"] = verification
        return payload

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
    meta = _safe_json(run_dir / "problem" / "meta.json", {}) or {}
    source_path = run_dir / "problem" / "source_statement.md"
    canonical_path = run_dir / "problem" / "statement.md"
    references = _list_reference_files(meta.get("reference_dir") if isinstance(meta, dict) else None)

    base: dict[str, Any] | None = None
    for problem_path in (source_path, canonical_path):
        if problem_path.exists():
            base = {
                "kind": problem_path.stem,
                "path": str(problem_path),
                "content": problem_path.read_text(encoding="utf-8"),
            }
            break
    if base is None:
        writing_input = run_dir / "writing" / "input.md"
        if writing_input.exists():
            base = {
                "kind": "writing_input",
                "path": str(writing_input),
                "content": writing_input.read_text(encoding="utf-8"),
            }
    if base is None and not meta and not references:
        return None
    if base is None:
        base = {}

    if isinstance(meta, dict) and meta:
        base["meta"] = {
            "title": meta.get("title"),
            "tags": meta.get("tags") or [],
            "source_language": meta.get("source_language"),
            "canonical_language": meta.get("canonical_language"),
            "translated_from_source": bool(meta.get("translated_from_source")),
            "reference_dir": meta.get("reference_dir"),
        }
        if canonical_path.exists() and source_path.exists() and canonical_path.read_bytes() != source_path.read_bytes():
            base["canonical_content"] = canonical_path.read_text(encoding="utf-8")
    if references:
        base["references"] = references
    return base


def _list_reference_files(reference_dir: str | None) -> list[dict[str, Any]]:
    if not reference_dir:
        return []
    base = Path(reference_dir)
    if not base.exists() or not base.is_dir():
        return []
    entries: list[dict[str, Any]] = []
    for path in sorted(base.rglob("*")):
        if not path.is_file():
            continue
        try:
            relative = path.relative_to(base)
        except ValueError:
            continue
        if relative.parts and relative.parts[0] == ".extracted":
            continue
        suffix = path.suffix.lower()
        kind = (
            "pdf"
            if suffix == ".pdf"
            else ("text" if suffix in {".md", ".tex", ".txt"} else "other")
        )
        entry: dict[str, Any] = {
            "name": str(relative),
            "kind": kind,
            "size": path.stat().st_size,
        }
        if suffix == ".pdf":
            extracted = base / ".extracted" / relative.with_suffix(".txt")
            entry["extracted"] = str(extracted) if extracted.exists() else None
        if suffix in {".md", ".tex", ".txt"} and path.stat().st_size <= 200_000:
            try:
                entry["content"] = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                pass
        entries.append(entry)
    return entries


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

    session_path = run_dir / "reasoning" / "session.txt"
    session_id = session_path.read_text(encoding="utf-8").strip() if session_path.exists() else None
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
        "session_id": session_id,
    }


def _create_prepared_run(
    *,
    config_path: Path | None,
    payload: RunCreateRequest,
) -> tuple[str, str, str, str, str]:
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
    _write_web_references(run_dir, payload.references)
    _finalize_web_problem_artifacts(
        run_dir=run_dir,
        problem=problem,
        repo_root=run_paths.repo_root,
        config=run_config,
    )
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
    with RunIndexStore(run_config.database.connection_url) as index:
        index.initialize()
        record = manifest_run_record(run_dir)
        if record is not None:
            index.upsert_run(record)
    return manifest.run_id, problem.problem_id, str(statement_path), feature_flags.pipeline.value, problem.title or problem.problem_id


def _continue_prepared_run(
    *,
    config_path: Path | None,
    previous_run_dir: Path,
    feedback: str,
    pipeline: str,
    model: str,
) -> tuple[str, str, str, str, str]:
    """Create a new run that continues from a previous one with user feedback.

    The continuation merges three things into the new run's problem markdown:
    the original problem statement, the previous blueprint (whether verified
    or not), and the user's natural-language feedback. The new run is a fresh
    codex session — the verification audit trail makes attempt history visible
    in the run list rather than mutating an existing artifact.
    """
    previous_problem = previous_run_dir / "problem"
    statement_path = previous_problem / "statement.md"
    if not statement_path.exists():
        statement_path = previous_problem / "source_statement.md"
    if not statement_path.exists():
        raise FileNotFoundError("previous run has no problem statement")
    original_statement = statement_path.read_text(encoding="utf-8")

    blueprint_candidates = sorted(
        (previous_run_dir / "reasoning").glob("blueprint_r*.md"),
        key=lambda candidate: _latest_revision(candidate),
    )
    previous_blueprint = blueprint_candidates[-1].read_text(encoding="utf-8") if blueprint_candidates else ""

    decision_files = sorted(
        (previous_run_dir / "verification").glob("verification_decision_r*.json"),
        key=lambda candidate: _latest_revision(candidate),
    )
    previous_decision = ""
    if decision_files:
        decision = _safe_json(decision_files[-1], {})
        if isinstance(decision, dict):
            previous_decision = decision.get("decision") or decision.get("verdict") or ""

    sections = [
        "# Continuation request",
        "",
        f"This run continues from `{previous_run_dir.name}`"
        + (f" (previous decision: `{previous_decision}`)" if previous_decision else "")
        + ".",
        "",
        "## Original problem",
        "",
        original_statement.strip(),
        "",
        "## User feedback",
        "",
        feedback.strip(),
        "",
    ]
    if previous_blueprint:
        sections.extend(
            [
                "## Previous attempt (for revision)",
                "",
                previous_blueprint.strip(),
                "",
            ]
        )
    continuation_markdown = "\n".join(sections)

    previous_meta = _safe_json(previous_problem / "meta.json", {}) or {}
    previous_title = previous_meta.get("title") if isinstance(previous_meta, dict) else None
    title = f"{previous_title or 'Continuation'} (continued)"

    references = []
    previous_refs_dir = previous_problem / "statement.refs"
    if previous_refs_dir.exists():
        for ref_path in sorted(previous_refs_dir.rglob("*")):
            if not ref_path.is_file():
                continue
            try:
                relative = ref_path.relative_to(previous_refs_dir)
            except ValueError:
                continue
            if relative.parts and relative.parts[0] == ".extracted":
                continue
            try:
                references.append(
                    ReferenceFile(name=str(relative), content=ref_path.read_text(encoding="utf-8"))
                )
            except (UnicodeDecodeError, OSError):
                continue

    payload = RunCreateRequest(
        title=title,
        problem_markdown=continuation_markdown,
        pipeline=pipeline,
        model=model,
        references=references,
    )
    return _create_prepared_run(config_path=config_path, payload=payload)


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


def _continue_prepared_writing_run(
    *,
    config_path: Path | None,
    previous_run_dir: Path,
    feedback: str,
    manuscript_markdown: str,
    model: str,
) -> tuple[str, str, str]:
    previous_input_path = previous_run_dir / "writing" / "input.md"
    if not previous_input_path.exists():
        raise FileNotFoundError("previous writing run has no input.md")
    previous_input = previous_input_path.read_text(encoding="utf-8")

    manuscript = _read_text_if_exists(_latest_revisioned_file(previous_run_dir / "writing", "manuscript_draft_r*.md"))
    citation_report = _read_text_if_exists(_latest_revisioned_file(previous_run_dir / "writing", "citation_report_r*.md"))
    review_report = _read_text_if_exists(_latest_revisioned_file(previous_run_dir / "writing", "review_report_r*.md"))
    revision_tasks = _read_text_if_exists(_latest_revisioned_file(previous_run_dir / "writing", "revision_tasks_r*.json"))

    run_config = load_config(config_path)
    run_config.model = model
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
    previous_manifest = _safe_json(previous_run_dir / "manifest.json", {}) or {}
    previous_problem = previous_manifest.get("problem", {}) if isinstance(previous_manifest, dict) else {}
    previous_title = previous_problem.get("title") if isinstance(previous_problem, dict) else None
    problem = ProblemInput(
        problem_id=_slug(f"{previous_title or previous_run_dir.name} continued"),
        problem_path="writing/input.md",
        title=f"{previous_title or 'Writing project'} (continued)",
        tags=["paper-writing", "continuation"],
    )
    run_dir, manifest = create_run_manifest(config=run_config, paths=run_paths, problem=problem)
    input_path = _write_web_writing_continuation_input(
        run_dir,
        previous_run_dir=previous_run_dir,
        previous_input=previous_input,
        previous_manuscript=manuscript,
        previous_citation_report=citation_report,
        previous_review_report=review_report,
        previous_revision_tasks=revision_tasks,
        feedback=feedback,
        current_manuscript=manuscript_markdown,
    )
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
            "continued_from": previous_run_dir.name,
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

    app.include_router(create_problem_garden_router(config, store_class=ProblemGardenStore))

    @app.get("/", response_class=HTMLResponse)
    def index() -> str:
        index_path = ASSET_DIR / "index.html"
        return index_path.read_text(encoding="utf-8")

    @app.get("/api/runs")
    def list_runs() -> dict[str, Any]:
        run_root = config.run_root_path
        run_dirs = []
        if run_root.exists():
            run_dirs = sorted((candidate for candidate in run_root.iterdir() if candidate.is_dir()), reverse=True)
        with RunIndexStore(config.database.connection_url) as index:
            index.initialize()
            index.sync_run_directories(run_dirs)
            runs = [
                {
                    "run_id": row["run_id"],
                    "status": row["status"],
                    "pipeline": row["pipeline"] or None,
                    "model": row["model"] or None,
                    "display_title": row["display_title"],
                    "problem": {
                        **(row["manifest"].get("problem", {}) if isinstance(row["manifest"], dict) else {}),
                        "problem_id": row["problem_id"],
                        "title": row["problem_title"] or row["display_title"],
                        "display_title": row["display_title"],
                    },
                }
                for row in index.list_runs(run_root=run_root, limit=20)
            ]
        return {"runs": runs}

    @app.post("/api/runs")
    def create_run(payload: RunCreateRequest) -> dict[str, Any]:
        if not (payload.title or "").strip():
            raise HTTPException(status_code=400, detail="title must not be blank")
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

        run_id, problem_id, problem_path, pipeline, display_title = _create_prepared_run(config_path=config_path, payload=payload)
        return JSONResponse(
            status_code=202,
            content={
                "run_id": run_id,
                "problem_id": problem_id,
                "display_title": display_title,
                "problem_path": problem_path,
                "status": "queued",
                "pipeline": pipeline,
                "model": payload.model,
            },
        )

    @app.post("/api/runs/{run_id}/continue")
    def continue_run(run_id: str, payload: RunContinueRequest) -> JSONResponse:
        run_root = config.run_root_path
        try:
            previous = read_run_snapshot(run_root, run_id, project_root=config.project_root_path)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail="run not found") from exc
        if not payload.feedback.strip():
            raise HTTPException(status_code=400, detail="feedback must not be blank")
        pipeline = payload.pipeline or previous.get("pipeline") or "reasoning-verification"
        model = payload.model or previous.get("model") or DEFAULT_MODEL
        if model not in SUPPORTED_MODELS:
            raise HTTPException(status_code=400, detail="unsupported model")
        if not model_is_configured(config, model):
            raise HTTPException(status_code=400, detail="model credentials are not configured")
        try:
            new_run_id, problem_id, _, new_pipeline, display_title = _continue_prepared_run(
                config_path=config_path,
                previous_run_dir=Path(previous["run_dir"]),
                feedback=payload.feedback,
                pipeline=pipeline,
                model=model,
            )
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        return JSONResponse(
            status_code=202,
            content={
                "run_id": new_run_id,
                "problem_id": problem_id,
                "display_title": display_title,
                "status": "queued",
                "pipeline": new_pipeline,
                "model": model,
                "continued_from": run_id,
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

    @app.post("/api/writing/projects/{run_id}/continue")
    def continue_writing_project(run_id: str, payload: WritingProjectContinueRequest) -> dict[str, Any]:
        if not payload.feedback.strip():
            raise HTTPException(status_code=400, detail="feedback must not be blank")
        model = payload.model or DEFAULT_MODEL
        if model not in SUPPORTED_MODELS:
            raise HTTPException(status_code=400, detail="unsupported model")
        if model not in config.model_connections:
            raise HTTPException(status_code=400, detail="model is not configured")
        if not model_is_configured(config, model):
            raise HTTPException(status_code=400, detail="model credentials are not configured")
        previous_run_dir = (config.run_root_path / run_id).resolve()
        try:
            previous_run_dir.relative_to(config.run_root_path.resolve())
        except ValueError as exc:
            raise HTTPException(status_code=404, detail="run not found") from exc
        if not previous_run_dir.exists() or not previous_run_dir.is_dir():
            raise HTTPException(status_code=404, detail="run not found")
        previous_snapshot = read_run_snapshot(config.run_root_path, run_id, project_root=config.project_root_path)
        if previous_snapshot.get("pipeline") != PipelinePreset.WRITING_ONLY.value:
            raise HTTPException(status_code=400, detail="run is not a writing project")
        try:
            new_run_id, project_id, input_path = _continue_prepared_writing_run(
                config_path=config_path,
                previous_run_dir=previous_run_dir,
                feedback=payload.feedback,
                manuscript_markdown=payload.manuscript_markdown,
                model=model,
            )
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        return JSONResponse(
            status_code=202,
            content={
                "run_id": new_run_id,
                "project_id": project_id,
                "input_path": input_path,
                "status": "queued",
                "pipeline": PipelinePreset.WRITING_ONLY.value,
                "model": model,
                "continued_from": run_id,
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
