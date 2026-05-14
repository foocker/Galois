"""Galois-owned runner for the mathematical paper writing agent."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import subprocess
import sys
from datetime import datetime, timezone

from galois.platform.config import DEFAULT_MODEL


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def vendored_writing_dir(repo_root: Path | None = None) -> Path:
    root = repo_root or _repo_root()
    return root / "three_horse" / "writing"


def _bool_false(value: str) -> bool:
    return value in {"0", "false", "False", "no", "No"}


def _project_id(writing_file: str) -> str:
    stem = Path(writing_file).stem
    normalized = re.sub(r"[^a-zA-Z0-9_-]+", "-", stem).strip("-")
    return normalized or "paper-project"


def _resolve_input_path(*, asset_root: Path, writing_file: str) -> tuple[str, Path]:
    candidate = Path(writing_file)
    if candidate.is_absolute():
        resolved = candidate.resolve()
        return resolved.as_posix(), resolved
    return candidate.as_posix(), (asset_root / candidate).resolve()


def _ensure_runtime_workspace(runtime_root: Path) -> Path:
    runtime_root.mkdir(parents=True, exist_ok=True)
    for relative in ("results", "memory", "citations", "downloads"):
        (runtime_root / relative).mkdir(parents=True, exist_ok=True)
    return runtime_root


def _read_session_id(session_file: Path) -> str:
    if session_file.exists() and session_file.stat().st_size > 0:
        return session_file.read_text(encoding="utf-8").strip()
    return ""


def _extract_session_id(output: str) -> str:
    matches = re.findall(r"session id: ([0-9a-f-]+)", output, flags=re.IGNORECASE)
    return matches[-1] if matches else ""


def _resolve_mode(
    *,
    resume: str,
    session_file: Path,
    codex_root: Path,
    runtime_root: Path,
    initial_prompt: str,
    resume_prompt: str,
) -> tuple[str, str, list[str], str]:
    session_id = _read_session_id(session_file)
    mode = "new"
    prompt = initial_prompt
    codex_args: list[str] = []

    if _bool_false(resume):
        mode = "new-forced"
    elif resume in {"last", "LAST"}:
        mode = "resume-last"
        prompt = resume_prompt
        codex_args = ["exec", "resume", "--last"]
    elif resume in {"auto", ""} and session_id:
        mode = "resume"
        prompt = resume_prompt
        codex_args = ["exec", "resume", session_id]
    elif resume not in {"auto", ""}:
        mode = "resume"
        session_id = resume
        prompt = resume_prompt
        codex_args = ["exec", "resume", session_id]

    if not codex_args:
        codex_args = ["exec", "-C", str(codex_root)]
        if runtime_root != codex_root:
            codex_args.extend(["--add-dir", str(runtime_root)])
    return mode, prompt, codex_args, session_id


def _build_prompts(
    *,
    writing_file: str,
    absolute_writing_file: Path,
    asset_root: Path,
    runtime_root: Path,
    project_id: str,
    results_dir: Path,
    memory_dir: Path,
    citations_dir: Path,
    downloads_dir: Path,
    log_dir: Path,
) -> tuple[str, str]:
    project_dir = results_dir / project_id
    runtime_scope = (
        f"Run-local output dirs: RESULTS_DIR={results_dir}, MEMORY_DIR={memory_dir}, "
        f"CITATIONS_DIR={citations_dir}, DOWNLOADS_DIR={downloads_dir}, LOG_DIR={log_dir}. "
        f"Write all required artifacts under {project_dir}. Static protocol assets stay under {asset_root}; "
        f"do not copy reference repositories into {runtime_root}."
    )
    input_scope = ""
    try:
        absolute_writing_file.relative_to(asset_root)
    except ValueError:
        input_scope = (
            f" Allowed external input for this run: {absolute_writing_file}. Read it directly even though it is outside "
            f"{asset_root}, and do not duplicate it into the output tree except as quoted user-provided draft material when needed."
        )
    artifact_contract = (
        f"Primary deliverables must be written to {project_dir}: "
        "`manuscript_draft.md`, `review_report.md`, `citation_report.md`, `revision_tasks.json`, and `export_bundle.json`. "
        "Use English only. Preserve mathematical claims. Do not invent citations. Do not claim a proof is correct; report inspected risks. "
        "Treat the input `Requested Work` as the primary objective. The `Draft`, `References`, and `Reviewer Comments` sections are materials, "
        "not fixed modes; use any provided writing parameters for reference-count targets, page-count targets, and self-review revision rounds. "
        "Make `citation_report.md` begin with `# References` and a numbered list of verified references; put missing, unused, or lookup-only items later under `## Citation Audit`. "
        "Use `$math-paper-writing`, `$math-review`, and `$literature-citation` as appropriate. "
        "The final response may be brief, but the files must contain the substantive work."
    )
    initial_prompt = (
        f"Use AGENTS.md to run the Galois Paper Writing workflow for {writing_file}. "
        f"Project_id: {project_id}. {runtime_scope}{input_scope} {artifact_contract}"
    )
    resume_prompt = (
        f"Continue the Galois Paper Writing workflow for {writing_file}. "
        f"Project_id: {project_id}. First inspect existing artifacts under {project_dir}, then finish missing or incomplete artifacts. "
        f"{runtime_scope}{input_scope} {artifact_contract}"
    )
    return initial_prompt, resume_prompt


def _write_summary_log(
    *,
    log_file: Path,
    writing_file: str,
    mode: str,
    asset_root: Path,
    runtime_root: Path,
    session_id: str,
    exit_code: int,
    project_dir: Path,
    output: str,
) -> None:
    artifact_names = (
        "manuscript_draft.md",
        "review_report.md",
        "citation_report.md",
        "revision_tasks.json",
        "export_bundle.json",
    )
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(f"asset_root: {asset_root}\n")
        handle.write(f"runtime_root: {runtime_root}\n")
        handle.write(f"writing_file: {writing_file}\n")
        handle.write(f"mode: {mode}\n")
        if session_id:
            handle.write(f"session_id: {session_id}\n")
        handle.write(f"exit_code: {exit_code}\n")
        handle.write(f"project_dir: {project_dir}\n")
        for name in artifact_names:
            handle.write(f"{name}: {'present' if (project_dir / name).exists() else 'missing'}\n")
        tail = [line.rstrip() for line in output.splitlines() if line.strip()][-40:]
        if tail:
            handle.write("\n## transcript tail\n")
            for line in tail:
                handle.write(f"{line}\n")


def run_writing_project(
    *,
    repo_root: Path | None = None,
    workdir: Path | None = None,
    env: dict[str, str] | None = None,
) -> int:
    root = repo_root or _repo_root()
    runtime_env = os.environ.copy()
    if env:
        runtime_env.update(env)

    asset_root = (workdir or vendored_writing_dir(root)).resolve()
    runtime_root = Path(runtime_env.get("GALOIS_WRITING_RUNTIME_DIR", str(asset_root))).resolve()
    writing_file, absolute_writing_file = _resolve_input_path(
        asset_root=asset_root,
        writing_file=runtime_env.get("WRITING_FILE", "data/example.md"),
    )
    project_id = runtime_env.get("GALOIS_WRITING_PROJECT_ID", _project_id(writing_file))
    runtime_root = _ensure_runtime_workspace(runtime_root)
    results_dir = Path(runtime_env.get("RESULTS_DIR", str(runtime_root / "results")))
    memory_dir = Path(runtime_env.get("MEMORY_DIR", str(runtime_root / "memory")))
    citations_dir = Path(runtime_env.get("CITATIONS_DIR", str(runtime_root / "citations")))
    downloads_dir = Path(runtime_env.get("DOWNLOADS_DIR", str(runtime_root / "downloads")))
    log_dir = Path(runtime_env.get("LOG_DIR", str(runtime_root / "logs")))
    session_file = Path(runtime_env.get("SESSION_FILE", str(log_dir / f"{project_id}.session")))
    model = runtime_env.get("MODEL", DEFAULT_MODEL)
    reasoning_effort = runtime_env.get("REASONING_EFFORT", "high")
    resume = runtime_env.get("RESUME", "auto")
    codex_bin = runtime_env.get("CODEX_BIN", "codex")

    if not absolute_writing_file.exists():
        raise FileNotFoundError(f"Writing input file not found: {absolute_writing_file}")

    runtime_env["GALOIS_WRITING_RUNTIME_DIR"] = str(runtime_root)
    runtime_env["GALOIS_WRITING_WORKDIR"] = str(asset_root)
    runtime_env["GALOIS_WRITING_ASSET_DIR"] = str(asset_root)
    runtime_env["WRITING_FILE"] = writing_file
    runtime_env["GALOIS_WRITING_PROJECT_ID"] = project_id
    runtime_env.setdefault("RESULTS_DIR", str(results_dir))
    runtime_env.setdefault("MEMORY_DIR", str(memory_dir))
    runtime_env.setdefault("CITATIONS_DIR", str(citations_dir))
    runtime_env.setdefault("DOWNLOADS_DIR", str(downloads_dir))

    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"{project_id}.md"
    project_dir = results_dir / project_id

    initial_prompt, resume_prompt = _build_prompts(
        writing_file=writing_file,
        absolute_writing_file=absolute_writing_file,
        asset_root=asset_root,
        runtime_root=runtime_root,
        project_id=project_id,
        results_dir=results_dir,
        memory_dir=memory_dir,
        citations_dir=citations_dir,
        downloads_dir=downloads_dir,
        log_dir=log_dir,
    )
    mode, prompt, codex_args, resume_id = _resolve_mode(
        resume=resume,
        session_file=session_file,
        codex_root=asset_root,
        runtime_root=runtime_root,
        initial_prompt=initial_prompt,
        resume_prompt=resume_prompt,
    )

    print(f"Running writing project {writing_file} -> {log_file}")
    print(f"Mode: {mode}")
    if resume_id:
        print(f"Session: {resume_id}")

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write("\n")
        handle.write(f"===== galois.writing.runner {timestamp} =====\n")

    command = [
        codex_bin,
        *codex_args,
        "-m",
        model,
        "--config",
        f'model_reasoning_effort="{reasoning_effort}"',
        "--dangerously-bypass-approvals-and-sandbox",
        "-",
    ]
    process = subprocess.Popen(
        command,
        cwd=str(runtime_root),
        env=runtime_env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    if process.stdin is not None:
        try:
            process.stdin.write(prompt)
            if not prompt.endswith("\n"):
                process.stdin.write("\n")
        except BrokenPipeError:
            pass
        finally:
            process.stdin.close()

    output_chunks: list[str] = []
    assert process.stdout is not None
    for chunk in process.stdout:
        print(chunk, end="")
        output_chunks.append(chunk)
    completed = int(process.wait())
    output = "".join(output_chunks)

    new_session_id = _extract_session_id(output)
    effective_session_id = new_session_id or resume_id
    if new_session_id:
        session_file.parent.mkdir(parents=True, exist_ok=True)
        session_file.write_text(f"{new_session_id}\n", encoding="utf-8")
        print(f"Saved session id -> {session_file}")
    else:
        print("No session id found in output; session file unchanged.", file=sys.stderr)

    _write_summary_log(
        log_file=log_file,
        writing_file=writing_file,
        mode=mode,
        asset_root=asset_root,
        runtime_root=runtime_root,
        session_id=effective_session_id,
        exit_code=completed,
        project_dir=project_dir,
        output=output,
    )
    if completed == 0:
        print(f"Finished writing project {writing_file} -> {project_dir}")
    else:
        print(f"Writing run failed with exit code {completed}; log: {log_file}", file=sys.stderr)
    return completed


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the Galois Paper Writing adapter.")
    parser.add_argument("--repo-root", type=Path, default=_repo_root())
    parser.add_argument("--workdir", type=Path, default=None)
    args = parser.parse_args()
    return run_writing_project(
        repo_root=args.repo_root.resolve(),
        workdir=args.workdir.resolve() if args.workdir else None,
    )


if __name__ == "__main__":
    raise SystemExit(main())
