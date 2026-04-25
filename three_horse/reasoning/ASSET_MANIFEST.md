# Reasoning Assets

This directory contains the Rethlas-derived natural-language proof generation runtime assets used by Galois.

Kept here:

- `AGENTS.md` for the agent protocol and workflow guidance.
- `.codex/` for Codex configuration and subagent definitions.
- `.agents/skills/` for generation skills copied from `Rethlas/agents/generation`.
- `mcp/` for reasoning tools exposed to the agent.
- `scripts/` and `tests/` for upstream-compatible debugging and smoke checks.
- `data/example*.md` for small local examples.

Do not keep here:

- `.venv/`, `__pycache__/`, `.pytest_cache/`, or compiled Python files.
- `logs/`, `results/`, `memory/`, `downloads/`, or `.session` files.
- Large generated datasets unless they are deliberately promoted to benchmark fixtures.
