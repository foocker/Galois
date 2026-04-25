"""Shared artifact contracts for the first Galois pipeline."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, is_dataclass
from enum import Enum
from typing import Any


class Verdict(str, Enum):
    CORRECT = "correct"
    WRONG = "wrong"


class ExecutionStatus(str, Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"


class StepStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"


@dataclass(slots=True)
class ComponentRef:
    name: str
    version: str = "dev"


@dataclass(slots=True)
class ProblemSpec:
    problem_id: str
    title: str
    statement: str
    tags: list[str] = field(default_factory=list)
    source_path: str | None = None


@dataclass(slots=True)
class BlueprintArtifact:
    problem_id: str
    revision: int
    content: str
    notes: list[str] = field(default_factory=list)
    component: ComponentRef = field(default_factory=lambda: ComponentRef(name="unknown"))


@dataclass(slots=True)
class VerificationIssue:
    location: str
    issue: str


@dataclass(slots=True)
class VerificationArtifact:
    problem_id: str
    revision: int
    verdict: Verdict
    summary: str
    critical_errors: list[VerificationIssue] = field(default_factory=list)
    gaps: list[VerificationIssue] = field(default_factory=list)
    repair_hints: str = ""
    component: ComponentRef = field(default_factory=lambda: ComponentRef(name="unknown"))


@dataclass(slots=True)
class LeanExecutionArtifact:
    problem_id: str
    status: ExecutionStatus
    summary: str
    files_touched: list[str] = field(default_factory=list)
    remaining_sorries: int = 0
    compile_passed: bool = False
    notes: list[str] = field(default_factory=list)
    component: ComponentRef = field(default_factory=lambda: ComponentRef(name="unknown"))


@dataclass(slots=True)
class StepRecord:
    step: str
    status: StepStatus
    component: ComponentRef
    artifact_path: str
    started_at: str
    finished_at: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class RunRecord:
    run_id: str
    benchmark: str
    problem_id: str
    started_at: str
    finished_at: str
    final_status: str
    steps: list[StepRecord] = field(default_factory=list)


def to_dict(value: Any) -> Any:
    """Convert dataclasses and enums into plain JSON-serializable values."""
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {key: to_dict(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {key: to_dict(item) for key, item in value.items()}
    if isinstance(value, list):
        return [to_dict(item) for item in value]
    return value
