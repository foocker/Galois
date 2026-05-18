# Agent Runtime API

This branch exposes a backend-neutral math research runtime. Frontend clients and
other backend services should depend only on this API contract, not on the concrete
agent implementation behind it.

## CLI

```bash
uv run agent-runtime serve --host 127.0.0.1 --port 8765

uv run agent-runtime create \
  --problem-file problem.md \
  --title "Compactness problem" \
  --instruction strategy.md \
  --reference notes.md \
  --json

uv run agent-runtime continue <project_id> --prompt "Try the boundary case again." --json
uv run agent-runtime status <run_id> --json
uv run agent-runtime artifacts <run_id> --json
uv run agent-runtime events <run_id> --json
```

## HTTP Contract

Base URL: `http://127.0.0.1:8765`

### `GET /v1/health`

Returns:

```json
{ "status": "ok", "capability": "math_research" }
```

### `POST /v1/projects`

Creates a project and starts the first run.

```json
{
  "title": "Compactness problem",
  "problem": {
    "format": "markdown",
    "content": "Prove that ..."
  },
  "instructions": [
    { "name": "strategy.md", "content": "Prefer a topological proof." }
  ],
  "references": [
    { "name": "notes.md", "content": "..." }
  ],
  "execution": {
    "verification": true,
    "model": "gpt-5.4",
    "reasoning_effort": "high"
  }
}
```

Returns `202` with `project_id`, `latest_run_id`, `status`, `capability`, and links.

### `POST /v1/projects/{project_id}/runs`

Continues an existing project with a new prompt. Project workspace state is reused
across runs, including memory, results, downloads, scripts, and current input files.
The workspace is thin: static runtime assets are linked from the local asset source,
while writable state is kept under the project. Each run keeps its own logs,
lifecycle events, input snapshot, and artifact snapshot.

```json
{
  "prompt": "The first proof missed a boundary case. Continue from the prior work.",
  "instructions": [
    { "name": "extra-hint.md", "content": "Check the endpoint." }
  ],
  "references": []
}
```

Returns `202` with the same response shape as project creation.

### `GET /v1/runs/{run_id}`

Returns run status plus neutral artifacts:

```json
{
  "project_id": "compactness-problem",
  "run_id": "...",
  "status": "succeeded",
  "capability": "math_research",
  "continued_from": null,
  "artifacts": {
    "solution": { "content": "# Solution\n..." },
    "verified_solution": null
  }
}
```

### `GET /v1/runs/{run_id}/artifacts`

Returns only artifacts.

### `GET /v1/runs/{run_id}/events`

Returns frontend-pollable lifecycle events:

```json
{
  "run_id": "...",
  "capability": "math_research",
  "events": [
    { "type": "created", "status": "queued", "created_at": "..." },
    { "type": "running", "status": "running", "created_at": "..." },
    { "type": "succeeded", "status": "succeeded", "created_at": "..." }
  ]
}
```

## Public API Guardrails

Public responses must not include provider names, local filesystem paths, session ids,
or internal artifact filenames. The external contract is about projects, runs, events,
and artifacts; the provider implementation is private.
