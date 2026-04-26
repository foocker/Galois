"""Benchmark suite helpers for Galois proof-system experiments."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import tomllib
from typing import Any

from .contracts import PipelinePreset, ProblemInput


@dataclass(slots=True)
class BenchmarkProblem:
    problem_id: str
    path: str
    title: str | None = None
    tags: list[str] | None = None

    def as_problem_input(self) -> ProblemInput:
        return ProblemInput(
            problem_id=self.problem_id,
            problem_path=self.path,
            title=self.title,
            tags=list(self.tags or []),
        )


@dataclass(slots=True)
class BenchmarkSuite:
    suite_id: str
    description: str
    default_pipeline: PipelinePreset
    problems: list[BenchmarkProblem]
    source_path: Path | None = None


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _default_suite_path(repo_root: Path | None = None) -> Path:
    root = repo_root or _repo_root()
    return root / "benchmarks" / "manifests" / "reasoning_data_examples.toml"


def discover_reasoning_data_suite(repo_root: Path | None = None) -> BenchmarkSuite:
    root = repo_root or _repo_root()
    data_dir = root / "three_horse" / "reasoning" / "data"
    problems: list[BenchmarkProblem] = []
    for problem_path in sorted(data_dir.glob("*.md")):
        title = problem_path.read_text(encoding="utf-8").splitlines()[0].strip()
        problems.append(
            BenchmarkProblem(
                problem_id=problem_path.stem,
                path=str(problem_path.relative_to(root)),
                title=title or problem_path.stem,
                tags=["examples", "reasoning-data"],
            )
        )
    return BenchmarkSuite(
        suite_id="reasoning-data-examples",
        description="Example benchmark generated from repo-local three_horse/reasoning/data problems.",
        default_pipeline=PipelinePreset.REASONING_VERIFICATION,
        problems=problems,
    )


def load_suite(path: Path | None = None, repo_root: Path | None = None) -> BenchmarkSuite:
    suite_path = path or _default_suite_path(repo_root)
    if not suite_path.exists():
        if path is None:
            return discover_reasoning_data_suite(repo_root)
        raise FileNotFoundError(f"benchmark suite manifest not found: {suite_path}")

    raw = tomllib.loads(suite_path.read_text(encoding="utf-8"))
    default_pipeline = PipelinePreset(str(raw.get("default_pipeline", PipelinePreset.REASONING_VERIFICATION.value)))
    problems = [
        BenchmarkProblem(
            problem_id=str(item["id"]),
            path=str(item["path"]),
            title=str(item["title"]) if item.get("title") is not None else None,
            tags=[str(tag) for tag in item.get("tags", [])],
        )
        for item in raw.get("problems", [])
    ]
    return BenchmarkSuite(
        suite_id=str(raw["suite_id"]),
        description=str(raw.get("description", "")),
        default_pipeline=default_pipeline,
        problems=problems,
        source_path=suite_path,
    )


def suite_to_dict(suite: BenchmarkSuite) -> dict[str, Any]:
    return {
        "suite_id": suite.suite_id,
        "description": suite.description,
        "default_pipeline": suite.default_pipeline.value,
        "source_path": str(suite.source_path) if suite.source_path else None,
        "problems": [
            {
                "id": problem.problem_id,
                "path": problem.path,
                "title": problem.title,
                "tags": list(problem.tags or []),
            }
            for problem in suite.problems
        ],
    }


def build_suite_plan(
    *,
    suite: BenchmarkSuite,
    pipeline: PipelinePreset | None = None,
    repair_loop_enabled: bool | None = None,
    max_repair_rounds: int | None = None,
    limit: int | None = None,
) -> dict[str, Any]:
    selected_pipeline = pipeline or suite.default_pipeline
    selected_problems = suite.problems
    if limit is not None:
        selected_problems = selected_problems[: max(limit, 0)]
    return {
        "suite_id": suite.suite_id,
        "problem_count": len(selected_problems),
        "total_problem_count": len(suite.problems),
        "limit": limit,
        "pipeline": selected_pipeline.value,
        "repair_loop_enabled": repair_loop_enabled,
        "max_repair_rounds": max_repair_rounds,
        "runs": [
            {
                "problem_id": problem.problem_id,
                "problem_path": problem.path,
                "title": problem.title,
                "pipeline": selected_pipeline.value,
                "tags": list(problem.tags or []),
            }
            for problem in selected_problems
        ],
    }


def write_suite(path: Path, suite: BenchmarkSuite) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f'suite_id = "{suite.suite_id}"',
        f'description = "{suite.description}"',
        f'default_pipeline = "{suite.default_pipeline.value}"',
        "",
    ]
    for problem in suite.problems:
        lines.extend(
            [
                "[[problems]]",
                f'id = "{problem.problem_id}"',
                f'path = "{problem.path}"',
            ]
        )
        if problem.title:
            lines.append(f'title = {json.dumps(problem.title, ensure_ascii=False)}')
        if problem.tags:
            tags = ", ".join(json.dumps(tag, ensure_ascii=False) for tag in problem.tags)
            lines.append(f"tags = [{tags}]")
        lines.append("")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
