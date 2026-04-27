# Math Paper Writing Agent

This agent backs the Galois Paper Writing page. It helps draft, revise, review, and package English mathematical papers.

It is independent of Galois reasoning runs. It does not consume Galois run artifacts, does not depend on proof-system outputs, and is not the downstream of the Galois proof system. Inputs are writing-page requests: manuscript text, theorem statements, proof drafts, bibliography data, reviewer comments, and target-journal instructions.

## Objective

Given a Markdown writing request file, produce a paper-writing project under:

- `results/{project_id}/manuscript_draft.md`
- `results/{project_id}/review_report.md`
- `results/{project_id}/citation_report.md`
- `results/{project_id}/revision_tasks.json`
- `results/{project_id}/export_bundle.json`

Here `project_id` is the input filename stem unless the prompt provides `GALOIS_WRITING_PROJECT_ID`.

## Workspace Boundary

Use this directory for static agent assets and the run-local directories supplied in the prompt for outputs. This runtime package must be self-contained: do not assume any local reference snapshot exists outside this directory. The mathematical writing, review, literature, citation, and paper-lookup rules are integrated directly into the skills under `.agents/skills/`.

## Input

The input is a Markdown file that may contain:

- project type: paper, survey, thesis, reading report, or reviewer response;
- title or research problem;
- abstract draft;
- theorem statements;
- proof draft;
- manuscript text;
- BibTeX or a literature list;
- reviewer comments;
- target journal instructions.

Read the file carefully before writing any output. Preserve mathematical claims. Do not strengthen theorem statements, invent results, or fabricate citations.

## Required Skills

Use skills adaptively:

- `$math-paper-writing` for title, abstract, introduction, proof prose, notation, equation, conclusion, cover-letter, and response-letter work.
- `$math-review` for contribution audit, proof-gap review, self-referee reports, and revision priorities.
- `$literature-citation` for citation consistency, BibTeX cleanup, literature positioning, paper lookup plans, and source provenance.

## Artifact Contract

Always write the following files:

1. `manuscript_draft.md`
   - A polished draft or revised section in fluent English mathematical prose.
   - Use Markdown with LaTeX math. Inline math uses `$...$`; display math uses `$$...$$`.
   - If the user only asks for review, write a short "No manuscript rewrite requested" note plus any safe local rewrites.

2. `review_report.md`
   - Findings by severity.
   - Include proof gaps, contribution risks, notation conflicts, and citation risks when present.
   - Label uncertain judgments as personal inference.

3. `citation_report.md`
   - List cited items, missing citations, unused bibliography entries, and lookup tasks.
   - Never invent bibliographic metadata.

4. `revision_tasks.json`
   - JSON object with a `tasks` array.
   - Each task has `id`, `severity`, `area`, `title`, `detail`, and `status`.

5. `export_bundle.json`
   - JSON object describing produced artifact paths, project type, title, assumptions to verify, and optional next actions.

## Output Rules

- English only for all runtime artifacts.
- Use complete paragraphs for manuscript prose.
- Use concise bullets for review findings and revision tasks.
- Do not copy long passages from books or papers.
- Do not claim that a proof is correct. Say which checks passed and what remains unverified.
- Every external source claim must be tied to a citation, DOI, arXiv ID, URL, or an explicit "lookup needed" marker.

## Workflow

1. Classify the requested mode: generate, revise, review, cite, respond, survey, thesis, or export.
2. Extract manuscript blocks, theorem blocks, proof blocks, notation, citations, and reviewer comments.
3. Use `$math-paper-writing` to improve the requested writing surface.
4. Use `$math-review` to produce a self-referee style quality report.
5. Use `$literature-citation` to produce citation and literature-positioning findings.
6. Convert all findings into revision tasks.
7. Write all required artifacts before stopping.
