"""FastAPI workbench for launching and inspecting Galois research runs."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import threading
from pathlib import Path
from time import strftime
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .config import load_config
from .contracts import PipelinePreset
from .paths import resolve_paths


ASSET_DIR = Path(__file__).with_name("web_assets")


class RunCreateRequest(BaseModel):
    title: str | None = None
    problem_markdown: str
    pipeline: str = "reasoning-verification"


def _slug(text: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return normalized[:48] or "problem"


def _new_web_problem_id(title: str | None) -> str:
    return f"web_{strftime('%Y%m%dT%H%M%S')}_{_slug(title or 'problem')}_{uuid4().hex[:6]}"


def _write_problem_input(project_root: Path, problem_id: str, problem_markdown: str) -> Path:
    input_dir = project_root / "web_inputs"
    input_dir.mkdir(parents=True, exist_ok=True)
    problem_path = input_dir / f"{problem_id}.md"
    problem_path.write_text(problem_markdown.strip() + "\n", encoding="utf-8")
    return problem_path


def _web_run_dir(project_root: Path, problem_id: str) -> Path:
    return project_root / "web_runs" / problem_id


def _write_web_status(web_run_dir: Path, payload: dict[str, Any]) -> None:
    web_run_dir.mkdir(parents=True, exist_ok=True)
    (web_run_dir / "status.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _read_web_status(project_root: Path, run_id: str) -> dict[str, Any] | None:
    status_path = _web_run_dir(project_root, run_id) / "status.json"
    if not status_path.exists():
        return None
    return _safe_json(status_path, {})


def _extract_run_field(output: str, field: str) -> str | None:
    prefix = f"{field}="
    for line in output.splitlines():
        if line.startswith(prefix):
            return line[len(prefix) :].strip()
    return None


def build_launch_command(
    *,
    problem_id: str,
    problem_path: str,
    title: str | None,
    config_path: Path | None,
    pipeline: str,
) -> list[str]:
    command = [
        sys.executable,
        "-u",
        "-m",
        "galois.platform.cli",
        "launch",
        "--problem-id",
        problem_id,
        "--problem-path",
        problem_path,
        "--pipeline",
        pipeline,
    ]
    if title:
        command.extend(["--title", title])
    if config_path is not None:
        command.extend(["--config", str(config_path)])
    return command


def _find_run_by_problem_id(run_root: Path, problem_id: str) -> Path | None:
    if not run_root.exists():
        return None
    for run_dir in sorted((candidate for candidate in run_root.iterdir() if candidate.is_dir()), reverse=True):
        manifest = _safe_json(run_dir / "manifest.json", {})
        if manifest.get("problem", {}).get("problem_id") == problem_id:
            return run_dir
    return None


def _base_launch_status(
    *,
    problem_id: str,
    problem_path: str,
    title: str | None,
    pipeline: str,
) -> dict[str, Any]:
    return {
        "run_id": problem_id,
        "pipeline": pipeline,
        "problem": {"problem_id": problem_id, "problem_path": problem_path, "title": title},
    }


def run_launch_process(
    *,
    command: list[str],
    cwd: Path,
    web_run_dir: Path,
    problem_id: str,
    problem_path: str,
    title: str | None,
    pipeline: str,
) -> None:
    output_path = web_run_dir / "launch.log"
    error_path = web_run_dir / "launch_error.log"
    base_status = _base_launch_status(
        problem_id=problem_id,
        problem_path=problem_path,
        title=title,
        pipeline=pipeline,
    )
    _write_web_status(web_run_dir, {**base_status, "status": "running", "command": command})

    real_run_id: str | None = None
    real_run_dir: str | None = None
    with output_path.open("w", encoding="utf-8") as stdout_handle, error_path.open("w", encoding="utf-8") as stderr_handle:
        process = subprocess.Popen(
            command,
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=stderr_handle,
        )
        if process.stdout is not None:
            for line in process.stdout:
                stdout_handle.write(line)
                stdout_handle.flush()
                if extracted := _extract_run_field(line, "run_id"):
                    real_run_id = extracted
                if extracted := _extract_run_field(line, "run_dir"):
                    real_run_dir = extracted
                if real_run_id or real_run_dir:
                    _write_web_status(
                        web_run_dir,
                        {
                            **base_status,
                            "status": "running",
                            "command": command,
                            "real_run_id": real_run_id,
                            "real_run_dir": real_run_dir,
                            "stdout_path": str(output_path),
                            "stderr_path": str(error_path),
                        },
                    )
        returncode = process.wait()

    _write_web_status(
        web_run_dir,
        {
            **base_status,
            "status": "launched" if returncode == 0 else "failed",
            "command": command,
            "real_run_id": real_run_id,
            "real_run_dir": real_run_dir,
            "returncode": returncode,
            "stdout_path": str(output_path),
            "stderr_path": str(error_path),
        },
    )


def start_launch_thread(
    *,
    problem_id: str,
    problem_path: str,
    title: str | None,
    config_path: Path | None,
    pipeline: str,
) -> None:
    def launch() -> None:
        config = load_config(config_path)
        command = build_launch_command(
            problem_id=problem_id,
            problem_path=problem_path,
            title=title,
            config_path=config_path,
            pipeline=pipeline,
        )
        project_root = config.project_root_path
        web_run_dir = _web_run_dir(project_root, problem_id)
        run_launch_process(
            command=command,
            cwd=config.repo_root,
            web_run_dir=web_run_dir,
            problem_id=problem_id,
            problem_path=problem_path,
            title=title,
            pipeline=pipeline,
        )

    thread = threading.Thread(target=launch, name=f"galois-web-{problem_id}", daemon=True)
    thread.start()


def _safe_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


def _latest_revision(path: Path) -> int:
    match = re.search(r"_r(\d+)\.md$", path.name)
    return int(match.group(1)) if match else 0


def _latest_blueprint(run_dir: Path) -> Path | None:
    blueprints = sorted(
        (run_dir / "reasoning").glob("blueprint_r*.md"),
        key=lambda candidate: (_latest_revision(candidate), candidate.name),
    )
    return blueprints[-1] if blueprints else None


def _read_events(run_dir: Path, limit: int = 40) -> list[dict[str, Any]]:
    events_path = run_dir / "events.jsonl"
    if not events_path.exists():
        return []
    events: list[dict[str, Any]] = []
    for line in events_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events[-limit:]


def _output_payload(run_dir: Path) -> dict[str, Any] | None:
    blueprint_path = _latest_blueprint(run_dir)
    if blueprint_path is not None:
        return {
            "kind": "reasoning_blueprint",
            "path": str(blueprint_path),
            "content": blueprint_path.read_text(encoding="utf-8"),
        }

    summary_path = run_dir / "summary.md"
    if summary_path.exists():
        return {
            "kind": "summary",
            "path": str(summary_path),
            "content": summary_path.read_text(encoding="utf-8"),
        }
    return None


def read_run_snapshot(run_root: Path, run_id: str, project_root: Path | None = None) -> dict[str, Any]:
    if project_root is not None:
        web_status = _read_web_status(project_root, run_id)
        if web_status:
            real_run_id = web_status.get("real_run_id")
            real_run_dir = Path(str(web_status.get("real_run_dir", ""))) if web_status.get("real_run_dir") else None
            if not real_run_id or not real_run_dir or not real_run_dir.exists():
                matched_run_dir = _find_run_by_problem_id(run_root, run_id)
                if matched_run_dir is not None:
                    real_run_id = matched_run_dir.name
                    real_run_dir = matched_run_dir
            if real_run_id and real_run_dir and real_run_dir.exists():
                snapshot = read_run_snapshot(real_run_dir.parent, str(real_run_id))
                snapshot["web_run_id"] = run_id
                snapshot["launch"] = web_status
                return snapshot
            return {
                "run_id": run_id,
                "run_dir": str(_web_run_dir(project_root, run_id)),
                "status": web_status.get("status", "queued"),
                "pipeline": web_status.get("pipeline"),
                "problem": web_status.get("problem", {}),
                "workflows": [],
                "features": {},
                "events": [],
                "subagents": [],
                "output": None,
                "launch": web_status,
            }

    resolved_run_root = run_root.resolve()
    run_dir = (resolved_run_root / run_id).resolve()
    if run_dir.parent != resolved_run_root or not run_dir.exists() or not run_dir.is_dir():
        raise FileNotFoundError(run_id)

    manifest = _safe_json(run_dir / "manifest.json", {})
    subagents = _safe_json(run_dir / "subagents.json", [])
    events = _read_events(run_dir)
    output = _output_payload(run_dir)

    return {
        "run_id": manifest.get("run_id", run_dir.name),
        "run_dir": str(run_dir),
        "status": manifest.get("status", "unknown"),
        "pipeline": manifest.get("pipeline"),
        "problem": manifest.get("problem", {}),
        "workflows": manifest.get("workflows", []),
        "features": manifest.get("features", {}),
        "events": events,
        "subagents": subagents,
        "output": output,
    }


def create_app(config_path: Path | None = None) -> FastAPI:
    config = load_config(config_path)
    paths = resolve_paths(config)
    app = FastAPI(title="Galois Research Workbench")

    if ASSET_DIR.exists():
        app.mount("/assets", StaticFiles(directory=ASSET_DIR), name="assets")

    @app.get("/", response_class=HTMLResponse)
    def index() -> str:
        index_path = ASSET_DIR / "index.html"
        return index_path.read_text(encoding="utf-8")

    @app.get("/api/runs")
    def list_runs() -> dict[str, Any]:
        run_root = config.run_root_path
        runs = []
        if run_root.exists():
            for run_dir in sorted((candidate for candidate in run_root.iterdir() if candidate.is_dir()), reverse=True):
                manifest = _safe_json(run_dir / "manifest.json", {})
                runs.append(
                    {
                        "run_id": manifest.get("run_id", run_dir.name),
                        "status": manifest.get("status", "unknown"),
                        "pipeline": manifest.get("pipeline"),
                        "problem": manifest.get("problem", {}),
                    }
                )
        web_root = paths.project_root / "web_runs"
        if web_root.exists():
            for web_dir in sorted((candidate for candidate in web_root.iterdir() if candidate.is_dir()), reverse=True):
                status = _safe_json(web_dir / "status.json", {})
                runs.append(
                    {
                        "run_id": status.get("run_id", web_dir.name),
                        "status": status.get("status", "queued"),
                        "pipeline": status.get("pipeline"),
                        "problem": status.get("problem", {}),
                        "real_run_id": status.get("real_run_id"),
                    }
                )
        return {"runs": runs[:20]}

    @app.post("/api/runs")
    def create_run(payload: RunCreateRequest) -> dict[str, Any]:
        if not payload.problem_markdown.strip():
            raise HTTPException(status_code=400, detail="problem_markdown must not be blank")
        if payload.pipeline not in {pipeline.value for pipeline in PipelinePreset}:
            raise HTTPException(status_code=400, detail="unsupported pipeline")

        problem_id = _new_web_problem_id(payload.title)
        problem_path = _write_problem_input(paths.project_root, problem_id, payload.problem_markdown)
        web_run_dir = _web_run_dir(paths.project_root, problem_id)
        _write_web_status(
            web_run_dir,
            {
                "run_id": problem_id,
                "status": "queued",
                "pipeline": payload.pipeline,
                "problem": {"problem_id": problem_id, "problem_path": str(problem_path), "title": payload.title},
            },
        )
        start_launch_thread(
            problem_id=problem_id,
            problem_path=str(problem_path),
            title=payload.title,
            config_path=config_path,
            pipeline=payload.pipeline,
        )
        return JSONResponse(
            status_code=202,
            content={
                "run_id": problem_id,
                "problem_id": problem_id,
                "problem_path": str(problem_path),
                "status": "queued",
                "pipeline": payload.pipeline,
            },
        )

    @app.get("/api/runs/{run_id}")
    def get_run(run_id: str) -> dict[str, Any]:
        try:
            return read_run_snapshot(config.run_root_path, run_id, project_root=paths.project_root)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail="run not found") from exc

    return app


app = create_app()
