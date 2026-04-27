# Deep Review Workflow

Use this file for submitted paper deep review, serious manuscript self-review, benchmark paper review, and any case where novelty or field position matters.

The numbered steps are internal process. Do not use them as delivered report headings.

## Workflow

1. Establish the field problem map independently of the manuscript.
   - Identify core problems, leading approaches, standard baselines, known limitations, and the current frontier.
   - For gap-filling claims, ask whether the gap is technically hard, low priority, already solved in a neighboring field, or artificially framed.

2. Extract explicit and implicit contributions.
   - Record stated contributions from the abstract and introduction.
   - Identify implicit contributions signaled by phrases such as "we design", "novel", "without", "autonomous", "discover", "eliminate", "beyond", or methods presented without attribution.
   - Check whether each contribution corresponds to actual technical content rather than rhetorical packaging.

3. Search and inspect prior work anchored to each contribution.
   - Identify the single most direct predecessor for each serious claim.
   - Inspect direct predecessors deeply enough to describe their technical content.
   - Trace frameworks historically when the manuscript presents a standard construction as new.
   - Search recent parallel work when the area is active.

4. Quantify or structurally compare the increment.
   - For numerical claims, include predecessor result, current result, absolute difference, percentage improvement, and whether the methodological increment justifies the gain.
   - For pure mathematics, compare strength of results: weaker assumptions, stronger conclusions, sharper bounds, broader generality, new cases, new proof techniques, or removal of a known obstruction.

5. Apply the independent coordinate system.
   - Judge whether the increment addresses important field problems.
   - Distinguish framework-level contributions from improvements inside an inherited framework.
   - State the contribution level relative to top-tier work in the field.

6. Run attribution and packaging checks.
   - Separate what belongs to prior frameworks from what this manuscript contributes.
   - Enumerate strong claim phrases and check whether the technical content supports them.
   - Watch for asymmetric baselines, repackaged terminology, hidden priors, and claims of autonomous discovery that rely on human design choices.

7. Check method completeness and proof integrity.
   - For empirical work, check architecture, training, hyperparameters, ablations, code availability, data processing, and failure cases.
   - For mathematical work, check assumptions, definitions, notation, proof dependencies, and line-by-line derivations where feasible.

8. Perform a second-order consistency check.
   - For each critique, ask whether the manuscript contains contrary evidence.
   - Check whether another section already addresses the issue.
   - Check whether the critique falls outside the paper's actual scope.
   - Correct the report before delivery.

## Chain-Value Analysis

When a manuscript builds on an existing framework, analyze the contribution chain from the earliest reformulation to the current paper. For each layer, state:

- what technical component changed;
- whether any qualitative conclusion changed;
- whether the quantitative or structural gain is materially larger than prior increments;
- what lateral implications the change has outside the paper's chosen framing.

## Method Completeness

For methodological innovation claims, missing implementation detail is a review issue. Check algorithms, theorem dependencies, architecture, training settings, datasets, evaluation scripts, hyperparameters, ablations, and limitations. "Left to a future version" is not sufficient for a claim the paper currently makes.
