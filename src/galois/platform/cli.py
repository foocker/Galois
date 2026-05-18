"""First real CLI for the Galois control plane."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import os
import subprocess
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path

from .benchmark import build_suite_plan, discover_reasoning_data_suite, load_suite, suite_to_dict, write_suite
from .artifacts import (
    archive_reasoning_blueprint,
    archive_writing_project,
    call_verification_api,
    next_artifact_revision,
    normalize_verification_response,
    resolve_problem_statement,
    reasoning_workspace_dir,
    write_reasoning_repair_input,
)
from .config import PlatformConfig, SUPPORTED_MODELS, load_config, model_is_configured
from .contracts import LaunchMode, PipelinePreset, ProblemInput, RunStatus, WorkflowKind, WorkflowLaunch
from .launcher import (
    RunningService,
    WorkflowResult,
    run_workflow,
    start_service_workflow,
    stop_service_workflow,
)
from .paths import ensure_run_layout, resolve_paths
from .run_registry import (
    append_event,
    create_run_manifest,
    update_manifest_status,
    write_manifest,
)
from .serialization import sanitize_for_run_artifact
from .subagents import SubagentManager
from .workflows import build_workflow_plan
from .workflows import build_writing_workflow_plan


@dataclass(slots=True)
class RunFeatureFlags:
    pipeline: PipelinePreset
    verification_enabled: bool
    repair_loop_enabled: bool
    max_repair_rounds: int

PIPELINE_CHOICES = tuple(pipeline.value for pipeline in PipelinePreset)

_WIRE_FAILURE_DECISIONS = frozenset(
    {
        "blueprint_missing",
        "verification_unavailable",
        "verification_api_failed",
        "verification_malformed",
        "verification_not_attempted",
    }
)


def _apply_model_override(config: PlatformConfig, model_override: str | None) -> PlatformConfig:
    if model_override:
        if model_override not in SUPPORTED_MODELS:
            raise SystemExit(f"unsupported model: {model_override}")
        if model_override not in config.model_connections:
            raise SystemExit(f"model is not configured: {model_override}")
        if not model_is_configured(config, model_override):
            raise SystemExit(f"model credentials are not configured: {model_override}")
        config.model = model_override
    return config


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Galois control-plane bootstrap.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    show_parser = subparsers.add_parser("config", help="Print the resolved Galois config.")
    show_parser.add_argument("--config", type=Path, default=None)

    suite_parser = subparsers.add_parser("suite", help="Inspect or materialize benchmark suites.")
    suite_subparsers = suite_parser.add_subparsers(dest="suite_command", required=True)
    suite_list_parser = suite_subparsers.add_parser("list", help="Print benchmark suite problems as JSON.")
    suite_list_parser.add_argument("--suite", type=Path, default=None)
    suite_list_parser.add_argument("--config", type=Path, default=None)
    suite_plan_parser = suite_subparsers.add_parser(
        "plan",
        help="Print the per-problem run plan for a benchmark suite without launching agents.",
    )
    suite_plan_parser.add_argument("--suite", type=Path, default=None)
    suite_plan_parser.add_argument("--config", type=Path, default=None)
    suite_plan_parser.add_argument("--pipeline", choices=PIPELINE_CHOICES, default=None)
    suite_plan_parser.add_argument("--repair-loop", dest="repair_loop", action="store_true", default=None)
    suite_plan_parser.add_argument("--no-repair-loop", dest="repair_loop", action="store_false")
    suite_plan_parser.add_argument("--max-repair-rounds", type=int, default=None)
    suite_plan_parser.add_argument(
        "--limit",
        type=int,
        default=2,
        help="Limit planned problems for quick local checks. Defaults to 2.",
    )
    suite_plan_parser.add_argument(
        "--all",
        action="store_true",
        help="Plan every problem in the suite. Use only for larger benchmark passes.",
    )
    suite_init_parser = suite_subparsers.add_parser(
        "init-examples",
        help="Create the default example suite manifest from three_horse/reasoning/data.",
    )
    suite_init_parser.add_argument("--output", type=Path, default=None)
    suite_init_parser.add_argument("--config", type=Path, default=None)

    plan_parser = subparsers.add_parser("plan", help="Create a run manifest and print workflow plan.")
    plan_parser.add_argument("--problem-id", required=True)
    plan_parser.add_argument("--problem-path", required=True)
    plan_parser.add_argument("--title", default=None)
    plan_parser.add_argument("--config", type=Path, default=None)
    plan_parser.add_argument("--model", choices=SUPPORTED_MODELS, default=None, help="Override the configured model for this run.")
    plan_parser.add_argument(
        "--pipeline",
        choices=PIPELINE_CHOICES,
        default=None,
        help="Top-level system combination. Supported values: reasoning-only, reasoning-verification, writing-only.",
    )
    plan_parser.add_argument("--reasoning-only", action="store_true", help="Run only natural-language reasoning.")
    plan_parser.add_argument(
        "--verification",
        dest="verification",
        action="store_true",
        default=None,
        help="Enable the Rethlas-derived pure-language proof verifier.",
    )
    plan_parser.add_argument(
        "--no-verification",
        dest="verification",
        action="store_false",
        help="Disable the Rethlas-derived pure-language proof verifier.",
    )
    plan_parser.add_argument(
        "--repair-loop",
        dest="repair_loop",
        action="store_true",
        default=None,
        help="Enable the outer platform repair loop when verification asks for repair.",
    )
    plan_parser.add_argument(
        "--no-repair-loop",
        dest="repair_loop",
        action="store_false",
        help="Disable the outer platform repair loop. Agent-internal retries are unaffected.",
    )
    plan_parser.add_argument(
        "--max-repair-rounds",
        type=int,
        default=None,
        help="Override the configured outer platform repair-loop bound for this run.",
    )

    launch_parser = subparsers.add_parser("launch", help="Create a run and launch configured workflows.")
    launch_parser.add_argument("--problem-id", required=True)
    launch_parser.add_argument("--problem-path", required=True)
    launch_parser.add_argument("--title", default=None)
    launch_parser.add_argument("--config", type=Path, default=None)
    launch_parser.add_argument("--model", choices=SUPPORTED_MODELS, default=None, help="Override the configured model for this run.")
    launch_parser.add_argument(
        "--pipeline",
        choices=PIPELINE_CHOICES,
        default=None,
        help="Top-level system combination. Supported values: reasoning-only, reasoning-verification, writing-only.",
    )
    launch_parser.add_argument("--reasoning-only", action="store_true", help="Run only natural-language reasoning.")
    launch_parser.add_argument(
        "--verification",
        dest="verification",
        action="store_true",
        default=None,
        help="Enable the Rethlas-derived pure-language proof verifier.",
    )
    launch_parser.add_argument(
        "--no-verification",
        dest="verification",
        action="store_false",
        help="Disable the Rethlas-derived pure-language proof verifier.",
    )
    launch_parser.add_argument(
        "--repair-loop",
        dest="repair_loop",
        action="store_true",
        default=None,
        help="Enable the outer platform repair loop when verification asks for repair.",
    )
    launch_parser.add_argument(
        "--no-repair-loop",
        dest="repair_loop",
        action="store_false",
        help="Disable the outer platform repair loop. Agent-internal retries are unaffected.",
    )
    launch_parser.add_argument(
        "--max-repair-rounds",
        type=int,
        default=None,
        help="Override the configured outer platform repair-loop bound for this run.",
    )
    launch_parser.add_argument(
        "--skip-services",
        action="store_true",
        help="Skip service workflows such as verification API; useful for offline local checks.",
    )

    inspect_parser = subparsers.add_parser("inspect", help="Print manifest, events, and subagent status.")
    inspect_parser.add_argument("run_id_or_path")
    inspect_parser.add_argument("--config", type=Path, default=None)
    inspect_parser.add_argument("--tail", type=int, default=5, help="Number of recent events to show.")

    garden_parser = subparsers.add_parser("garden", help="Manage Problem Garden data.")
    garden_subparsers = garden_parser.add_subparsers(dest="garden_command", required=True)
    erdos_parser = garden_subparsers.add_parser(
        "import-erdos",
        help="Fetch teorth/erdosproblems and upsert it into the Problem Garden database.",
    )
    erdos_parser.add_argument("--config", type=Path, default=None)
    erdos_parser.add_argument("--source-url", default=None, help="Override the problems.yaml URL.")
    erdos_parser.add_argument("--cache", type=Path, default=None, help="YAML cache path.")
    erdos_parser.add_argument("--no-fetch-yaml", action="store_true", help="Use an existing YAML cache file.")
    erdos_parser.add_argument("--fetch-pages", action="store_true", help="Fetch erdosproblems.com pages for statements.")
    erdos_parser.add_argument("--status", default="open", help="Filter by normalized status. Defaults to open.")
    erdos_parser.add_argument("--limit", type=int, default=10, help="Import only the first N matching records. Defaults to 10.")
    erdos_parser.add_argument("--dry-run", action="store_true", help="Parse and report without writing to the database.")
    opg_parser = garden_subparsers.add_parser(
        "import-open-problem-garden",
        help="Fetch openproblemgarden.org and normalize entries for the Problem Garden.",
    )
    opg_parser.add_argument("--config", type=Path, default=None)
    opg_parser.add_argument("--output-dir", type=Path, default=None, help="Markdown/JSON output directory.")
    opg_parser.add_argument("--cache-dir", type=Path, default=None, help="HTML cache directory.")
    opg_parser.add_argument(
        "--category",
        action="append",
        default=None,
        help="Open Problem Garden category slug. Repeat to import multiple categories.",
    )
    opg_parser.add_argument("--limit", type=int, default=None, help="Limit imported problems across all categories.")
    opg_parser.add_argument("--pages", type=int, default=None, help="Limit category listing pages per category.")
    opg_parser.add_argument("--include-spam", action="store_true", help="Keep obvious spam entries instead of skipping them.")
    opg_parser.add_argument("--no-cache", action="store_true", help="Ignore cached HTML and fetch pages again.")
    opg_parser.add_argument("--delay", type=float, default=0.0, help="Sleep between page fetches.")
    opg_parser.add_argument("--timeout", type=float, default=10.0)
    opg_parser.add_argument("--max-workers", type=int, default=8, help="Concurrent problem-page fetch workers.")
    opg_parser.add_argument("--dry-run", action="store_true", help="Crawl and report without writing files or database rows.")
    opg_parser.add_argument("--write-files", dest="write_files", action="store_true", default=True, help="Write Markdown and index.json files. Enabled by default.")
    opg_parser.add_argument("--no-write-files", dest="write_files", action="store_false", help="Do not write Markdown or index.json files.")
    opg_parser.add_argument("--no-clean-output", action="store_true", help="Do not remove previous opg-*.md files before writing.")
    opg_parser.add_argument("--import-db", action="store_true", help="Upsert normalized problems into the Problem Garden database.")

    web_parser = subparsers.add_parser("web", help="Start the Galois research workbench web UI.")
    web_parser.add_argument("--host", default="127.0.0.1")
    web_parser.add_argument("--port", type=int, default=8000)
    web_parser.add_argument("--config", type=Path, default=None)
    return parser


def cmd_show_config(config_path: Path | None) -> int:
    config = load_config(config_path)
    print(f"backend={config.backend}")
    print(f"model={config.model}")
    print(f"model_reasoning_effort={config.model_reasoning_effort}")
    print(f"codex_bin={config.codex.bin}")
    print(f"codex_base_url_env={config.codex.base_url_env}")
    print(f"codex_base_url_set={bool(config.codex.base_url)}")
    print(f"codex_api_key_env={config.codex.api_key_env}")
    print(f"codex_api_key_set={config.codex.has_api_key}")
    print(f"reasoning_dir={config.reasoning.workdir}")
    print(f"reasoning_enabled={config.reasoning.enabled}")
    print(f"verification_dir={config.verification.workdir}")
    print(f"verification_enabled={config.verification.enabled}")
    print(f"writing_dir={config.writing.workdir}")
    print(f"writing_enabled={config.writing.enabled}")
    print(f"max_repair_rounds={config.max_repair_rounds}")
    print(f"project_root={config.project_root}")
    print(f"run_root={config.run_root}")
    print(f"project_root_path={config.project_root_path}")
    print(f"run_root_path={config.run_root_path}")
    return 0


def cmd_suite_list(suite_path: Path | None, config_path: Path | None) -> int:
    config = load_config(config_path)
    suite = load_suite(suite_path, repo_root=config.repo_root)
    print(json.dumps(suite_to_dict(suite), ensure_ascii=False, indent=2))
    return 0


def cmd_suite_init_examples(output_path: Path | None, config_path: Path | None) -> int:
    config = load_config(config_path)
    suite = discover_reasoning_data_suite(config.repo_root)
    destination = output_path or config.benchmark_root_path / "manifests" / "reasoning_data_examples.toml"
    write_suite(destination, suite)
    print(f"suite_id={suite.suite_id}")
    print(f"problems={len(suite.problems)}")
    print(f"path={destination}")
    return 0


def cmd_suite_plan(
    *,
    suite_path: Path | None,
    config_path: Path | None,
    pipeline: str | None,
    repair_loop: bool | None,
    max_repair_rounds: int | None,
    limit: int,
    all_problems: bool,
) -> int:
    config = load_config(config_path)
    suite = load_suite(suite_path, repo_root=config.repo_root)
    selected_pipeline = PipelinePreset(pipeline) if pipeline else suite.default_pipeline
    if max_repair_rounds is None:
        max_repair_rounds = config.max_repair_rounds
    if repair_loop is None:
        repair_loop = max_repair_rounds > 0
    if selected_pipeline == PipelinePreset.REASONING_ONLY:
        repair_loop = False
        max_repair_rounds = 0
    if max_repair_rounds <= 0:
        repair_loop = False
    if not repair_loop:
        max_repair_rounds = 0
    plan = build_suite_plan(
        suite=suite,
        pipeline=selected_pipeline,
        repair_loop_enabled=repair_loop,
        max_repair_rounds=max_repair_rounds,
        limit=None if all_problems else limit,
    )
    print(json.dumps(plan, ensure_ascii=False, indent=2))
    return 0


def _problem_from_args(problem_id: str, problem_path: str, title: str | None) -> ProblemInput:
    return ProblemInput(
        problem_id=problem_id,
        problem_path=problem_path,
        title=title,
    )


def _print_launch_plan(launches) -> None:
    for launch in launches:
        print(f"[{launch.kind.value}] cwd={launch.cwd}")
        print(f"[{launch.kind.value}] mode={launch.mode.value}")
        print(f"[{launch.kind.value}] entrypoint={launch.entrypoint}")
        if launch.arguments:
            print(f"[{launch.kind.value}] arguments={' '.join(launch.arguments)}")
        if launch.environment:
            env_summary = " ".join(f"{k}={v}" for k, v in sorted(launch.environment.items()))
            print(f"[{launch.kind.value}] env={env_summary}")
        if launch.healthcheck_url:
            print(f"[{launch.kind.value}] healthcheck={launch.healthcheck_url}")


def _looks_mostly_english(text: str) -> bool:
    sample = text[:4000]
    if not sample.strip():
        return True
    ascii_letters = sum(1 for ch in sample if ("a" <= ch.lower() <= "z"))
    non_ascii = sum(1 for ch in sample if ord(ch) > 127 and not ch.isspace())
    if non_ascii == 0:
        return True
    return ascii_letters >= non_ascii * 3


def _translate_statement_to_english(
    *,
    statement: str,
    config: PlatformConfig,
    repo_root: Path,
    run_dir: Path,
) -> str:
    prompt = (
        "Translate the following mathematical problem statement into clear, faithful English. "
        "Preserve all mathematical meaning, notation, quantifiers, and structure. "
        "Do not solve the problem. Do not add commentary. Return only the translated English statement.\n\n"
        f"{statement.strip()}\n"
    )
    completed = subprocess.run(
        [
            config.codex.bin,
            "exec",
            "-C",
            str(repo_root),
            "-m",
            config.model,
            "--output-last-message",
            str(run_dir / "problem" / "statement_english.txt"),
            "--dangerously-bypass-approvals-and-sandbox",
            prompt,
        ],
        cwd=repo_root,
        env={**os.environ},
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"statement translation failed with exit code {completed.returncode}: {completed.stderr.strip()}")
    translated_path = run_dir / "problem" / "statement_english.txt"
    translated = translated_path.read_text(encoding="utf-8").strip()
    if not translated:
        raise RuntimeError("statement translation returned empty output")
    return translated + ("\n" if not translated.endswith("\n") else "")


def _copy_problem_artifacts(run_dir: Path, problem: ProblemInput, repo_root: Path, config: PlatformConfig) -> None:
    problem_dir = run_dir / "problem"
    problem_dir.mkdir(parents=True, exist_ok=True)
    source_path = Path(problem.problem_path)
    if not source_path.is_absolute():
        source_path = repo_root / source_path
    source_path = source_path.resolve()
    source_text = source_path.read_text(encoding="utf-8") if source_path.exists() else ""
    translated_from_source = False
    canonical_statement = source_text
    source_language = "english" if _looks_mostly_english(source_text) else "non_english"
    if source_text and source_language != "english":
        canonical_statement = _translate_statement_to_english(
            statement=source_text,
            config=config,
            repo_root=repo_root,
            run_dir=run_dir,
        )
        translated_from_source = True
    if source_path.exists():
        (problem_dir / "source_statement.md").write_text(source_text, encoding="utf-8")
        (problem_dir / "statement.md").write_text(canonical_statement, encoding="utf-8")
    payload = {
        "problem_id": problem.problem_id,
        "title": problem.title,
        "source_path": str(source_path),
        "tags": problem.tags,
        "source_language": source_language,
        "canonical_language": "english",
        "translated_from_source": translated_from_source,
    }
    (problem_dir / "meta.json").write_text(
        json.dumps(sanitize_for_run_artifact(payload, run_dir=run_dir), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _resolve_run_feature_flags(
    *,
    verification_default: bool,
    max_repair_rounds_default: int,
    pipeline: str | PipelinePreset | None = None,
    reasoning_only: bool,
    verification_override: bool | None,
    repair_loop_override: bool | None = None,
    max_repair_rounds_override: int | None = None,
) -> RunFeatureFlags:
    if reasoning_only:
        selected_pipeline = PipelinePreset.REASONING_ONLY
    elif pipeline is None:
        if verification_default:
            selected_pipeline = PipelinePreset.REASONING_VERIFICATION
        else:
            selected_pipeline = PipelinePreset.REASONING_ONLY
    elif isinstance(pipeline, PipelinePreset):
        selected_pipeline = pipeline
    else:
        selected_pipeline = PipelinePreset(pipeline)

    if selected_pipeline == PipelinePreset.REASONING_ONLY:
        verification_enabled = False
    elif selected_pipeline == PipelinePreset.REASONING_VERIFICATION:
        verification_enabled = True
    elif selected_pipeline == PipelinePreset.WRITING_ONLY:
        verification_enabled = False
    else:
        raise ValueError(f"unsupported pipeline: {selected_pipeline}")

    if verification_override is not None:
        verification_enabled = verification_override

    max_repair_rounds = (
        max_repair_rounds_default if max_repair_rounds_override is None else max(max_repair_rounds_override, 0)
    )
    if not verification_enabled:
        repair_loop_enabled = False
    else:
        repair_loop_enabled = repair_loop_override if repair_loop_override is not None else max_repair_rounds > 0
    if max_repair_rounds <= 0:
        repair_loop_enabled = False
    if not repair_loop_enabled:
        max_repair_rounds = 0

    return RunFeatureFlags(
        pipeline=selected_pipeline,
        verification_enabled=verification_enabled,
        repair_loop_enabled=repair_loop_enabled,
        max_repair_rounds=max_repair_rounds,
    )


def _prepare_reasoning_workspace(run_dir: Path, repo_root: Path) -> Path:
    workspace_dir = reasoning_workspace_dir(run_dir)
    workspace_dir.mkdir(parents=True, exist_ok=True)

    for relative in ("memory", "results"):
        (workspace_dir / relative).mkdir(parents=True, exist_ok=True)
    return workspace_dir


def _prepare_verification_workspace(run_dir: Path, repo_root: Path) -> Path:
    workspace_dir = run_dir / "verification" / "workspace"
    workspace_dir.mkdir(parents=True, exist_ok=True)

    for relative in ("memory", "results"):
        (workspace_dir / relative).mkdir(parents=True, exist_ok=True)
    return workspace_dir


def _prepare_writing_workspace(run_dir: Path, repo_root: Path) -> Path:
    workspace_dir = run_dir / "writing" / "workspace"
    workspace_dir.mkdir(parents=True, exist_ok=True)

    for relative in ("memory", "results", "citations", "downloads"):
        (workspace_dir / relative).mkdir(parents=True, exist_ok=True)
    return workspace_dir


def _stage_input_for_writing_workspace(
    *,
    run_dir: Path,
    repo_root: Path,
    problem: ProblemInput,
) -> None:
    source_path = Path(problem.problem_path)
    if not source_path.is_absolute():
        source_path = repo_root / source_path
    source_path = source_path.resolve()
    writing_input = run_dir / "writing" / "input.md"
    if writing_input.exists():
        return
    if source_path.exists() and source_path != writing_input:
        writing_input.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, writing_input)


def _stage_problem_for_reasoning_workspace(
    *,
    run_dir: Path,
    repo_root: Path,
    problem: ProblemInput,
) -> None:
    source_path = Path(problem.problem_path)
    if not source_path.is_absolute():
        source_path = repo_root / source_path
    source_path = source_path.resolve()
    run_problem = run_dir / "problem" / "statement.md"
    if run_problem.exists():
        return
    if source_path.exists() and source_path != run_problem:
        run_problem.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, run_problem)


def _publish_reasoning_repair_contract(run_dir: Path, revision: int) -> str | None:
    source_path = run_dir / "reasoning" / f"repair_input_r{revision}.json"
    if not source_path.exists():
        return None
    workspace_dir = reasoning_workspace_dir(run_dir)
    contract_dir = workspace_dir / "contracts"
    contract_dir.mkdir(parents=True, exist_ok=True)
    destination_path = contract_dir / source_path.name
    shutil.copyfile(source_path, destination_path)
    return str(destination_path)


def _publish_verified_blueprint(run_dir: Path, problem: ProblemInput, blueprint: BlueprintArchiveResult) -> str | None:
    if not blueprint.markdown_path:
        return None
    source_path = Path(blueprint.markdown_path)
    if not source_path.exists():
        return None
    destination_path = reasoning_workspace_dir(run_dir) / "results" / problem.problem_id / "blueprint_verified.md"
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_path, destination_path)
    return str(destination_path)


def _feature_payload(feature_flags: RunFeatureFlags) -> dict[str, object]:
    return {
        "pipeline": feature_flags.pipeline.value,
        "verification_enabled": feature_flags.verification_enabled,
        "repair_loop_enabled": feature_flags.repair_loop_enabled,
        "max_repair_rounds": feature_flags.max_repair_rounds,
    }


def _parse_iso8601(timestamp: str | None) -> datetime | None:
    if not timestamp:
        return None
    normalized = timestamp.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        return None


def _duration_seconds(started_at: str | None, finished_at: str | None) -> int | None:
    started = _parse_iso8601(started_at)
    finished = _parse_iso8601(finished_at)
    if started is None or finished is None:
        return None
    return max(0, int(round((finished - started).total_seconds())))


def _load_run_events(run_dir: Path) -> list[dict[str, object]]:
    events_path = run_dir / "events.jsonl"
    if not events_path.exists():
        return []
    events: list[dict[str, object]] = []
    for line in events_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        payload = json.loads(line)
        if isinstance(payload, dict):
            events.append(payload)
    return events


def _compute_run_metrics(run_dir: Path, results: list[WorkflowResult]) -> dict[str, int]:
    metrics = {
        "total_runtime_seconds": 0,
        "reasoning_runtime_seconds": 0,
        "verification_runtime_seconds": 0,
        "writing_runtime_seconds": 0,
        "reasoning_attempts": 0,
        "verification_calls": 0,
        "search_calls": 0,
        "repair_rounds": 0,
    }

    started_values = [value for value in (_parse_iso8601(result.started_at) for result in results) if value is not None]
    finished_values = [value for value in (_parse_iso8601(result.finished_at) for result in results) if value is not None]
    if started_values and finished_values:
        metrics["total_runtime_seconds"] = max(0, int(round((max(finished_values) - min(started_values)).total_seconds())))

    for result in results:
        duration = _duration_seconds(result.started_at, result.finished_at) or 0
        if result.workflow == WorkflowKind.REASONING.value:
            metrics["reasoning_runtime_seconds"] += duration
        elif result.workflow == WorkflowKind.VERIFICATION.value:
            metrics["verification_runtime_seconds"] += duration
        elif result.workflow == WorkflowKind.WRITING.value:
            metrics["writing_runtime_seconds"] += duration

    events = _load_run_events(run_dir)
    metrics["reasoning_attempts"] = sum(1 for event in events if event.get("event_type") == "reasoning_iteration_started")
    metrics["verification_calls"] = sum(
        1
        for event in events
        if event.get("event_type") == "artifact_collected"
        and isinstance(event.get("payload"), dict)
        and event["payload"].get("artifact") == "verification_report"
    )
    metrics["repair_rounds"] = sum(
        1
        for event in events
        if event.get("event_type") == "repair_input_written"
        and isinstance(event.get("payload"), dict)
        and event["payload"].get("written")
    )

    reasoning_events = run_dir / "reasoning" / "workspace" / "memory"
    if reasoning_events.exists():
        for events_file in reasoning_events.glob("*/events.jsonl"):
            for line in events_file.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                payload = json.loads(line)
                if not isinstance(payload, dict):
                    continue
                record = payload.get("record") if payload.get("channel") == "events" else payload
                if isinstance(record, dict) and record.get("event_type") == "search_math_results":
                    metrics["search_calls"] += 1

    return metrics


def _write_summary(run_dir: Path, results: list[WorkflowResult], feature_flags: RunFeatureFlags) -> None:
    metrics = _compute_run_metrics(run_dir, results)
    (run_dir / "metrics.json").write_text(
        json.dumps(sanitize_for_run_artifact(metrics, run_dir=run_dir), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    lines = ["# Galois Run Summary", ""]
    lines.extend(
        [
            "## Mode",
            "",
            f"- pipeline: `{feature_flags.pipeline.value}`",
            f"- verification_enabled: `{feature_flags.verification_enabled}`",
            f"- repair_loop_enabled: `{feature_flags.repair_loop_enabled}`",
            f"- max_repair_rounds: `{feature_flags.max_repair_rounds}`",
            "",
        ]
    )
    lines.extend(
        [
            "## Metrics",
            "",
            f"- total_runtime_seconds: `{metrics['total_runtime_seconds']}`",
            f"- reasoning_runtime_seconds: `{metrics['reasoning_runtime_seconds']}`",
            f"- verification_runtime_seconds: `{metrics['verification_runtime_seconds']}`",
            f"- writing_runtime_seconds: `{metrics['writing_runtime_seconds']}`",
            f"- reasoning_attempts: `{metrics['reasoning_attempts']}`",
            f"- verification_calls: `{metrics['verification_calls']}`",
            f"- search_calls: `{metrics['search_calls']}`",
            f"- repair_rounds: `{metrics['repair_rounds']}`",
            "",
        ]
    )
    for result in results:
        stdout_path = sanitize_for_run_artifact(result.stdout_path, run_dir=run_dir)
        stderr_path = sanitize_for_run_artifact(result.stderr_path, run_dir=run_dir)
        lines.extend(
            [
                f"## {result.workflow}",
                "",
                f"- status: `{result.status}`",
                f"- mode: `{result.mode.value}`",
                f"- exit_code: `{result.exit_code}`",
                f"- stdout: `{stdout_path}`",
                f"- stderr: `{stderr_path}`",
                "",
            ]
        )
        if result.error:
            lines.extend([f"error: {result.error}", ""])

    decision_files = sorted((run_dir / "verification").glob("verification_decision_r*.json"))
    repair_files = sorted((run_dir / "reasoning").glob("repair_input_r*.json"))
    if decision_files:
        latest = json.loads(decision_files[-1].read_text(encoding="utf-8"))
        lines.extend(
            [
                "## Contracts",
                "",
                f"- verification_decision: `{latest.get('decision')}`",
                f"- verification_decision_path: `{sanitize_for_run_artifact(decision_files[-1], run_dir=run_dir)}`",
                f"- repair_input_path: `{sanitize_for_run_artifact(repair_files[-1], run_dir=run_dir)}`"
                if repair_files
                else "- repair_input_path: ``",
                "",
            ]
        )

    wire_failures = [
        event for event in _load_run_events(run_dir)
        if event.get("event_type") == "wire_failed" and isinstance(event.get("payload"), dict)
    ]
    if wire_failures:
        latest_failure = wire_failures[-1].get("payload") or {}
        lines.extend(
            [
                "## Wire Failure",
                "",
                f"- decision: `{latest_failure.get('decision')}`",
                f"- attempt: `{latest_failure.get('attempt')}`",
                "",
            ]
        )
    (run_dir / "summary.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def _wire_reasoning_to_downstream(
    *,
    run_dir: Path,
    run_id: str,
    problem: ProblemInput,
    repo_root: Path,
    feature_flags: RunFeatureFlags,
    verification_url: str | None,
) -> str:
    revision = next_artifact_revision(run_dir, "reasoning", "blueprint_r*.md")
    blueprint = archive_reasoning_blueprint(run_dir, problem, revision=revision)
    append_event(
        run_dir,
        run_id=run_id,
        workflow="reasoning",
        event_type="artifact_collected",
        payload={
            "artifact": "blueprint",
            "revision": revision,
            "found": blueprint.found,
            "source_path": blueprint.source_path,
            "markdown_path": blueprint.markdown_path,
            "json_path": blueprint.json_path,
        },
    )
    if not blueprint.found:
        return "blueprint_missing"

    if not feature_flags.verification_enabled:
        append_event(
            run_dir,
            run_id=run_id,
            workflow="verification",
            event_type="verification_skipped",
            payload={
                "revision": revision,
                "reason": "disabled",
            },
        )
        return "verification_disabled"

    if verification_url is None:
        append_event(
            run_dir,
            run_id=run_id,
            workflow="verification",
            event_type="verification_unavailable",
            payload={
                "revision": revision,
                "reason": "service_unavailable",
            },
        )
        return "verification_unavailable"

    statement, statement_path = resolve_problem_statement(problem, repo_root, run_dir=run_dir)
    verification = call_verification_api(
        run_dir=run_dir,
        problem=problem,
        statement=statement,
        proof=blueprint.content,
        url=verification_url,
        revision=revision,
    )
    append_event(
        run_dir,
        run_id=run_id,
        workflow="verification",
        event_type="artifact_collected",
        payload={
            "artifact": "verification_report",
            "revision": revision,
            "attempted": verification.attempted,
            "succeeded": verification.succeeded,
            "statement_path": str(statement_path),
            "request_path": verification.request_path,
            "response_path": verification.response_path,
            "error": verification.error,
        },
    )
    normalized = normalize_verification_response(
        run_dir=run_dir,
        problem=problem,
        revision=revision,
        request_result=verification,
    )
    append_event(
        run_dir,
        run_id=run_id,
        workflow="verification",
        event_type="verification_decision",
        payload={
            "revision": revision,
            "status": normalized.status,
            "decision": normalized.decision,
            "normalized_path": normalized.normalized_path,
            "decision_path": normalized.decision_path,
            "raw_response_path": normalized.raw_response_path,
            "error": normalized.error,
        },
    )
    repair_input = write_reasoning_repair_input(
        run_dir=run_dir,
        problem=problem,
        blueprint=blueprint,
        normalized=normalized,
        revision=revision,
    )
    append_event(
        run_dir,
        run_id=run_id,
        workflow="reasoning",
        event_type="repair_input_written",
        payload={
            "revision": revision,
            "written": repair_input.written,
            "path": repair_input.path,
        },
    )
    published_repair_path = _publish_reasoning_repair_contract(run_dir, revision)
    append_event(
        run_dir,
        run_id=run_id,
        workflow="reasoning",
        event_type="repair_contract_published",
        payload={
            "revision": revision,
            "published": bool(published_repair_path),
            "path": published_repair_path,
        },
    )
    published_verified_path = None
    if normalized.decision == "accepted":
        published_verified_path = _publish_verified_blueprint(run_dir, problem, blueprint)
        append_event(
            run_dir,
            run_id=run_id,
            workflow="reasoning",
            event_type="verified_blueprint_published",
            payload={
                "revision": revision,
                "published": bool(published_verified_path),
                "path": published_verified_path,
            },
        )
    return normalized.decision


def _wire_writing_to_downstream(
    *,
    run_dir: Path,
    run_id: str,
    problem: ProblemInput,
) -> str:
    revision = next_artifact_revision(run_dir, "writing", "paper_project_r*.json")
    project = archive_writing_project(run_dir, problem, revision=revision)
    append_event(
        run_dir,
        run_id=run_id,
        workflow="writing",
        event_type="artifact_collected",
        payload={
            "artifact": "paper_project",
            "revision": revision,
            "found": project.found,
            "project_id": project.project_id,
            "source_dir": project.source_dir,
            "artifact_paths": project.artifact_paths or {},
        },
    )
    return "writing_artifacts_collected" if project.found else "writing_artifacts_missing"


def _find_launch(launches: list[WorkflowLaunch], kind: WorkflowKind) -> WorkflowLaunch | None:
    for launch in launches:
        if launch.kind == kind:
            return launch
    return None


def _resolve_run_dir(run_id_or_path: str, run_root: Path) -> Path:
    candidate = Path(run_id_or_path)
    if candidate.exists():
        return candidate.resolve()
    return (run_root / run_id_or_path).resolve()


def cmd_plan_run(
    problem_id: str,
    problem_path: str,
    title: str | None,
    config_path: Path | None,
    reasoning_only: bool,
    verification: bool | None,
    pipeline: str | None = None,
    repair_loop: bool | None = None,
    max_repair_rounds: int | None = None,
    model_override: str | None = None,
) -> int:
    config = _apply_model_override(load_config(config_path), model_override)
    paths = resolve_paths(config)
    ensure_run_layout(paths)
    feature_flags = _resolve_run_feature_flags(
        verification_default=config.verification.enabled,
        max_repair_rounds_default=config.max_repair_rounds,
        pipeline=pipeline,
        reasoning_only=reasoning_only,
        verification_override=verification,
        repair_loop_override=repair_loop,
        max_repair_rounds_override=max_repair_rounds,
    )

    problem = _problem_from_args(problem_id, problem_path, title)
    run_dir, manifest = create_run_manifest(config=config, paths=paths, problem=problem)
    launches = build_workflow_plan(
        config=config,
        paths=paths,
        problem=problem,
        run_dir=run_dir,
        verification_enabled=feature_flags.verification_enabled,
    ) if feature_flags.pipeline != PipelinePreset.WRITING_ONLY else build_writing_workflow_plan(
        config=config,
        paths=paths,
        problem=problem,
        run_dir=run_dir,
    )
    manifest.pipeline = feature_flags.pipeline
    manifest.features = _feature_payload(feature_flags)
    manifest.workflows = [launch.kind for launch in launches]
    write_manifest(run_dir, manifest)

    print(f"run_id={manifest.run_id}")
    print(f"run_dir={run_dir}")
    print(f"pipeline={feature_flags.pipeline.value}")
    print(f"model={config.model}")
    print(f"verification_enabled={feature_flags.verification_enabled}")
    print(f"repair_loop_enabled={feature_flags.repair_loop_enabled}")
    print(f"max_repair_rounds={feature_flags.max_repair_rounds}")
    _print_launch_plan(launches)
    return 0


def execute_run_workflows(
    *,
    config: PlatformConfig,
    paths,
    run_dir: Path,
    manifest,
    problem: ProblemInput,
    launches: list[WorkflowLaunch],
    feature_flags: RunFeatureFlags,
) -> int:
    update_manifest_status(run_dir, manifest, RunStatus.RUNNING)

    print(f"run_id={manifest.run_id}")
    print(f"run_dir={run_dir}")
    print(f"pipeline={feature_flags.pipeline.value}")
    print(f"model={config.model}")
    print(f"verification_enabled={feature_flags.verification_enabled}")
    print(f"repair_loop_enabled={feature_flags.repair_loop_enabled}")
    print(f"max_repair_rounds={feature_flags.max_repair_rounds}")

    results: list[WorkflowResult] = []
    services: list[RunningService] = []
    manager = SubagentManager()
    final_status = RunStatus.SUCCEEDED
    service_error: str | None = None
    reasoning_launch = _find_launch(launches, WorkflowKind.REASONING)
    writing_launch = _find_launch(launches, WorkflowKind.WRITING)
    try:
        verification_url: str | None = None
        for launch in launches:
            if launch.mode == LaunchMode.SERVICE:
                service = start_service_workflow(
                    run_dir=run_dir,
                    run_id=manifest.run_id,
                    launch=launch,
                    manager=manager,
                )
                services.append(service)
                task = service.manager.get_task(service.task_id)
                print(f"[{launch.kind.value}] service_ready pid={task.pid if task else None}")
                if launch.kind.value == "verification":
                    verification_url = "http://127.0.0.1:8091/verify"

        for launch in launches:
            if launch.mode == LaunchMode.SERVICE or launch.kind in {WorkflowKind.REASONING, WorkflowKind.WRITING}:
                continue
            result = run_workflow(run_dir=run_dir, run_id=manifest.run_id, launch=launch, manager=manager)
            results.append(result)
            print(f"[{result.workflow}] status={result.status} exit_code={result.exit_code}")
            if result.status != "succeeded":
                final_status = RunStatus.FAILED
                break
        if final_status == RunStatus.SUCCEEDED and reasoning_launch is not None:
            decision = ""
            attempts = 0
            while final_status == RunStatus.SUCCEEDED:
                attempts += 1
                append_event(
                    run_dir,
                    run_id=manifest.run_id,
                    workflow="reasoning",
                    event_type="reasoning_iteration_started",
                    payload={"attempt": attempts},
                )
                print(f"[{reasoning_launch.kind.value}] status=running attempt={attempts}")
                reasoning_result = run_workflow(
                    run_dir=run_dir,
                    run_id=manifest.run_id,
                    launch=reasoning_launch,
                    manager=manager,
                )
                results.append(reasoning_result)
                print(f"[{reasoning_result.workflow}] status={reasoning_result.status} exit_code={reasoning_result.exit_code}")
                if reasoning_result.status != "succeeded":
                    final_status = RunStatus.FAILED
                    break

                decision = _wire_reasoning_to_downstream(
                    run_dir=run_dir,
                    run_id=manifest.run_id,
                    problem=problem,
                    repo_root=paths.repo_root,
                    feature_flags=feature_flags,
                    verification_url=verification_url,
                )
                append_event(
                    run_dir,
                    run_id=manifest.run_id,
                    workflow="reasoning",
                    event_type="reasoning_iteration_finished",
                    payload={
                        "attempt": attempts,
                        "decision": decision,
                    },
                )
                if decision in _WIRE_FAILURE_DECISIONS:
                    final_status = RunStatus.FAILED
                    service_error = service_error or f"wire_failed:{decision}"
                    append_event(
                        run_dir,
                        run_id=manifest.run_id,
                        workflow="reasoning",
                        event_type="wire_failed",
                        payload={"attempt": attempts, "decision": decision},
                    )
                    print(f"[reasoning] wire_failed decision={decision}")
                    break
                if decision != "repair_needed":
                    break
                if not feature_flags.repair_loop_enabled:
                    append_event(
                        run_dir,
                        run_id=manifest.run_id,
                        workflow="reasoning",
                        event_type="repair_loop_skipped",
                        payload={
                            "attempts": attempts,
                            "reason": "disabled",
                        },
                    )
                    break
                if attempts > feature_flags.max_repair_rounds:
                    append_event(
                        run_dir,
                        run_id=manifest.run_id,
                        workflow="reasoning",
                        event_type="repair_loop_exhausted",
                        payload={
                            "attempts": attempts,
                            "max_repair_rounds": feature_flags.max_repair_rounds,
                        },
                    )
                    break
                repair_path = run_dir / "reasoning" / f"repair_input_r{attempts}.json"
                reasoning_launch.environment["REPAIR_INPUT_FILE"] = str(
                    reasoning_workspace_dir(run_dir) / "contracts" / repair_path.name
                )
                reasoning_launch.environment["RESUME"] = "auto" if config.resume_enabled else "0"
        if final_status == RunStatus.SUCCEEDED and writing_launch is not None:
            append_event(
                run_dir,
                run_id=manifest.run_id,
                workflow="writing",
                event_type="writing_iteration_started",
                payload={"attempt": 1},
            )
            print(f"[{writing_launch.kind.value}] status=running attempt=1")
            writing_result = run_workflow(
                run_dir=run_dir,
                run_id=manifest.run_id,
                launch=writing_launch,
                manager=manager,
            )
            results.append(writing_result)
            print(f"[{writing_result.workflow}] status={writing_result.status} exit_code={writing_result.exit_code}")
            if writing_result.status != "succeeded":
                final_status = RunStatus.FAILED
            else:
                decision = _wire_writing_to_downstream(
                    run_dir=run_dir,
                    run_id=manifest.run_id,
                    problem=problem,
                )
                append_event(
                    run_dir,
                    run_id=manifest.run_id,
                    workflow="writing",
                    event_type="writing_iteration_finished",
                    payload={
                        "attempt": 1,
                        "decision": decision,
                    },
                )
    except Exception as exc:
        final_status = RunStatus.FAILED
        service_error = str(exc)
        append_event(
            run_dir,
            run_id=manifest.run_id,
            event_type="run_error",
            payload={"error": service_error},
        )
        print(f"launch failed: {service_error}")
    finally:
        while services:
            service = services.pop()
            service_result = stop_service_workflow(
                run_dir=run_dir,
                run_id=manifest.run_id,
                service=service,
                failed_error=service_error if final_status == RunStatus.FAILED else None,
            )
            results.insert(0, service_result)
            print(
                f"[{service_result.workflow}] status={service_result.status} "
                f"exit_code={service_result.exit_code}"
            )
        manager.write_snapshots(run_dir / "subagents.json")

    _write_summary(run_dir, results, feature_flags)
    update_manifest_status(run_dir, manifest, final_status)
    append_event(
        run_dir,
        run_id=manifest.run_id,
        event_type="run_finished",
        payload={
            "status": final_status.value,
            **_feature_payload(feature_flags),
            "workflow_results": [
                {
                    **asdict(result),
                    "mode": result.mode.value,
                }
                for result in results
            ],
        },
    )
    return 0 if final_status == RunStatus.SUCCEEDED else 1


def cmd_launch_run(
    problem_id: str,
    problem_path: str,
    title: str | None,
    config_path: Path | None,
    reasoning_only: bool,
    verification: bool | None,
    skip_services: bool,
    pipeline: str | None = None,
    repair_loop: bool | None = None,
    max_repair_rounds: int | None = None,
    model_override: str | None = None,
) -> int:
    config = _apply_model_override(load_config(config_path), model_override)
    paths = resolve_paths(config)
    ensure_run_layout(paths)
    feature_flags = _resolve_run_feature_flags(
        verification_default=config.verification.enabled,
        max_repair_rounds_default=config.max_repair_rounds,
        pipeline=pipeline,
        reasoning_only=reasoning_only,
        verification_override=verification,
        repair_loop_override=repair_loop,
        max_repair_rounds_override=max_repair_rounds,
    )

    problem = _problem_from_args(problem_id, problem_path, title)
    run_dir, manifest = create_run_manifest(config=config, paths=paths, problem=problem)
    _copy_problem_artifacts(run_dir, problem, paths.repo_root, config)

    launches = build_workflow_plan(
        config=config,
        paths=paths,
        problem=problem,
        run_dir=run_dir,
        verification_enabled=feature_flags.verification_enabled,
    ) if feature_flags.pipeline != PipelinePreset.WRITING_ONLY else build_writing_workflow_plan(
        config=config,
        paths=paths,
        problem=problem,
        run_dir=run_dir,
    )
    if skip_services:
        launches = [launch for launch in launches if launch.mode.value != "service"]
    if _find_launch(launches, WorkflowKind.REASONING) is not None:
        _prepare_reasoning_workspace(run_dir, paths.repo_root)
        _stage_problem_for_reasoning_workspace(run_dir=run_dir, repo_root=paths.repo_root, problem=problem)
    if _find_launch(launches, WorkflowKind.VERIFICATION) is not None:
        _prepare_verification_workspace(run_dir, paths.repo_root)
    if _find_launch(launches, WorkflowKind.WRITING) is not None:
        _prepare_writing_workspace(run_dir, paths.repo_root)
        _stage_input_for_writing_workspace(run_dir=run_dir, repo_root=paths.repo_root, problem=problem)
    manifest.pipeline = feature_flags.pipeline
    manifest.features = _feature_payload(feature_flags)
    manifest.workflows = [launch.kind for launch in launches]
    write_manifest(run_dir, manifest)

    append_event(
        run_dir,
        run_id=manifest.run_id,
        event_type="run_created",
        payload={
            "problem": asdict(problem),
            "run_dir": str(run_dir),
            "workflow_count": len(launches),
            "skip_services": skip_services,
            **_feature_payload(feature_flags),
        },
    )
    return execute_run_workflows(
        config=config,
        paths=paths,
        run_dir=run_dir,
        manifest=manifest,
        problem=problem,
        launches=launches,
        feature_flags=feature_flags,
    )


def cmd_inspect_run(run_id_or_path: str, tail: int, config_path: Path | None) -> int:
    config = load_config(config_path)
    run_dir = _resolve_run_dir(run_id_or_path, config.run_root_path)
    if not run_dir.exists():
        raise SystemExit(f"run not found: {run_dir}")

    manifest_path = run_dir / "manifest.json"
    events_path = run_dir / "events.jsonl"
    subagents_path = run_dir / "subagents.json"
    summary_path = run_dir / "summary.md"

    print(f"run_dir={run_dir}")
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        print(f"run_id={manifest.get('run_id')}")
        print(f"status={manifest.get('status')}")
        print(f"pipeline={manifest.get('pipeline')}")
        print(f"problem_id={manifest.get('problem', {}).get('problem_id')}")
        print(f"workflows={','.join(manifest.get('workflows', []))}")
        features = manifest.get("features") or {}
        if features:
            print(f"features={json.dumps(features, ensure_ascii=False, sort_keys=True)}")
    else:
        print("manifest=missing")

    if subagents_path.exists():
        subagents = json.loads(subagents_path.read_text(encoding="utf-8"))
        print(f"subagents={len(subagents)}")
        for task in subagents:
            print(
                f"[subagent] {task.get('task_id')} workflow={task.get('workflow_kind')} "
                f"status={task.get('status')} returncode={task.get('returncode')} "
                f"pid={task.get('pid')}"
            )
    else:
        print("subagents=missing")

    if events_path.exists():
        events = [line for line in events_path.read_text(encoding="utf-8").splitlines() if line]
        print(f"events={len(events)}")
        for line in events[-max(tail, 0) :]:
            event = json.loads(line)
            print(
                f"[event] {event.get('event_type')} workflow={event.get('workflow')} "
                f"timestamp={event.get('timestamp')}"
            )
    else:
        print("events=missing")

    if summary_path.exists():
        print(f"summary={summary_path}")
    return 0


def cmd_web(host: str, port: int, config_path: Path | None) -> int:
    import uvicorn

    from .web import create_app

    uvicorn.run(create_app(config_path=config_path), host=host, port=port)
    return 0


def cmd_import_erdos_problems(
    *,
    config_path: Path | None,
    source_url: str | None,
    cache_path: Path | None,
    no_fetch_yaml: bool,
    fetch_pages: bool,
    status: str | None,
    limit: int | None,
    dry_run: bool,
) -> int:
    from datetime import UTC

    from galois.tools.erdos_problems import (
        DEFAULT_CACHE_PATH,
        ERDOS_PROBLEMS_YAML_URL,
        build_garden_problems,
        fetch_yaml,
        load_yaml_records,
        write_yaml_cache,
    )

    from .problem_garden import ProblemGardenStore

    config = load_config(config_path)
    yaml_url = source_url or ERDOS_PROBLEMS_YAML_URL
    cache = cache_path or DEFAULT_CACHE_PATH
    if not no_fetch_yaml:
        write_yaml_cache(fetch_yaml(yaml_url), cache)
    records = load_yaml_records(cache)
    normalized_status = status.strip() if status else None
    problems, errors = build_garden_problems(
        records,
        fetch_pages=fetch_pages,
        limit=limit,
        status=normalized_status or None,
    )
    if dry_run:
        print(
            json.dumps(
                {
                    "source_url": yaml_url,
                    "cache": str(cache),
                    "records": len(records),
                    "status": normalized_status,
                    "parsed": len(problems),
                    "errors": errors,
                    "sample_ids": [problem["id"] for problem in problems[:5]],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0 if not errors else 2

    with ProblemGardenStore(config.database.connection_url) as store:
        store.initialize()
        imported = store.upsert_problems(problems)
        store.record_import_batch(
            batch_id=f"erdosproblems-{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}",
            source_name="teorth/erdosproblems",
            source_url=yaml_url,
            item_count=len(problems) + len(errors),
            imported_count=imported,
            skipped_count=len(errors),
            fetch_pages=fetch_pages,
        )
    print(
        json.dumps(
            {
                "source_url": yaml_url,
                "cache": str(cache),
                "records": len(records),
                "status": normalized_status,
                "imported": imported,
                "errors": errors,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if not errors else 2


def cmd_import_open_problem_garden(
    *,
    config_path: Path | None,
    output_dir: Path | None,
    cache_dir: Path | None,
    category_slugs: list[str] | None,
    limit: int | None,
    pages: int | None,
    include_spam: bool,
    no_cache: bool,
    delay: float,
    timeout: float,
    max_workers: int,
    dry_run: bool,
    write_files: bool,
    clean_output: bool,
    import_db: bool,
) -> int:
    from datetime import UTC

    from galois.tools.open_problem_garden import (
        DEFAULT_CACHE_DIR,
        DEFAULT_OUTPUT_DIR,
        OPEN_PROBLEM_GARDEN_BASE_URL,
        crawl_open_problem_garden,
        write_problem_files,
    )

    from .problem_garden import ProblemGardenStore

    result = crawl_open_problem_garden(
        category_slugs=category_slugs,
        limit=limit,
        pages=pages,
        include_spam=include_spam,
        cache_dir=cache_dir or DEFAULT_CACHE_DIR,
        use_cache=not no_cache,
        timeout=timeout,
        delay=delay,
        max_workers=max_workers,
    )
    written: list[Path] = []
    imported = 0
    should_write_files = write_files and not dry_run
    should_import_db = import_db and not dry_run
    if should_write_files:
        written = write_problem_files(
            result.problems,
            output_dir=output_dir or DEFAULT_OUTPUT_DIR,
            errors=result.errors,
            skipped=result.skipped,
            clean=clean_output,
        )
    if should_import_db:
        config = load_config(config_path)
        with ProblemGardenStore(config.database.connection_url) as store:
            store.initialize()
            imported = store.upsert_problems(result.problems)
            store.record_import_batch(
                batch_id=f"openproblemgarden-{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}",
                source_name="openproblemgarden.org",
                source_url=OPEN_PROBLEM_GARDEN_BASE_URL,
                item_count=len(result.problems) + len(result.skipped) + len(result.errors),
                imported_count=imported,
                skipped_count=len(result.skipped) + len(result.errors),
                fetch_pages=True,
            )
    print(
        json.dumps(
            {
                "source_url": OPEN_PROBLEM_GARDEN_BASE_URL,
                "categories": category_slugs or "all",
                "parsed": len(result.problems),
                "skipped": len(result.skipped),
                "errors": result.errors,
                "sample_ids": [problem["id"] for problem in result.problems[:5]],
                "written": [str(path) for path in written],
                "imported": imported,
                "dry_run": dry_run,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if not result.errors else 2


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "config":
        return cmd_show_config(args.config)
    if args.command == "suite":
        if args.suite_command == "list":
            return cmd_suite_list(args.suite, args.config)
        if args.suite_command == "plan":
            return cmd_suite_plan(
                suite_path=args.suite,
                config_path=args.config,
                pipeline=args.pipeline,
                repair_loop=args.repair_loop,
                max_repair_rounds=args.max_repair_rounds,
                limit=args.limit,
                all_problems=args.all,
            )
        if args.suite_command == "init-examples":
            return cmd_suite_init_examples(args.output, args.config)
        raise SystemExit(f"unknown suite command: {args.suite_command}")
    if args.command == "plan":
        return cmd_plan_run(
            args.problem_id,
            args.problem_path,
            args.title,
            args.config,
            args.reasoning_only,
            args.verification,
            args.pipeline,
            args.repair_loop,
            args.max_repair_rounds,
            args.model,
        )
    if args.command == "launch":
        return cmd_launch_run(
            args.problem_id,
            args.problem_path,
            args.title,
            args.config,
            args.reasoning_only,
            args.verification,
            args.skip_services,
            args.pipeline,
            args.repair_loop,
            args.max_repair_rounds,
            args.model,
        )
    if args.command == "inspect":
        return cmd_inspect_run(args.run_id_or_path, args.tail, getattr(args, "config", None))
    if args.command == "garden":
        if args.garden_command == "import-erdos":
            return cmd_import_erdos_problems(
                config_path=args.config,
                source_url=args.source_url,
                cache_path=args.cache,
                no_fetch_yaml=args.no_fetch_yaml,
                fetch_pages=args.fetch_pages,
                status=args.status,
                limit=args.limit,
                dry_run=args.dry_run,
            )
        if args.garden_command == "import-open-problem-garden":
            return cmd_import_open_problem_garden(
                config_path=args.config,
                output_dir=args.output_dir,
                cache_dir=args.cache_dir,
                category_slugs=args.category,
                limit=args.limit,
                pages=args.pages,
                include_spam=args.include_spam,
                no_cache=args.no_cache,
                delay=args.delay,
                timeout=args.timeout,
                max_workers=args.max_workers,
                dry_run=args.dry_run,
                write_files=args.write_files,
                clean_output=not args.no_clean_output,
                import_db=args.import_db,
            )
        raise SystemExit(f"unknown garden command: {args.garden_command}")
    if args.command == "web":
        return cmd_web(args.host, args.port, args.config)
    raise SystemExit(f"unknown command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
