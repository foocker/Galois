#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROBLEM_FILE="${PROBLEM_FILE:-data/example.md}"
LOG_DIR="${LOG_DIR:-$ROOT_DIR/logs/example}"
RESULTS_DIR="${RESULTS_DIR:-$ROOT_DIR/results}"
MODEL="${MODEL:-gpt-5.4}"
REASONING_EFFORT="${REASONING_EFFORT:-xhigh}"
RESUME="${RESUME:-auto}"

if [[ ! -f "$ROOT_DIR/$PROBLEM_FILE" ]]; then
  echo "Problem file not found: $ROOT_DIR/$PROBLEM_FILE" >&2
  exit 1
fi

mkdir -p "$LOG_DIR"

problem_id="$(basename "$PROBLEM_FILE" .md)"
log_file="$LOG_DIR/${problem_id}.md"
session_file="${SESSION_FILE:-$LOG_DIR/${problem_id}.session}"
tmp_output="$(mktemp)"
trap 'rm -f "$tmp_output"' EXIT

open_problem_guard="Open Problem Research Protocol enforcement: if the problem is open or a frontier fails, do not produce a terminal status report, do not stop at an honest-conclusion summary, and immediately select the next frontier with a concrete research action unless blueprint_verified.md has already been produced. Maintain results/${problem_id}/blueprint.md as a living research ledger/research checkpoint even before verification; record substantial partial progress, failed frontiers, experiment paths, and the next exact action there."
initial_prompt="Use AGENTS.md exactly to solve the math problem in ${PROBLEM_FILE}. Before downloading papers, inspect downloads/${problem_id}/ and reuse existing local files when they are relevant. ${open_problem_guard}"
resume_prompt="Continue solving the math problem in ${PROBLEM_FILE}. Use AGENTS.md exactly. First inspect memory/${problem_id}/ and downloads/${problem_id}/, then continue from the existing proof state without repeating searches or downloads unless the prior artifacts are insufficient. ${open_problem_guard}"

resume_id="${CODEX_SESSION_ID:-}"
mode="new"
prompt="$initial_prompt"
codex_args=()

case "$RESUME" in
  0|false|False|no|No)
    mode="new-forced"
    ;;
  last|LAST)
    mode="resume-last"
    prompt="$resume_prompt"
    codex_args=(exec resume --last)
    ;;
  auto|"")
    if [[ -z "$resume_id" && -s "$session_file" ]]; then
      resume_id="$(tr -d '[:space:]' < "$session_file")"
    fi
    if [[ -n "$resume_id" ]]; then
      mode="resume"
      prompt="$resume_prompt"
      codex_args=(exec resume "$resume_id")
    fi
    ;;
  *)
    if [[ -z "$resume_id" ]]; then
      resume_id="$RESUME"
    fi
    mode="resume"
    prompt="$resume_prompt"
    codex_args=(exec resume "$resume_id")
    ;;
esac

if [[ ${#codex_args[@]} -eq 0 ]]; then
  codex_args=(exec -C "$ROOT_DIR")
fi

echo "Running ${PROBLEM_FILE} -> $log_file"
echo "Mode: $mode"
if [[ -n "$resume_id" ]]; then
  echo "Session: $resume_id"
fi

{
  echo
  echo "===== run_example_resume $(date -u +%Y-%m-%dT%H:%M:%SZ) ====="
  echo "problem_file: $PROBLEM_FILE"
  echo "mode: $mode"
  if [[ -n "$resume_id" ]]; then
    echo "resume_session_id: $resume_id"
  fi
} >>"$log_file"

set +e
(
  cd "$ROOT_DIR"
  codex "${codex_args[@]}" \
    -m "$MODEL" \
    --config "model_reasoning_effort=\"$REASONING_EFFORT\"" \
    --dangerously-bypass-approvals-and-sandbox \
    "$prompt"
) 2>&1 | tee -a "$log_file" | tee "$tmp_output"
status=${PIPESTATUS[0]}
set -e

new_session_id="$(
  grep -Eio 'session id: [0-9a-f-]+' "$tmp_output" | tail -n 1 | awk '{print $3}' || true
)"
if [[ -n "$new_session_id" ]]; then
  printf '%s\n' "$new_session_id" >"$session_file"
  echo "Saved session id -> $session_file"
else
  echo "No session id found in output; session file unchanged." >&2
fi

if [[ "$status" -ne 0 ]]; then
  echo "Run failed with exit code $status; log: $log_file" >&2
  exit "$status"
fi

verified_artifact="$RESULTS_DIR/${problem_id}/blueprint_verified.md"
if [[ -f "$verified_artifact" ]]; then
  echo "Finished ${PROBLEM_FILE} -> $log_file"
  echo "Verified artifact: $verified_artifact"
else
  echo "Stopped without verified result for ${PROBLEM_FILE}; resume again to continue. Log: $log_file"
fi
