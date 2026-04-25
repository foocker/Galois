"""Repository-level configuration loading for Galois."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import tomllib


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


@dataclass(slots=True)
class WorkflowAreaConfig:
    enabled: bool
    workdir: str


@dataclass(slots=True)
class CodexConfig:
    bin: str
    base_url_env: str
    api_key_env: str

    @property
    def base_url(self) -> str:
        return os.getenv(self.base_url_env, "")

    @property
    def has_api_key(self) -> bool:
        return bool(os.getenv(self.api_key_env, ""))


@dataclass(slots=True)
class PlatformConfig:
    backend: str
    model: str
    model_reasoning_effort: str
    personality: str
    codex: CodexConfig
    reasoning: WorkflowAreaConfig
    verification: WorkflowAreaConfig
    resume_enabled: bool
    max_repair_rounds: int
    benchmark_root: str
    run_root: str
    config_path: Path
    repo_root: Path
    project_root: str = "projects/default"

    @property
    def benchmark_root_path(self) -> Path:
        return self.repo_root / self.benchmark_root

    @property
    def project_root_path(self) -> Path:
        project_root = Path(self.project_root)
        if project_root.is_absolute():
            return project_root
        return self.repo_root / project_root

    @property
    def run_root_path(self) -> Path:
        run_root = Path(self.run_root)
        if run_root.is_absolute():
            return run_root
        return self.project_root_path / run_root


def load_config(path: Path | None = None) -> PlatformConfig:
    repo_root = _repo_root()
    config_path = path or repo_root / "configs" / "defaults.toml"
    raw = tomllib.loads(config_path.read_text(encoding="utf-8"))

    return PlatformConfig(
        backend=str(raw["backend"]),
        model=str(raw["model"]),
        model_reasoning_effort=str(raw["model_reasoning_effort"]),
        personality=str(raw["personality"]),
        codex=CodexConfig(
            bin=str(raw.get("codex", {}).get("bin", "codex")),
            base_url_env=str(raw.get("codex", {}).get("base_url_env", "OPENAI_BASE_URL")),
            api_key_env=str(raw.get("codex", {}).get("api_key_env", "OPENAI_API_KEY")),
        ),
        reasoning=WorkflowAreaConfig(
            enabled=bool(raw["reasoning"]["enabled"]),
            workdir=str(raw["reasoning"]["workdir"]),
        ),
        verification=WorkflowAreaConfig(
            enabled=bool(raw["verification"]["enabled"]),
            workdir=str(raw["verification"]["workdir"]),
        ),
        resume_enabled=bool(raw["platform"]["resume_enabled"]),
        max_repair_rounds=int(raw["platform"].get("max_repair_rounds", 1)),
        project_root=str(raw["platform"].get("project_root", "projects/default")),
        benchmark_root=str(raw["platform"]["benchmark_root"]),
        run_root=str(raw["platform"]["run_root"]),
        config_path=config_path,
        repo_root=repo_root,
    )
