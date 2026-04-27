# Writing Asset Manifest

This directory contains the runtime agent assets for the Galois Paper Writing page. It is independent of Galois reasoning runs, does not consume Galois run artifacts, does not depend on proof-system outputs, and is not the downstream of the Galois proof system.

## Integrated Skill System

The root-level source snapshots are ignored and are not required at runtime. The core material selected from the local source libraries has been integrated into the runtime skills. For math review, the review methodology is split into the `math-review` entry point plus first-party category files. For literature and citation work, the relevant scientific source skills are copied locally under `literature-citation/scientific-skills/` and adapted by `paper-writing-page.md`.

- `.agents/skills/math-paper-writing/SKILL.md`: mathematical paper structure, English exposition, proof prose, notation, revision, response-letter, and submission rules.
- `.agents/skills/math-review/SKILL.md`: evidence-based referee review, proof-gap detection, contribution calibration, attribution discipline, inspection-depth labeling, and revision-priority discipline.
- `.agents/skills/literature-citation/SKILL.md`: literature search strategy, paper lookup, metadata validation, BibTeX cleanup, citation consistency, and source-provenance rules.
- `.agents/skills/literature-citation/scientific-skills/`: local copies of the source `literature-review`, `citation-management`, and `paper-lookup` skills from `scientific-agent-skills`.
- `.agents/skills/literature-citation/paper-writing-page.md`: mathematical paper adaptation for literature positioning, citation reports, lookup tasks, and Paper Writing page artifacts.

The runtime agent should read the three skills directly. `$math-review` and `$literature-citation` are complete standalone skills and do not require root-level source snapshots.

## Citation Lookup Execution Chain

The Paper Writing page has a backend citation lookup chain:

- `POST /api/citations/search`: default source chain is `arxiv`, `crossref`, and `openalex`.
- `POST /api/citations/resolve`: resolves DOI and arXiv identifiers through source-specific adapters and records per-source statuses.
- `POST /api/citations/validate`: parses BibTeX, resolves identifiers, and flags missing identifiers or title/year mismatches.

The chain writes source-specific evidence only. Missing results, inaccessible services, and manual databases remain `lookup_needed`.

## Runtime Files

- `AGENTS.md`: top-level writing workflow contract.
- `.agents/skills/math-paper-writing/SKILL.md`: mathematical paper drafting and revision rules.
- `.agents/skills/math-review/SKILL.md`: self-referee and proof-gap review entry point.
- `.agents/skills/math-review/review-methodology/`: first-party category files for principles, deep review, proof verification, specialized reviews, output contracts, and writing standards.
- `.agents/skills/literature-citation/SKILL.md`: literature search and citation-management entry point.
- `.agents/skills/literature-citation/scientific-skills/`: copied source files for literature review, citation management, and paper lookup.
- `.agents/skills/literature-citation/paper-writing-page.md`: writing-page adaptation and artifact contract.
- `data/example.md`: small manual-run example.
- `TODO.md`: follow-up implementation plan for improving the writing workflow.
