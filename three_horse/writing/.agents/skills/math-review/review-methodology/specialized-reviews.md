# Specialized Reviews

Use this file for review modes that should not receive a generic full paper review by default.

## Rapid Screening

Use for batch triage or early "should I read this?" decisions. Rapid screening must not be presented as deep review.

```markdown
Paper: [title or identifier]
Verdict: [one calibrated sentence]

Key findings:
- [specific contribution or risk]
- [specific evidence or missing evidence]
- [inspection limit]
```

## PhD Thesis or Chapter Review

Focus on whether the body of work meets degree expectations:

- central contribution and whether it is substantive;
- proof or experiment sufficiency at thesis level;
- relation between thesis claims and publication record if supplied;
- clarity, organization, and definitions;
- unresolved issues that must be fixed before defense or submission.

Do not verify every claim unless deep proof review is requested.

## Benchmark Paper Review

For a new benchmark, inspect the evaluation code or repository when available. The implementation often defines the task more precisely than the paper text.

Check:

- model input/output interface and whether context can be modified;
- data extraction, transformation, filtering, and deduplication;
- metric implementation, pass@k, timeouts, normalization, and scoring;
- equivalence of paired tasks or controlled comparisons;
- whether the claimed novelty dimension is genuinely unique or tautological for all comparable benchmarks;
- the user perspective: what a new model evaluator must do from download to final number.

If code or data cannot be inspected, state that limitation.

## AI-System Capability Report Review

For reports demonstrating an AI system's mathematical capability, check:

- multi-level attribution: base model, training, inference, system architecture, prompts, tools, human selection, and evaluation;
- pass@1 versus pass@k, including whether best-of-many success is being described as single-run capability;
- evaluator independence and expertise;
- objective correctness criteria, formal verification, known-answer comparison, or subjective adjudication;
- limitations of self-verification when generator and verifier share blind spots;
- precision of "autonomous" and the amount of human input in task choice, system design, execution, and evaluation;
- refusal rates, incorrect outputs, corrected outputs, variance across runs, and failure disclosure;
- extrapolation boundaries between controlled evaluation and open-ended real research;
- compute and economic feasibility.

## POC or Intermediate Research Results

The core question is whether current evidence supports progressing to the next stage.

Use this delivery shape:

- Current Stage Verdict: stage and operational definition.
- Strongest evidence supporting the verdict.
- Claims of advancement not yet supported.
- Missing evidence type, such as out-of-distribution test, prospective prediction, new theorem case, or independent replication.
- Stage-advancement roadmap with concrete experiment, proof task, success criterion, and resource estimate.

High in-distribution performance, broad coverage statistics, or rediscovery of known knowledge does not by itself establish a new rule, mechanism, or theorem-level advance.
