"""PostgreSQL-backed index for web run history."""

from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime
import json
import re
from pathlib import Path
from typing import Any

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb


def readable_run_title(problem: dict[str, Any], *, run_id: str, statement: str = "") -> str:
    title = str(problem.get("title") or "").strip()
    if title:
        return title
    problem_id = str(problem.get("problem_id") or "").strip()
    if problem_id and not _looks_generated_problem_id(problem_id):
        return _humanize_slug(problem_id)
    statement_title = _title_from_markdown(statement)
    if statement_title:
        return statement_title
    return f"Untitled run {run_id[:8]}"


def manifest_run_record(run_dir: Path) -> dict[str, Any] | None:
    manifest = _safe_json(run_dir / "manifest.json", {})
    if not manifest:
        return None
    run_id = str(manifest.get("run_id") or run_dir.name)
    problem = manifest.get("problem") if isinstance(manifest.get("problem"), dict) else {}
    statement = _read_statement(run_dir, str(problem.get("problem_path") or ""))
    return {
        "run_id": run_id,
        "run_root": str(run_dir.parent.resolve()),
        "run_dir": str(run_dir.resolve()),
        "display_title": readable_run_title(problem, run_id=run_id, statement=statement),
        "auto_display_title": readable_run_title(problem, run_id=run_id, statement=statement),
        "problem_id": str(problem.get("problem_id") or ""),
        "problem_title": str(problem.get("title") or ""),
        "problem_path": str(problem.get("problem_path") or ""),
        "status": str(manifest.get("status") or "unknown"),
        "pipeline": str(manifest.get("pipeline") or ""),
        "model": str(manifest.get("model") or ""),
        "manifest": manifest,
    }


def _safe_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return fallback


def _read_statement(run_dir: Path, problem_path: str) -> str:
    candidates = [
        run_dir / "problem" / "source_statement.md",
        run_dir / "problem" / "statement.md",
        run_dir / "writing" / "input.md",
    ]
    if problem_path:
        external = Path(problem_path)
        candidates.append(external if external.is_absolute() else Path.cwd() / external)
        candidates.append(run_dir / external)
    for path in candidates:
        if path.exists():
            return path.read_text(encoding="utf-8", errors="replace")
    return ""


def _title_from_markdown(markdown: str) -> str:
    for line in markdown.splitlines():
        text = line.strip()
        if not text:
            continue
        heading = re.match(r"^#{1,3}\s+(.+)$", text)
        if heading:
            candidate = heading.group(1).strip()
            if not _looks_placeholder_title(candidate):
                return candidate[:120]
            continue
        candidate = re.sub(r"\s+", " ", text).strip(" .")
        if not _looks_placeholder_title(candidate):
            return candidate[:120]
    return ""


def _looks_generated_problem_id(problem_id: str) -> bool:
    value = problem_id.strip().lower()
    return (
        not value
        or value in {"problem", "paper-project", "untitled", "example"}
        or value.startswith("web_")
        or re.fullmatch(r"example\d*", value) is not None
    )


def _looks_placeholder_title(title: str) -> bool:
    value = title.strip().lower().strip(".:")
    return value in {"problem", "title", "statement", "context", "benchmark formulation", "references"}


def _humanize_slug(value: str) -> str:
    text = re.sub(r"[-_]+", " ", value).strip()
    return text[:1].upper() + text[1:] if text else value


def _run_sort_key(record: dict[str, Any]) -> datetime:
    run_id = str(record.get("run_id", ""))
    match = re.match(r"(\d{8}T\d{6})Z", run_id)
    if not match:
        return datetime.min
    return datetime.strptime(match.group(1), "%Y%m%dT%H%M%S")


class RunIndexStore:
    """Repository wrapper for indexed web runs."""

    def __init__(self, database_url: str):
        self.database_url = database_url
        self._connection: psycopg.Connection[dict[str, Any]] | None = None

    def __enter__(self) -> "RunIndexStore":
        self._connection = psycopg.connect(self.database_url, row_factory=dict_row)
        return self

    def __exit__(self, *_exc: object) -> None:
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    @property
    def connection(self) -> psycopg.Connection[dict[str, Any]]:
        if self._connection is None:
            raise RuntimeError("RunIndexStore must be used as a context manager")
        return self._connection

    def initialize(self) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS run_index (
                    run_id text PRIMARY KEY,
                    run_root text NOT NULL DEFAULT '',
                    run_dir text NOT NULL,
                    display_title text NOT NULL,
                    auto_display_title text NOT NULL DEFAULT '',
                    problem_id text NOT NULL DEFAULT '',
                    problem_title text NOT NULL DEFAULT '',
                    problem_path text NOT NULL DEFAULT '',
                    status text NOT NULL DEFAULT 'unknown',
                    pipeline text NOT NULL DEFAULT '',
                    model text NOT NULL DEFAULT '',
                    manifest jsonb NOT NULL DEFAULT '{}'::jsonb,
                    created_at timestamptz NOT NULL DEFAULT now(),
                    updated_at timestamptz NOT NULL DEFAULT now()
                )
                """
            )
            cursor.execute("ALTER TABLE run_index ADD COLUMN IF NOT EXISTS run_root text NOT NULL DEFAULT ''")
            cursor.execute("ALTER TABLE run_index ADD COLUMN IF NOT EXISTS auto_display_title text NOT NULL DEFAULT ''")
            cursor.execute("UPDATE run_index SET auto_display_title = display_title WHERE auto_display_title = ''")
            cursor.execute("CREATE INDEX IF NOT EXISTS run_index_updated_at_idx ON run_index(updated_at DESC)")
            cursor.execute("CREATE INDEX IF NOT EXISTS run_index_run_root_idx ON run_index(run_root)")
        self.connection.commit()

    def upsert_run(self, record: dict[str, Any]) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO run_index (
                    run_id,
                    run_root,
                    run_dir,
                    display_title,
                    auto_display_title,
                    problem_id,
                    problem_title,
                    problem_path,
                    status,
                    pipeline,
                    model,
                    manifest
                )
                VALUES (
                    %(run_id)s,
                    %(run_root)s,
                    %(run_dir)s,
                    %(display_title)s,
                    %(auto_display_title)s,
                    %(problem_id)s,
                    %(problem_title)s,
                    %(problem_path)s,
                    %(status)s,
                    %(pipeline)s,
                    %(model)s,
                    %(manifest)s::jsonb
                )
                ON CONFLICT (run_id) DO UPDATE SET
                    run_dir = EXCLUDED.run_dir,
                    run_root = EXCLUDED.run_root,
                    auto_display_title = EXCLUDED.auto_display_title,
                    problem_id = EXCLUDED.problem_id,
                    problem_title = EXCLUDED.problem_title,
                    problem_path = EXCLUDED.problem_path,
                    status = EXCLUDED.status,
                    pipeline = EXCLUDED.pipeline,
                    model = EXCLUDED.model,
                    manifest = EXCLUDED.manifest,
                    updated_at = now()
                """,
                {
                    **record,
                    "manifest": Jsonb(record.get("manifest") or {}),
                },
            )
        self.connection.commit()

    def sync_run_directories(self, run_dirs: Iterable[Path]) -> None:
        records = [record for run_dir in run_dirs if (record := manifest_run_record(run_dir))]
        records.sort(key=_run_sort_key, reverse=True)
        for record in records:
            self.upsert_run(record)

    def list_runs(self, *, run_root: Path, limit: int = 20) -> list[dict[str, Any]]:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT run_id, run_dir, display_title, auto_display_title, problem_id, problem_title, problem_path, status, pipeline, model, manifest
                FROM run_index
                WHERE run_root = %s
                ORDER BY run_id DESC
                LIMIT %s
                """,
                (str(run_root.resolve()), limit),
            )
            return [dict(row) for row in cursor.fetchall()]
