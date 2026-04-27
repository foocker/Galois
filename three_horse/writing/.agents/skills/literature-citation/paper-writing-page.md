# Galois Paper Writing Page Adaptation

Use this file to adapt the copied scientific literature, citation-management, and paper-lookup source skills to English mathematical paper writing.

## Boundary

This is a standalone literature and citation module for the Galois Paper Writing page. It does not consume Galois run artifacts, does not depend on proof-system outputs, and is not the downstream of the Galois proof system. Inputs are manuscript text, theorem statements, proof drafts, bibliography data, reviewer comments, target-journal instructions, and explicit lookup requests from the writing page.

Do not depend on root-level references/scientific-agent-skills. The local `scientific-skills/` directory inside this skill is the runtime source.

## Mathematical Literature Positioning

When positioning a mathematical manuscript:

- Begin with the mathematical problem, obstruction, or theorem family, not with a generic history paragraph.
- Separate direct predecessors from broad background, surveys, textbooks, software papers, and adjacent applications.
- Group prior work by idea, proof method, assumptions, conclusions, examples, constants, or scope.
- State what each direct predecessor proves, under what hypotheses, and how the current manuscript differs.
- Treat "first", "novel", "no prior work", and "new" as precedent-check claims requiring lookup.
- Prefer original sources for named theorems, definitions, constructions, datasets, and algorithms.
- Mark citation-chain uncertainty when a source is cited through another paper rather than inspected directly.

## Lookup Policy

Use `scientific-skills/paper-lookup/SKILL.md` for database selection. For mathematics, prioritize:

- arXiv for preprints in mathematics, CS, physics, statistics, and related areas;
- Crossref for DOI metadata and published article records;
- OpenAlex for cross-field discovery, author disambiguation, citation graph metadata, and related work;
- MathSciNet, zbMATH, publisher pages, and author pages as manual or user-provided lookup targets.

If network access, API keys, database access, or source files are unavailable, record `lookup_needed` with the exact missing identifier, database, or query string. Do not fill missing volume, issue, page, DOI, arXiv version, venue, or author metadata by memory.

## API Execution Chain

When the Paper Writing page backend is available, citation work should use the local execution chain instead of ad hoc browser search:

1. Discovery: call `POST /api/citations/search` with the manuscript phrase, title, author, or theorem name. Unless the user narrows the sources, use the full default chain: `arxiv`, `crossref`, and `openalex`.
2. Identifier verification: for every DOI, arXiv ID, DOI URL, arXiv URL, or candidate identifier found in the manuscript or search results, call `POST /api/citations/resolve`.
3. Bibliography validation: call `POST /api/citations/validate` on the BibTeX block before finalizing `citation_report.md`.
4. Reporting: copy resolved DOI/arXiv IDs, source URLs, source statuses, title/year mismatches, and `lookup_needed` items into the citation report and revision tasks.

Expected request shapes:

```json
{"query": "compactness theorem", "sources": ["arxiv", "crossref", "openalex"], "limit": 10}
{"identifier": "10.1000/example", "sources": ["crossref", "openalex"]}
{"bibtex": "@article{key, title={...}, author={...}, year={...}, doi={...}}", "sources": ["crossref", "openalex"]}
```

The execution chain never upgrades uncertainty into a citation. A source-level `error`, `not_found`, or missing identifier remains unresolved until the user provides a source or a later lookup verifies it.

## Citation Consistency

Check both directions:

- Every `\cite{key}` or Markdown citation key should exist in the bibliography.
- Every bibliography entry should be cited, marked as background, or removed.
- Duplicate entries should be merged.
- Citation keys should be stable, readable, and consistent.
- Bibliography entries should distinguish article, book, inproceedings, preprint, thesis, software, dataset, and unpublished work.

## BibTeX Rules

For BibTeX entries:

- Required fields: author, title, year.
- Journal articles usually need journal, volume, number when available, pages, and DOI.
- Books need publisher, place if style requires it, edition when relevant, and ISBN when available.
- Preprints need archive, arXiv ID, and version if cited.
- Preserve mathematical capitalization with braces where needed.
- Normalize author names without changing identity.
- Mark uncertain fields as `lookup_needed` rather than guessing.

## Paper Writing Page Artifacts

For `citation_report.md`, include:

1. Cited keys found.
2. Bibliography entries found.
3. Missing bibliography entries.
4. Unused bibliography entries.
5. Metadata needing lookup.
6. Prior-art or precedent-check tasks.
7. Suggested databases and query strings.
8. Source-provenance warnings.

For `revision_tasks.json`, convert every missing or uncertain citation issue into a concrete task with `id`, `severity`, `area`, `title`, `detail`, `status`, `evidence`, and `acceptance_criteria`.

Use `lookup_needed` for unresolved source work. Do not invent bibliographic metadata.
