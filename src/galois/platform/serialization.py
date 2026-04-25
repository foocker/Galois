"""Serialization helpers for persisted run artifacts."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from enum import Enum
from pathlib import Path
import re
from typing import Any


_ABSOLUTE_PATH_TOKEN = re.compile(r"(?P<prefix>^|[\s'\"=({\[<])(?P<path>/[A-Za-z0-9._~@%+/\-]+)")


def default_repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _resolved(path: Path | str | None) -> Path | None:
    if path is None:
        return None
    return Path(path).expanduser().resolve()


def _roots(*, repo_root: Path | str | None, run_dir: Path | str | None) -> list[Path]:
    candidates = [_resolved(repo_root) or default_repo_root().resolve(), _resolved(run_dir)]
    roots: list[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        if candidate is None:
            continue
        key = candidate.as_posix()
        if key not in seen:
            roots.append(candidate)
            seen.add(key)
    return roots


def _relative_to(path: Path, root: Path) -> str | None:
    try:
        relative = path.relative_to(root)
    except ValueError:
        return None
    return relative.as_posix() if relative.as_posix() != "." else "."


def _external_display(path: Path) -> str:
    parts = [part for part in path.parts if part not in {"", path.anchor, "/"}]
    if not parts:
        return "external"
    tail = parts[-3:]
    return Path("external", *tail).as_posix()


def artifact_path(
    value: Path | str,
    *,
    repo_root: Path | str | None = None,
    run_dir: Path | str | None = None,
) -> str:
    """Return a stable relative display path when the path is under known roots."""

    path = Path(value).expanduser()
    if not path.is_absolute():
        return path.as_posix()

    resolved = path.resolve()
    for root in _roots(repo_root=repo_root, run_dir=run_dir):
        relative = _relative_to(resolved, root)
        if relative is not None:
            return relative
    return _external_display(resolved)


def _sanitize_string(
    value: str,
    *,
    repo_root: Path | str | None = None,
    run_dir: Path | str | None = None,
) -> str:
    def _replace_path(match: re.Match[str]) -> str:
        prefix = match.group("prefix")
        path_text = match.group("path")
        return f"{prefix}{artifact_path(path_text, repo_root=repo_root, run_dir=run_dir)}"

    value = _ABSOLUTE_PATH_TOKEN.sub(_replace_path, value)

    for root in _roots(repo_root=repo_root, run_dir=run_dir):
        root_text = root.as_posix()
        value = value.replace(f"{root_text}/", "")
        pattern = re.escape(root_text) + r"(?=$|[\s'\"`:;,)\]}])"
        value = re.sub(pattern, ".", value)
    return value


def sanitize_for_run_artifact(
    value: Any,
    *,
    repo_root: Path | str | None = None,
    run_dir: Path | str | None = None,
) -> Any:
    """Recursively convert repo/run absolute paths to stable relative strings.

    This is intentionally for persisted metadata only. Runtime launch objects
    should keep their original absolute paths for subprocess execution.
    """

    if value is None or isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Path):
        return artifact_path(value, repo_root=repo_root, run_dir=run_dir)
    if isinstance(value, str):
        return _sanitize_string(value, repo_root=repo_root, run_dir=run_dir)
    if is_dataclass(value) and not isinstance(value, type):
        return sanitize_for_run_artifact(asdict(value), repo_root=repo_root, run_dir=run_dir)
    if isinstance(value, dict):
        return {
            str(sanitize_for_run_artifact(key, repo_root=repo_root, run_dir=run_dir)): sanitize_for_run_artifact(
                item,
                repo_root=repo_root,
                run_dir=run_dir,
            )
            for key, item in value.items()
        }
    if isinstance(value, (tuple, list, set)):
        return [sanitize_for_run_artifact(item, repo_root=repo_root, run_dir=run_dir) for item in value]
    return value
