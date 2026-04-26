# Verification Assets

This directory contains the Rethlas-derived natural-language proof verification runtime assets used by Galois.

Kept here:

- `AGENTS.md` for the verifier protocol.
- `.codex/` for Codex configuration.
- `.agents/skills/` for verification skills copied from `Rethlas/agents/verification`.
- `mcp/` for verifier tools exposed to the agent.
- `schemas/` for verification output contracts.
- `api/server.py` as a compatibility entrypoint that re-exports `galois.verification.service`.
- `scripts/` and `tests/` for upstream-compatible debugging and quick checks.

Do not keep here:

- `.venv/`, `__pycache__/`, `.pytest_cache/`, or compiled Python files.
- `logs/`, `results/`, `memory/`, `downloads/`, or `.session` files.
- Ad hoc verifier output artifacts unless they are part of a named benchmark fixture.
