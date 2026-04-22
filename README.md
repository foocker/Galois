# Galois

Galois is a new math-agent workspace that separates:

- `platform/`: project/session/runtime/workflow control
- `lean_executor/`: Lean formalization execution
- `reasoning/`: natural-language mathematical reasoning
- `verification/`: proof checking and repair feedback

The initial goal is not to merge existing repositories directly. Instead, this
repository will define clean interfaces, run comparative experiments, and only
keep components that show clear value on benchmark problem sets.

## Principles

- Keep upstream repositories separate during early development.
- Rebuild the control/runtime layer cleanly instead of copying shell-heavy
  orchestration.
- Absorb useful workflow and prompt ideas from prior systems only after
  ablation and benchmarking.
- Optimize for experimentation, replay, and component replacement.

## Initial Layout

```text
platform/        runtime, sessions, workflows, adapters
lean_executor/   Lean task execution and formalization loops
reasoning/       blueprint generation and math research workflows
verification/    proof checking, verdicts, repair hints
benchmarks/      problem sets, configs, run manifests, reports
configs/         system and experiment configuration
prompts/         prompt assets promoted into Galois
skills/          reusable workflow skills promoted into Galois
scripts/         developer and experiment entry scripts
docs/            architecture and design notes
```

## Near-Term Plan

1. Define artifact contracts between `reasoning`, `verification`, and
   `lean_executor`.
2. Build experiment-friendly runners and result capture in `platform`.
3. Add small benchmark sets before introducing any heavy workflow logic.
4. Import only the minimum proven-useful ideas from prior systems.
