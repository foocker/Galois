# Frontend Integration Guide

This document describes the expected frontend interaction model for the research
runtime API. The UI should depend only on the public project/run/artifact contract
and should not expose the underlying agent implementation.

## Core Screens

### New Research Task

Use this screen to create a project and start the first run.

Load selectable backend options from:

```http
GET /v1/config
```

Recommended controls:

- Model selector: examples include `gpt-5.5`, `gpt-5.4`, or other backend-allowed model ids.
- Reasoning effort selector: `low`, `medium`, `high`, `xhigh`.
- Verification toggle.
- Problem editor: main prompt/problem statement. Markdown and TeX input should be allowed.
- Extra instructions editor: optional guidance such as proof style, constraints, or output preference.
- References uploader/editor: optional `.md`, `.txt`, `.tex`, or pre-extracted reference text.
- Run button.

On submit, call:

```http
POST /v1/projects
```

Example payload:

```json
{
  "title": "Compactness problem",
  "problem": {
    "format": "markdown",
    "content": "Prove that every continuous function on a compact space attains a maximum."
  },
  "instructions": [
    {
      "name": "strategy.md",
      "content": "Prefer a concise topological proof."
    }
  ],
  "references": [],
  "execution": {
    "verification": true,
    "model": "gpt-5.5",
    "reasoning_effort": "high"
  }
}
```

The response returns `project_id`, `latest_run_id`, `status`, and polling links.
The first response may be `queued` because runs are scheduled by the backend.

### Run Monitor

After create or continue, show the active run page.

Frontend behavior:

- Poll `GET /v1/runs/{run_id}` for current status and latest artifacts.
- Poll `GET /v1/runs/{run_id}/events` for lifecycle timeline.
- Stop frequent polling when status becomes `succeeded` or `failed`.
- Keep a visible queued/running/succeeded/failed state.

Suggested polling interval:

- `queued`: every 2-5 seconds.
- `running`: every 5-10 seconds.
- terminal status: stop or refresh manually.

Status meanings:

```text
queued     accepted, waiting for worker capacity
running    agent is currently executing
succeeded  run completed; artifacts may be rendered
failed     run failed; show a generic failure message and allow retry/continue
```

### Project List And Re-entry

Use this screen when users return to the app or switch between tasks.

Call:

```http
GET /v1/projects
```

When opening a project, call:

```http
GET /v1/projects/{project_id}
GET /v1/projects/{project_id}/runs
```

Use project detail to restore title, problem, execution settings, and latest run.
Use run history to show previous versions and let users inspect older outputs.

### Result Viewer

When artifacts are available, render:

- `artifacts.solution.content`
- `artifacts.verified_solution.content` when present

The content is Markdown and may contain TeX. The frontend should render:

- Markdown headings, lists, code blocks, tables.
- Inline TeX such as `$x^2$`.
- Display TeX such as `\[ x^2 = 4k^2 \]`.

Recommended rendering stack:

- Markdown parser with sanitization.
- TeX renderer such as KaTeX or MathJax.
- Code highlighting if needed.

If both solution and verified solution exist, prefer showing the verified solution
as the main result and keep the unverified solution available as a secondary tab.

### Continue Existing Project

After a project has a result or partial progress, users should be able to add a
new prompt and continue from the existing project state.

Recommended controls:

- Continue prompt editor: "revise this proof", "handle the missing case", "try another approach", etc.
- Optional new instructions.
- Optional new references.
- Optional execution settings override.
- Run agent button.

Call:

```http
POST /v1/projects/{project_id}/runs
```

Example payload:

```json
{
  "prompt": "The previous proof missed the boundary case. Continue from the existing work and repair it.",
  "instructions": [
    {
      "name": "revision.md",
      "content": "Keep the final proof self-contained."
    }
  ],
  "references": [],
  "execution": {
    "verification": true,
    "model": "gpt-5.5",
    "reasoning_effort": "high"
  }
}
```

The response returns a new `latest_run_id`. Navigate to the same run monitor flow
and poll that run. The backend reuses the project workspace, so the continuation
can build on prior memory, results, downloads, and scripts.

## Suggested User Flow

```text
1. User logs in.
2. User opens "New Research Task".
3. User selects model and reasoning effort.
4. User enters problem and optional instructions/references.
5. User clicks "Run Agent".
6. Frontend calls POST /v1/projects.
7. Frontend navigates to run monitor with latest_run_id.
8. Frontend polls run status/events.
9. When result appears, frontend renders Markdown and TeX.
10. User can add a continue prompt and click "Run Agent" again.
11. Frontend calls POST /v1/projects/{project_id}/runs.
12. Frontend monitors the new run and renders the new result.
```

## Frontend State Shape

Suggested client-side state:

```ts
type ResearchProject = {
  projectId: string;
  title: string | null;
  latestRunId: string;
};

type ResearchRun = {
  runId: string;
  projectId: string;
  status: "queued" | "running" | "succeeded" | "failed";
  continuedFrom: string | null;
  artifacts: {
    solution: { content: string } | null;
    verified_solution: { content: string } | null;
  };
};

type RunEvent = {
  type: string;
  status: string;
  created_at: string;
  message?: string;
};
```

## Error Handling

Frontend should handle:

- `not_found`: project or run not found.
- `insufficient_credits`: show recharge or upgrade action.
- `busy`: the user or system is temporarily at capacity; keep the input and show retry action.
- `runtime_failed`: show failure on the run page and allow continue/retry.
- `internal_error`: show a generic error.
- Network errors: show retry action.

See `docs/API_ERRORS.md` for the exact error shape. Do not show internal backend
logs or local filesystem paths to end users.

## Product Notes

- The backend queues work, so the UI should make queued state feel normal.
- Multiple users may submit tasks at once; frontend should not assume immediate execution.
- A single project can have multiple runs, but the backend serializes runs for the same project.
- The UI should treat model ids as configuration from the web product, not infer backend implementation details.
