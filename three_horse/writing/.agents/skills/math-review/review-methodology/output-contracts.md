# Output Contracts

Use this file whenever the review runs inside the Galois Paper Writing page or needs to produce persistent paper-review artifacts. This module does not consume Galois run artifacts, does not depend on proof-system outputs, and is not the downstream of the Galois proof system.

## Paper Writing Page Artifact Mapping

When running inside the paper writing page workflow, put review information into the standard project artifacts:

- `review_report.md`: referee-style report, proof-risk report, or research-progress assessment.
- `revision_tasks.json`: machine-readable tasks converted from unresolved findings.
- `citation_report.md`: citation, attribution, and source-provenance findings; detailed lookup belongs to `$literature-citation`.
- `export_bundle.json`: paper-review status, inspection limits, unresolved risks, and next actions.
- `manuscript_draft.md`: if the user requested only review, keep this short and state that no manuscript rewrite was requested.

## Review Report Contract

Use this shape unless a specialized mode is more appropriate:

1. Summary Verdict
2. Inspection Scope
3. Contribution and Field Positioning
4. Major Issues
5. Proof and Notation Risks
6. Citation and Integrity Risks
7. Minor Issues
8. Revision Priorities
9. Inspection Limits

For deep paper reviews, top-level sections should normally be no more than:

1. Summary Verdict
2. Field Positioning
3. Strengths, omitted if the user asks for no strengths
4. Weaknesses and Issues
5. Overall Assessment

Never use internal process step numbers as report headings.

Each substantive issue should include, in prose or compact bullets:

- severity: blocker, major, moderate, minor, or note;
- area: contribution, theorem, proof, notation, citation, exposition, experiment, figure, table, integrity, or submission;
- location: theorem, section, equation, paragraph, figure, table, or global;
- finding;
- evidence or `personal inference`;
- why it matters;
- concrete revision action;
- inspection depth.

Avoid vague comments such as "improve the proof" or "add more citations." Name the exact proof step, theorem assumption, citation gap, or comparison class.

## Revision Task Contract

Every unresolved blocker, major issue, citation risk, proof risk, author-decision item, or submission-blocking concern must become a task in `revision_tasks.json`.

Each task has:

- `id`: stable slug;
- `severity`: blocker, major, moderate, or minor;
- `area`: theorem, proof, citation, exposition, notation, experiment, integrity, or submission;
- `title`: short action title;
- `detail`: concrete revision needed;
- `status`: `open`, `blocked`, or `needs_author_decision`;
- `evidence`: manuscript location or source pointer;
- `acceptance_criteria`: how completion can be inspected.

A task must be directly checkable.

## Coordination

Use `$literature-citation` when bibliographic metadata, arXiv/DOI/OpenAlex/Semantic Scholar/MathSciNet/zbMATH lookup, direct-predecessor source resolution, BibTeX cleanup, or citation provenance is needed. If lookup is needed but not performed, write `lookup_needed`.

Use `$math-paper-writing` when the user asks for title, abstract, introduction, conclusion, proof-prose, cover-letter, or reviewer-response rewriting, or when revision tasks should become draftable paper sections.
