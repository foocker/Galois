# Galois Research Workbench Design

Date: 2026-04-25
Status: Approved design, pending implementation plan

## Goal

Build the first real Galois frontend MVP: an academic-calm mathematical research workbench where users submit Markdown-formatted math problems, wait while Galois performs real research/reasoning, and read the resulting answer artifact.

The page should also make the broader platform roadmap visible: concept explanation, problem solving, research-level exploration, theorem search, paper reading assistance, and paper writing polish.

## Product Positioning

Galois is not a casual chatbot. It is a durable mathematical research platform centered on runs, artifacts, verification state, and reusable research output.

The first UI should therefore feel like a scholarly workbench:

- calm and rigorous rather than playful
- precise and artifact-oriented rather than conversational
- suitable for long-form mathematical reading and writing
- transparent about reasoning, verification, repair, and failure states

## Users

Primary users:

- mathematical researchers
- advanced students
- theorem-proving practitioners
- technical writers working with mathematical text

Their main job in the MVP is to submit a Markdown mathematical problem and receive a structured answer or proof attempt from the existing Galois control plane.

## MVP Scope

### In Scope

- A single web workbench page served by Galois.
- Markdown problem title and body input.
- Pipeline selection, defaulting to `reasoning-verification`.
- Real run creation using the existing Galois run infrastructure.
- Live polling of run manifest, events, summary, and key artifacts.
- Visible run status ladder: queued, reasoning, verification, repair loop, complete, failed.
- Final answer display from the latest reasoning blueprint artifact when available, with summary fallback.
- Failure display with useful diagnostics and artifact paths.
- Visible roadmap/navigation for future Galois capabilities.

### Out of Scope

- Authentication or multi-user accounts.
- Persistent database beyond existing run directories.
- Rich Markdown editor with syntax highlighting.
- Real theorem search index.
- Real paper ingestion or PDF parsing UI.
- Collaborative editing.
- Full frontend framework build system.

## Recommended Architecture

Use FastAPI plus static HTML/CSS/JavaScript for the MVP.

Rationale:

- The current repository is Python-first and already depends on FastAPI/uvicorn.
- There is no existing Node/frontend stack.
- The fastest path to a real MVP is to reuse the existing control plane directly.
- A static frontend avoids introducing build complexity before the product workflow is validated.

### Proposed Files

- `src/galois/platform/web.py`: FastAPI app and API endpoints.
- `src/galois/platform/web_assets/index.html`: research workbench page.
- `src/galois/platform/web_assets/styles.css`: academic-calm visual system.
- `src/galois/platform/web_assets/app.js`: run submission and polling client.
- `tests/test_web_app.py`: focused API/unit coverage where practical.

The exact test path can be adjusted to match existing test conventions.

## Backend Design

### Run Creation

Endpoint: `POST /api/runs`

Input:

```json
{
  "title": "Optional title",
  "problem_markdown": "Markdown problem statement",
  "pipeline": "reasoning-verification"
}
```

Behavior:

1. Validate non-empty Markdown.
2. Create a stable problem id from timestamp/slug.
3. Write the submitted Markdown to a repo-local input file under the project runtime area.
4. Start the existing Galois run path in a background task.
5. Return the new run id and run directory.

The implementation should prefer existing control-plane functions where possible. If the synchronous `cmd_launch_run` path is reused, run it in a background worker so the HTTP request returns quickly.

### Run Status

Endpoint: `GET /api/runs/{run_id}`

Return:

- manifest summary
- recent events
- subagent snapshot if present
- summary markdown if present
- latest reasoning blueprint markdown if present
- latest verification decision if present
- useful artifact paths
- derived display status

### Run Listing

Endpoint: `GET /api/runs`

Return recent runs from the configured run root. Keep the payload small: run id, title, status, pipeline, created ordering inferred from run id/path.

### Static App

Endpoint: `GET /`

Serve `index.html` and static assets.

## Frontend Design

### Layout

Three-region workbench:

1. Left rail: Galois identity, roadmap modules, recent runs.
2. Center: problem composition and submission.
3. Right panel: run telemetry, state ladder, final output.

On narrower screens, collapse to a stacked layout with the roadmap above or below the editor. Critical functionality must remain visible.

### Visual Direction

- Light-first interface.
- Warm paper background instead of pure white.
- Ink-like primary text.
- Restrained accent colors: muted blue-green for active research, muted amber for planned modules, red only for failure.
- Typography should favor readable system serif/sans pairing where available.
- Avoid chat bubbles, generic AI gradients, glassmorphism, and neon dashboard styling.

### Roadmap Modules

Show explicit future platform direction:

- Problem Research — active in MVP.
- Concept Explanation — planned.
- Research Exploration — planned.
- Theorem Search — planned.
- Paper Reading — planned.
- Writing Polish — planned.

Each module should include a one-line explanation and clear status label.

### Input Experience

Fields:

- Title input.
- Markdown textarea.
- Pipeline select with `reasoning-verification` and `reasoning-only`.
- Example problem action.
- Submit/run action.

The form should communicate that the input is Markdown and can include LaTeX math delimiters.

### Waiting State

After submission:

- Disable duplicate submission unless the user edits again.
- Show run id.
- Poll status at a modest interval.
- Display a progress ladder:
  - Queued
  - Reasoning
  - Verification
  - Repair Loop
  - Complete

The ladder is derived from manifest status, workflows, events, and artifact presence. It should not overclaim exact progress if the backend only exposes coarse signals.

### Output Experience

Primary output:

- latest `reasoning/blueprint_r*.md`

Fallback:

- `summary.md`

Diagnostics:

- verification decision path
- repair input path if any
- stderr/stdout paths from workflow results when failed

For MVP, plain Markdown rendering can be minimal. It is acceptable to display rendered paragraphs and code/pre blocks or a readable preformatted Markdown block. Avoid adding a large renderer dependency unless necessary.

## Error Handling

User-facing errors should be calm and actionable:

- Empty input: ask for a Markdown problem statement.
- Run launch failure: show that the run could not start and include the backend error.
- Run failure: show failed status, final events, summary if present, and artifact paths.
- Missing output: explain that no blueprint artifact was found yet and keep polling until terminal state.

## Testing Strategy

Focus on backend correctness first:

- API rejects empty Markdown.
- API writes a problem file under runtime/project state.
- Run status endpoint can read a synthetic run directory.
- Artifact selection chooses the latest blueprint revision.
- Static index route returns the workbench page.

A full real reasoning run may depend on external model configuration and should not be required for unit tests.

## Implementation Notes

- Do not introduce a Node build system for the MVP.
- Keep the frontend assets hand-authored and small.
- Preserve existing CLI behavior.
- Avoid changing existing run directory contracts unless necessary.
- Keep API payloads derived from existing artifacts rather than inventing a new persistence layer.

## Open Questions

- Whether to keep `uv run galois web` as the only user-facing local launch entry.
- Whether future iterations should replace the static frontend with a component framework.
- Whether Markdown rendering should later include KaTeX/MathJax for formula display.
