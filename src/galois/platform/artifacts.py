"""Artifact collection and contract wiring for workflow outputs."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
import shutil
from urllib import error, request

from galois.contracts import ComponentRef, VerificationArtifact, VerificationIssue, Verdict, to_dict

from .contracts import ProblemInput
from .serialization import sanitize_for_run_artifact


@dataclass(slots=True)
class BlueprintArchiveResult:
    found: bool
    source_path: str | None = None
    markdown_path: str | None = None
    json_path: str | None = None
    content: str = ""


@dataclass(slots=True)
class VerificationRequestResult:
    attempted: bool
    succeeded: bool
    request_path: str | None = None
    response_path: str | None = None
    error: str | None = None


@dataclass(slots=True)
class VerificationNormalizationResult:
    status: str
    normalized_path: str | None = None
    decision_path: str | None = None
    decision: str = ""
    raw_response_path: str | None = None
    error: str | None = None


@dataclass(slots=True)
class ReasoningRepairInputResult:
    written: bool
    path: str | None = None


@dataclass(slots=True)
class WritingArchiveResult:
    found: bool
    project_id: str
    source_dir: str | None = None
    artifact_paths: dict[str, str] | None = None


def resolve_problem_statement(problem: ProblemInput, repo_root: Path, run_dir: Path | None = None) -> tuple[str, Path]:
    if run_dir is not None:
        staged_path = run_dir / "problem" / "statement.md"
        if staged_path.exists():
            return staged_path.read_text(encoding="utf-8"), staged_path
    problem_path = Path(problem.problem_path)
    if not problem_path.is_absolute():
        problem_path = repo_root / problem_path
    problem_path = problem_path.resolve()
    return problem_path.read_text(encoding="utf-8"), problem_path


def reasoning_problem_id(problem: ProblemInput) -> str:
    return Path(problem.problem_path).stem


def reasoning_workspace_dir(run_dir: Path) -> Path:
    return run_dir / "reasoning" / "workspace"


def writing_workspace_dir(run_dir: Path) -> Path:
    return run_dir / "writing" / "workspace"


def next_artifact_revision(run_dir: Path, workflow: str, pattern: str) -> int:
    workflow_dir = run_dir / workflow
    if not workflow_dir.exists():
        return 1

    max_revision = 0
    for candidate in workflow_dir.glob(pattern):
        name = candidate.stem
        if candidate.suffix == ".json" and name.endswith(".normalized"):
            name = name[: -len(".normalized")]
        marker = "_r"
        if marker not in name:
            continue
        tail = name.rsplit(marker, 1)[-1]
        if tail.isdigit():
            max_revision = max(max_revision, int(tail))
    return max_revision + 1


def discover_reasoning_blueprint(run_dir: Path, problem: ProblemInput) -> Path | None:
    problem_id = reasoning_problem_id(problem)
    workspace_dir = reasoning_workspace_dir(run_dir)
    candidates = [
        workspace_dir / "results" / problem_id / "blueprint_verified.md",
        workspace_dir / "results" / problem_id / "blueprint.md",
        run_dir / "reasoning" / "results" / problem_id / "blueprint_verified.md",
        run_dir / "reasoning" / "results" / problem_id / "blueprint.md",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate

    results_root = run_dir / "reasoning" / "results"
    if not results_root.exists():
        return None
    discovered = sorted(results_root.glob("**/blueprint_verified.md")) + sorted(results_root.glob("**/blueprint.md"))
    return discovered[0] if discovered else None


def _normalize_markdown_math_delimiters(content: str) -> str:
    content = re.sub(r"\\\[(.+?)\\\]", lambda match: f"$${match.group(1).strip()}$$", content, flags=re.DOTALL)
    content = re.sub(r"\\\((.+?)\\\)", lambda match: f"${match.group(1).strip()}$", content, flags=re.DOTALL)
    return content


def archive_reasoning_blueprint(run_dir: Path, problem: ProblemInput, revision: int = 1) -> BlueprintArchiveResult:
    source_path = discover_reasoning_blueprint(run_dir, problem)
    if source_path is None:
        return BlueprintArchiveResult(found=False)

    content = _normalize_markdown_math_delimiters(source_path.read_text(encoding="utf-8"))
    destination_md = run_dir / "reasoning" / f"blueprint_r{revision}.md"
    destination_json = run_dir / "reasoning" / f"blueprint_r{revision}.json"
    destination_md.parent.mkdir(parents=True, exist_ok=True)
    destination_md.write_text(content, encoding="utf-8")
    destination_json.write_text(
        json.dumps(
            sanitize_for_run_artifact(
                {
                    "problem_id": problem.problem_id,
                    "reasoning_problem_id": reasoning_problem_id(problem),
                    "revision": revision,
                    "source_path": str(source_path),
                    "markdown_path": str(destination_md),
                    "content": content,
                },
                run_dir=run_dir,
            ),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return BlueprintArchiveResult(
        found=True,
        source_path=str(source_path),
        markdown_path=str(destination_md),
        json_path=str(destination_json),
        content=content,
    )


def discover_writing_project_dir(run_dir: Path, problem: ProblemInput) -> Path | None:
    candidates = [
        writing_workspace_dir(run_dir) / "results" / problem.problem_id,
        run_dir / "writing" / "results" / problem.problem_id,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate

    results_root = writing_workspace_dir(run_dir) / "results"
    if not results_root.exists():
        return None
    discovered = sorted(candidate for candidate in results_root.iterdir() if candidate.is_dir())
    return discovered[0] if discovered else None


def archive_writing_project(run_dir: Path, problem: ProblemInput, revision: int = 1) -> WritingArchiveResult:
    source_dir = discover_writing_project_dir(run_dir, problem)
    if source_dir is None:
        return WritingArchiveResult(found=False, project_id=problem.problem_id)

    artifact_names = (
        "manuscript_draft.md",
        "review_report.md",
        "citation_report.md",
        "revision_tasks.json",
        "export_bundle.json",
    )
    destination_dir = run_dir / "writing"
    destination_dir.mkdir(parents=True, exist_ok=True)
    artifact_paths: dict[str, str] = {}
    for name in artifact_names:
        source_path = source_dir / name
        if not source_path.exists():
            continue
        destination_path = destination_dir / f"{Path(name).stem}_r{revision}{Path(name).suffix}"
        shutil.copyfile(source_path, destination_path)
        artifact_paths[name] = str(destination_path)

    manifest_path = destination_dir / f"paper_project_r{revision}.json"
    manifest_path.write_text(
        json.dumps(
            sanitize_for_run_artifact(
                {
                    "project_id": problem.problem_id,
                    "revision": revision,
                    "source_dir": str(source_dir),
                    "artifact_paths": artifact_paths,
                },
                run_dir=run_dir,
            ),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    artifact_paths["paper_project"] = str(manifest_path)
    return WritingArchiveResult(
        found=bool(artifact_paths),
        project_id=problem.problem_id,
        source_dir=str(source_dir),
        artifact_paths=artifact_paths,
    )


def call_verification_api(
    *,
    run_dir: Path,
    problem: ProblemInput,
    statement: str,
    proof: str,
    url: str = "http://127.0.0.1:8091/verify",
    revision: int = 1,
    timeout_seconds: int = 60,
) -> VerificationRequestResult:
    verification_dir = run_dir / "verification"
    verification_dir.mkdir(parents=True, exist_ok=True)
    request_path = verification_dir / f"verification_request_r{revision}.json"
    response_path = verification_dir / f"verification_r{revision}.json"

    payload = {
        "statement": statement,
        "proof": proof,
    }
    request_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    http_request = request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(http_request, timeout=timeout_seconds) as response:
            raw = response.read().decode("utf-8")
    except (OSError, error.URLError) as exc:
        error_path = verification_dir / f"verification_error_r{revision}.txt"
        error_path.write_text(str(exc) + "\n", encoding="utf-8")
        return VerificationRequestResult(
            attempted=True,
            succeeded=False,
            request_path=str(request_path),
            response_path=None,
            error=str(exc),
        )

    response_path.write_text(raw.rstrip() + "\n", encoding="utf-8")
    return VerificationRequestResult(
        attempted=True,
        succeeded=True,
        request_path=str(request_path),
        response_path=str(response_path),
    )


def normalize_verification_response(
    *,
    run_dir: Path,
    problem: ProblemInput,
    revision: int = 1,
    request_result: VerificationRequestResult,
) -> VerificationNormalizationResult:
    verification_dir = run_dir / "verification"
    normalized_path = verification_dir / f"verification_r{revision}.normalized.json"
    decision_path = verification_dir / f"verification_decision_r{revision}.json"

    if not request_result.attempted:
        decision = {
            "status": "not_attempted",
            "decision": "verification_not_attempted",
            "error": request_result.error,
        }
        decision_path.write_text(
            json.dumps(sanitize_for_run_artifact(decision, run_dir=run_dir), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return VerificationNormalizationResult(
            status="not_attempted",
            normalized_path=None,
            decision_path=str(decision_path),
            decision=decision["decision"],
            raw_response_path=request_result.response_path,
            error=request_result.error,
        )

    if not request_result.succeeded or request_result.response_path is None:
        decision = {
            "status": "api_failed",
            "decision": "verification_api_failed",
            "error": request_result.error,
        }
        decision_path.write_text(
            json.dumps(sanitize_for_run_artifact(decision, run_dir=run_dir), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return VerificationNormalizationResult(
            status="api_failed",
            normalized_path=None,
            decision_path=str(decision_path),
            decision=decision["decision"],
            raw_response_path=request_result.response_path,
            error=request_result.error,
        )

    raw_path = Path(request_result.response_path)
    try:
        payload = json.loads(raw_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        decision = {
            "status": "malformed_response",
            "decision": "verification_malformed",
            "error": str(exc),
        }
        decision_path.write_text(
            json.dumps(sanitize_for_run_artifact(decision, run_dir=run_dir), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return VerificationNormalizationResult(
            status="malformed_response",
            normalized_path=None,
            decision_path=str(decision_path),
            decision=decision["decision"],
            raw_response_path=request_result.response_path,
            error=str(exc),
        )

    try:
        verdict_raw = str(payload["verdict"]).strip().lower()
        verification_report = payload["verification_report"]
        summary = str(verification_report["summary"])
        critical_errors = [
            VerificationIssue(location=str(item["location"]), issue=str(item["issue"]))
            for item in verification_report.get("critical_errors", [])
        ]
        gaps = [
            VerificationIssue(location=str(item["location"]), issue=str(item["issue"]))
            for item in verification_report.get("gaps", [])
        ]
        if verdict_raw == Verdict.CORRECT.value:
            verdict = Verdict.CORRECT
            decision_value = "accepted"
            status = "normalized"
        elif verdict_raw == Verdict.WRONG.value:
            verdict = Verdict.WRONG
            decision_value = "repair_needed"
            status = "normalized"
        else:
            raise ValueError(f"unsupported verdict: {verdict_raw}")
        artifact = VerificationArtifact(
            problem_id=problem.problem_id,
            revision=revision,
            verdict=verdict,
            summary=summary,
            critical_errors=critical_errors,
            gaps=gaps,
            repair_hints=str(payload.get("repair_hints", "")),
            component=ComponentRef(name="verification"),
        )
    except (KeyError, TypeError, ValueError) as exc:
        decision = {
            "status": "malformed_response",
            "decision": "verification_malformed",
            "error": str(exc),
        }
        decision_path.write_text(
            json.dumps(sanitize_for_run_artifact(decision, run_dir=run_dir), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return VerificationNormalizationResult(
            status="malformed_response",
            normalized_path=None,
            decision_path=str(decision_path),
            decision=decision["decision"],
            raw_response_path=request_result.response_path,
            error=str(exc),
        )

    normalized_path.write_text(json.dumps(to_dict(artifact), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    decision = {
        "status": status,
        "decision": decision_value,
        "normalized_path": sanitize_for_run_artifact(str(normalized_path), run_dir=run_dir),
        "raw_response_path": sanitize_for_run_artifact(request_result.response_path, run_dir=run_dir),
        "verdict": artifact.verdict.value,
    }
    decision_path.write_text(json.dumps(decision, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return VerificationNormalizationResult(
        status=status,
        normalized_path=str(normalized_path),
        decision_path=str(decision_path),
        decision=decision_value,
        raw_response_path=request_result.response_path,
        error=None,
    )


def write_reasoning_repair_input(
    *,
    run_dir: Path,
    problem: ProblemInput,
    blueprint: BlueprintArchiveResult,
    normalized: VerificationNormalizationResult,
    revision: int = 1,
) -> ReasoningRepairInputResult:
    if normalized.decision != "repair_needed" or not normalized.normalized_path:
        return ReasoningRepairInputResult(written=False)

    normalized_payload = json.loads(Path(normalized.normalized_path).read_text(encoding="utf-8"))
    path = run_dir / "reasoning" / f"repair_input_r{revision}.json"
    payload = {
        "problem_id": problem.problem_id,
        "revision": revision,
        "blueprint_markdown_path": blueprint.markdown_path,
        "blueprint_json_path": blueprint.json_path,
        "verification_normalized_path": normalized.normalized_path,
        "repair_hints": normalized_payload.get("repair_hints", ""),
        "critical_errors": normalized_payload.get("critical_errors", []),
        "gaps": normalized_payload.get("gaps", []),
        "summary": normalized_payload.get("summary", ""),
    }
    path.write_text(json.dumps(sanitize_for_run_artifact(payload, run_dir=run_dir), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return ReasoningRepairInputResult(written=True, path=str(path))
