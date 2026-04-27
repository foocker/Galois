"""Repository-level configuration loading for Galois."""

from __future__ import annotations

from dataclasses import dataclass, field
import os
from pathlib import Path
import tomllib


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


SUPPORTED_MODELS = ("gpt-5.4", "gpt-5.5", "gemini-pro-3.1")
DEFAULT_MODEL = "gpt-5.4"


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
class ModelConnectionConfig:
    base_url_env: str
    api_key_env: str

    @property
    def base_url(self) -> str:
        return os.getenv(self.base_url_env, "")

    @property
    def api_key(self) -> str:
        return os.getenv(self.api_key_env, "")

    @property
    def configured(self) -> bool:
        return bool(self.base_url and self.api_key)


@dataclass(slots=True)
class PlatformConfig:
    backend: str
    model: str
    model_reasoning_effort: str
    personality: str
    codex: CodexConfig
    reasoning: WorkflowAreaConfig
    verification: WorkflowAreaConfig
    writing: WorkflowAreaConfig
    resume_enabled: bool
    max_repair_rounds: int
    benchmark_root: str
    run_root: str
    config_path: Path
    repo_root: Path
    project_root: str = "projects/default"
    model_connections: dict[str, ModelConnectionConfig] = field(default_factory=dict)

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

    def model_connection(self, model: str | None = None) -> ModelConnectionConfig | None:
        return self.model_connections.get(model or self.model)


def _load_model_connections(raw: dict, codex: CodexConfig) -> dict[str, ModelConnectionConfig]:
    raw_models = raw.get("models", {})
    if not raw_models:
        return {
            str(raw["model"]): ModelConnectionConfig(
                base_url_env=codex.base_url_env,
                api_key_env=codex.api_key_env,
            )
        }
    return {
        str(model): ModelConnectionConfig(
            base_url_env=str(payload.get("base_url_env", codex.base_url_env)),
            api_key_env=str(payload.get("api_key_env", codex.api_key_env)),
        )
        for model, payload in raw_models.items()
    }


def model_is_configured(config: PlatformConfig, model: str | None = None) -> bool:
    connection = config.model_connection(model)
    return bool(connection and connection.configured)


def model_runtime_environment(config: PlatformConfig, model: str | None = None) -> dict[str, str]:
    connection = config.model_connection(model)
    if connection is None:
        return {}
    env: dict[str, str] = {}
    if connection.base_url:
        env["OPENAI_BASE_URL"] = connection.base_url
    if connection.api_key:
        env["OPENAI_API_KEY"] = connection.api_key
    return env


def load_config(path: Path | None = None) -> PlatformConfig:
    repo_root = _repo_root()
    config_path = path or repo_root / "configs" / "defaults.toml"
    raw = tomllib.loads(config_path.read_text(encoding="utf-8"))

    codex = CodexConfig(
        bin=str(raw.get("codex", {}).get("bin", "codex")),
        base_url_env=str(raw.get("codex", {}).get("base_url_env", "OPENAI_BASE_URL")),
        api_key_env=str(raw.get("codex", {}).get("api_key_env", "OPENAI_API_KEY")),
    )

    return PlatformConfig(
        backend=str(raw["backend"]),
        model=str(raw["model"]),
        model_reasoning_effort=str(raw["model_reasoning_effort"]),
        personality=str(raw["personality"]),
        codex=codex,
        reasoning=WorkflowAreaConfig(
            enabled=bool(raw["reasoning"]["enabled"]),
            workdir=str(raw["reasoning"]["workdir"]),
        ),
        verification=WorkflowAreaConfig(
            enabled=bool(raw["verification"]["enabled"]),
            workdir=str(raw["verification"]["workdir"]),
        ),
        writing=WorkflowAreaConfig(
            enabled=bool(raw.get("writing", {}).get("enabled", True)),
            workdir=str(raw.get("writing", {}).get("workdir", "three_horse/writing")),
        ),
        resume_enabled=bool(raw["platform"]["resume_enabled"]),
        max_repair_rounds=int(raw["platform"].get("max_repair_rounds", 1)),
        project_root=str(raw["platform"].get("project_root", "projects/default")),
        benchmark_root=str(raw["platform"]["benchmark_root"]),
        run_root=str(raw["platform"]["run_root"]),
        config_path=config_path,
        repo_root=repo_root,
        model_connections=_load_model_connections(raw, codex),
    )
