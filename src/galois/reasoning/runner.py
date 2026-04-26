"""Galois-owned runner for the Rethlas natural-language reasoning agent."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import subprocess
import sys
from datetime import datetime, timezone
from typing import TextIO


OPEN_PROBLEM_GUARD = (
    "Open Problem Research Protocol enforcement: if the problem is open or a frontier fails, "
    "do not produce a terminal status report, do not stop at an honest-conclusion summary, "
    "and immediately select the next frontier with a concrete research action unless "
    "blueprint_verified.md has already been produced. Maintain results/{problem_id}/blueprint.md "
    "as a living research ledger/research checkpoint even before verification; record substantial "
    "partial progress, failed frontiers, experiment paths, and the next exact action there."
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def vendored_reasoning_dir(repo_root: Path | None = None) -> Path:
    root = repo_root or _repo_root()
    return root / "three_horse" / "reasoning"


def _bool_false(value: str) -> bool:
    return value in {"0", "false", "False", "no", "No"}


def _problem_id(problem_file: str) -> str:
    return Path(problem_file).stem


def _read_session_id(session_file: Path) -> str:
    if session_file.exists() and session_file.stat().st_size > 0:
        return session_file.read_text(encoding="utf-8").strip()
    return ""


def _ensure_runtime_workspace(*, runtime_root: Path) -> Path:
    runtime_root.mkdir(parents=True, exist_ok=True)
    for relative in ("results", "memory"):
        (runtime_root / relative).mkdir(parents=True, exist_ok=True)
    return runtime_root


def _resolve_problem_path(*, asset_root: Path, problem_file: str) -> tuple[str, Path]:
    candidate = Path(problem_file)
    if candidate.is_absolute():
        resolved = candidate.resolve()
        return resolved.as_posix(), resolved
    return candidate.as_posix(), (asset_root / candidate).resolve()


def _build_problem_scope(*, absolute_problem_file: Path, asset_root: Path, problem_file: str) -> str:
    try:
        absolute_problem_file.relative_to(asset_root)
    except ValueError:
        return (
            f" Allowed external input for this run: {problem_file}. Read it directly even though it is outside "
            f"{asset_root}, and do not duplicate it into the run-local output tree."
        )
    return ""


def _downloads_reuse_guidance(downloads_problem_dir: Path) -> str:
    return (
        f"If {downloads_problem_dir} exists, inspect it before downloading papers and reuse existing local files when they are relevant. "
    )


def _downloads_resume_guidance(memory_problem_dir: Path, downloads_problem_dir: Path) -> str:
    return (
        f"First inspect {memory_problem_dir}. If {downloads_problem_dir} exists, inspect it too, then continue from the existing proof state "
        "without repeating searches or downloads unless the prior artifacts are insufficient. "
    )


def _build_verifying_prompts(
    *,
    problem_file: str,
    downloads_problem_dir: Path,
    memory_problem_dir: Path,
    runtime_scope: str,
    blueprint_contract: str,
    verification_contract: str,
    problem_scope: str,
    repair_input_file: str,
    verification_guard: str,
) -> tuple[str, str]:
    verification_focus = (
        " Use English only for all reasoning, search queries, notes, proof drafts, and final artifacts in this workflow, even if the original problem statement was written in another language. "
        " Platform-managed verification is enabled for this run. Prioritize producing concrete mathematical artifacts first: subgoals, proof steps, and a complete draft in `blueprint.md`. "
        "Do not spend long stretches on meta-discussion about interpretation, workflow policy, artifact naming, or whether to verify. "
        "Do not emit repeated planning blocks or repeated `I'm thinking`-style self-commentary. "
        "Do not call `verify_proof_service` or invoke `$verify-proof`. The platform will verify `blueprint.md` after this reasoning pass. "
    )
    initial_prompt = (
        f"Use AGENTS.md exactly to solve the math problem in {problem_file}. "
        + _downloads_reuse_guidance(downloads_problem_dir)
    )
    resume_prompt = (
        f"Continue solving the math problem in {problem_file}. Use AGENTS.md exactly. "
        + _downloads_resume_guidance(memory_problem_dir, downloads_problem_dir)
    )
    if repair_input_file:
        repair_suffix = (
            f" Before taking a new step, read the repair contract at {repair_input_file} "
            "and revise the current blueprint using its verification feedback."
        )
    else:
        repair_suffix = ""
    return (
        (
            initial_prompt
            + f"{runtime_scope}{blueprint_contract}{verification_focus}{verification_contract}{problem_scope} {verification_guard}"
            + repair_suffix
        ),
        (
            resume_prompt
            + f"{runtime_scope}{blueprint_contract}{verification_focus}{verification_contract}{problem_scope} {verification_guard}"
            + repair_suffix
        ),
    )


def _build_reasoning_only_prompts(
    *,
    problem_file: str,
    downloads_problem_dir: Path,
    memory_problem_dir: Path,
    runtime_scope: str,
    blueprint_contract: str,
    problem_scope: str,
    repair_input_file: str,
) -> tuple[str, str]:
    strict_contract = (
        " Use English only for all reasoning, search queries, notes, proof drafts, and final artifacts in this workflow, even if the original problem statement was written in another language. "
        " Strict reasoning-only mode for this run. Do not call `verify_proof_service` or invoke `$verify-proof`. "
        "Ignore any AGENTS.md instruction whose purpose is proof verification, verification repair, or waiting for a second verified artifact. "
        "Use AGENTS.md only for the reasoning workflow: problem reading, memory updates, search, decomposition, proof development, and writing the final blueprint. "
        "Do not create empty `downloads/{problem_id}` or `scripts/{problem_id}` directories just to satisfy path conventions. "
        "Create `downloads/{problem_id}` only when a file is actually downloaded, and create `scripts/{problem_id}` only when a reusable script artifact is actually written. "
        "Finish the reasoning stage by producing the best complete `blueprint.md` you can. No downstream verifier or formalizer should be assumed in this run."
    )
    initial_prompt = (
        f"Solve the math problem in {problem_file} using the local AGENTS.md reasoning workflow. "
        + _downloads_reuse_guidance(downloads_problem_dir)
        + f"{runtime_scope}{blueprint_contract}{strict_contract}{problem_scope}"
    )
    resume_prompt = (
        f"Continue solving the math problem in {problem_file} using the local AGENTS.md reasoning workflow. "
        + _downloads_resume_guidance(memory_problem_dir, downloads_problem_dir)
        + f"{runtime_scope}{blueprint_contract}{strict_contract}{problem_scope}"
    )
    if repair_input_file:
        repair_suffix = (
            f" If a repair contract is present at {repair_input_file}, treat it only as mathematical feedback for improving "
            "the current `blueprint.md`; do not treat it as a requirement to start any verification loop."
        )
        initial_prompt += repair_suffix
        resume_prompt += repair_suffix
    return initial_prompt, resume_prompt


def _build_prompts(
    problem_file: str,
    repair_input_file: str,
    *,
    absolute_problem_file: Path,
    asset_root: Path,
    runtime_root: Path,
    problem_id: str,
    results_dir: Path,
    memory_dir: Path,
    downloads_dir: Path,
    scripts_dir: Path,
    log_dir: Path,
    verification_enabled: bool,
    verification_mode: str,
) -> tuple[str, str]:
    guard = OPEN_PROBLEM_GUARD.format(problem_id=problem_id)
    runtime_scope = (
        f"Run-local output dirs: RESULTS_DIR={results_dir}, MEMORY_DIR={memory_dir}, DOWNLOADS_DIR={downloads_dir}, "
        f"SCRIPTS_DIR={scripts_dir}, LOG_DIR={log_dir}. Treat these as the targets for results/, memory/, downloads/, "
        f"scripts/experiments/, and logs/ in AGENTS.md. Write proof artifacts under {results_dir / problem_id}/ and "
        f"memory artifacts under {memory_dir / problem_id}/. Static protocol assets stay under {asset_root}; do not copy them "
        f"into {runtime_root}."
    )
    blueprint_contract = (
        f" The primary deliverable for this run is {results_dir / problem_id / 'blueprint.md'}. "
        "Write it as a polished, self-contained final document, not a lab notebook. "
        "It must integrate the original problem statement and the complete solution in one coherent markdown artifact. "
        "Use this integrated top-level structure: `# Title`, then `## Problem`, then `## Solution`. "
        "Inside `## Solution`, organize substantial arguments with mathematical subsections such as `### Lemma`, `#### Proof`, `### Proposition`, `### Claim`, or `### Main Theorem` when they materially improve clarity or traceability. "
        "Do not start new top-level `#` sections for intermediate results; keep all lemmas, propositions, and the final theorem nested inside `## Solution`. "
        "If you rely on a theorem or lemma found in a search library, state it clearly in the solution and record its exact source identifier in the same subsection so the result remains traceable. "
        "Do not force an over-short single-block proof when the argument naturally needs intermediate results. "
        "When writing LaTeX math in markdown, use `$...$` for inline math and `$$...$$` for display math; do not use `\\(...\\)` or `\\[...\\]`. "
        "The file must contain only the final mathematical exposition, with no workflow log, checkpoint, status note, failed-path diary, experiment journal, or next-step planning anywhere in blueprint.md."
    )
    problem_scope = _build_problem_scope(
        absolute_problem_file=absolute_problem_file,
        asset_root=asset_root,
        problem_file=problem_file,
    )
    if verification_enabled:
        if verification_mode == "external":
            verification_contract = (
                " The platform will verify `blueprint.md` after this reasoning pass and handle any repair loop. "
                "Keep `blueprint.md` readable as a finished mathematical writeup even before platform verification runs. "
                "Do not wait for or publish a second verified artifact from inside the reasoning agent."
            )
            verification_guard = ""
        else:
            verification_contract = (
                " Verification is enabled for this run. You may call `verify_proof_service` when and only when a full proof draft "
                f"has been assembled in {results_dir / problem_id / 'blueprint.md'}. If verification succeeds, publish "
                f"{results_dir / problem_id / 'blueprint_verified.md'}. Keep blueprint.md readable as a finished mathematical writeup even before verification."
            )
            verification_guard = guard
        return _build_verifying_prompts(
            problem_file=problem_file,
            downloads_problem_dir=downloads_dir / problem_id,
            memory_problem_dir=memory_dir / problem_id,
            runtime_scope=runtime_scope,
            blueprint_contract=blueprint_contract,
            verification_contract=verification_contract,
            problem_scope=problem_scope,
            repair_input_file=repair_input_file,
            verification_guard=verification_guard,
        )
    return _build_reasoning_only_prompts(
        problem_file=problem_file,
        downloads_problem_dir=downloads_dir / problem_id,
        memory_problem_dir=memory_dir / problem_id,
        runtime_scope=runtime_scope,
        blueprint_contract=blueprint_contract,
        problem_scope=problem_scope,
        repair_input_file=repair_input_file,
    )


def _resolve_mode(
    *,
    resume: str,
    session_file: Path,
    codex_root: Path,
    runtime_root: Path,
    code_session_id: str,
    initial_prompt: str,
    resume_prompt: str,
) -> tuple[str, str, list[str], str]:
    resume_id = code_session_id
    mode = "new"
    prompt = initial_prompt
    codex_args: list[str] = []

    if _bool_false(resume):
        mode = "new-forced"
    elif resume == "last" or resume == "LAST":
        mode = "resume-last"
        prompt = resume_prompt
        codex_args = ["exec", "resume", "--last"]
    elif resume == "auto" or resume == "":
        if not resume_id:
            resume_id = _read_session_id(session_file)
        if resume_id:
            mode = "resume"
            prompt = resume_prompt
            codex_args = ["exec", "resume", resume_id]
    else:
        if not resume_id:
            resume_id = resume
        mode = "resume"
        prompt = resume_prompt
        codex_args = ["exec", "resume", resume_id]

    if not codex_args:
        codex_args = ["exec", "-C", str(codex_root)]
        if runtime_root != codex_root:
            codex_args.extend(["--add-dir", str(runtime_root)])
    return mode, prompt, codex_args, resume_id


def _extract_session_id(output: str) -> str:
    matches = re.findall(r"session id: ([0-9a-f-]+)", output, flags=re.IGNORECASE)
    return matches[-1] if matches else ""


def _looks_like_user_prompt_line(line: str) -> bool:
    return "AGENTS.md" in line and "blueprint.md" in line and "RESULTS_DIR=" in line


def _compact_transcript_lines(lines: list[str]) -> list[str]:
    compacted: list[str] = []
    index = 0
    while index < len(lines):
        if (
            index + 1 < len(lines)
            and lines[index] == "user"
            and _looks_like_user_prompt_line(lines[index + 1])
        ):
            repeat_count = 1
            scan = index + 2
            while (
                scan + 1 < len(lines)
                and lines[scan] == "user"
                and lines[scan + 1] == lines[index + 1]
            ):
                repeat_count += 1
                scan += 2
            compacted.extend((lines[index], lines[index + 1]))
            if repeat_count > 1:
                compacted.append(f"[repeated {repeat_count - 1} times]")
            index = scan
            continue

        repeat_count = 1
        scan = index + 1
        while scan < len(lines) and lines[scan] == lines[index]:
            repeat_count += 1
            scan += 1
        compacted.append(lines[index])
        if repeat_count > 1:
            compacted.append(f"[repeated {repeat_count - 1} times]")
        index = scan
    return compacted


def _looks_like_meta_reasoning(line: str) -> bool:
    lowered = line.lower()
    return (
        lowered.startswith("i’m thinking")
        or lowered.startswith("i'm thinking")
        or lowered.startswith("i’m considering")
        or lowered.startswith("i'm considering")
        or "workflow policy" in lowered
        or "artifact naming" in lowered
        or lowered.startswith("**planning")
        or lowered.startswith("plan:")
    )


def _has_concrete_progress(*, results_dir: Path, problem_id: str, memory_dir: Path) -> bool:
    if (results_dir / problem_id / "blueprint.md").exists():
        return True
    for channel in ("proof_steps.jsonl", "subgoals.jsonl"):
        path = memory_dir / problem_id / channel
        if path.exists() and path.stat().st_size > 0:
            return True
    return False


def _should_abort_for_stall(
    *,
    verification_enabled: bool,
    stalled_meta_lines: int,
    stall_line_budget: int,
    results_dir: Path,
    problem_id: str,
    memory_dir: Path,
) -> bool:
    if not verification_enabled or stall_line_budget <= 0:
        return False
    if _has_concrete_progress(results_dir=results_dir, problem_id=problem_id, memory_dir=memory_dir):
        return False
    return stalled_meta_lines >= stall_line_budget


def _write_summary_log(
    *,
    log_file: Path,
    problem_file: str,
    mode: str,
    asset_root: Path,
    runtime_root: Path,
    session_id: str,
    exit_code: int,
    verified_artifact: Path,
    output: str,
    verification_enabled: bool,
) -> None:
    compacted_lines = _compact_transcript_lines([line.rstrip() for line in output.splitlines() if line.strip()])
    tail_lines = compacted_lines[-40:]
    if verified_artifact.exists():
        status = "verified"
    elif exit_code == 0:
        status = "succeeded"
    else:
        status = "failed"
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(f"asset_root: {asset_root}\n")
        handle.write(f"runtime_root: {runtime_root}\n")
        handle.write(f"problem_file: {problem_file}\n")
        handle.write(f"mode: {mode}\n")
        handle.write(f"verification_enabled: {verification_enabled}\n")
        if session_id:
            handle.write(f"session_id: {session_id}\n")
        handle.write(f"status: {status}\n")
        handle.write(f"exit_code: {exit_code}\n")
        if verified_artifact.exists():
            handle.write(f"verified_artifact: {verified_artifact}\n")
        handle.write("full_transcript: see sibling stdout_r*.log and stderr_r*.log in this directory\n")
        if tail_lines:
            handle.write("\n## transcript tail\n")
            for line in tail_lines:
                handle.write(f"{line}\n")


def _terminate_process(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=2)


def run_reasoning_resume(
    *,
    repo_root: Path | None = None,
    workdir: Path | None = None,
    env: dict[str, str] | None = None,
) -> int:
    root = repo_root or _repo_root()
    runtime_env = os.environ.copy()
    if env:
        runtime_env.update(env)

    asset_root = (workdir or vendored_reasoning_dir(root)).resolve()
    runtime_root = Path(runtime_env.get("GALOIS_REASONING_RUNTIME_DIR", str(asset_root))).resolve()
    problem_file, absolute_problem_file = _resolve_problem_path(
        asset_root=asset_root,
        problem_file=runtime_env.get("PROBLEM_FILE", "data/example.md"),
    )
    problem_id = runtime_env.get("GALOIS_REASONING_PROBLEM_ID", _problem_id(problem_file))
    runtime_root = _ensure_runtime_workspace(runtime_root=runtime_root)
    log_dir = Path(runtime_env.get("LOG_DIR", str(runtime_root / "logs" / problem_id)))
    results_dir = Path(runtime_env.get("RESULTS_DIR", str(runtime_root / "results")))
    memory_dir = Path(runtime_env.get("MEMORY_DIR", str(runtime_root / "memory")))
    downloads_dir = Path(runtime_env.get("DOWNLOADS_DIR", str(runtime_root / "downloads")))
    scripts_dir = Path(runtime_env.get("SCRIPTS_DIR", str(runtime_root / "scripts")))
    repair_input_file = runtime_env.get("REPAIR_INPUT_FILE", "")
    verification_enabled = not _bool_false(runtime_env.get("GALOIS_REASONING_VERIFICATION_ENABLED", "1"))
    verification_mode = runtime_env.get("GALOIS_REASONING_VERIFICATION_MODE", "agent")
    model = runtime_env.get("MODEL", "gpt-5.4")
    reasoning_effort = runtime_env.get("REASONING_EFFORT", "xhigh")
    resume = runtime_env.get("RESUME", "auto")
    codex_bin = runtime_env.get("CODEX_BIN", "codex")
    stall_line_budget = int(runtime_env.get("GALOIS_REASONING_STALL_LINE_BUDGET", "120"))

    runtime_env["GALOIS_REASONING_RUNTIME_DIR"] = str(runtime_root)
    runtime_env["GALOIS_REASONING_WORKDIR"] = str(asset_root)
    runtime_env["GALOIS_REASONING_ASSET_DIR"] = str(asset_root)
    runtime_env.setdefault("RESULTS_DIR", str(results_dir))
    runtime_env.setdefault("MEMORY_DIR", str(memory_dir))
    runtime_env.setdefault("DOWNLOADS_DIR", str(downloads_dir))
    runtime_env.setdefault("SCRIPTS_DIR", str(scripts_dir))
    runtime_env["PROBLEM_FILE"] = problem_file

    if not absolute_problem_file.exists():
        raise FileNotFoundError(f"Problem file not found: {absolute_problem_file}")
    if repair_input_file and not Path(repair_input_file).exists():
        raise FileNotFoundError(f"Repair input file not found: {repair_input_file}")

    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"{problem_id}.md"
    session_file = Path(runtime_env.get("SESSION_FILE", str(log_dir / f"{problem_id}.session")))

    initial_prompt, resume_prompt = _build_prompts(
        problem_file,
        repair_input_file,
        absolute_problem_file=absolute_problem_file,
        asset_root=asset_root,
        runtime_root=runtime_root,
        problem_id=problem_id,
        results_dir=results_dir,
        memory_dir=memory_dir,
        downloads_dir=downloads_dir,
        scripts_dir=scripts_dir,
        log_dir=log_dir,
        verification_enabled=verification_enabled,
        verification_mode=verification_mode,
    )
    mode, prompt, codex_args, resume_id = _resolve_mode(
        resume=resume,
        session_file=session_file,
        codex_root=asset_root,
        runtime_root=runtime_root,
        code_session_id=runtime_env.get("CODEX_SESSION_ID", ""),
        initial_prompt=initial_prompt,
        resume_prompt=resume_prompt,
    )

    print(f"Running {problem_file} -> {log_file}")
    print(f"Mode: {mode}")
    if resume_id:
        print(f"Session: {resume_id}")

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write("\n")
        handle.write(f"===== galois.reasoning.runner {timestamp} =====\n")

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
    stalled_meta_lines = 0
    stalled_reason = ""
    assert process.stdout is not None
    for chunk in process.stdout:
        print(chunk, end="")
        output_chunks.append(chunk)
        for line in chunk.splitlines():
            if _looks_like_meta_reasoning(line.strip()):
                stalled_meta_lines += 1
            if _should_abort_for_stall(
                verification_enabled=verification_enabled,
                stalled_meta_lines=stalled_meta_lines,
                stall_line_budget=stall_line_budget,
                results_dir=results_dir,
                problem_id=problem_id,
                memory_dir=memory_dir,
            ):
                stalled_reason = "stalled_meta_reasoning: reasoning stalled before producing proof artifacts"
                _terminate_process(process)
                break
        if stalled_reason:
            break
    completed = process.wait()
    output = "".join(output_chunks)
    if stalled_reason and completed == 0:
        completed = 2
        output = f"{output}\n{stalled_reason}\n"

    new_session_id = _extract_session_id(output)
    effective_session_id = new_session_id or resume_id
    if new_session_id:
        session_file.parent.mkdir(parents=True, exist_ok=True)
        session_file.write_text(f"{new_session_id}\n", encoding="utf-8")
        print(f"Saved session id -> {session_file}")
    else:
        print("No session id found in output; session file unchanged.", file=sys.stderr)

    if completed != 0:
        _write_summary_log(
            log_file=log_file,
            problem_file=problem_file,
            mode=mode,
            asset_root=asset_root,
            runtime_root=runtime_root,
            session_id=effective_session_id,
            exit_code=int(completed),
            verified_artifact=results_dir / problem_id / "blueprint_verified.md",
            output=output,
            verification_enabled=verification_enabled,
        )
        if stalled_reason:
            with log_file.open("a", encoding="utf-8") as handle:
                handle.write(f"{stalled_reason}\n")
        print(f"Run failed with exit code {completed}; log: {log_file}", file=sys.stderr)
        return int(completed)

    verified_artifact = results_dir / problem_id / "blueprint_verified.md"
    _write_summary_log(
        log_file=log_file,
        problem_file=problem_file,
        mode=mode,
        asset_root=asset_root,
        runtime_root=runtime_root,
        session_id=effective_session_id,
        exit_code=0,
        verified_artifact=verified_artifact,
        output=output,
        verification_enabled=verification_enabled,
    )
    if verified_artifact.exists():
        print(f"Finished {problem_file} -> {log_file}")
        print(f"Verified artifact: {verified_artifact}")
    else:
        if verification_enabled:
            print(f"Stopped without verified result for {problem_file}; resume again to continue. Log: {log_file}")
        else:
            print(f"Finished {problem_file} -> {log_file}")
            print(f"Blueprint artifact: {results_dir / problem_id / 'blueprint.md'}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the internalized Galois reasoning adapter.")
    parser.add_argument("--repo-root", type=Path, default=_repo_root())
    parser.add_argument("--workdir", type=Path, default=None)
    args = parser.parse_args()
    return run_reasoning_resume(
        repo_root=args.repo_root.resolve(),
        workdir=args.workdir.resolve() if args.workdir else None,
    )


if __name__ == "__main__":
    raise SystemExit(main())
