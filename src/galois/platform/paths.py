"""Path resolution helpers for the Galois control plane."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .config import PlatformConfig


@dataclass(slots=True)
class RepoPaths:
    repo_root: Path
    reasoning_dir: Path
    verification_dir: Path
    writing_dir: Path
    project_root: Path
    benchmark_root: Path
    run_root: Path
    service_root: Path
    artifact_root: Path
    report_root: Path
    references_dir: Path


def resolve_paths(config: PlatformConfig) -> RepoPaths:
    repo_root = config.repo_root
    return RepoPaths(
        repo_root=repo_root,
        reasoning_dir=repo_root / config.reasoning.workdir,
        verification_dir=repo_root / config.verification.workdir,
        writing_dir=repo_root / config.writing.workdir,
        project_root=config.project_root_path,
        benchmark_root=config.benchmark_root_path,
        run_root=config.run_root_path,
        service_root=config.project_root_path / "services",
        artifact_root=config.project_root_path / "artifacts",
        report_root=config.project_root_path / "reports",
        references_dir=repo_root / "references",
    )


def ensure_run_layout(paths: RepoPaths) -> None:
    paths.project_root.mkdir(parents=True, exist_ok=True)
    paths.run_root.mkdir(parents=True, exist_ok=True)
    paths.service_root.mkdir(parents=True, exist_ok=True)
    paths.artifact_root.mkdir(parents=True, exist_ok=True)
    paths.report_root.mkdir(parents=True, exist_ok=True)
