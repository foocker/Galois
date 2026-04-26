# Galois Research Workbench Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a real FastAPI-backed academic research workbench for submitting Markdown math problems to Galois and reading run artifacts.

**Architecture:** Add a small FastAPI app under `src/galois/platform/web.py` that serves static assets and exposes run APIs backed by the existing run directory contract. The frontend is hand-authored HTML/CSS/JS in `src/galois/platform/web_assets/`, with no Node build step.

**Tech Stack:** Python 3.11, FastAPI, existing Galois control plane, plain HTML/CSS/JavaScript, pytest.

---

## File Structure

- `src/galois/platform/web.py`: FastAPI app, request/response models, run launch background worker, run/artifact readers.
- `src/galois/platform/cli.py`: optional `web` subcommand to start the app with uvicorn.
- `src/galois/platform/web_assets/index.html`: single-page research workbench shell.
- `src/galois/platform/web_assets/styles.css`: academic-calm visual design.
- `src/galois/platform/web_assets/app.js`: submit problem, poll run status, render progress/output.
- `tests/test_web_app.py`: focused tests for validation, status readers, static route, and API behavior that does not require real LLM execution.
- `.impeccable.md`: design context already created.
- `README.md`: short usage note for launching the web workbench.

## Chunk 1: Backend API Skeleton

### Task 1: Add test coverage for app factory and validation

**Files:**
- Create: `tests/test_web_app.py`
- Create: `src/galois/platform/web.py`

- [ ] **Step 1: Write failing tests**
  - Test `GET /` returns the workbench HTML.
  - Test `POST /api/runs` rejects blank Markdown with HTTP 422 or 400.
  - Test artifact helpers choose the latest `reasoning/blueprint_r*.md`.

- [ ] **Step 2: Run focused tests**
  - Run: `uv run pytest tests/test_web_app.py -v`
  - Expected: fail because `galois.platform.web` does not exist.

- [ ] **Step 3: Implement minimal app factory**
  - Add `create_app(config_path: Path | None = None) -> FastAPI`.
  - Serve static files from `web_assets`.
  - Add placeholder `GET /api/runs` and `GET /api/runs/{run_id}` readers.
  - Add validation for `POST /api/runs`.

- [ ] **Step 4: Run focused tests**
  - Run: `uv run pytest tests/test_web_app.py -v`
  - Expected: pass for skeleton behavior.

## Chunk 2: Real Run Launching

### Task 2: Connect `POST /api/runs` to existing launch path

**Files:**
- Modify: `src/galois/platform/web.py`
- Test: `tests/test_web_app.py`

- [ ] **Step 1: Add launch tests with monkeypatching**
  - Verify submitted Markdown is written under project runtime state.
  - Monkeypatch the background launch function so tests do not call real agents.
  - Verify API returns `run_id`, `run_dir`, `status`.

- [ ] **Step 2: Implement launch worker**
  - Write submitted Markdown to a file under `projects/default/web_inputs/` or equivalent configured project root.
  - Start a daemon thread/background task that calls `cmd_launch_run(...)` with `problem_id`, `problem_path`, title, selected pipeline, and defaults.
  - Return immediately after creating the run shell or launch handle.

- [ ] **Step 3: Avoid blocking request thread**
  - Ensure the endpoint returns before the long reasoning workflow finishes.
  - Store launch errors in a small `web_launch_error.json` file or event if possible.

- [ ] **Step 4: Run focused tests**
  - Run: `uv run pytest tests/test_web_app.py -v`
  - Expected: pass without external model/API dependencies.

## Chunk 3: Run Status and Artifacts

### Task 3: Implement status readers

**Files:**
- Modify: `src/galois/platform/web.py`
- Test: `tests/test_web_app.py`

- [ ] **Step 1: Add synthetic run tests**
  - Create temporary run dirs with `manifest.json`, `events.jsonl`, `summary.md`, `subagents.json`, and blueprint revisions.
  - Verify `GET /api/runs/{run_id}` returns derived status and latest output.

- [ ] **Step 2: Implement readers**
  - Parse manifest safely.
  - Parse recent events with tail limit.
  - Read latest `reasoning/blueprint_r*.md` by revision number.
  - Fallback to `summary.md` if no blueprint exists.
  - Include artifact path metadata.

- [ ] **Step 3: Implement recent runs list**
  - Return newest run directories from configured run root.
  - Keep payload compact.

- [ ] **Step 4: Run focused tests**
  - Run: `uv run pytest tests/test_web_app.py -v`
  - Expected: pass.

## Chunk 4: Static Research Workbench

### Task 4: Build the academic-calm UI

**Files:**
- Create: `src/galois/platform/web_assets/index.html`
- Create: `src/galois/platform/web_assets/styles.css`
- Create: `src/galois/platform/web_assets/app.js`

- [ ] **Step 1: Create HTML structure**
  - Left rail: identity, roadmap modules, recent runs.
  - Center: title, Markdown textarea, pipeline select, example, submit.
  - Right panel: run status ladder, telemetry, output.

- [ ] **Step 2: Add CSS design system**
  - Warm paper background.
  - Ink text.
  - Muted scholarly accents.
  - Responsive stacked layout below tablet width.

- [ ] **Step 3: Add JS behavior**
  - Submit to `POST /api/runs`.
  - Poll `GET /api/runs/{run_id}`.
  - Render events, progress ladder, artifact output, failures.
  - Load recent runs from `GET /api/runs`.

- [ ] **Step 4: Smoke check static route**
  - Run: `uv run pytest tests/test_web_app.py -v`
  - Expected: pass.

## Chunk 5: CLI and Docs

### Task 5: Add launch command and documentation

**Files:**
- Modify: `src/galois/platform/cli.py`
- Modify: `README.md`
- Test: `tests/test_web_app.py` or CLI parser test if existing pattern supports it.

- [ ] **Step 1: Add `galois-run web` subcommand**
  - Arguments: `--host`, `--port`, `--config`.
  - Implementation imports uvicorn lazily.
  - App target can be `galois.platform.web:create_app` or direct instantiated app.

- [ ] **Step 2: Document usage**
  - Add README section that points users to `uv run galois-run web`.
  - Explain that real runs require the same environment variables as CLI runs.

- [ ] **Step 3: Run targeted validation**
  - Run: `uv run pytest tests/test_web_app.py -v`
  - Run: `uv run galois-run web --help`
  - Expected: tests pass and help prints.

## Final Verification

- [ ] Run: `uv run pytest -v`
- [ ] Run: `uv run galois-run web --help`
- [ ] Optionally run local server: `uv run galois-run web`
- [ ] Open the local URL printed by `uv run galois-run web` and submit a small Markdown problem if model credentials are configured.
