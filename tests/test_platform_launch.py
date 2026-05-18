from __future__ import annotations

import importlib
import json
import os
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from galois.platform.artifacts import (
    BlueprintArchiveResult,
    VerificationRequestResult,
    archive_reasoning_blueprint,
    archive_writing_project,
    call_verification_api,
    next_artifact_revision,
    normalize_verification_response,
    reasoning_workspace_dir,
    write_reasoning_repair_input,
)
from galois.platform.config import CodexConfig, PlatformConfig, WorkflowAreaConfig
from galois.platform.contracts import LaunchMode, PipelinePreset, ProblemInput, RunStatus, WorkflowKind
from galois.platform.launcher import WorkflowResult, run_workflow
from galois.platform.paths import resolve_paths
from galois.platform.run_registry import create_run_manifest
from galois.platform.subagents import SubagentManager
from galois.platform.workflows import build_workflow_plan


def test_cli_prefers_verification_flags_and_rejects_legacy_verification_aliases() -> None:
    from galois.platform.cli import build_parser

    parser = build_parser()
    base_args = [
        "launch",
        "--problem-id",
        "example",
        "--problem-path",
        "three_horse/reasoning/data/example.md",
    ]

    args = parser.parse_args([*base_args, "--no-verification"])
    assert args.verification is False

    try:
        parser.parse_args([*base_args, "--verification" + "-nlp"])
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("legacy verification alias should not be accepted")

    preset_args = parser.parse_args([*base_args, "--pipeline", "reasoning-only", "--no-repair-loop"])
    assert preset_args.pipeline == "reasoning-only"
    assert preset_args.repair_loop is False

    model_args = parser.parse_args([*base_args, "--model", "gpt-5.4"])
    assert model_args.model == "gpt-5.4"
    gemini_args = parser.parse_args([*base_args, "--model", "gemini-pro-3.1"])
    assert gemini_args.model == "gemini-pro-3.1"

    try:
        parser.parse_args([*base_args, "--model", "gpt-5.3-codex"])
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("unsupported model should not be accepted")


def test_launch_run_prints_reasoning_status_after_service_ready(monkeypatch, tmp_path: Path, capsys) -> None:
    from galois.platform import cli as platform_cli
    from galois.platform.run_registry import utc_now_iso

    repo_root = Path(__file__).resolve().parents[1]
    run_root = tmp_path / "runs"
    config_path = tmp_path / "config.toml"
    config_path.write_text(
        f"""
backend = "codex"
model = "gpt-5.4"
model_reasoning_effort = "xhigh"
personality = "pragmatic"

[codex]
bin = "codex"
base_url_env = "OPENAI_BASE_URL"
api_key_env = "OPENAI_API_KEY"

[reasoning]
enabled = true
workdir = "three_horse/reasoning"

[verification]
enabled = true
workdir = "three_horse/verification"

[platform]
resume_enabled = true
max_repair_rounds = 0
benchmark_root = "benchmarks"
run_root = "{run_root}"
""".lstrip(),
        encoding="utf-8",
    )

    def fake_start_service_workflow(*, run_dir, run_id, launch, manager=None):
        return platform_cli.RunningService(
            launch=launch,
            manager=manager or SubagentManager(),
            task_id="ga-service",
            started_at=utc_now_iso(),
            stdout_path=str(run_dir / "verification" / "logs" / "stdout_r1.log"),
            stderr_path=str(run_dir / "verification" / "logs" / "stderr_r1.log"),
        )

    def fake_stop_service_workflow(*, run_dir, run_id, service, failed_error=None):
        return WorkflowResult(
            workflow=service.launch.kind.value,
            mode=service.launch.mode,
            command=[service.launch.entrypoint, *service.launch.arguments],
            cwd=service.launch.cwd,
            started_at=service.started_at,
            finished_at=utc_now_iso(),
            pid=1234,
            exit_code=0,
            stdout_path=service.stdout_path,
            stderr_path=service.stderr_path,
            status="succeeded",
            subagent_task_id=service.task_id,
            subagent_session_id="ga_service",
        )

    def fake_run_workflow(*, run_dir, run_id, launch, manager=None):
        if launch.kind == WorkflowKind.REASONING:
            problem_dir = reasoning_workspace_dir(run_dir) / "results" / "example"
            problem_dir.mkdir(parents=True, exist_ok=True)
            (problem_dir / "blueprint.md").write_text("proof attempt", encoding="utf-8")
            stdout_path = run_dir / "reasoning" / "logs" / "stdout_r1.log"
            stderr_path = run_dir / "reasoning" / "logs" / "stderr_r1.log"
            stdout_path.parent.mkdir(parents=True, exist_ok=True)
            stdout_path.write_text("reasoning\n", encoding="utf-8")
            stderr_path.write_text("", encoding="utf-8")
            return WorkflowResult(
                workflow=launch.kind.value,
                mode=launch.mode,
                command=[launch.entrypoint, *launch.arguments],
                cwd=launch.cwd,
                started_at=utc_now_iso(),
                finished_at=utc_now_iso(),
                pid=2001,
                exit_code=0,
                stdout_path=str(stdout_path),
                stderr_path=str(stderr_path),
                status="succeeded",
                subagent_task_id="ga-001",
                subagent_session_id="ga_session_1",
            )
        raise AssertionError(f"unexpected workflow kind: {launch.kind}")

    def fake_call_verification_api(*, run_dir, problem, statement, proof, url, revision=1, timeout_seconds=60):
        verification_dir = run_dir / "verification"
        verification_dir.mkdir(parents=True, exist_ok=True)
        response_path = verification_dir / f"verification_r{revision}.json"
        response_path.write_text(
            json.dumps(
                {
                    "verdict": "correct",
                    "repair_hints": "",
                    "verification_report": {"summary": "ok", "critical_errors": [], "gaps": []},
                }
            )
            + "\n",
            encoding="utf-8",
        )
        return VerificationRequestResult(
            attempted=True,
            succeeded=True,
            response_path=str(response_path),
        )

    monkeypatch.setattr(platform_cli, "start_service_workflow", fake_start_service_workflow)
    monkeypatch.setattr(platform_cli, "stop_service_workflow", fake_stop_service_workflow)
    monkeypatch.setattr(platform_cli, "run_workflow", fake_run_workflow)
    monkeypatch.setattr(platform_cli, "call_verification_api", fake_call_verification_api)

    exit_code = platform_cli.cmd_launch_run(
        problem_id="example",
        problem_path=str(repo_root / "three_horse" / "reasoning" / "data" / "example.md"),
        title="Example",
        config_path=config_path,
        reasoning_only=False,
        verification=True,
        skip_services=False,
        pipeline="reasoning-verification",
        repair_loop=False,
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "[verification] service_ready pid=" in captured.out
    assert "[reasoning] status=running attempt=1" in captured.out
    assert "[reasoning] status=succeeded exit_code=0" in captured.out


def test_reasoning_and_verification_adapters_exist() -> None:
    from galois.reasoning.runner import run_reasoning_resume, vendored_reasoning_dir
    from galois.verification.service import app
    from galois.writing.runner import run_writing_project, vendored_writing_dir

    repo_root = Path(__file__).resolve().parents[1]
    assert vendored_reasoning_dir(repo_root) == repo_root / "three_horse" / "reasoning"
    assert vendored_writing_dir(repo_root) == repo_root / "three_horse" / "writing"
    assert callable(run_reasoning_resume)
    assert callable(run_writing_project)
    assert not (repo_root / "three_horse" / "reasoning" / "tests" / "run_example_resume.sh").exists()
    assert app.title == "Verification Agent API"


def test_writing_runner_builds_command_and_saves_session(tmp_path: Path) -> None:
    from galois.writing.runner import run_writing_project

    workdir = tmp_path / "writing-assets"
    data_dir = workdir / "data"
    data_dir.mkdir(parents=True)
    (workdir / "AGENTS.md").write_text("writing instructions", encoding="utf-8")
    (data_dir / "paper.md").write_text("# Paper\nDraft.", encoding="utf-8")

    fake_codex = tmp_path / "fake_codex.py"
    fake_codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env python3",
                "import os, pathlib, sys",
                "pathlib.Path('codex_args.txt').write_text('\\n'.join(sys.argv[1:]), encoding='utf-8')",
                "prompt = sys.stdin.read()",
                "pathlib.Path('codex_stdin.txt').write_text(prompt, encoding='utf-8')",
                "project = pathlib.Path(os.environ['RESULTS_DIR']) / os.environ['GALOIS_WRITING_PROJECT_ID']",
                "project.mkdir(parents=True, exist_ok=True)",
                "(project / 'manuscript_draft.md').write_text('# Draft\\n', encoding='utf-8')",
                "(project / 'review_report.md').write_text('# Review\\n', encoding='utf-8')",
                "(project / 'citation_report.md').write_text('# Citations\\n', encoding='utf-8')",
                "(project / 'revision_tasks.json').write_text('{\"tasks\": []}\\n', encoding='utf-8')",
                "(project / 'export_bundle.json').write_text('{\"artifact_paths\": {}}\\n', encoding='utf-8')",
                "print('session id: 123e4567-e89b-12d3-a456-426614174000')",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    fake_codex.chmod(0o755)

    runtime = tmp_path / "runtime"
    session_file = tmp_path / "session.txt"
    exit_code = run_writing_project(
        repo_root=Path(__file__).resolve().parents[1],
        workdir=workdir,
        env={
            "CODEX_BIN": str(fake_codex),
            "WRITING_FILE": "data/paper.md",
            "GALOIS_WRITING_PROJECT_ID": "paper",
            "GALOIS_WRITING_RUNTIME_DIR": str(runtime),
            "LOG_DIR": str(tmp_path / "logs"),
            "RESULTS_DIR": str(runtime / "results"),
            "SESSION_FILE": str(session_file),
            "RESUME": "0",
            "MODEL": "test-model",
            "REASONING_EFFORT": "low",
            "PYTHONPATH": os.environ.get("PYTHONPATH", ""),
        },
    )

    assert exit_code == 0
    assert session_file.read_text(encoding="utf-8").strip() == "123e4567-e89b-12d3-a456-426614174000"
    stdin_text = (runtime / "codex_stdin.txt").read_text(encoding="utf-8")
    args_text = (runtime / "codex_args.txt").read_text(encoding="utf-8")
    assert "test-model" in args_text
    assert "Galois Paper Writing workflow" in stdin_text
    assert "manuscript_draft.md" in stdin_text
    assert "Every used reference must appear in manuscript_draft.md as an inline citation" in stdin_text
    assert "If authors are provided, manuscript_draft.md must include them below the title" in stdin_text
    assert (runtime / "results" / "paper" / "review_report.md").exists()


def test_writing_workflow_plan_targets_three_horse_writing(tmp_path: Path) -> None:
    from galois.platform.workflows import build_writing_workflow_plan

    repo_root = Path(__file__).resolve().parents[1]
    config = PlatformConfig(
        backend="codex",
        model="gpt-5.4",
        model_reasoning_effort="xhigh",
        personality="pragmatic",
        codex=CodexConfig(bin="codex", base_url_env="OPENAI_BASE_URL", api_key_env="OPENAI_API_KEY"),
        reasoning=WorkflowAreaConfig(enabled=True, workdir="three_horse/reasoning"),
        verification=WorkflowAreaConfig(enabled=True, workdir="three_horse/verification"),
        writing=WorkflowAreaConfig(enabled=True, workdir="three_horse/writing"),
        resume_enabled=True,
        max_repair_rounds=1,
        benchmark_root="benchmarks",
        run_root=str(tmp_path / "runs"),
        project_root=str(tmp_path),
        config_path=tmp_path / "config.toml",
        repo_root=repo_root,
    )
    paths = resolve_paths(config)
    run_dir = tmp_path / "runs" / "run-1"
    problem = ProblemInput(problem_id="paper", problem_path="three_horse/writing/data/example.md", title="Paper")

    launches = build_writing_workflow_plan(config=config, paths=paths, problem=problem, run_dir=run_dir)

    assert [launch.kind for launch in launches] == [WorkflowKind.WRITING]
    launch = launches[0]
    assert launch.cwd == str(repo_root / "three_horse" / "writing")
    assert launch.environment["WRITING_FILE"] == str(run_dir / "writing" / "input.md")
    assert launch.environment["GALOIS_WRITING_PROJECT_ID"] == "paper"
    assert "galois.writing.runner" in " ".join(launch.arguments)


def test_archive_writing_project_copies_standard_artifacts(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    project_dir = run_dir / "writing" / "workspace" / "results" / "paper"
    project_dir.mkdir(parents=True)
    (project_dir / "manuscript_draft.md").write_text("# Draft\n", encoding="utf-8")
    (project_dir / "review_report.md").write_text("# Review\n", encoding="utf-8")
    (project_dir / "citation_report.md").write_text("# Citations\n", encoding="utf-8")
    (project_dir / "revision_tasks.json").write_text('{"tasks": []}\n', encoding="utf-8")
    (project_dir / "export_bundle.json").write_text('{"artifact_paths": {}}\n', encoding="utf-8")

    result = archive_writing_project(run_dir, ProblemInput(problem_id="paper", problem_path="paper.md"), revision=1)

    assert result.found is True
    assert (run_dir / "writing" / "manuscript_draft_r1.md").read_text(encoding="utf-8") == "# Draft\n"
    assert (run_dir / "writing" / "paper_project_r1.json").exists()


def test_reasoning_runner_builds_resume_command_and_saves_session(tmp_path: Path) -> None:
    from galois.reasoning.runner import run_reasoning_resume

    workdir = tmp_path / "reasoning-workspace"
    data_dir = workdir / "data"
    data_dir.mkdir(parents=True)
    (workdir / "AGENTS.md").write_text("agent instructions", encoding="utf-8")
    (data_dir / "example.md").write_text("# Problem\nShow something.", encoding="utf-8")

    fake_codex = tmp_path / "fake_codex.py"
    fake_codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env python3",
                "import pathlib, sys",
                "pathlib.Path('codex_args.txt').write_text('\\n'.join(sys.argv[1:]), encoding='utf-8')",
                "pathlib.Path('codex_stdin.txt').write_text(sys.stdin.read(), encoding='utf-8')",
                "print('session id: 123e4567-e89b-12d3-a456-426614174000')",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    fake_codex.chmod(0o755)

    session_file = tmp_path / "session.txt"
    log_dir = tmp_path / "logs"
    results_dir = tmp_path / "results"
    exit_code = run_reasoning_resume(
        repo_root=Path(__file__).resolve().parents[1],
        workdir=workdir,
        env={
            "CODEX_BIN": str(fake_codex),
            "PROBLEM_FILE": "data/example.md",
            "LOG_DIR": str(log_dir),
            "RESULTS_DIR": str(results_dir),
            "SESSION_FILE": str(session_file),
            "RESUME": "0",
            "MODEL": "test-model",
            "REASONING_EFFORT": "low",
            "PYTHONPATH": os.environ.get("PYTHONPATH", ""),
        },
    )

    assert exit_code == 0
    assert session_file.read_text(encoding="utf-8").strip() == "123e4567-e89b-12d3-a456-426614174000"
    args_text = (workdir / "codex_args.txt").read_text(encoding="utf-8")
    stdin_text = (workdir / "codex_stdin.txt").read_text(encoding="utf-8")
    assert "test-model" in args_text
    assert 'model_reasoning_effort="low"' in args_text
    assert "-" in args_text.splitlines()
    assert "Use AGENTS.md exactly" in stdin_text


def test_agent_runners_default_to_platform_default_model(monkeypatch, tmp_path: Path) -> None:
    from galois.platform.config import DEFAULT_MODEL
    from galois.reasoning.runner import run_reasoning_resume
    from galois.writing.runner import run_writing_project

    monkeypatch.delenv("MODEL", raising=False)

    codex_calls = tmp_path / "codex_calls"
    fake_codex = tmp_path / "fake_codex.py"
    fake_codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env python3",
                "import os, pathlib, sys",
                f"calls = pathlib.Path({str(codex_calls)!r})",
                "calls.mkdir(parents=True, exist_ok=True)",
                "call_id = len(list(calls.glob('*.args')))",
                "(calls / f'{call_id}.args').write_text('\\n'.join(sys.argv[1:]), encoding='utf-8')",
                "sys.stdin.read()",
                "if 'GALOIS_WRITING_PROJECT_ID' in os.environ:",
                "    project = pathlib.Path(os.environ['RESULTS_DIR']) / os.environ['GALOIS_WRITING_PROJECT_ID']",
                "    project.mkdir(parents=True, exist_ok=True)",
                "    (project / 'manuscript_draft.md').write_text('# Draft\\n', encoding='utf-8')",
                "    (project / 'review_report.md').write_text('# Review\\n', encoding='utf-8')",
                "    (project / 'citation_report.md').write_text('# Citations\\n', encoding='utf-8')",
                "    (project / 'revision_tasks.json').write_text('{\"tasks\": []}\\n', encoding='utf-8')",
                "    (project / 'export_bundle.json').write_text('{\"artifact_paths\": {}}\\n', encoding='utf-8')",
                "print('session id: 123e4567-e89b-12d3-a456-426614174000')",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    fake_codex.chmod(0o755)

    reasoning_workdir = tmp_path / "reasoning-assets"
    (reasoning_workdir / "data").mkdir(parents=True)
    (reasoning_workdir / "AGENTS.md").write_text("agent instructions", encoding="utf-8")
    (reasoning_workdir / "data" / "example.md").write_text("# Problem\nShow something.", encoding="utf-8")
    reasoning_exit = run_reasoning_resume(
        repo_root=Path(__file__).resolve().parents[1],
        workdir=reasoning_workdir,
        env={
            "CODEX_BIN": str(fake_codex),
            "PROBLEM_FILE": "data/example.md",
            "LOG_DIR": str(tmp_path / "reasoning-logs"),
            "RESULTS_DIR": str(tmp_path / "reasoning-results"),
            "SESSION_FILE": str(tmp_path / "reasoning.session"),
            "RESUME": "0",
            "REASONING_EFFORT": "low",
            "PYTHONPATH": os.environ.get("PYTHONPATH", ""),
        },
    )

    writing_workdir = tmp_path / "writing-assets"
    (writing_workdir / "data").mkdir(parents=True)
    (writing_workdir / "AGENTS.md").write_text("writing instructions", encoding="utf-8")
    (writing_workdir / "data" / "paper.md").write_text("# Paper\nDraft.", encoding="utf-8")
    writing_runtime = tmp_path / "writing-runtime"
    writing_exit = run_writing_project(
        repo_root=Path(__file__).resolve().parents[1],
        workdir=writing_workdir,
        env={
            "CODEX_BIN": str(fake_codex),
            "WRITING_FILE": "data/paper.md",
            "GALOIS_WRITING_PROJECT_ID": "paper",
            "GALOIS_WRITING_RUNTIME_DIR": str(writing_runtime),
            "LOG_DIR": str(tmp_path / "writing-logs"),
            "RESULTS_DIR": str(writing_runtime / "results"),
            "SESSION_FILE": str(tmp_path / "writing.session"),
            "RESUME": "0",
            "REASONING_EFFORT": "low",
            "PYTHONPATH": os.environ.get("PYTHONPATH", ""),
        },
    )

    assert reasoning_exit == 0
    assert writing_exit == 0
    args_texts = [path.read_text(encoding="utf-8") for path in sorted(codex_calls.glob("*.args"))]
    assert len(args_texts) == 2
    assert all(DEFAULT_MODEL in args_text for args_text in args_texts)


def test_verification_service_defaults_to_platform_default_model(monkeypatch) -> None:
    import galois.verification.service as verification_service
    from galois.platform.config import DEFAULT_MODEL

    monkeypatch.delenv("CODEX_MODEL", raising=False)
    service = importlib.reload(verification_service)

    command = service.build_codex_command(run_id="run", statement="S", proof="P")

    assert command[command.index("-m") + 1] == DEFAULT_MODEL


def test_reasoning_only_prompt_uses_trimmed_contract(tmp_path: Path) -> None:
    from galois.reasoning.runner import _build_prompts

    asset_root = tmp_path / "reasoning-assets"
    runtime_root = tmp_path / "run-local"
    results_dir = runtime_root / "results"
    memory_dir = runtime_root / "memory"
    downloads_dir = runtime_root / "downloads"
    scripts_dir = runtime_root / "scripts"
    log_dir = runtime_root / "logs" / "example"
    problem_path = runtime_root / "problem" / "statement.md"
    problem_path.parent.mkdir(parents=True)
    problem_path.write_text("# Problem\nShow something.", encoding="utf-8")

    initial_prompt, resume_prompt = _build_prompts(
        str(problem_path),
        "",
        absolute_problem_file=problem_path,
        asset_root=asset_root,
        runtime_root=runtime_root,
        problem_id="example",
        results_dir=results_dir,
        memory_dir=memory_dir,
        downloads_dir=downloads_dir,
        scripts_dir=scripts_dir,
        log_dir=log_dir,
        verification_enabled=False,
        verification_mode="disabled",
    )

    for prompt in (initial_prompt, resume_prompt):
        assert "Use AGENTS.md exactly" not in prompt
        assert "Strict reasoning-only mode for this run" in prompt
        assert "No downstream verifier or formalizer should be assumed in this run." in prompt
        assert "Do not call `verify_proof_service` or invoke `$verify-proof`." in prompt
        assert "blueprint_verified.md" not in prompt


def test_verification_prompt_prioritizes_proof_before_verifier_work(tmp_path: Path) -> None:
    from galois.reasoning.runner import _build_prompts

    asset_root = tmp_path / "reasoning-assets"
    runtime_root = tmp_path / "run-local"
    results_dir = runtime_root / "results"
    memory_dir = runtime_root / "memory"
    downloads_dir = runtime_root / "downloads"
    scripts_dir = runtime_root / "scripts"
    log_dir = runtime_root / "logs" / "example"
    problem_path = runtime_root / "problem" / "statement.md"
    problem_path.parent.mkdir(parents=True)
    problem_path.write_text("# Problem\nShow something.", encoding="utf-8")

    initial_prompt, resume_prompt = _build_prompts(
        str(problem_path),
        "",
        absolute_problem_file=problem_path,
        asset_root=asset_root,
        runtime_root=runtime_root,
        problem_id="example",
        results_dir=results_dir,
        memory_dir=memory_dir,
        downloads_dir=downloads_dir,
        scripts_dir=scripts_dir,
        log_dir=log_dir,
        verification_enabled=True,
        verification_mode="external",
    )

    for prompt in (initial_prompt, resume_prompt):
        assert "Verification is enabled for this run." in prompt
        assert "Verification is platform-managed for this run" in prompt
        assert "You may also call `verify_proof_service` yourself" in prompt
        assert "Do not call `verify_proof_service`" not in prompt


def test_copy_problem_artifacts_translates_non_english_statement_to_canonical_english(monkeypatch, tmp_path: Path) -> None:
    from galois.platform import cli as platform_cli

    repo_root = Path(__file__).resolve().parents[1]
    source_path = tmp_path / "problem_zh.md"
    source_text = "证明：对于度量空间 X，子集 A 是紧致的。"
    source_path.write_text(source_text, encoding="utf-8")
    run_dir = tmp_path / "run"
    problem = ProblemInput(problem_id="example9", problem_path=str(source_path), title="Example 9")

    config = PlatformConfig(
        backend="codex",
        model="gpt-5.4",
        model_reasoning_effort="xhigh",
        personality="pragmatic",
        codex=CodexConfig(bin="codex", base_url_env="OPENAI_BASE_URL", api_key_env="OPENAI_API_KEY"),
        reasoning=WorkflowAreaConfig(enabled=True, workdir="three_horse/reasoning"),
        verification=WorkflowAreaConfig(enabled=True, workdir="three_horse/verification"),
        writing=WorkflowAreaConfig(enabled=True, workdir="three_horse/writing"),
        resume_enabled=True,
        max_repair_rounds=1,
        benchmark_root="benchmarks",
        run_root="runs",
        config_path=repo_root / "configs" / "defaults.toml",
        repo_root=repo_root,
    )

    monkeypatch.setattr(
        platform_cli,
        "_translate_statement_to_english",
        lambda *, statement, config, repo_root, run_dir: "Prove: A is compact.\n",
    )

    platform_cli._copy_problem_artifacts(run_dir, problem, repo_root, config)

    assert (run_dir / "problem" / "statement.md").read_text(encoding="utf-8") == "Prove: A is compact.\n"
    assert (run_dir / "problem" / "source_statement.md").read_text(encoding="utf-8") == source_text
    meta = json.loads((run_dir / "problem" / "meta.json").read_text(encoding="utf-8"))
    assert meta["translated_from_source"] is True
    assert meta["canonical_language"] == "english"
    assert meta["source_language"] == "non_english"


def test_resolve_problem_statement_prefers_staged_run_statement(tmp_path: Path) -> None:
    from galois.platform.artifacts import resolve_problem_statement

    original_path = tmp_path / "source.md"
    original_path.write_text("证明：原始中文题面", encoding="utf-8")
    run_dir = tmp_path / "run"
    staged_path = run_dir / "problem" / "statement.md"
    staged_path.parent.mkdir(parents=True, exist_ok=True)
    staged_path.write_text("Prove: canonical English statement", encoding="utf-8")
    problem = ProblemInput(problem_id="example", problem_path=str(original_path))

    statement, resolved_path = resolve_problem_statement(problem, repo_root=tmp_path, run_dir=run_dir)

    assert statement == "Prove: canonical English statement"
    assert resolved_path == staged_path


def test_stage_problem_for_reasoning_workspace_preserves_existing_canonical_statement(tmp_path: Path) -> None:
    from galois.platform import cli as platform_cli

    source_path = tmp_path / "source.md"
    source_path.write_text("证明：原始中文题面", encoding="utf-8")
    run_dir = tmp_path / "run"
    staged_path = run_dir / "problem" / "statement.md"
    staged_path.parent.mkdir(parents=True, exist_ok=True)
    staged_path.write_text("Prove: canonical English statement", encoding="utf-8")
    problem = ProblemInput(problem_id="example", problem_path=str(source_path))

    platform_cli._stage_problem_for_reasoning_workspace(run_dir=run_dir, repo_root=tmp_path, problem=problem)

    assert staged_path.read_text(encoding="utf-8") == "Prove: canonical English statement"


def test_launch_run_verification_uses_canonical_english_statement(monkeypatch, tmp_path: Path) -> None:
    from galois.platform import cli as platform_cli
    from galois.platform.run_registry import utc_now_iso

    repo_root = Path(__file__).resolve().parents[1]
    run_root = tmp_path / "runs"
    source_path = tmp_path / "problem_zh.md"
    source_path.write_text("证明：原始中文题面", encoding="utf-8")
    config_path = tmp_path / "config.toml"
    config_path.write_text(
        f"""
backend = "codex"
model = "gpt-5.4"
model_reasoning_effort = "xhigh"
personality = "pragmatic"

[codex]
bin = "codex"
base_url_env = "OPENAI_BASE_URL"
api_key_env = "OPENAI_API_KEY"

[reasoning]
enabled = true
workdir = "three_horse/reasoning"

[verification]
enabled = true
workdir = "three_horse/verification"

[platform]
resume_enabled = true
max_repair_rounds = 0
benchmark_root = "benchmarks"
run_root = "{run_root}"
""".lstrip(),
        encoding="utf-8",
    )

    seen: dict[str, str] = {}

    monkeypatch.setattr(
        platform_cli,
        "_translate_statement_to_english",
        lambda **kwargs: "Prove: canonical English statement\n",
    )

    def fake_start_service_workflow(*, run_dir, run_id, launch, manager=None):
        return platform_cli.RunningService(
            launch=launch,
            manager=manager or SubagentManager(),
            task_id="ga-service",
            started_at=utc_now_iso(),
            stdout_path=str(run_dir / "verification" / "logs" / "stdout_r1.log"),
            stderr_path=str(run_dir / "verification" / "logs" / "stderr_r1.log"),
        )

    def fake_stop_service_workflow(*, run_dir, run_id, service, failed_error=None):
        return WorkflowResult(
            workflow=service.launch.kind.value,
            mode=service.launch.mode,
            command=[service.launch.entrypoint, *service.launch.arguments],
            cwd=service.launch.cwd,
            started_at=service.started_at,
            finished_at=utc_now_iso(),
            pid=1234,
            exit_code=0,
            stdout_path=service.stdout_path,
            stderr_path=service.stderr_path,
            status="succeeded",
            subagent_task_id=service.task_id,
            subagent_session_id="ga_service",
        )

    def fake_run_workflow(*, run_dir, run_id, launch, manager=None):
        problem_dir = reasoning_workspace_dir(run_dir) / "results" / "problem_zh"
        problem_dir.mkdir(parents=True, exist_ok=True)
        (problem_dir / "blueprint.md").write_text("proof attempt", encoding="utf-8")
        stdout_path = run_dir / "reasoning" / "logs" / "stdout_r1.log"
        stderr_path = run_dir / "reasoning" / "logs" / "stderr_r1.log"
        stdout_path.parent.mkdir(parents=True, exist_ok=True)
        stdout_path.write_text("reasoning\n", encoding="utf-8")
        stderr_path.write_text("", encoding="utf-8")
        return WorkflowResult(
            workflow=launch.kind.value,
            mode=launch.mode,
            command=[launch.entrypoint, *launch.arguments],
            cwd=launch.cwd,
            started_at=utc_now_iso(),
            finished_at=utc_now_iso(),
            pid=2001,
            exit_code=0,
            stdout_path=str(stdout_path),
            stderr_path=str(stderr_path),
            status="succeeded",
            subagent_task_id="ga-001",
            subagent_session_id="ga_session_1",
        )

    def fake_call_verification_api(*, run_dir, problem, statement, proof, url, revision=1, timeout_seconds=60):
        seen["statement"] = statement
        verification_dir = run_dir / "verification"
        verification_dir.mkdir(parents=True, exist_ok=True)
        response_path = verification_dir / f"verification_r{revision}.json"
        response_path.write_text(
            json.dumps(
                {
                    "verdict": "correct",
                    "repair_hints": "",
                    "verification_report": {"summary": "ok", "critical_errors": [], "gaps": []},
                }
            )
            + "\n",
            encoding="utf-8",
        )
        return VerificationRequestResult(
            attempted=True,
            succeeded=True,
            response_path=str(response_path),
        )

    monkeypatch.setattr(platform_cli, "start_service_workflow", fake_start_service_workflow)
    monkeypatch.setattr(platform_cli, "stop_service_workflow", fake_stop_service_workflow)
    monkeypatch.setattr(platform_cli, "run_workflow", fake_run_workflow)
    monkeypatch.setattr(platform_cli, "call_verification_api", fake_call_verification_api)

    exit_code = platform_cli.cmd_launch_run(
        problem_id="example",
        problem_path=str(source_path),
        title="Example",
        config_path=config_path,
        reasoning_only=False,
        verification=True,
        skip_services=False,
        pipeline="reasoning-verification",
        repair_loop=False,
    )

    assert exit_code == 0
    assert seen["statement"] == "Prove: canonical English statement\n"


def test_reasoning_runner_uses_run_local_overlay_workspace(tmp_path: Path) -> None:
    from galois.reasoning.runner import run_reasoning_resume

    asset_root = tmp_path / "reasoning-assets"
    (asset_root / "data").mkdir(parents=True)
    (asset_root / ".agents" / "skills").mkdir(parents=True)
    (asset_root / ".codex").mkdir(parents=True)
    (asset_root / "mcp").mkdir(parents=True)
    (asset_root / "AGENTS.md").write_text("agent instructions", encoding="utf-8")
    (asset_root / "EXTRA_GUIDE.md").write_text("workflow", encoding="utf-8")
    (asset_root / ".codex" / "config.toml").write_text("model = 'test'\n", encoding="utf-8")
    (asset_root / "mcp" / "__init__.py").write_text("", encoding="utf-8")
    (asset_root / "mcp" / "server.py").write_text("print('mcp placeholder')\n", encoding="utf-8")

    runtime_root = tmp_path / "run-local"
    problem_path = runtime_root / "problem" / "statement.md"
    problem_path.parent.mkdir(parents=True)
    problem_path.write_text("# Problem\nShow something.", encoding="utf-8")

    fake_codex = tmp_path / "fake_codex.py"
    fake_codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env python3",
                "import pathlib, sys, time",
                "prompt = sys.stdin.read().strip()",
                "pathlib.Path('codex_stdin.txt').write_text(prompt, encoding='utf-8')",
                "pathlib.Path('cwd.txt').write_text(str(pathlib.Path.cwd()), encoding='utf-8')",
                "pathlib.Path('results/example').mkdir(parents=True, exist_ok=True)",
                "pathlib.Path('results/example/blueprint.md').write_text('# Problem\\n\\n## Statement\\nShow something.\\n\\n## Solution\\nA complete solution.\\n', encoding='utf-8')",
                "pathlib.Path('memory/example').mkdir(parents=True, exist_ok=True)",
                "pathlib.Path('memory/example/meta.json').write_text('{\"problem_id\":\"example\"}', encoding='utf-8')",
                "print('user', flush=True)",
                "print(prompt, flush=True)",
                "print('user', flush=True)",
                "print(prompt, flush=True)",
                "print('Run the proof verifier on this full blueprint and repair any reported gaps.', flush=True)",
                "print('Run the proof verifier on this full blueprint and repair any reported gaps.', flush=True)",
                "print('verify_proof_service_unavailable', flush=True)",
                "print('verify_proof_service_unavailable', flush=True)",
                "print('progress line 1', flush=True)",
                "time.sleep(0.05)",
                "print('session id: 123e4567-e89b-12d3-a456-426614174000', flush=True)",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    fake_codex.chmod(0o755)

    exit_code = run_reasoning_resume(
        repo_root=Path(__file__).resolve().parents[1],
        workdir=asset_root,
        env={
            "CODEX_BIN": str(fake_codex),
            "PROBLEM_FILE": str(problem_path),
            "GALOIS_REASONING_PROBLEM_ID": "example",
            "GALOIS_REASONING_RUNTIME_DIR": str(runtime_root),
            "GALOIS_REASONING_VERIFICATION_ENABLED": "0",
            "SESSION_FILE": str(runtime_root / "reasoning.session"),
            "RESUME": "0",
            "MODEL": "test-model",
            "REASONING_EFFORT": "low",
            "PYTHONPATH": os.environ.get("PYTHONPATH", ""),
        },
    )

    assert exit_code == 0
    assert (runtime_root / "results" / "example" / "blueprint.md").exists()
    assert not (runtime_root / "results" / "example" / "blueprint_verified.md").exists()
    assert (runtime_root / "memory" / "example" / "meta.json").exists()
    assert not (asset_root / "memory" / "example" / "meta.json").exists()
    assert not (runtime_root / ".agents").exists()
    assert not (runtime_root / ".codex").exists()
    assert not (runtime_root / "mcp").exists()
    assert not (runtime_root / "AGENTS.md").exists()
    assert not (runtime_root / "EXTRA_GUIDE.md").exists()
    assert not (runtime_root / "data").exists()
    assert (runtime_root / "cwd.txt").read_text(encoding="utf-8").strip() == str(runtime_root)
    stdin_text = (runtime_root / "codex_stdin.txt").read_text(encoding="utf-8")
    assert "Strict reasoning-only mode for this run" in stdin_text
    assert "do not call `verify_proof_service`" in stdin_text.lower()
    log_text = (runtime_root / "logs" / "example" / "example.md").read_text(encoding="utf-8")
    assert "verification_enabled: False" in log_text
    assert "status: succeeded" in log_text


def test_reasoning_runner_detects_stalled_meta_reasoning(tmp_path: Path) -> None:
    from galois.reasoning.runner import run_reasoning_resume

    asset_root = tmp_path / "reasoning-assets"
    (asset_root / "data").mkdir(parents=True)
    (asset_root / "AGENTS.md").write_text("agent instructions", encoding="utf-8")

    runtime_root = tmp_path / "run-local"
    problem_path = runtime_root / "problem" / "statement.md"
    problem_path.parent.mkdir(parents=True)
    problem_path.write_text("# Problem\nShow something.", encoding="utf-8")

    fake_codex = tmp_path / "fake_codex.py"
    fake_codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env python3",
                "import sys, time",
                "sys.stdin.read()",
                "for _ in range(6):",
                "    print('**Planning proof structure**', flush=True)",
                "    print('I\\'m thinking about whether I should discuss workflow policy before writing proof steps.', flush=True)",
                "    time.sleep(0.05)",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    fake_codex.chmod(0o755)

    exit_code = run_reasoning_resume(
        repo_root=Path(__file__).resolve().parents[1],
        workdir=asset_root,
        env={
            "CODEX_BIN": str(fake_codex),
            "PROBLEM_FILE": str(problem_path),
            "GALOIS_REASONING_PROBLEM_ID": "example",
            "GALOIS_REASONING_RUNTIME_DIR": str(runtime_root),
            "GALOIS_REASONING_VERIFICATION_ENABLED": "1",
            "GALOIS_REASONING_STALL_LINE_BUDGET": "8",
            "SESSION_FILE": str(runtime_root / "reasoning.session"),
            "RESUME": "0",
            "MODEL": "test-model",
            "REASONING_EFFORT": "low",
            "PYTHONPATH": os.environ.get("PYTHONPATH", ""),
        },
    )

    assert exit_code != 0
    log_text = (runtime_root / "logs" / "example" / "example.md").read_text(encoding="utf-8")
    assert "status: failed" in log_text
    assert "stalled_meta_reasoning" in log_text


def test_default_config_places_runs_under_project_root() -> None:
    from galois.platform.config import load_config

    repo_root = Path(__file__).resolve().parents[1]
    config = load_config(repo_root / "configs" / "defaults.toml")

    assert config.model == "gpt-5.5"
    assert config.project_root == "projects/default"
    assert config.project_root_path == repo_root / "projects" / "default"
    assert config.run_root_path == repo_root / "projects" / "default" / "runs"


def test_build_workflow_plan_normalizes_reasoning_problem_path() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    config = PlatformConfig(
        backend="codex",
        model="gpt-5.4",
        model_reasoning_effort="xhigh",
        personality="pragmatic",
        codex=CodexConfig(bin="codex", base_url_env="OPENAI_BASE_URL", api_key_env="OPENAI_API_KEY"),
        reasoning=WorkflowAreaConfig(enabled=True, workdir="three_horse/reasoning"),
        verification=WorkflowAreaConfig(enabled=True, workdir="three_horse/verification"),
        writing=WorkflowAreaConfig(enabled=True, workdir="three_horse/writing"),
        resume_enabled=True,
        max_repair_rounds=1,
        benchmark_root="benchmarks",
        run_root="runs",
        config_path=repo_root / "configs" / "defaults.toml",
        repo_root=repo_root,
        project_root="projects/default",
    )
    paths = resolve_paths(config)
    problem = ProblemInput(
        problem_id="example",
        problem_path=str(repo_root / "three_horse" / "reasoning" / "data" / "example.md"),
        title="Example",
    )

    launches = build_workflow_plan(config=config, paths=paths, problem=problem, run_dir=repo_root / "runs" / "test")

    reasoning = next(launch for launch in launches if launch.kind == WorkflowKind.REASONING)
    verification = next(launch for launch in launches if launch.kind == WorkflowKind.VERIFICATION)
    assert reasoning.environment["PROBLEM_FILE"].endswith("/runs/test/problem/statement.md")
    assert reasoning.environment["GALOIS_REASONING_RUNTIME_DIR"].endswith("/runs/test/reasoning/workspace")
    assert reasoning.environment["GALOIS_REASONING_VERIFICATION_ENABLED"] == "1"
    assert reasoning.environment["GALOIS_REASONING_VERIFICATION_MODE"] == "external"
    assert "GALOIS_REASONING_LEAN_ENABLED" not in reasoning.environment
    assert verification.environment["GALOIS_VERIFICATION_AGENT_DIR"].endswith("/three_horse/verification")


def test_run_workflow_captures_stdout_stderr_and_events(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    config = PlatformConfig(
        backend="codex",
        model="gpt-5.4",
        model_reasoning_effort="xhigh",
        personality="pragmatic",
        codex=CodexConfig(bin="codex", base_url_env="OPENAI_BASE_URL", api_key_env="OPENAI_API_KEY"),
        reasoning=WorkflowAreaConfig(enabled=False, workdir="three_horse/reasoning"),
        verification=WorkflowAreaConfig(enabled=False, workdir="three_horse/verification"),
        writing=WorkflowAreaConfig(enabled=True, workdir="three_horse/writing"),
        resume_enabled=True,
        max_repair_rounds=1,
        benchmark_root="benchmarks",
        run_root=str(tmp_path),
        config_path=repo_root / "configs" / "defaults.toml",
        repo_root=repo_root,
    )
    paths = resolve_paths(config)
    run_dir, manifest = create_run_manifest(
        config=config,
        paths=paths,
        problem=ProblemInput(problem_id="example-check", problem_path="three_horse/reasoning/data/example.md"),
    )
    launch = build_workflow_plan(
        config=PlatformConfig(
            backend=config.backend,
            model=config.model,
            model_reasoning_effort=config.model_reasoning_effort,
            personality=config.personality,
            codex=config.codex,
            reasoning=WorkflowAreaConfig(enabled=True, workdir="three_horse/reasoning"),
            verification=WorkflowAreaConfig(enabled=False, workdir="three_horse/verification"),
            writing=WorkflowAreaConfig(enabled=True, workdir="three_horse/writing"),
            resume_enabled=config.resume_enabled,
            max_repair_rounds=config.max_repair_rounds,
            benchmark_root=config.benchmark_root,
            run_root=config.run_root,
            config_path=config.config_path,
            repo_root=config.repo_root,
        ),
        paths=paths,
        problem=ProblemInput(problem_id="example-check", problem_path="three_horse/reasoning/data/example.md"),
        run_dir=run_dir,
    )[0]
    launch.entrypoint = sys.executable
    launch.cwd = str(tmp_path)
    launch.arguments = ["-c", "import sys; print('out'); print('err', file=sys.stderr)"]

    result = run_workflow(run_dir=run_dir, run_id=manifest.run_id, launch=launch)

    assert result.status == RunStatus.SUCCEEDED.value
    assert Path(result.stdout_path).read_text(encoding="utf-8").strip() == "out"
    assert Path(result.stderr_path).read_text(encoding="utf-8").strip() == "err"


def test_launch_run_prepares_minimal_overlay_workspaces(monkeypatch, tmp_path: Path) -> None:
    from galois.platform import cli as platform_cli
    from galois.platform.run_registry import utc_now_iso

    repo_root = Path(__file__).resolve().parents[1]
    run_root = tmp_path / "runs"
    config_path = tmp_path / "config.toml"
    config_path.write_text(
        f"""
backend = "codex"
model = "gpt-5.4"
model_reasoning_effort = "xhigh"
personality = "pragmatic"

[codex]
bin = "codex"
base_url_env = "OPENAI_BASE_URL"
api_key_env = "OPENAI_API_KEY"

[reasoning]
enabled = true
workdir = "three_horse/reasoning"

[verification]
enabled = true
workdir = "three_horse/verification"

[platform]
resume_enabled = true
max_repair_rounds = 1
benchmark_root = "benchmarks"
run_root = "{run_root}"
""".lstrip(),
        encoding="utf-8",
    )

    def fake_run_workflow(*, run_dir, run_id, launch, manager=None):
        if launch.kind == WorkflowKind.REASONING:
            assert launch.environment["GALOIS_REASONING_VERIFICATION_ENABLED"] == "0"
        problem_dir = reasoning_workspace_dir(run_dir) / "results" / "example"
        problem_dir.mkdir(parents=True, exist_ok=True)
        (problem_dir / "blueprint.md").write_text("proof attempt", encoding="utf-8")
        stdout_path = run_dir / "reasoning" / "logs" / "stdout_r1.log"
        stderr_path = run_dir / "reasoning" / "logs" / "stderr_r1.log"
        stdout_path.parent.mkdir(parents=True, exist_ok=True)
        stdout_path.write_text("reasoning\n", encoding="utf-8")
        stderr_path.write_text("", encoding="utf-8")
        return WorkflowResult(
            workflow=launch.kind.value,
            mode=launch.mode,
            command=[launch.entrypoint, *launch.arguments],
            cwd=launch.cwd,
            started_at=utc_now_iso(),
            finished_at=utc_now_iso(),
            pid=2001,
            exit_code=0,
            stdout_path=str(stdout_path),
            stderr_path=str(stderr_path),
            status="succeeded",
            subagent_task_id="ga-001",
            subagent_session_id="ga_session_1",
        )

    monkeypatch.setattr(platform_cli, "run_workflow", fake_run_workflow)

    exit_code = platform_cli.cmd_launch_run(
        problem_id="example",
        problem_path=str(repo_root / "three_horse" / "reasoning" / "data" / "example.md"),
        title="Example",
        config_path=config_path,
        reasoning_only=False,
        verification=False,
        skip_services=False,
        pipeline="reasoning-only",
    )

    assert exit_code == 0
    run_dir = sorted(run_root.iterdir())[0]
    workspace = reasoning_workspace_dir(run_dir)
    assert (workspace / "memory").is_dir()
    assert (workspace / "results").is_dir()
    assert not (run_dir / "verification" / "workspace").exists()


def test_launch_run_prepares_minimal_verification_workspace(monkeypatch, tmp_path: Path) -> None:
    from galois.platform import cli as platform_cli
    from galois.platform.run_registry import utc_now_iso

    repo_root = Path(__file__).resolve().parents[1]
    run_root = tmp_path / "runs"
    config_path = tmp_path / "config.toml"
    config_path.write_text(
        f"""
backend = "codex"
model = "gpt-5.4"
model_reasoning_effort = "xhigh"
personality = "pragmatic"

[codex]
bin = "codex"
base_url_env = "OPENAI_BASE_URL"
api_key_env = "OPENAI_API_KEY"

[reasoning]
enabled = true
workdir = "three_horse/reasoning"

[verification]
enabled = true
workdir = "three_horse/verification"

[platform]
resume_enabled = true
max_repair_rounds = 1
benchmark_root = "benchmarks"
run_root = "{run_root}"
""".lstrip(),
        encoding="utf-8",
    )

    def fake_start_service_workflow(*, run_dir, run_id, launch, manager=None):
        return platform_cli.RunningService(
            launch=launch,
            manager=manager or SubagentManager(),
            task_id="ga-service",
            started_at=utc_now_iso(),
            stdout_path=str(run_dir / "verification" / "logs" / "stdout_r1.log"),
            stderr_path=str(run_dir / "verification" / "logs" / "stderr_r1.log"),
        )

    def fake_stop_service_workflow(*, run_dir, run_id, service, failed_error=None):
        return WorkflowResult(
            workflow=service.launch.kind.value,
            mode=service.launch.mode,
            command=[service.launch.entrypoint, *service.launch.arguments],
            cwd=service.launch.cwd,
            started_at=service.started_at,
            finished_at=utc_now_iso(),
            pid=1234,
            exit_code=0,
            stdout_path=service.stdout_path,
            stderr_path=service.stderr_path,
            status="succeeded",
            subagent_task_id=service.task_id,
            subagent_session_id="ga_service",
        )

    def fake_run_workflow(*, run_dir, run_id, launch, manager=None):
        problem_dir = reasoning_workspace_dir(run_dir) / "results" / "example"
        problem_dir.mkdir(parents=True, exist_ok=True)
        (problem_dir / "blueprint.md").write_text("proof attempt", encoding="utf-8")
        stdout_path = run_dir / "reasoning" / "logs" / "stdout_r1.log"
        stderr_path = run_dir / "reasoning" / "logs" / "stderr_r1.log"
        stdout_path.parent.mkdir(parents=True, exist_ok=True)
        stdout_path.write_text("reasoning\n", encoding="utf-8")
        stderr_path.write_text("", encoding="utf-8")
        return WorkflowResult(
            workflow=launch.kind.value,
            mode=launch.mode,
            command=[launch.entrypoint, *launch.arguments],
            cwd=launch.cwd,
            started_at=utc_now_iso(),
            finished_at=utc_now_iso(),
            pid=2001,
            exit_code=0,
            stdout_path=str(stdout_path),
            stderr_path=str(stderr_path),
            status="succeeded",
            subagent_task_id="ga-001",
            subagent_session_id="ga_session_1",
        )

    def fake_call_verification_api(*, run_dir, problem, statement, proof, url, revision=1, timeout_seconds=60):
        verification_dir = run_dir / "verification"
        verification_dir.mkdir(parents=True, exist_ok=True)
        response_path = verification_dir / f"verification_r{revision}.json"
        response_path.write_text(
            json.dumps(
                {
                    "verdict": "correct",
                    "repair_hints": "",
                    "verification_report": {"summary": "ok", "critical_errors": [], "gaps": []},
                }
            )
            + "\n",
            encoding="utf-8",
        )
        return VerificationRequestResult(
            attempted=True,
            succeeded=True,
            response_path=str(response_path),
        )

    monkeypatch.setattr(platform_cli, "start_service_workflow", fake_start_service_workflow)
    monkeypatch.setattr(platform_cli, "stop_service_workflow", fake_stop_service_workflow)
    monkeypatch.setattr(platform_cli, "run_workflow", fake_run_workflow)
    monkeypatch.setattr(platform_cli, "call_verification_api", fake_call_verification_api)

    exit_code = platform_cli.cmd_launch_run(
        problem_id="example",
        problem_path=str(repo_root / "three_horse" / "reasoning" / "data" / "example.md"),
        title="Example",
        config_path=config_path,
        reasoning_only=False,
        verification=True,
        skip_services=False,
        pipeline="reasoning-verification",
        repair_loop=False,
    )

    assert exit_code == 0
    run_dir = sorted(run_root.iterdir())[0]
    workspace = run_dir / "verification" / "workspace"
    assert (workspace / "memory").is_dir()
    assert (workspace / "results").is_dir()


def test_launch_run_model_override_flows_to_manifest_and_workflow(monkeypatch, tmp_path: Path, capsys) -> None:
    from galois.platform import cli as platform_cli
    from galois.platform.run_registry import utc_now_iso

    repo_root = Path(__file__).resolve().parents[1]
    run_root = tmp_path / "runs"
    config_path = tmp_path / "config.toml"
    config_path.write_text(
        f"""
backend = "codex"
model = "gpt-5.4"
model_reasoning_effort = "xhigh"
personality = "pragmatic"

[codex]
bin = "codex"
base_url_env = "OPENAI_BASE_URL"
api_key_env = "OPENAI_API_KEY"

[models."gpt-5.4"]
base_url_env = "OPENAI_BASE_URL"
api_key_env = "OPENAI_API_KEY"

[models."gpt-5.5"]
base_url_env = "OPENAI_BASE_URL"
api_key_env = "OPENAI_API_KEY"

[models."gemini-pro-3.1"]
base_url_env = "GEMINI_BASE_URL"
api_key_env = "GEMINI_API_KEY"

[reasoning]
enabled = true
workdir = "three_horse/reasoning"

[verification]
enabled = true
workdir = "three_horse/verification"

[platform]
resume_enabled = true
max_repair_rounds = 0
benchmark_root = "benchmarks"
run_root = "{run_root}"
""".lstrip(),
        encoding="utf-8",
    )
    monkeypatch.setenv("OPENAI_BASE_URL", "https://api.openai.example/v1")
    monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
    seen: dict[str, str] = {}

    def fake_run_workflow(*, run_dir, run_id, launch, manager=None):
        seen["model"] = launch.environment["MODEL"]
        problem_dir = reasoning_workspace_dir(run_dir) / "results" / "example"
        problem_dir.mkdir(parents=True, exist_ok=True)
        (problem_dir / "blueprint.md").write_text("proof attempt", encoding="utf-8")
        stdout_path = run_dir / "reasoning" / "logs" / "stdout_r1.log"
        stderr_path = run_dir / "reasoning" / "logs" / "stderr_r1.log"
        stdout_path.parent.mkdir(parents=True, exist_ok=True)
        stdout_path.write_text("reasoning\n", encoding="utf-8")
        stderr_path.write_text("", encoding="utf-8")
        return WorkflowResult(
            workflow=launch.kind.value,
            mode=launch.mode,
            command=[launch.entrypoint, *launch.arguments],
            cwd=launch.cwd,
            started_at=utc_now_iso(),
            finished_at=utc_now_iso(),
            pid=2001,
            exit_code=0,
            stdout_path=str(stdout_path),
            stderr_path=str(stderr_path),
            status="succeeded",
            subagent_task_id="ga-001",
            subagent_session_id="ga_session_1",
        )

    monkeypatch.setattr(platform_cli, "run_workflow", fake_run_workflow)

    exit_code = platform_cli.cmd_launch_run(
        problem_id="example",
        problem_path=str(repo_root / "three_horse" / "reasoning" / "data" / "example.md"),
        title="Example",
        config_path=config_path,
        reasoning_only=False,
        verification=False,
        skip_services=False,
        pipeline="reasoning-only",
        model_override="gpt-5.5",
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "model=gpt-5.5" in captured.out
    assert seen["model"] == "gpt-5.5"
    run_dir = sorted(run_root.iterdir())[0]
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["model"] == "gpt-5.5"


def test_subagent_manager_spawns_thread_and_child_process(tmp_path: Path) -> None:
    manager = SubagentManager()
    stdout_path = tmp_path / "stdout.log"
    stderr_path = tmp_path / "stderr.log"

    task = manager.spawn_process(
        "sleeping subagent",
        argv=[sys.executable, "-c", "import time; print('ready', flush=True); time.sleep(0.2)"],
        cwd=str(tmp_path),
        env={},
        stdout_path=stdout_path,
        stderr_path=stderr_path,
        workflow_kind="test",
    )

    deadline = time.monotonic() + 2
    while task.process is None and time.monotonic() < deadline:
        time.sleep(0.01)
    assert task.process is not None
    finished = manager.wait(task.task_id)
    assert finished.status == "complete"
    assert finished.returncode == 0


def test_inspect_run_reports_subagents(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    run_root = tmp_path / "runs"
    config_path = tmp_path / "config.toml"
    config_path.write_text(
        f"""
backend = "codex"
model = "gpt-5.4"
model_reasoning_effort = "xhigh"
personality = "pragmatic"

[reasoning]
enabled = false
workdir = "three_horse/reasoning"

[verification]
enabled = false
workdir = "three_horse/verification"

[platform]
resume_enabled = true
benchmark_root = "benchmarks"
run_root = "{run_root}"
""".lstrip(),
        encoding="utf-8",
    )

    launched = subprocess.run(
        [
            sys.executable,
            "-m",
            "galois.platform.cli",
            "launch",
            "--config",
            str(config_path),
            "--problem-id",
            "inspect-example",
            "--problem-path",
            str(repo_root / "three_horse" / "reasoning" / "data" / "example.md"),
        ],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )
    assert launched.returncode == 0, launched.stderr
    run_dir_line = next(line for line in launched.stdout.splitlines() if line.startswith("run_dir="))
    run_dir = run_dir_line.split("=", 1)[1]

    inspected = subprocess.run(
        [
            sys.executable,
            "-m",
            "galois.platform.cli",
            "inspect",
            "--config",
            str(config_path),
            run_dir,
        ],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert inspected.returncode == 0, inspected.stderr
    assert "status=succeeded" in inspected.stdout
    assert "subagents=0" in inspected.stdout


def test_archive_reasoning_blueprint_and_call_verification_api(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    blueprint_path = run_dir / "reasoning" / "results" / "example" / "blueprint.md"
    blueprint_path.parent.mkdir(parents=True)
    blueprint_path.write_text("proof blueprint", encoding="utf-8")
    problem = ProblemInput(problem_id="example", problem_path="three_horse/reasoning/data/example.md")

    archived = archive_reasoning_blueprint(run_dir, problem)
    assert archived.found is True

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self) -> None:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            response = json.dumps(
                {"verdict": "correct", "statement_seen": payload["statement"], "proof_seen": payload["proof"]}
            ).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

        def log_message(self, format: str, *args) -> None:
            return

    server = HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        result = call_verification_api(
            run_dir=run_dir,
            problem=problem,
            statement="statement",
            proof=archived.content,
            url=f"http://127.0.0.1:{server.server_port}/verify",
        )
    finally:
        server.shutdown()
        thread.join(timeout=2)

    assert result.succeeded is True
    response = json.loads(Path(result.response_path or "").read_text(encoding="utf-8"))
    assert response["statement_seen"] == "statement"
    assert response["proof_seen"] == "proof blueprint"


def test_normalize_verification_response_variants(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    verification_dir = run_dir / "verification"
    verification_dir.mkdir(parents=True)
    problem = ProblemInput(problem_id="example", problem_path="three_horse/reasoning/data/example.md")

    correct_raw = verification_dir / "verification_r1.json"
    correct_raw.write_text(
        json.dumps(
            {
                "verdict": "correct",
                "repair_hints": "",
                "verification_report": {"summary": "looks good", "critical_errors": [], "gaps": []},
            }
        ),
        encoding="utf-8",
    )
    normalized = normalize_verification_response(
        run_dir=run_dir,
        problem=problem,
        request_result=VerificationRequestResult(attempted=True, succeeded=True, response_path=str(correct_raw)),
    )
    assert normalized.decision == "accepted"

    wrong_raw = verification_dir / "verification_r2.json"
    wrong_raw.write_text(
        json.dumps(
            {
                "verdict": "wrong",
                "repair_hints": "fix step 2",
                "verification_report": {
                    "summary": "bad gap",
                    "critical_errors": [{"location": "step 2", "issue": "unsupported"}],
                    "gaps": [],
                },
            }
        ),
        encoding="utf-8",
    )
    wrong = normalize_verification_response(
        run_dir=run_dir,
        problem=problem,
        revision=2,
        request_result=VerificationRequestResult(attempted=True, succeeded=True, response_path=str(wrong_raw)),
    )
    assert wrong.decision == "repair_needed"

    blueprint = BlueprintArchiveResult(
        found=True,
        markdown_path=str(run_dir / "reasoning" / "blueprint_r1.md"),
        json_path=str(run_dir / "reasoning" / "blueprint_r1.json"),
        content="proof",
    )
    Path(blueprint.markdown_path).parent.mkdir(parents=True, exist_ok=True)
    Path(blueprint.markdown_path).write_text("proof", encoding="utf-8")
    Path(blueprint.json_path).write_text("{}", encoding="utf-8")

    repair = write_reasoning_repair_input(run_dir=run_dir, problem=problem, blueprint=blueprint, normalized=wrong)
    assert repair.written is True


def test_reasoning_workspace_discovery_and_revision_helpers(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    workspace_blueprint = reasoning_workspace_dir(run_dir) / "results" / "example" / "blueprint.md"
    workspace_blueprint.parent.mkdir(parents=True, exist_ok=True)
    workspace_blueprint.write_text("workspace proof blueprint", encoding="utf-8")
    problem = ProblemInput(problem_id="example", problem_path="three_horse/reasoning/data/example.md")

    archived = archive_reasoning_blueprint(run_dir, problem)

    assert archived.found is True
    assert archived.source_path == str(workspace_blueprint)
    (run_dir / "reasoning" / "blueprint_r1.md").parent.mkdir(parents=True, exist_ok=True)
    (run_dir / "reasoning" / "blueprint_r1.md").write_text("r1", encoding="utf-8")
    (run_dir / "reasoning" / "blueprint_r2.md").write_text("r2", encoding="utf-8")
    assert next_artifact_revision(run_dir, "reasoning", "blueprint_r*.md") == 3


def test_archive_reasoning_blueprint_normalizes_latex_delimiters(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    workspace_blueprint = reasoning_workspace_dir(run_dir) / "results" / "example" / "blueprint.md"
    workspace_blueprint.parent.mkdir(parents=True, exist_ok=True)
    workspace_blueprint.write_text(
        "# Title\n\n## Problem\nProve \\(a=b\\).\n\n## Solution\nWe have \\[a=b\\].\n",
        encoding="utf-8",
    )
    problem = ProblemInput(problem_id="example", problem_path="three_horse/reasoning/data/example.md")

    archived = archive_reasoning_blueprint(run_dir, problem)

    archived_text = Path(archived.markdown_path or "").read_text(encoding="utf-8")
    assert "Prove $a=b$." in archived_text
    assert "We have $$a=b$$." in archived_text


def test_resolve_run_feature_flags_disables_downstream_stages() -> None:
    from galois.platform.cli import _resolve_run_feature_flags

    flags = _resolve_run_feature_flags(
        verification_default=True,
        max_repair_rounds_default=1,
        reasoning_only=True,
        verification_override=None,
    )
    assert flags.pipeline == PipelinePreset.REASONING_ONLY
    assert flags.verification_enabled is False
    assert flags.repair_loop_enabled is False
    assert flags.max_repair_rounds == 0

    flags = _resolve_run_feature_flags(
        verification_default=False,
        max_repair_rounds_default=2,
        pipeline="reasoning-verification",
        reasoning_only=False,
        verification_override=None,
        repair_loop_override=False,
    )
    assert flags.pipeline == PipelinePreset.REASONING_VERIFICATION
    assert flags.verification_enabled is True
    assert flags.repair_loop_enabled is False
    assert flags.max_repair_rounds == 0


def test_build_workflow_plan_can_disable_verification_service() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    config = PlatformConfig(
        backend="codex",
        model="gpt-5.4",
        model_reasoning_effort="xhigh",
        personality="pragmatic",
        codex=CodexConfig(bin="codex", base_url_env="OPENAI_BASE_URL", api_key_env="OPENAI_API_KEY"),
        reasoning=WorkflowAreaConfig(enabled=True, workdir="three_horse/reasoning"),
        verification=WorkflowAreaConfig(enabled=True, workdir="three_horse/verification"),
        writing=WorkflowAreaConfig(enabled=True, workdir="three_horse/writing"),
        resume_enabled=True,
        max_repair_rounds=1,
        benchmark_root="benchmarks",
        run_root="runs",
        config_path=repo_root / "configs" / "defaults.toml",
        repo_root=repo_root,
    )
    paths = resolve_paths(config)
    problem = ProblemInput(
        problem_id="example",
        problem_path=str(repo_root / "three_horse" / "reasoning" / "data" / "example.md"),
        title="Example",
    )

    launches = build_workflow_plan(
        config=config,
        paths=paths,
        problem=problem,
        run_dir=repo_root / "runs" / "test",
        verification_enabled=False,
    )

    assert [launch.kind for launch in launches] == [WorkflowKind.REASONING]


def test_build_workflow_plan_stages_external_problem_under_run_workspace(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    external_problem = tmp_path / "benchmarks" / "problem.md"
    external_problem.parent.mkdir(parents=True)
    external_problem.write_text("Prove an external benchmark statement.", encoding="utf-8")
    config = PlatformConfig(
        backend="codex",
        model="gpt-5.4",
        model_reasoning_effort="xhigh",
        personality="pragmatic",
        codex=CodexConfig(bin="codex", base_url_env="OPENAI_BASE_URL", api_key_env="OPENAI_API_KEY"),
        reasoning=WorkflowAreaConfig(enabled=True, workdir="three_horse/reasoning"),
        verification=WorkflowAreaConfig(enabled=False, workdir="three_horse/verification"),
        writing=WorkflowAreaConfig(enabled=True, workdir="three_horse/writing"),
        resume_enabled=True,
        max_repair_rounds=1,
        benchmark_root="benchmarks",
        run_root="runs",
        config_path=repo_root / "configs" / "defaults.toml",
        repo_root=repo_root,
    )
    paths = resolve_paths(config)
    problem = ProblemInput(problem_id="external-example", problem_path=str(external_problem), title="External Example")

    launches = build_workflow_plan(config=config, paths=paths, problem=problem, run_dir=tmp_path / "runs" / "test")

    assert launches[0].environment["PROBLEM_FILE"].endswith("/runs/test/problem/statement.md")


def test_outer_repair_loop_can_be_disabled_for_verification_pipeline(monkeypatch, tmp_path: Path) -> None:
    from galois.platform import cli as platform_cli
    from galois.platform.run_registry import utc_now_iso

    repo_root = Path(__file__).resolve().parents[1]
    run_root = tmp_path / "runs"
    config_path = tmp_path / "config.toml"
    config_path.write_text(
        f"""
backend = "codex"
model = "gpt-5.4"
model_reasoning_effort = "xhigh"
personality = "pragmatic"

[codex]
bin = "codex"
base_url_env = "OPENAI_BASE_URL"
api_key_env = "OPENAI_API_KEY"

[reasoning]
enabled = true
workdir = "three_horse/reasoning"

[verification]
enabled = true
workdir = "three_horse/verification"

[platform]
resume_enabled = true
max_repair_rounds = 1
benchmark_root = "benchmarks"
run_root = "{run_root}"
""".lstrip(),
        encoding="utf-8",
    )

    call_state = {"reasoning_runs": 0, "verification_calls": 0}

    def fake_start_service_workflow(*, run_dir, run_id, launch, manager=None):
        return platform_cli.RunningService(
            launch=launch,
            manager=manager or SubagentManager(),
            task_id="ga-service",
            started_at=utc_now_iso(),
            stdout_path=str(run_dir / "verification" / "logs" / "stdout_r1.log"),
            stderr_path=str(run_dir / "verification" / "logs" / "stderr_r1.log"),
        )

    def fake_stop_service_workflow(*, run_dir, run_id, service, failed_error=None):
        return WorkflowResult(
            workflow=service.launch.kind.value,
            mode=service.launch.mode,
            command=[service.launch.entrypoint, *service.launch.arguments],
            cwd=service.launch.cwd,
            started_at=service.started_at,
            finished_at=utc_now_iso(),
            pid=1234,
            exit_code=0,
            stdout_path=service.stdout_path,
            stderr_path=service.stderr_path,
            status="succeeded",
            subagent_task_id=service.task_id,
            subagent_session_id="ga_service",
        )

    def fake_run_workflow(*, run_dir, run_id, launch, manager=None):
        call_state["reasoning_runs"] += 1
        problem_dir = reasoning_workspace_dir(run_dir) / "results" / "example"
        problem_dir.mkdir(parents=True, exist_ok=True)
        (problem_dir / "blueprint.md").write_text("proof attempt 1", encoding="utf-8")
        stdout_path = run_dir / "reasoning" / "logs" / "stdout_r1.log"
        stderr_path = run_dir / "reasoning" / "logs" / "stderr_r1.log"
        stdout_path.parent.mkdir(parents=True, exist_ok=True)
        stdout_path.write_text("reasoning attempt 1\n", encoding="utf-8")
        stderr_path.write_text("", encoding="utf-8")
        return WorkflowResult(
            workflow=launch.kind.value,
            mode=launch.mode,
            command=[launch.entrypoint, *launch.arguments],
            cwd=launch.cwd,
            started_at=utc_now_iso(),
            finished_at=utc_now_iso(),
            pid=2001,
            exit_code=0,
            stdout_path=str(stdout_path),
            stderr_path=str(stderr_path),
            status="succeeded",
            subagent_task_id="ga-001",
            subagent_session_id="ga_session_1",
        )

    def fake_call_verification_api(*, run_dir, problem, statement, proof, url, revision=1, timeout_seconds=60):
        call_state["verification_calls"] += 1
        verification_dir = run_dir / "verification"
        verification_dir.mkdir(parents=True, exist_ok=True)
        response_path = verification_dir / f"verification_r{revision}.json"
        response_path.write_text(
            json.dumps(
                {
                    "verdict": "wrong",
                    "repair_hints": "fix step 2",
                    "verification_report": {
                        "summary": "needs repair",
                        "critical_errors": [{"location": "step 2", "issue": "unsupported"}],
                        "gaps": [],
                    },
                }
            )
            + "\n",
            encoding="utf-8",
        )
        return VerificationRequestResult(attempted=True, succeeded=True, response_path=str(response_path))

    monkeypatch.setattr(platform_cli, "start_service_workflow", fake_start_service_workflow)
    monkeypatch.setattr(platform_cli, "stop_service_workflow", fake_stop_service_workflow)
    monkeypatch.setattr(platform_cli, "run_workflow", fake_run_workflow)
    monkeypatch.setattr(platform_cli, "call_verification_api", fake_call_verification_api)

    exit_code = platform_cli.cmd_launch_run(
        problem_id="example",
        problem_path=str(repo_root / "three_horse" / "reasoning" / "data" / "example.md"),
        title="Example",
        config_path=config_path,
        reasoning_only=False,
        verification=None,
        skip_services=False,
        pipeline="reasoning-verification",
        repair_loop=False,
    )

    assert exit_code == 0
    run_dir = sorted(run_root.iterdir())[0]
    assert call_state["reasoning_runs"] == 1
    assert call_state["verification_calls"] == 1
    assert (run_dir / "reasoning" / "repair_input_r1.json").exists()


def test_write_summary_includes_metrics_section_and_metrics_file(tmp_path: Path) -> None:
    from galois.platform.cli import RunFeatureFlags, _write_summary

    run_dir = tmp_path / "run"
    run_dir.mkdir(parents=True)
    (run_dir / "events.jsonl").write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "timestamp": "2026-04-24T09:00:00Z",
                        "run_id": "run-1",
                        "workflow": "reasoning",
                        "event_type": "reasoning_iteration_started",
                        "payload": {"attempt": 1},
                    }
                ),
                json.dumps(
                    {
                        "timestamp": "2026-04-24T09:01:00Z",
                        "run_id": "run-1",
                        "workflow": "verification",
                        "event_type": "artifact_collected",
                        "payload": {"artifact": "verification_report"},
                    }
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    verification_dir = run_dir / "verification"
    verification_dir.mkdir(parents=True)
    (verification_dir / "verification_decision_r2.json").write_text(json.dumps({"decision": "accepted"}) + "\n", encoding="utf-8")

    results = [
        WorkflowResult(
            workflow="verification",
            mode=LaunchMode.SERVICE,
            command=["python", "-m", "uvicorn"],
            cwd=".",
            started_at="2026-04-24T08:59:55Z",
            finished_at="2026-04-24T09:01:25Z",
            pid=100,
            exit_code=0,
            stdout_path=str(run_dir / "verification" / "logs" / "stdout_r1.log"),
            stderr_path=str(run_dir / "verification" / "logs" / "stderr_r1.log"),
            status="succeeded",
        ),
        WorkflowResult(
            workflow="reasoning",
            mode=LaunchMode.ONESHOT,
            command=["python", "-m", "galois.reasoning.runner"],
            cwd="three_horse/reasoning",
            started_at="2026-04-24T09:00:01Z",
            finished_at="2026-04-24T09:01:24Z",
            pid=101,
            exit_code=0,
            stdout_path=str(run_dir / "reasoning" / "logs" / "stdout_r1.log"),
            stderr_path=str(run_dir / "reasoning" / "logs" / "stderr_r1.log"),
            status="succeeded",
        ),
    ]

    _write_summary(
        run_dir,
        results,
        RunFeatureFlags(
            pipeline=PipelinePreset.REASONING_VERIFICATION,
            verification_enabled=True,
            repair_loop_enabled=True,
            max_repair_rounds=1,
        ),
    )

    summary = (run_dir / "summary.md").read_text(encoding="utf-8")
    assert "## Metrics" in summary
    assert "- verification_runtime_seconds: `90`" in summary


def test_benchmark_suite_manifest_uses_reasoning_data_examples_set() -> None:
    from galois.platform.benchmark import build_suite_plan, load_suite

    repo_root = Path(__file__).resolve().parents[1]
    suite = load_suite(repo_root / "benchmarks" / "manifests" / "reasoning_data_examples.toml", repo_root=repo_root)

    assert suite.suite_id == "reasoning-data-examples"
    assert suite.default_pipeline == PipelinePreset.REASONING_VERIFICATION
    plan = build_suite_plan(
        suite=suite,
        pipeline=PipelinePreset.REASONING_VERIFICATION,
        repair_loop_enabled=True,
        max_repair_rounds=1,
        limit=2,
    )
    assert plan["problem_count"] == 2
