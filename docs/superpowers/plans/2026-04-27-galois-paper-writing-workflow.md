# Galois Paper Writing Workflow Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first executable Galois Paper Writing workflow from the three retained reference libraries.

**Architecture:** Keep `references/` as source snapshots and create a runtime agent asset under `three_horse/writing/`. Add a `galois.writing.runner` adapter that launches the writing agent and archives manuscript, review, citation, and revision artifacts into run-local `writing/` directories. Wire the platform and Web API to this workflow without making it depend on Galois reasoning runs.

**Tech Stack:** Python dataclasses/FastAPI, existing Galois workflow launcher, Codex CLI agent assets, Markdown/JSON artifacts.

---

## Chunk 1: Runtime Writing Agent Assets

**Files:**
- Create: `three_horse/writing/AGENTS.md`
- Create: `three_horse/writing/ASSET_MANIFEST.md`
- Create: `three_horse/writing/.agents/skills/math-paper-writing/SKILL.md`
- Create: `three_horse/writing/.agents/skills/math-review/SKILL.md`
- Create: `three_horse/writing/.agents/skills/literature-citation/SKILL.md`
- Create: `three_horse/writing/data/example.md`

- [ ] **Step 1: Create agent contract**

Define input, output, memory, and artifact rules for independent mathematical paper writing.

- [ ] **Step 2: Add three runtime skills**

Condense the three reference libraries into writing, review, and literature/citation skills.

- [ ] **Step 3: Add example writing input**

Provide a small Markdown example for tests and manual runs.

## Chunk 2: Python Runner and Platform Wiring

**Files:**
- Create: `src/galois/writing/__init__.py`
- Create: `src/galois/writing/runner.py`
- Modify: `src/galois/platform/config.py`
- Modify: `src/galois/platform/paths.py`
- Modify: `src/galois/platform/contracts.py`
- Modify: `src/galois/platform/workflows.py`
- Modify: `src/galois/platform/cli.py`
- Modify: `configs/defaults.toml`

- [ ] **Step 1: Add config and path support**

Add a `writing` workflow area and `writing_dir` path.

- [ ] **Step 2: Add workflow kind and launch builder**

Add `WorkflowKind.WRITING` and a `build_writing_launch` function.

- [ ] **Step 3: Add runner**

Implement `galois.writing.runner` to launch Codex with the writing agent contract and write run artifacts.

- [ ] **Step 4: Prepare writing workspace**

Create run-local `writing/workspace/{results,memory,citations,downloads}`.

## Chunk 3: Web API and Verification

**Files:**
- Modify: `src/galois/platform/web.py`
- Modify: `src/galois/platform/web_assets/index.html`
- Modify: `src/galois/platform/web_assets/app.js`
- Modify: `src/galois/platform/web_assets/styles.css`
- Modify: `tests/test_platform_launch.py`
- Modify: `tests/test_web_app.py`
- Modify: `tests/test_asset_integrity.py`

- [ ] **Step 1: Add Paper Writing API**

Add an endpoint that creates an independent writing project run and starts the writing workflow.

- [ ] **Step 2: Replace placeholder UI**

Create a first usable Paper Writing page with project inputs, local actions, and status output.

- [ ] **Step 3: Add tests**

Test asset presence, workflow launch construction, and API payload creation.

- [ ] **Step 4: Run focused tests**

Run `pytest tests/test_platform_launch.py tests/test_web_app.py tests/test_asset_integrity.py`.
