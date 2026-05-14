# Mathematical Paper Writing Case Library

This file converts the original case manifest and downloaded-paper intent into runtime Markdown case cards. It does not require PDFs. Use these cards to guide new writing, critique, and revision; do not copy external article prose.

For choosing among local classic-paper models by field or paper type, see `classic-literature-map.md`.

## Case Use Rules

- Use cases as patterns, not source text.
- When a case is tied to a copyrighted paper or book example, extract the lesson only.
- Produce original manuscript prose for the user.
- If bibliographic details are uncertain, mark them as `lookup_needed`.
- Prefer theorem-level specificity over generic praise.

## Title Cases

### Li-Yorke: Short Result-Title Pattern

Model source: Li and Yorke, "Period three implies chaos."

Use when:

- The result has a memorable, precise implication.
- The theorem can be expressed as object/property -> consequence.
- A short title would be clearer than a broad topic title.

Pattern:

```text
[Concrete hypothesis] implies [striking conclusion]
```

Do:

- Name the exact hypothesis or object.
- Use a mathematically meaningful consequence.
- Keep the title short if the result itself carries the force.

Do not:

- Use a clever title if it hides the actual theorem.
- Replace precision with drama.

Original example to generate:

```text
Uniform spectral gaps imply exponential mixing
```

### Kac / Drum: Question-Title Pattern

Model source: "Can one hear the shape of a drum?" and related inverse spectral titles.

Use when:

- The paper is expository or problem-driven.
- The central question is recognizable and honest.
- The answer or counterexample is developed in the body.

Pattern:

```text
Can [observable data] determine [mathematical object]?
```

Do:

- Make the question concrete.
- Ensure the paper actually answers or substantially advances the question.

Do not:

- Use a question title for a purely technical incremental result.

## Abstract Cases

### Green-Tao: Three-Part Abstract Pattern

Model source: Green and Tao, "The primes contain arbitrarily long arithmetic progressions."

Use when:

- The paper proves a major theorem.
- The abstract must state the result, method, and imported tools compactly.

Pattern:

1. State the main theorem directly.
2. Identify the key strategy or transference principle.
3. Name the major tool or comparison theorem when it clarifies the contribution.

Do:

- Put the theorem-level result early.
- Keep the method statement shorter than the result statement.
- Mention tools only if they explain why the theorem is plausible.

Do not:

- Spend the abstract on background history.
- Include proof details, theorem numbers, citations, or internal references.

Original example to generate:

```text
We prove that every sufficiently regular sparse set satisfying a uniform restriction estimate contains arbitrarily long polynomial configurations. The argument transfers a density-increment scheme from the ambient group to a pseudorandom majorant and combines it with a quantitative inverse theorem for the associated Gowers norm.
```

### Lasota-Yorke: Minimal Abstract Pattern

Model source: a short invariant-measure abstract.

Use when:

- The paper is short.
- The main contribution is one clean existence, uniqueness, stability, or equivalence result.

Pattern:

```text
We prove [precise result] for [precise class] under [main assumptions].
```

Do:

- State the object and result in one or two sentences.
- Avoid inflated motivation.

Do not:

- Add generic field background merely to lengthen the abstract.

## Introduction Cases

### Serre / GAGA: Two-Viewpoint Bridge Pattern

Use when:

- The paper compares two mathematical worlds, such as algebraic/analytic, local/global, finite/infinite, discrete/continuous, or synthetic/computational.
- The contribution is an equivalence, comparison theorem, transfer principle, or dictionary.

Pattern:

1. Name the two viewpoints and the common object.
2. Give one or two familiar overlap examples.
3. State the precise bridge the paper proves.
4. Say which machinery makes the bridge possible.
5. Preview applications showing why the bridge matters.

Do:

- Make the comparison concrete before introducing machinery.
- State the main equivalence early.
- Separate preliminaries from the proof of the bridge.

Do not:

- Let background on either viewpoint delay the main theorem.
- Leave the reader guessing which comparison is new.

### Katz / Monodromy: Problem-To-Mechanism Pattern

Use when:

- The paper proves a known-looking theorem by a new mechanism.
- The proof route passes through several technical reductions.
- The introduction must convince the reader that the machinery is purposeful.

Pattern:

1. State the classical problem or theorem.
2. Reinterpret it in the paper's technical language.
3. State the new method in one sentence.
4. List the main reductions in chronological order.
5. Mark borrowed ingredients and new ingredients.

Do:

- Tell the reader what each later section accomplishes.
- Identify the final step that ties the ingredients together.

Do not:

- Present the technical route as a list of objects with no governing problem.

### Witten: Cross-Field Accessibility Pattern

Use when:

- The paper imports ideas from another field.
- One audience needs a compact but serious introduction to unfamiliar concepts.
- The paper will derive a familiar mathematical theorem from a surprising framework.

Pattern:

1. Name the external framework and why it matters.
2. Translate only the concepts needed for the mathematical application.
3. State the key algebraic or structural relations.
4. Explain the mathematical question these relations address.
5. Return to the main theorem with the new viewpoint prepared.

Do:

- Define unfamiliar objects through their role in the argument.
- Keep physical, computational, or external motivation subordinate to the mathematical route.

Do not:

- Assume the reader accepts the external framework as motivation by itself.

### Anderson / Geometrization: Survey-Introduction Pattern

Use when:

- Writing a survey or broad introduction.
- The paper must move from a classical lower-dimensional problem to a modern generalization.

Pattern:

1. Start with the familiar classification or benchmark problem.
2. Explain the obstruction in the higher-dimensional or generalized setting.
3. Introduce the modern method or theorem as the organizing principle.
4. Tell the reader what the survey or paper will explain.

Do:

- Use history only to orient the mathematical problem.
- Keep named milestones connected by ideas, not chronology alone.

Do not:

- Turn the introduction into a timeline with no argument.

## Body and Proof Cases

### Serre / Finite-Field Method Pattern

Use when a proof transfers a problem to a simpler universe and back.

Pattern:

1. State the target theorem.
2. Prove a clean special case where the mechanism is transparent.
3. Explain the reduction from the general case to the special case.
4. Record remarks, variants, or questions after the proof.

Do:

- Label the special case and reduction separately.
- State exactly which finite, local, generic, or model-theoretic fact survives transfer.

Do not:

- Hide the reduction behind "by standard spreading out" unless the audience can safely supply it.

### Definition-to-Model Pattern

Use when introducing a model, operator, equation, or space.

Pattern:

1. Explain why the object is needed.
2. Define it.
3. State the convention or notation scope.
4. Immediately use it in a lemma, proposition, or example.

Do not:

- Dump a block of notation before the reader knows the goal.
- Define symbols that never appear again.

### Long-Proof Partition Pattern

Use when a proof exceeds one conceptual step.

Pattern:

1. State proof strategy.
2. Split into claims or lemmas.
3. For each step, say what it proves and why it is needed.
4. Reassemble the final conclusion.

Do:

- Name the role of each lemma.
- Make dependencies visible.

Do not:

- Hide a major step behind "It remains to show..." without explanation.

### Milnor: Construction-And-Verification Pattern

Use when the paper constructs a mathematical object with a universal or classification property.

Pattern:

1. State the desired object and universal property.
2. Give the construction.
3. Prove basic lemmas establishing well-definedness and topology/algebra/geometry.
4. Verify the defining property.
5. Derive consequences or classification statements.

Do:

- Put technical lemmas before the construction only when they are immediately needed.
- Tell the reader which lemmas are deferred and why.

Do not:

- Let the construction appear before the reader knows what property it is meant to satisfy.

## Figure and Table Cases

Use when revising computational or applied mathematics.

Pattern for figure prose:

1. State what the figure shows.
2. Define axes, symbols, parameters, and units.
3. State the claim supported by the figure.
4. Mention limitations if the figure is only illustrative.

Do not:

- Say only "The result is shown in Figure 2."
- Use figures as decoration.

## Conclusion Cases

Pattern:

1. Return to the main theorem or method.
2. Summarize what was actually proved.
3. State limitations if they matter.
4. Give future directions that follow from the proof, examples, or open cases.

Do not:

- Repeat the abstract sentence by sentence.
- Introduce a new theorem or unsupported application.

## Acknowledgment Cases

Use controlled, factual acknowledgments:

- funding and grant numbers;
- specific mathematical conversations;
- referee suggestions;
- host institutions.

Do not invent support, funding, or personal thanks.

## Revision Cases

### Deletion and Compression

Use when text is verbose or repetitive.

Actions:

- Remove empty phrases.
- Replace broad claims with theorem-level claims.
- Delete unused definitions and labels.
- Split overloaded sentences.
- Keep mathematical content intact.

### Equation-Density Revision

Use when a paragraph is a chain of displayed formulas.

Actions:

- Add a sentence before each key display explaining its purpose.
- Add a sentence after the display explaining what it gives.
- Remove numbers from unreferenced equations.
- Convert short noncentral displays to inline math.

## Cover Letter and Reviewer Response Cases

### Cover Letter

Pattern:

1. State submission title and article type.
2. State originality and no simultaneous submission when required.
3. Give one precise contribution sentence.
4. Identify corresponding author.

Do not oversell.

### Response Letter

Pattern:

1. Thank the reviewer/editor briefly.
2. Quote or paraphrase one comment.
3. State the change made.
4. Give manuscript location.
5. If disagreeing, provide a technical reason without emotional language.

## Self-Referee Cases

Use review categories:

- Acceptable after minor revision.
- Major revision required.
- Not ready because of proof gap.
- Not ready because contribution/literature position is unclear.
- Language obstructs mathematical understanding.

Every review must identify concrete evidence and concrete revision tasks.
