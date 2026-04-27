---
name: literature-citation
description: Use when searching papers, organizing literature, validating citations, cleaning BibTeX, checking citation consistency, or positioning mathematical work against prior literature.
---

# Literature and Citation

This is the standalone literature and citation module for the Galois Paper Writing page. It is adapted from the local `scientific-agent-skills/scientific-skills` literature-review, citation-management, and paper-lookup skills, copied into this skill so runtime work does not depend on external source trees.

This module is independent of Galois reasoning runs. It does not consume Galois run artifacts, does not depend on proof-system outputs, and is not the downstream of the Galois proof system. Do not depend on root-level references/scientific-agent-skills at runtime.

## Source Files

Load the copied source files as needed:

- [scientific-skills/literature-review/SKILL.md](scientific-skills/literature-review/SKILL.md): systematic literature review workflow, database strategy, inclusion/exclusion discipline, synthesis structure, and citation-style guidance.
- [scientific-skills/citation-management/SKILL.md](scientific-skills/citation-management/SKILL.md): citation metadata extraction, BibTeX cleanup, duplicate detection, validation, and reference-list hygiene.
- [scientific-skills/paper-lookup/SKILL.md](scientific-skills/paper-lookup/SKILL.md): broader copied database-selection notes; the Galois runtime citation chain below is limited to arXiv, Crossref, and OpenAlex.
- [paper-writing-page.md](paper-writing-page.md): Galois Paper Writing page adaptation for mathematical literature positioning, artifact outputs, and source-provenance rules.

The copied scientific source files may mention tools or scripts from their original environment. In this runtime, use them as methodology references. If a script, database, API key, or network lookup is unavailable, record `lookup_needed` instead of fabricating data.

## Runtime Citation APIs

The Galois backend exposes a concrete citation lookup execution chain for the Paper Writing page. Prefer these local APIs before manual metadata reconstruction:

- `POST /api/citations/search`: search by title, theorem phrase, author, or topic. The default chain: `arxiv`, `crossref`, and `openalex`.
- `POST /api/citations/resolve`: resolve a DOI, arXiv ID, DOI URL, arXiv URL, or bibliography identifier. DOI resolution cross-checks Crossref and OpenAlex; arXiv resolution checks arXiv and OpenAlex.
- `POST /api/citations/validate`: parse BibTeX, resolve each DOI/arXiv/URL identifier, compare title and year against returned metadata, and mark unresolved entries as `lookup_needed`.

API results must be treated as source-specific evidence, not as an oracle. Preserve each source record, status, identifier, and URL in `citation_report.md` when relevant. If a source returns an error, no result, or inaccessible manual database, keep the issue as `lookup_needed` with the exact source and query.

## Task Routing

- Literature search or prior-work synthesis: read `paper-writing-page.md`, then `scientific-skills/literature-review/SKILL.md`; use paper lookup references for database-specific details.
- DOI, arXiv, Crossref, or OpenAlex lookup: read `paper-writing-page.md`, then `scientific-skills/paper-lookup/SKILL.md`.
- BibTeX cleanup, metadata validation, duplicate detection, or citation consistency: read `paper-writing-page.md`, then `scientific-skills/citation-management/SKILL.md`.
- Mathematical contribution positioning: read `paper-writing-page.md` first; add literature-review and paper-lookup sources only as needed.

## Core Discipline

- Never invent bibliographic metadata.
- Every external-source claim needs a citation, DOI, arXiv ID, URL, or `lookup_needed` marker.
- Distinguish full-text inspection from metadata-only lookup.
- Separate direct predecessors from broad background.
- Prefer original mathematical sources when possible, and mark secondary citation chains.
- Convert unresolved citation and lookup issues into `citation_report.md` entries and concrete `revision_tasks.json` tasks.
