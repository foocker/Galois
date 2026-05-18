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
- writing parameters: target reference count, target page count, and review-revision rounds;
- title or research problem;
- a single `Draft` section containing a theorem, proof draft, rough notes, or manuscript text;
- a `References` section containing BibTeX, arXiv IDs, DOI lists, seed papers, or literature notes;
- an `Authors` section;
- continuation feedback plus previous manuscript, citation, review, and revision-task artifacts;
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
   - Put the title first and the author line immediately below it.
   - If an `Authors` section is provided, use it exactly except for safe whitespace cleanup.
   - If authors are not provided, write `Author not provided` below the title and add a revision task requesting author metadata.
   - Use Markdown with LaTeX math. Inline math uses `$...$`; display math uses `$$...$$`.
   - If the user only asks for review, write a short "No manuscript rewrite requested" note plus any safe local rewrites.

2. `review_report.md`
   - Findings by severity.
   - Include proof gaps, contribution risks, notation conflicts, and citation risks when present.
   - Label uncertain judgments as personal inference.

3. `citation_report.md`
   - Begin with `# References`.
   - Include `## Used References`, `## Unused References`, and `## Lookup Needed` sections.
   - Put verified cited items in `## Used References` before any audit notes.
   - Each reference should use a standard bibliographic shape: authors, title, venue or preprint source, year, and DOI/arXiv/URL when known.
   - Put source entries supplied by the user but not cited in `manuscript_draft.md` under `## Unused References`.
   - Put missing citations, incomplete metadata, and lookup tasks under `## Lookup Needed`.
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
- Every used reference must appear in `manuscript_draft.md` as an inline citation using `\cite{key}` for keyed BibTeX-style sources or `[n]` for numbered references.
- Do not list references as used just because they appear in the bibliography. If the manuscript does not cite a supplied source, classify it as unused.
- In continuation requests, treat user feedback and the current edited manuscript as the highest-priority revision target. Preserve previous manuscript material only when it remains compatible with the feedback.

## Workflow

1. Interpret `Requested Work` as the primary objective. Do not force the task into a fixed mode if the user gave a natural-language goal.
2. Extract the available material from `Draft`, `Authors`, `References`, `Reviewer Comments`, continuation feedback, and previous artifacts; each section may be empty except that at least one should contain user material.
3. Read `Writing Parameters`; respect reference count, page count, and review-round targets as constraints when feasible.
4. Use `$literature-citation` to validate seed references and identify lookup or expansion tasks. Runtime source lookup is limited to arXiv, Crossref, and OpenAlex unless the user supplies other sources manually.
5. Use `$math-paper-writing` to produce the requested manuscript version: complete paper, expanded draft, revised section, response draft, or reference-informed rewrite.
6. If reviewer comments are present, incorporate them as required revision constraints and record response-relevant changes.
7. If `review_rounds` is greater than zero, run a self-referee pass with `$math-review`, revise the manuscript against the findings, and record each round's key findings in `review_report.md`. Repeat up to the requested number of rounds, bounded by the available evidence and time.
8. Convert unresolved writing, proof, citation, and source issues into revision tasks.
9. Write all required artifacts before stopping.
