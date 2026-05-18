from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from fastapi.testclient import TestClient


def _assert_public_payload_is_backend_neutral(payload: dict) -> None:
    text = json.dumps(payload, ensure_ascii=False).lower()
    assert "rethlas" not in text
    assert "lumen" not in text
    assert "codex" not in text
    assert "agents.md" not in text
    assert "blueprint" not in text
    assert "session" not in text
    assert "/tmp/" not in text


def test_v1_project_run_contract_is_backend_neutral(tmp_path: Path) -> None:
    from agent_runtime.service import ResearchRunContext, create_app

    seen_contexts: list[ResearchRunContext] = []

    def fake_launcher(context: ResearchRunContext) -> None:
        seen_contexts.append(context)
        output_dir = context.results_dir / context.problem_id
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "blueprint.md").write_text("# Solution\n\nA staged proof.", encoding="utf-8")

    app = create_app(runtime_root=tmp_path, launcher=fake_launcher, run_async=False)
    client = TestClient(app)

    response = client.post(
        "/v1/projects",
        json={
            "title": "Compactness problem",
            "problem": {
                "format": "markdown",
                "content": "Prove that a continuous function on a compact space attains a maximum.",
            },
            "instructions": [{"name": "strategy.md", "content": "Prefer a topological proof."}],
            "references": [{"name": "ref.md", "content": "Compactness notes."}],
            "execution": {
                "verification": False,
                "model": "gpt-5.4",
                "reasoning_effort": "high",
            },
        },
    )

    assert response.status_code == 202
    payload = response.json()
    _assert_public_payload_is_backend_neutral(payload)
    assert payload == {
        "project_id": "compactness-problem",
        "latest_run_id": payload["latest_run_id"],
        "status": "succeeded",
        "capability": "math_research",
        "title": "Compactness problem",
        "continued_from": None,
        "links": {
            "run": f"/v1/runs/{payload['latest_run_id']}",
            "artifacts": f"/v1/runs/{payload['latest_run_id']}/artifacts",
            "events": f"/v1/runs/{payload['latest_run_id']}/events",
        },
    }

    assert seen_contexts
    context = seen_contexts[0]
    assert context.problem_file.read_text(encoding="utf-8").startswith("Prove that")
    assert (context.reference_dir / "ref.md").read_text(encoding="utf-8") == "Compactness notes."
    assert (context.prompt_dir / "strategy.md").read_text(encoding="utf-8") == "Prefer a topological proof."

    run_response = client.get(f"/v1/runs/{payload['latest_run_id']}")
    assert run_response.status_code == 200
    run_payload = run_response.json()
    _assert_public_payload_is_backend_neutral(run_payload)
    assert run_payload["artifacts"]["solution"]["content"] == "# Solution\n\nA staged proof."
    assert run_payload["artifacts"]["verified_solution"] is None


def test_v1_continuation_preserves_project_context_and_prior_workspace(tmp_path: Path) -> None:
    from agent_runtime.service import ResearchRunContext, create_app

    seen_contexts: list[ResearchRunContext] = []

    def fake_launcher(context: ResearchRunContext) -> None:
        if seen_contexts:
            assert (context.results_dir / context.problem_id / "prior.md").read_text(encoding="utf-8") == "Prior result."
            assert (context.memory_dir / context.problem_id / "note.md").read_text(encoding="utf-8") == "Prior memory."
            assert (context.downloads_dir / context.problem_id / "paper.txt").read_text(encoding="utf-8") == "Prior download."
            assert (context.scripts_dir / context.problem_id / "experiment.py").read_text(encoding="utf-8") == "print('prior')\n"
        seen_contexts.append(context)
        if len(seen_contexts) == 1:
            (context.memory_dir / context.problem_id).mkdir(parents=True, exist_ok=True)
            (context.memory_dir / context.problem_id / "note.md").write_text("Prior memory.", encoding="utf-8")
            (context.downloads_dir / context.problem_id).mkdir(parents=True, exist_ok=True)
            (context.downloads_dir / context.problem_id / "paper.txt").write_text("Prior download.", encoding="utf-8")
            (context.scripts_dir / context.problem_id).mkdir(parents=True, exist_ok=True)
            (context.scripts_dir / context.problem_id / "experiment.py").write_text("print('prior')\n", encoding="utf-8")
        output_dir = context.results_dir / context.problem_id
        output_dir.mkdir(parents=True, exist_ok=True)
        if len(seen_contexts) == 1:
            (output_dir / "prior.md").write_text("Prior result.", encoding="utf-8")
        (output_dir / "blueprint.md").write_text(
            f"# Solution\n\ncontinuation={context.continuation_prompt or 'none'}",
            encoding="utf-8",
        )

    app = create_app(runtime_root=tmp_path, launcher=fake_launcher, run_async=False)
    client = TestClient(app)
    created = client.post(
        "/v1/projects",
        json={
            "title": "Initial project",
            "problem": {"content": "Solve the first version."},
            "instructions": [{"name": "starter.md", "content": "Initial guidance."}],
            "references": [{"name": "base.md", "content": "Initial reference."}],
            "execution": {"verification": False},
        },
    ).json()

    continued = client.post(
        f"/v1/projects/{created['project_id']}/runs",
        json={
            "prompt": "The first proof missed a boundary case. Continue from the prior work.",
            "instructions": [{"name": "extra-hint.md", "content": "Check the endpoint."}],
            "references": [{"name": "new.md", "content": "New reference."}],
        },
    )

    assert continued.status_code == 202
    payload = continued.json()
    _assert_public_payload_is_backend_neutral(payload)
    assert payload["project_id"] == created["project_id"]
    assert payload["continued_from"] == created["latest_run_id"]
    assert payload["status"] == "succeeded"

    assert len(seen_contexts) == 2
    context = seen_contexts[-1]
    assert context.previous_run_id == created["latest_run_id"]
    assert context.continuation_prompt.startswith("The first proof missed")
    assert (context.prompt_dir / "starter.md").read_text(encoding="utf-8") == "Initial guidance."
    assert (context.prompt_dir / "extra-hint.md").read_text(encoding="utf-8") == "Check the endpoint."
    assert (context.reference_dir / "base.md").read_text(encoding="utf-8") == "Initial reference."
    assert (context.reference_dir / "new.md").read_text(encoding="utf-8") == "New reference."


def test_project_workspace_is_reused_across_continuation_runs(tmp_path: Path) -> None:
    from agent_runtime.service import ResearchRunContext, create_app

    seen_contexts: list[ResearchRunContext] = []

    def fake_launcher(context: ResearchRunContext) -> None:
        seen_contexts.append(context)
        output_dir = context.results_dir / context.problem_id
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "blueprint.md").write_text(
            f"# Solution\n\nrun={len(seen_contexts)}",
            encoding="utf-8",
        )

    app = create_app(runtime_root=tmp_path, launcher=fake_launcher, run_async=False)
    client = TestClient(app)

    created = client.post(
        "/v1/projects",
        json={"title": "Reuse workspace", "problem": {"content": "Solve it."}},
    ).json()
    continued = client.post(
        f"/v1/projects/{created['project_id']}/runs",
        json={"prompt": "Continue the project."},
    ).json()

    assert len(seen_contexts) == 2
    assert seen_contexts[0].workspace_dir == seen_contexts[1].workspace_dir
    assert seen_contexts[0].workspace_dir == tmp_path / "projects" / created["project_id"] / "workspace" / "generation"
    assert seen_contexts[0].run_dir != seen_contexts[1].run_dir
    assert seen_contexts[0].run_dir == tmp_path / "projects" / created["project_id"] / "runs" / created["latest_run_id"]
    assert seen_contexts[1].run_dir == tmp_path / "projects" / created["project_id"] / "runs" / continued["latest_run_id"]
    assert seen_contexts[0].logs_dir == seen_contexts[0].run_dir / "logs"
    assert seen_contexts[1].logs_dir == seen_contexts[1].run_dir / "logs"


def test_project_workspace_uses_static_symlinks_and_writable_dirs(tmp_path: Path) -> None:
    from agent_runtime.service import ResearchRunContext, create_app

    seen_contexts: list[ResearchRunContext] = []

    def fake_launcher(context: ResearchRunContext) -> None:
        seen_contexts.append(context)
        output_dir = context.results_dir / context.problem_id
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "blueprint.md").write_text("# Solution\n", encoding="utf-8")

    app = create_app(runtime_root=tmp_path, launcher=fake_launcher, run_async=False)
    client = TestClient(app)

    created = client.post(
        "/v1/projects",
        json={
            "title": "Thin workspace",
            "problem": {"content": "Solve it."},
            "instructions": [{"name": "strategy.md", "content": "Keep it short."}],
            "references": [{"name": "note.md", "content": "Reference note."}],
        },
    ).json()

    assert created["status"] == "succeeded"
    assert seen_contexts
    context = seen_contexts[0]
    source = Path("references/Lumen/agents/generation").resolve()

    for name in ("AGENTS.md", ".agents", ".codex", "tests"):
        entry = context.workspace_dir / name
        assert entry.is_symlink()
        assert entry.resolve() == source / name

    mcp_dir = context.workspace_dir / "mcp"
    assert mcp_dir.is_dir()
    assert not mcp_dir.is_symlink()
    assert (mcp_dir / "server.py").is_file()
    assert not (mcp_dir / "server.py").is_symlink()
    assert (mcp_dir / "requirements.txt").is_symlink()
    assert (mcp_dir / "requirements.txt").resolve() == source / "mcp" / "requirements.txt"
    spec = importlib.util.spec_from_file_location("thin_workspace_mcp_server", mcp_dir / "server.py")
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.REPO_ROOT == context.workspace_dir
    assert module.MEMORY_ROOT == context.workspace_dir / "memory"

    for name in ("data", "input", "memory", "results", "downloads", "scripts", "logs"):
        entry = context.workspace_dir / name
        assert entry.is_dir()
        assert not entry.is_symlink()

    assert context.problem_file == context.workspace_dir / "data" / "thin-workspace.md"
    assert context.problem_file.read_text(encoding="utf-8") == "Solve it."
    assert (context.prompt_dir / "strategy.md").read_text(encoding="utf-8") == "Keep it short."
    assert (context.reference_dir / "note.md").read_text(encoding="utf-8") == "Reference note."


def test_run_directory_exposes_shared_workspace_dirs_without_copying(tmp_path: Path) -> None:
    from agent_runtime.service import ResearchRunContext, create_app

    seen_contexts: list[ResearchRunContext] = []

    def fake_launcher(context: ResearchRunContext) -> None:
        seen_contexts.append(context)
        (context.memory_dir / context.problem_id).mkdir(parents=True, exist_ok=True)
        (context.memory_dir / context.problem_id / "note.md").write_text("Memory note.", encoding="utf-8")
        (context.downloads_dir / context.problem_id).mkdir(parents=True, exist_ok=True)
        (context.downloads_dir / context.problem_id / "paper.txt").write_text("Downloaded note.", encoding="utf-8")
        (context.scripts_dir / context.problem_id).mkdir(parents=True, exist_ok=True)
        (context.scripts_dir / context.problem_id / "check.py").write_text("print('ok')\n", encoding="utf-8")
        output_dir = context.results_dir / context.problem_id
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "blueprint.md").write_text("# Solution\n", encoding="utf-8")

    app = create_app(runtime_root=tmp_path, launcher=fake_launcher, run_async=False)
    client = TestClient(app)

    created = client.post(
        "/v1/projects",
        json={"title": "Run entries", "problem": {"content": "Solve it."}},
    ).json()

    context = seen_contexts[0]
    run_dir = tmp_path / "projects" / created["project_id"] / "runs" / created["latest_run_id"]
    assert (run_dir / "input").is_dir()
    assert (run_dir / "logs").is_dir()
    assert (run_dir / "artifacts").is_dir()
    assert not (run_dir / "input").is_symlink()
    assert not (run_dir / "logs").is_symlink()
    assert not (run_dir / "artifacts").is_symlink()

    for name in ("memory", "results", "downloads", "scripts"):
        entry = run_dir / name
        assert entry.is_symlink()
        assert entry.resolve() == context.workspace_dir / name

    assert (run_dir / "memory" / "run-entries" / "note.md").read_text(encoding="utf-8") == "Memory note."
    assert (run_dir / "results" / "run-entries" / "blueprint.md").read_text(encoding="utf-8") == "# Solution\n"
    assert (run_dir / "downloads" / "run-entries" / "paper.txt").read_text(encoding="utf-8") == "Downloaded note."
    assert (run_dir / "scripts" / "run-entries" / "check.py").read_text(encoding="utf-8") == "print('ok')\n"


def test_existing_run_directory_is_backfilled_with_shared_entries(tmp_path: Path) -> None:
    from agent_runtime.service import ResearchRunContext, create_app

    seen_contexts: list[ResearchRunContext] = []

    def fake_launcher(context: ResearchRunContext) -> None:
        seen_contexts.append(context)
        output_dir = context.results_dir / context.problem_id
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "blueprint.md").write_text("# Solution\n", encoding="utf-8")

    app = create_app(runtime_root=tmp_path, launcher=fake_launcher, run_async=False)
    client = TestClient(app)

    created = client.post(
        "/v1/projects",
        json={"title": "Legacy run", "problem": {"content": "Solve it."}},
    ).json()

    run_dir = tmp_path / "projects" / created["project_id"] / "runs" / created["latest_run_id"]
    for name in ("memory", "results", "downloads", "scripts"):
        (run_dir / name).unlink()
    assert not (run_dir / "memory").exists()

    status = client.get(f"/v1/runs/{created['latest_run_id']}")

    assert status.status_code == 200
    for name in ("memory", "results", "downloads", "scripts"):
        entry = run_dir / name
        assert entry.is_symlink()
        assert entry.resolve() == seen_contexts[0].workspace_dir / name


def test_run_artifacts_are_snapshotted_per_run(tmp_path: Path) -> None:
    from agent_runtime.service import ResearchRunContext, create_app

    seen_contexts: list[ResearchRunContext] = []

    def fake_launcher(context: ResearchRunContext) -> None:
        seen_contexts.append(context)
        output_dir = context.results_dir / context.problem_id
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "blueprint.md").write_text(
            f"# Solution\n\nversion={len(seen_contexts)}",
            encoding="utf-8",
        )

    app = create_app(runtime_root=tmp_path, launcher=fake_launcher, run_async=False)
    client = TestClient(app)

    created = client.post(
        "/v1/projects",
        json={"title": "Snapshot project", "problem": {"content": "Solve it."}},
    ).json()
    first_run_id = created["latest_run_id"]
    continued = client.post(
        f"/v1/projects/{created['project_id']}/runs",
        json={"prompt": "Revise it."},
    ).json()
    second_run_id = continued["latest_run_id"]

    first_artifacts = client.get(f"/v1/runs/{first_run_id}/artifacts").json()
    second_artifacts = client.get(f"/v1/runs/{second_run_id}/artifacts").json()

    _assert_public_payload_is_backend_neutral(first_artifacts)
    _assert_public_payload_is_backend_neutral(second_artifacts)
    assert first_artifacts["artifacts"]["solution"]["content"] == "# Solution\n\nversion=1"
    assert second_artifacts["artifacts"]["solution"]["content"] == "# Solution\n\nversion=2"
    assert (tmp_path / "projects" / created["project_id"] / "runs" / first_run_id / "artifacts" / "solution.md").exists()
    assert (tmp_path / "projects" / created["project_id"] / "runs" / second_run_id / "artifacts" / "solution.md").exists()


def test_failed_continuation_does_not_expose_prior_workspace_artifacts(tmp_path: Path) -> None:
    from agent_runtime.service import ResearchRunContext, create_app

    seen_contexts: list[ResearchRunContext] = []

    def fake_launcher(context: ResearchRunContext) -> None:
        seen_contexts.append(context)
        if len(seen_contexts) == 2:
            raise RuntimeError("second run failed after prior result")
        output_dir = context.results_dir / context.problem_id
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "blueprint.md").write_text("# Solution\n\nversion=1", encoding="utf-8")

    app = create_app(runtime_root=tmp_path, launcher=fake_launcher, run_async=False)
    client = TestClient(app)

    created = client.post(
        "/v1/projects",
        json={"title": "Failed snapshot project", "problem": {"content": "Solve it."}},
    ).json()
    continued = client.post(
        f"/v1/projects/{created['project_id']}/runs",
        json={"prompt": "Try a failing continuation."},
    ).json()

    failed_run_id = continued["latest_run_id"]
    status = client.get(f"/v1/runs/{failed_run_id}").json()
    artifacts = client.get(f"/v1/runs/{failed_run_id}/artifacts").json()

    _assert_public_payload_is_backend_neutral(status)
    _assert_public_payload_is_backend_neutral(artifacts)
    assert status["status"] == "failed"
    assert artifacts["artifacts"]["solution"] is None
    assert artifacts["artifacts"]["verified_solution"] is None


def test_default_launcher_runs_vendored_generation_workspace(monkeypatch, tmp_path: Path) -> None:
    from agent_runtime.service import create_app

    captured: list[dict[str, object]] = []

    def fake_run(command: list[str], **kwargs):
        workspace = Path(kwargs["cwd"])
        prompt = command[-1]
        captured.append({"command": command, "workspace": workspace, "prompt": prompt})
        output_dir = workspace / "results" / "vendored-project"
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "blueprint.md").write_text("# Solution\n", encoding="utf-8")

        class Completed:
            returncode = 0
            stdout = "session id: 123e4567-e89b-12d3-a456-426614174000\n"

        return Completed()

    monkeypatch.setattr("subprocess.run", fake_run)
    monkeypatch.setenv("CODEX_BIN", "fake-codex")

    app = create_app(runtime_root=tmp_path, run_async=False)
    client = TestClient(app)
    response = client.post(
        "/v1/projects",
        json={
            "title": "Vendored project",
            "problem": {"content": "Solve the first version."},
            "instructions": [{"name": "strategy.md", "content": "Prefer a direct proof."}],
            "references": [{"name": "note.md", "content": "Reference note."}],
            "execution": {"verification": False, "model": "test-model", "reasoning_effort": "low"},
        },
    )

    assert response.status_code == 202
    payload = response.json()
    _assert_public_payload_is_backend_neutral(payload)
    assert captured
    command = captured[0]["command"]
    workspace = captured[0]["workspace"]
    prompt = captured[0]["prompt"]
    assert isinstance(command, list)
    assert isinstance(workspace, Path)
    assert isinstance(prompt, str)
    assert command[:3] == ["fake-codex", "exec", "-C"]
    assert command[3] == str(workspace)
    assert "test-model" in command
    assert 'model_reasoning_effort="low"' in command
    assert (workspace / "AGENTS.md").exists()
    assert (workspace / ".agents").exists()
    assert (workspace / "mcp" / "server.py").exists()
    assert (workspace / "data" / "vendored-project.md").read_text(encoding="utf-8") == "Solve the first version."
    assert (workspace / "data" / "vendored-project.refs" / "note.md").read_text(encoding="utf-8") == "Reference note."
    assert "data/vendored-project.md" in prompt
    assert "Use problem_id=vendored-project" in prompt
    assert "data/vendored-project.refs" in prompt
    assert "Prefer a direct proof." in prompt

    run_payload = client.get(f"/v1/runs/{payload['latest_run_id']}").json()
    _assert_public_payload_is_backend_neutral(run_payload)
    assert run_payload["artifacts"]["solution"]["content"] == "# Solution\n"


def test_v1_health_artifacts_events_and_file_validation(tmp_path: Path) -> None:
    from agent_runtime.service import ResearchRunContext, create_app

    def fake_launcher(context: ResearchRunContext) -> None:
        output_dir = context.results_dir / context.problem_id
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "blueprint.md").write_text("# Solution\n", encoding="utf-8")
        (output_dir / "blueprint_verified.md").write_text("# Verified Solution\n", encoding="utf-8")

    app = create_app(runtime_root=tmp_path, launcher=fake_launcher, run_async=False)
    client = TestClient(app)

    health = client.get("/v1/health")
    assert health.status_code == 200
    _assert_public_payload_is_backend_neutral(health.json())

    created = client.post(
        "/v1/projects",
        json={"title": "Artifact project", "problem": {"content": "Solve it."}, "execution": {"verification": True}},
    ).json()
    artifacts = client.get(f"/v1/runs/{created['latest_run_id']}/artifacts")
    events = client.get(f"/v1/runs/{created['latest_run_id']}/events")

    assert artifacts.status_code == 200
    artifact_payload = artifacts.json()
    _assert_public_payload_is_backend_neutral(artifact_payload)
    assert artifact_payload["artifacts"]["solution"]["content"] == "# Solution\n"
    assert artifact_payload["artifacts"]["verified_solution"]["content"] == "# Verified Solution\n"

    assert events.status_code == 200
    event_payload = events.json()
    _assert_public_payload_is_backend_neutral(event_payload)
    assert [event["type"] for event in event_payload["events"]] == ["created", "running", "succeeded"]

    invalid = client.post(
        "/v1/projects",
        json={
            "problem": {"content": "Solve it."},
            "instructions": [{"name": "../escape.md", "content": "bad"}],
        },
    )
    assert invalid.status_code == 400


def test_failure_events_remain_backend_neutral(tmp_path: Path) -> None:
    from agent_runtime.service import ResearchRunContext, create_app

    def failing_launcher(context: ResearchRunContext) -> None:
        raise RuntimeError("codex Rethlas Lumen AGENTS.md blueprint session /tmp/private")

    app = create_app(runtime_root=tmp_path, launcher=failing_launcher, run_async=False)
    client = TestClient(app)

    created = client.post(
        "/v1/projects",
        json={"title": "Failure project", "problem": {"content": "Solve it."}},
    ).json()

    events = client.get(f"/v1/runs/{created['latest_run_id']}/events")

    assert events.status_code == 200
    payload = events.json()
    _assert_public_payload_is_backend_neutral(payload)
    assert payload["events"][-1]["message"] == "runtime execution failed"


def test_agent_runtime_cli_uses_neutral_public_name() -> None:
    from agent_runtime.cli import build_parser

    parser = build_parser()
    args = parser.parse_args(["serve", "--host", "127.0.0.1", "--port", "8765"])

    assert args.command == "serve"
    assert args.host == "127.0.0.1"
    assert args.port == 8765

    create_args = parser.parse_args(
        [
            "create",
            "--problem-file",
            "problem.md",
            "--title",
            "CLI project",
            "--instruction",
            "hint.md",
            "--reference",
            "ref.md",
            "--json",
        ]
    )
    assert create_args.command == "create"
    assert create_args.problem_file == Path("problem.md")
    assert create_args.title == "CLI project"
    assert create_args.instructions == [Path("hint.md")]
    assert create_args.references == [Path("ref.md")]
    assert create_args.output_json is True

    continue_args = parser.parse_args(["continue", "project-1", "--prompt", "try again", "--json"])
    assert continue_args.command == "continue"
    assert continue_args.project_id == "project-1"
    assert continue_args.prompt == "try again"
    assert continue_args.output_json is True

    status_args = parser.parse_args(["status", "run-1", "--json"])
    assert status_args.command == "status"
    assert status_args.run_id == "run-1"

    artifacts_args = parser.parse_args(["artifacts", "run-1", "--json"])
    assert artifacts_args.command == "artifacts"
    assert artifacts_args.run_id == "run-1"
