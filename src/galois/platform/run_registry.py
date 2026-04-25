"""Run-directory creation and manifest persistence."""

from __future__ import annotations

from dataclasses import asdict
from datetime import UTC, datetime
import json
from pathlib import Path
import uuid
from typing import Any

from .config import PlatformConfig
from .contracts import ProblemInput, RunManifest, RunStatus
from .paths import RepoPaths
from .serialization import sanitize_for_run_artifact


def _utc_stamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def create_run_manifest(
    *,
    config: PlatformConfig,
    paths: RepoPaths,
    problem: ProblemInput,
) -> tuple[Path, RunManifest]:
    run_id = f"{_utc_stamp()}_{uuid.uuid4().hex[:8]}"
    run_dir = paths.run_root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    manifest = RunManifest(
        run_id=run_id,
        problem=problem,
        backend=config.backend,
        model=config.model,
        model_reasoning_effort=config.model_reasoning_effort,
        status=RunStatus.CREATED,
    )
    write_manifest(run_dir, manifest)
    return run_dir, manifest


def write_manifest(run_dir: Path, manifest: RunManifest) -> None:
    payload = sanitize_for_run_artifact(asdict(manifest), run_dir=run_dir)
    (run_dir / "manifest.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def update_manifest_status(run_dir: Path, manifest: RunManifest, status: RunStatus) -> None:
    manifest.status = status
    write_manifest(run_dir, manifest)


def append_event(
    run_dir: Path,
    *,
    run_id: str,
    event_type: str,
    workflow: str | None = None,
    payload: dict[str, Any] | None = None,
) -> None:
    event = {
        "timestamp": utc_now_iso(),
        "run_id": run_id,
        "workflow": workflow,
        "event_type": event_type,
        "payload": sanitize_for_run_artifact(payload or {}, run_dir=run_dir),
    }
    with (run_dir / "events.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
