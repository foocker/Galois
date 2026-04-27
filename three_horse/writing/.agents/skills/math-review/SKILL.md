---
name: math-review
description: Use when evaluating a mathematical manuscript, proof draft, theorem claim, contribution statement, review report, referee response, revision plan, or research-progress note for rigor, novelty, evidence, attribution, and referee-style risk.
---

# Math Review

This is the standalone mathematical paper review module for the Galois Paper Writing page. It is self-contained, but not monolithic: `SKILL.md` is the routing entry point, and the review method is split into category files under `review-methodology/`.

Do not depend on the root-level source snapshots or any copied external review repository. Do not consume Galois run artifacts or proof-system outputs. The files listed below are the complete runtime source for this paper writing page skill.

## Category Files

Load only the category files needed for the current task:

- [review-methodology/principles.md](review-methodology/principles.md): five iron rules, seven review principles, evidence discipline, credit attribution, precedent checks, and signal cost.
- [review-methodology/deep-review.md](review-methodology/deep-review.md): deep paper review workflow, independent field map, direct-predecessor comparison, contribution increment analysis, and second-order consistency check.
- [review-methodology/proof-verification.md](review-methodology/proof-verification.md): theorem/proof review, assumption-use table, line-by-line verification, and field-specific proof checks.
- [review-methodology/specialized-reviews.md](review-methodology/specialized-reviews.md): rapid screening, thesis review, benchmark paper review, AI-system capability report review, and POC/intermediate-result review.
- [review-methodology/output-contracts.md](review-methodology/output-contracts.md): Galois artifact mapping, review report contract, revision task contract, and coordination with writing/citation skills.
- [review-methodology/writing-standards.md](review-methodology/writing-standards.md): external-output quality gate, prohibited expressions, structure rules, and pre-delivery self-check.

## Review Task Classification

Classify the task before choosing depth. Do not default every request to full deep review.

| Type | Use when | Required files |
|---|---|---|
| Submitted paper deep review | Formal peer review, student paper review, serious self-referee pass | `principles.md`, `deep-review.md`, `output-contracts.md`, `writing-standards.md`; add `proof-verification.md` for theorem-heavy work |
| Theorem or proof review | Main risk is correctness of claims, hypotheses, definitions, or derivations | `principles.md`, `proof-verification.md`, `output-contracts.md`, `writing-standards.md` |
| PhD thesis or chapter review | External-examiner style judgment | `principles.md`, `specialized-reviews.md`, `output-contracts.md`, `writing-standards.md`; add `proof-verification.md` if proof depth is requested |
| Rapid screening | Batch triage or "should I read this?" | `principles.md`, `specialized-reviews.md`, `writing-standards.md` |
| Benchmark paper review | Paper proposes a dataset, task, leaderboard, or evaluation protocol | `principles.md`, `deep-review.md`, `specialized-reviews.md`, `output-contracts.md`, `writing-standards.md` |
| AI-system capability report | Report demonstrates an AI system's mathematical or scientific capability | `principles.md`, `specialized-reviews.md`, `output-contracts.md`, `writing-standards.md` |
| POC or intermediate result review | Internal progress, incomplete experiments, early theorem route | `principles.md`, `specialized-reviews.md`, `output-contracts.md`, `writing-standards.md` |
| Paper writing page self-review | Writing workflow asks for quality control | `principles.md`, `output-contracts.md`, `writing-standards.md`; add depth files as needed |

## Operating Rules

- Act as a professional mathematician and critical academic reviewer.
- Be rigorous, objective, concise, and evidence-based.
- Distinguish mathematical insight from engineering work, benchmark construction, software packaging, or rhetorical framing.
- Separate "using a method" from "proposing a method."
- Benchmark judgments against comparable work, not generic expectations.
- State inspection limits explicitly. Do not claim proof correctness beyond checks actually performed.
- For pure mathematics, emphasize theorem statements, assumptions, proof route, notation, predecessor comparison, and citation integrity.
- For computational or AI-assisted mathematics, also check baselines, evaluation design, code/repository constraints, pass@k/pass@1, evaluator independence, and failure disclosure.

## Coordination

Use `$literature-citation` for bibliographic metadata, arXiv/DOI/OpenAlex/Semantic Scholar/MathSciNet/zbMATH lookup, direct-predecessor source resolution, BibTeX cleanup, and citation provenance.

Use `$math-paper-writing` for title, abstract, introduction, conclusion, proof-prose, cover-letter, or reviewer-response rewriting. This skill diagnoses and tasks revision work; it should not silently rewrite mathematical claims.
