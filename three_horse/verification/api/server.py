"""Compatibility entrypoint for the internalized Galois verification service."""

from __future__ import annotations

from galois.verification.service import (  # noqa: F401
    VerifyRequest,
    app,
    build_codex_command,
    build_prompt,
    generate_run_id,
    health,
    normalize_reasoning_effort,
    run_codex_verification,
    verify,
)
