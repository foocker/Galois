"""Control-plane contracts for Galois runtime orchestration."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class WorkflowKind(str, Enum):
    REASONING = "reasoning"
    VERIFICATION = "verification"
    WRITING = "writing"


class RunStatus(str, Enum):
    CREATED = "created"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class LaunchMode(str, Enum):
    ONESHOT = "oneshot"
    SERVICE = "service"


class PipelinePreset(str, Enum):
    REASONING_ONLY = "reasoning-only"
    REASONING_VERIFICATION = "reasoning-verification"
    WRITING_ONLY = "writing-only"


@dataclass(slots=True)
class ProblemInput:
    problem_id: str
    problem_path: str
    title: str | None = None
    tags: list[str] = field(default_factory=list)


@dataclass(slots=True)
class RunManifest:
    run_id: str
    problem: ProblemInput
    backend: str
    model: str
    model_reasoning_effort: str
    status: RunStatus
    pipeline: PipelinePreset | None = None
    features: dict[str, object] = field(default_factory=dict)
    workflows: list[WorkflowKind] = field(default_factory=list)


@dataclass(slots=True)
class WorkflowLaunch:
    kind: WorkflowKind
    cwd: str
    entrypoint: str
    arguments: list[str] = field(default_factory=list)
    environment: dict[str, str] = field(default_factory=dict)
    mode: LaunchMode = LaunchMode.ONESHOT
    healthcheck_url: str | None = None
    startup_timeout_seconds: int = 30
