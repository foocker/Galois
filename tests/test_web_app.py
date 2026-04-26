from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient


def _write_config(path: Path, run_root: Path) -> None:
    path.write_text(
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


def test_index_serves_research_workbench(tmp_path: Path) -> None:
    from galois.platform.web import create_app

    config_path = tmp_path / "config.toml"
    _write_config(config_path, tmp_path / "runs")

    client = TestClient(create_app(config_path=config_path))
    response = client.get("/")

    assert response.status_code == 200
    assert "Galois" in response.text
    assert "Research Workbench" in response.text


def test_create_run_rejects_blank_problem_markdown(tmp_path: Path) -> None:
    from galois.platform.web import create_app

    config_path = tmp_path / "config.toml"
    _write_config(config_path, tmp_path / "runs")

    client = TestClient(create_app(config_path=config_path))
    response = client.post(
        "/api/runs",
        json={"title": "Blank", "problem_markdown": "   ", "pipeline": "reasoning-verification"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "problem_markdown must not be blank"


def test_latest_blueprint_prefers_highest_revision(tmp_path: Path) -> None:
    from galois.platform.web import read_run_snapshot

    run_root = tmp_path / "runs"
    run_dir = run_root / "20260425T100000Z_demo"
    reasoning_dir = run_dir / "reasoning"
    reasoning_dir.mkdir(parents=True)
    (reasoning_dir / "blueprint_r1.md").write_text("first", encoding="utf-8")
    (reasoning_dir / "blueprint_r3.md").write_text("third", encoding="utf-8")
    (reasoning_dir / "blueprint_r2.md").write_text("second", encoding="utf-8")
    (run_dir / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": run_dir.name,
                "status": "succeeded",
                "pipeline": "reasoning-verification",
                "problem": {"problem_id": "demo", "title": "Demo"},
                "workflows": ["reasoning", "verification"],
            }
        ),
        encoding="utf-8",
    )

    snapshot = read_run_snapshot(run_root, run_dir.name)

    assert snapshot["output"]["kind"] == "reasoning_blueprint"
    assert snapshot["output"]["content"] == "third"
    assert snapshot["output"]["path"].endswith("reasoning/blueprint_r3.md")


def test_create_run_writes_problem_and_starts_background_launch(monkeypatch, tmp_path: Path) -> None:
    from galois.platform import web

    config_path = tmp_path / "config.toml"
    run_root = tmp_path / "runs"
    _write_config(config_path, run_root)
    launches: list[dict[str, object]] = []

    def fake_start_launch(**kwargs: object) -> None:
        launches.append(kwargs)

    monkeypatch.setattr(web, "start_launch_thread", fake_start_launch)

    client = TestClient(web.create_app(config_path=config_path))
    response = client.post(
        "/api/runs",
        json={
            "title": "Euler identity",
            "problem_markdown": "Prove $e^{i\\pi}+1=0$.",
            "pipeline": "reasoning-only",
        },
    )

    assert response.status_code == 202
    payload = response.json()
    assert payload["status"] == "queued"
    assert payload["run_id"].startswith("web_")
    problem_path = Path(payload["problem_path"])
    assert problem_path.exists()
    assert problem_path.read_text(encoding="utf-8") == "Prove $e^{i\\pi}+1=0$.\n"
    assert launches == [
        {
            "problem_id": payload["problem_id"],
            "problem_path": str(problem_path),
            "title": "Euler identity",
            "config_path": config_path,
            "pipeline": "reasoning-only",
        }
    ]


def test_run_snapshot_reads_events_subagents_and_summary_fallback(tmp_path: Path) -> None:
    from galois.platform.web import read_run_snapshot

    run_root = tmp_path / "runs"
    run_dir = run_root / "20260425T110000Z_summary"
    run_dir.mkdir(parents=True)
    (run_dir / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": run_dir.name,
                "status": "failed",
                "pipeline": "reasoning-only",
                "problem": {"problem_id": "summary", "title": "Summary"},
                "workflows": ["reasoning"],
                "features": {"repair_loop_enabled": False},
            }
        ),
        encoding="utf-8",
    )
    (run_dir / "events.jsonl").write_text(
        json.dumps({"event_type": "run_created", "workflow": None}) + "\n"
        + json.dumps({"event_type": "run_finished", "workflow": None})
        + "\n",
        encoding="utf-8",
    )
    (run_dir / "subagents.json").write_text(json.dumps([{"task_id": "t1", "status": "failed"}]), encoding="utf-8")
    (run_dir / "summary.md").write_text("# Run Summary\n\nFailed cleanly.", encoding="utf-8")

    snapshot = read_run_snapshot(run_root, run_dir.name)

    assert snapshot["status"] == "failed"
    assert snapshot["features"] == {"repair_loop_enabled": False}
    assert [event["event_type"] for event in snapshot["events"]] == ["run_created", "run_finished"]
    assert snapshot["subagents"] == [{"task_id": "t1", "status": "failed"}]
    assert snapshot["output"] == {
        "kind": "summary",
        "path": str(run_dir / "summary.md"),
        "content": "# Run Summary\n\nFailed cleanly.",
    }


def test_list_runs_includes_recent_web_runs(monkeypatch, tmp_path: Path) -> None:
    from galois.platform import web

    config_path = tmp_path / "config.toml"
    _write_config(config_path, tmp_path / "runs")

    def fake_start_launch(**kwargs: object) -> None:
        return None

    monkeypatch.setattr(web, "start_launch_thread", fake_start_launch)
    client = TestClient(web.create_app(config_path=config_path))
    created = client.post(
        "/api/runs",
        json={"title": "Recent", "problem_markdown": "Show that $1+1=2$.", "pipeline": "reasoning-verification"},
    ).json()

    response = client.get("/api/runs")

    assert response.status_code == 200
    runs = response.json()["runs"]
    assert any(run["run_id"] == created["run_id"] and run["status"] == "queued" for run in runs)


def test_cli_parser_accepts_web_command() -> None:
    from galois.platform.cli import build_parser

    args = build_parser().parse_args(["web", "--host", "0.0.0.0", "--port", "8123", "--config", "config.toml"])

    assert args.command == "web"
    assert args.host == "0.0.0.0"
    assert args.port == 8123
    assert str(args.config) == "config.toml"


def test_launch_command_reuses_current_python_interpreter(tmp_path: Path) -> None:
    import sys

    from galois.platform.web import build_launch_command

    config_path = tmp_path / "config.toml"
    command = build_launch_command(
        problem_id="web_demo",
        problem_path="/tmp/problem.md",
        title="Demo title",
        config_path=config_path,
        pipeline="reasoning-verification",
    )

    assert command[:5] == [sys.executable, "-u", "-m", "galois.platform.cli", "launch"]
    assert "uv" not in command
    assert command[-4:] == ["--title", "Demo title", "--config", str(config_path)]


def test_run_snapshot_rejects_path_traversal(tmp_path: Path) -> None:
    from galois.platform.web import read_run_snapshot

    run_root = tmp_path / "runs"
    run_root.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "manifest.json").write_text(json.dumps({"run_id": "outside", "status": "succeeded"}), encoding="utf-8")

    try:
        read_run_snapshot(run_root, "../outside")
    except FileNotFoundError:
        pass
    else:
        raise AssertionError("expected traversal run id to be rejected")


def test_stream_launch_process_records_real_run_id_before_completion(monkeypatch, tmp_path: Path) -> None:
    from galois.platform import web

    status_dir = tmp_path / "web_runs" / "web_demo"
    calls: list[dict[str, object]] = []

    class FakeStdout:
        def __iter__(self):
            return iter(["run_id=20260425T120000Z_real\n", f"run_dir={tmp_path / 'runs' / '20260425T120000Z_real'}\n"])

    class FakeProcess:
        stdout = FakeStdout()
        returncode = 0

        def wait(self) -> int:
            calls.append({"waited": True})
            return self.returncode

    def fake_popen(command, cwd, text, stdout, stderr):
        calls.append({"command": command, "cwd": cwd, "text": text, "stdout": stdout, "stderr": stderr})
        return FakeProcess()

    monkeypatch.setattr(web.subprocess, "Popen", fake_popen)

    web.run_launch_process(
        command=["python", "-m", "galois.platform.cli", "launch"],
        cwd=tmp_path,
        web_run_dir=status_dir,
        problem_id="web_demo",
        problem_path=str(tmp_path / "problem.md"),
        title="Demo",
        pipeline="reasoning-only",
    )

    status = json.loads((status_dir / "status.json").read_text(encoding="utf-8"))
    assert status["status"] == "launched"
    assert status["real_run_id"] == "20260425T120000Z_real"
    assert status["real_run_dir"] == str(tmp_path / "runs" / "20260425T120000Z_real")
    assert (status_dir / "launch.log").read_text(encoding="utf-8").startswith("run_id=20260425T120000Z_real")


def test_launch_command_uses_unbuffered_python(tmp_path: Path) -> None:
    import sys

    from galois.platform.web import build_launch_command

    command = build_launch_command(
        problem_id="web_demo",
        problem_path="/tmp/problem.md",
        title=None,
        config_path=None,
        pipeline="reasoning-only",
    )

    assert command[:5] == [sys.executable, "-u", "-m", "galois.platform.cli", "launch"]


def test_web_snapshot_falls_back_to_matching_real_run(tmp_path: Path) -> None:
    from galois.platform.web import read_run_snapshot

    project_root = tmp_path / "project"
    run_root = project_root / "runs"
    web_id = "web_20260425T201429_demo"
    web_dir = project_root / "web_runs" / web_id
    web_dir.mkdir(parents=True)
    (web_dir / "status.json").write_text(
        json.dumps(
            {
                "run_id": web_id,
                "status": "running",
                "pipeline": "reasoning-verification",
                "problem": {"problem_id": web_id, "title": "Demo"},
            }
        ),
        encoding="utf-8",
    )
    real_dir = run_root / "20260425T121429Z_real"
    real_dir.mkdir(parents=True)
    (real_dir / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": real_dir.name,
                "status": "running",
                "pipeline": "reasoning-verification",
                "problem": {"problem_id": web_id, "title": "Demo"},
                "workflows": ["reasoning", "verification"],
            }
        ),
        encoding="utf-8",
    )

    snapshot = read_run_snapshot(run_root, web_id, project_root=project_root)

    assert snapshot["run_id"] == real_dir.name
    assert snapshot["web_run_id"] == web_id
    assert snapshot["workflows"] == ["reasoning", "verification"]
