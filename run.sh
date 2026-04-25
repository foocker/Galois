#!/usr/bin/env sh
set -eu

command="${1:-web}"
shift || true

show_help() {
  cat <<'HELP'
Galois local entrypoint

Usage:
  sh run.sh                 Start the research workbench web UI
  sh run.sh web             Start the research workbench web UI
  sh run.sh reasoning       Run the default reasoning-only example
  sh run.sh verify          Run the default reasoning + verification example
  sh run.sh plan            Plan the default example without launching workflows
  sh run.sh suite           List the local smoke suite
  sh run.sh inspect RUN_ID  Inspect a run id or run directory

Environment overrides:
  HOST=127.0.0.1 PORT=8000 sh run.sh web
  PROBLEM_ID=example PROBLEM_PATH=three_horse/reasoning/data/example.md sh run.sh reasoning
HELP
}

case "$command" in
  web)
    uv run galois-run web \
      --host "${HOST:-127.0.0.1}" \
      --port "${PORT:-8000}"
    ;;
  reasoning|reasoning-only)
    uv run galois-run launch-run \
      --problem-id "${PROBLEM_ID:-cap-set-problem}" \
      --problem-path "${PROBLEM_PATH:-benchmarks/problems/finite_fields/cap set problem.md}" \
      --pipeline reasoning-only
    ;;
  verify|reasoning-verification)
    uv run galois-run launch-run \
      --problem-id "${PROBLEM_ID:-example}" \
      --problem-path "${PROBLEM_PATH:-three_horse/reasoning/data/example.md}" \
      --pipeline reasoning-verification
    ;;
  plan)
    uv run galois-run plan-run \
      --problem-id "${PROBLEM_ID:-example}" \
      --problem-path "${PROBLEM_PATH:-three_horse/reasoning/data/example.md}" \
      --pipeline "${PIPELINE:-reasoning-verification}"
    ;;
  suite)
    uv run galois-run suite list
    ;;
  inspect)
    if [ "$#" -lt 1 ]; then
      echo "Usage: sh run.sh inspect RUN_ID_OR_PATH" >&2
      exit 2
    fi
    uv run galois-run inspect-run "$1"
    ;;
  help|-h|--help)
    show_help
    ;;
  *)
    echo "Unknown command: $command" >&2
    show_help >&2
    exit 2
    ;;
esac
