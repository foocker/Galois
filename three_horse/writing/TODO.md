# Galois Paper Writing TODO

This TODO captures follow-up work for the independent mathematical paper-writing system under `three_horse/writing`. Runtime assets must remain self-contained in this directory. Do not depend on root-level reference snapshots, and do not commit PDFs, compressed downloads, or crawler caches.

## P0: Runtime Skill Hardening

- [ ] Expand `math-paper-writing/references/case-library.md` with more parsed Markdown case cards for abstract, introduction, proof prose, reviewer response, and self-referee patterns.
- [ ] Add stronger before/after examples for title rewriting, abstract compression, proof transition insertion, notation conflict repair, and reviewer response drafting.
- [ ] Keep all skill and reference files in English, with no runtime dependency on ignored root `references/`.
- [ ] Add regression tests that fail when runtime skills point to root-level references or PDF downloads.

## P1: Agent Workflow Roles

- [ ] Split the paper-writing workflow into explicit agent roles: project planner, manuscript drafter, math reviewer, citation reviewer, revision manager, and exporter.
- [ ] Define handoff contracts between roles using structured JSON, not only Markdown prose.
- [ ] Ensure every role can run independently on partial input, without requiring a Galois reasoning run.
- [ ] Add an optional later import path from Galois reasoning output into the writing project.

## P2: Structured Project Model

- [ ] Add `paper_project.json` as the central state model for title candidates, abstract slots, sections, theorem blocks, proof blocks, notation table, citations, review findings, and revision tasks.
- [ ] Make `manuscript_draft.md`, `review_report.md`, `citation_report.md`, `revision_tasks.json`, and `export_bundle.json` derived artifacts from the project model.
- [ ] Add schema validation for revision tasks and export bundle metadata.
- [ ] Preserve incomplete or uncertain mathematical claims as explicit assumptions and tasks.

## P3: Local Checkers

- [ ] Implement a citation checker for `\cite{...}` keys and bibliography entries.
- [ ] Implement a label/reference checker for `\label`, `\ref`, and `\eqref`.
- [ ] Implement an equation-number audit for unreferenced displayed equations.
- [ ] Implement a proof-risk scanner for phrases such as "clear", "obvious", "standard", and "well known".
- [ ] Implement a notation first-use scanner for symbols, operators, spaces, constants, and abbreviations.
- [ ] Implement an abstract self-containment checker for theorem numbers, section references, citation-number dependence, and undefined notation.

## P4: Web Product Surface

- [ ] Replace the single writing form with a workbench containing Project Setup, Outline, Abstract Builder, Introduction Builder, Proof Polisher, Notation/Citation Audit, Self-Referee Report, Revision Board, and Export.
- [ ] Show artifact status clearly: pending, running, complete, failed, or needs author decision.
- [ ] Allow switching between manuscript, review, citation, tasks, and export bundle without losing context.
- [ ] Add editor affordances for Markdown/LaTeX text, section splitting, and copy-safe export.
- [ ] Preserve dark and light theme behavior.

## P5: Review and Citation Depth

- [ ] Expand `math-review` with more referee report templates, proof-gap categories, contribution benchmark patterns, and revision-task examples.
- [ ] Expand `literature-citation` with lookup-result schemas, BibTeX repair examples, source-provenance warnings, and literature-positioning paragraph templates.
- [ ] Add cross-skill contracts so `math-review` can emit `lookup_needed` tasks that `literature-citation` can resolve later.
- [ ] Add case-driven tests for missing predecessor, overclaimed novelty, hidden theorem assumption, missing citation, and uninspected figure/table critique.

## P6: Evaluation Fixtures

- [ ] Add small fixture inputs for theorem/proof notes, abstract revision, reviewer comments, citation cleanup, reading report, survey outline, and thesis chapter review.
- [ ] Add end-to-end tests that run the writing adapter against fixtures and verify that all required artifacts are produced.
- [ ] Verify generated JSON is valid and all required fields are present.
- [ ] Verify outputs do not fabricate citations, proof correctness, or bibliographic metadata.
- [ ] Track review quality failures as concrete fixture regressions, not informal impressions.
