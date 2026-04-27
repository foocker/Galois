# Review Principles

This file defines the core review discipline for mathematical manuscripts, math-AI papers, proof drafts, and research-progress reports.

## Five Iron Rules

### 1. Evidence-Based Critique

Every substantive criticism or recommendation must have:

- a claim: what is problematic;
- evidence: a manuscript location, citation, inspected figure/table, direct computation, internal contradiction, or reproducible reasoning;
- a warrant: why the evidence supports the judgment.

When evidence is genuinely unavailable but the judgment is useful, label it as `personal inference`. Such items should be rare and must not be presented as confident criticism.

Do not expose internal labels such as "Claim", "Evidence", or "Warrant" in delivered prose. Integrate the support naturally.

### 2. Independent Coordinate System

Do not evaluate a paper only within the narrative the authors construct. Build an independent coordinate system for the field: current core problems, strongest known approaches, standard assumptions, accepted benchmarks, and active research directions. The paper's chosen framing, baselines, terminology, and novelty claims are objects of review.

### 3. Credit Attribution

Default assumption: mathematical representations, problem reformulations, datasets, constructive frameworks, and standard proof devices belong to prior work unless independent inspection shows otherwise.

For every method or representation mentioned in a review, identify the earliest source you can substantiate, including year when possible. If origin is ambiguous, state the ambiguity instead of assigning credit. For work from the author's own group, check earlier group papers and preprints for reused terms, definitions, datasets, screening rules, and methods.

### 4. Full-Text Prior Work Inspection

The direct predecessor of every serious novelty claim must be inspected in full-text prior work form, not inferred from title or abstract. The standard is: describe the predecessor's technical approach at equation, theorem, algorithm, construction, or evaluation-design level and compare the actual increment.

If full inspection cannot be done, mark the item `lookup_needed` or state that the judgment is provisional.

### 5. Actual Inspection of Figures and Tables

Every critique about an experimental figure, comparison table, architecture diagram, plot, or numerical result must be based on actual inspection of figures and tables. If only the text description was available, say so and reduce confidence. For pure mathematics papers with no figures or tables, record `N/A - no figures/tables`.

## Seven Review Principles

### Evidence-Based Criticism

A substantive claim about quality, novelty, correctness, or sufficiency is valid only when grounded in a citation, manuscript evidence, inspected data, or logical derivation. Unsupported judgment must be scoped as `personal inference`.

### Uniqueness Test

Delete or rewrite any statement that could be copied into a review of another comparable paper without sounding wrong. Information-bearing review comments name a specific property, gap, contribution, comparison, or risk in this work.

### Silence as Signal

Absences can be evidence: missing comparison to the strongest baseline, missing limitation discussion, missing foundational citation, missing proof of an assumption, or missing quantification where quantification is standard. First define what a complete treatment should include, then compare the manuscript against it.

### Benchmark Over Absolutes

Avoid absolute judgments like "strong", "weak", "novel", or "excellent" unless anchored. Use the forced comparison: compared to which reference class, on which criterion, where does this work stand? If those three slots cannot be filled, remove the judgment.

### Define Before Discuss

Before evaluating a technical claim, define the relevant standard. For example, "complete proof" means no step within the paper's scope relies on an unstated assumption; "autonomous" means the amount and location of human intellectual input have been specified.

### Precedent Check

Absolute claims such as "first", "never before", "unique", "no prior work", and "without priors" require targeted prior-work checks. If a claim survives, narrow it to the defensible scope.

### Signal Cost Hierarchy

When using external signals, weight them by signal cost. Substantive discussion in a survey, named public endorsement, reproducible leaderboard evidence, or a formal venue decision carries more weight than casual mentions, internal promotional material, or list-style citations. Signal cost must calibrate confidence.
