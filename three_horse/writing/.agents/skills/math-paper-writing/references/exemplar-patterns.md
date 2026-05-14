# Mathematical Paper Exemplar Patterns

This reference distills reusable architecture from strong mathematical papers and lecture-style articles. The source Markdown is OCR-derived, so treat details as noisy. Use patterns, not wording; do not copy source prose.

For field-specific classic paper choices, first consult `classic-literature-map.md`, then load only the matching local Markdown source.

## When To Read

Read this file when planning or revising:

- a full paper outline;
- an introduction;
- a paper whose argument needs a clearer main route;
- a survey or lecture-style exposition;
- section ordering for a technical proof;
- a manuscript that feels correct but hard to read.

## Universal Patterns

### Resolution Ladder

The title, abstract, introduction, and body should all describe the whole paper at increasing resolution.

- Title: names the object, method, or result.
- Abstract: states problem, method, result, and significance in compressed form.
- Introduction: explains background, gap, contribution, method, literature position, and route.
- Body: executes the definitions, statements, proofs, examples, and applications.

If the abstract says only the topic, it is too weak. If the introduction withholds the main result until late, it is too slow. If the body introduces machinery before the reader knows the goal, it is misordered.

### Claim-Justification Locality

A reader reaching a period should know why every claim in that sentence is true, unless the sentence explicitly says that the explanation follows. This is especially important in proof prose, chains of equalities, and literature comparisons.

Use:

- "Combining Lemma 2.1 with the compactness of $X$ gives ..."
- "The next paragraph explains why this map is injective."
- "We isolate the only point where smoothness is used."

Avoid:

- asserting a result and justifying it several sentences later without warning;
- using an equation number as the whole explanation;
- hiding a major proof step under "clear" or "standard".

### Reader-Memory Reduction

Strong papers reduce what the reader must remember.

- State the role of each section before technical details.
- Break long proofs into claims or lemmas even when a lemma is used once.
- If several local statements are proved but one drives the rest of the paper, identify it.
- Reintroduce notation after a long absence.
- Use diagrams when they clarify maps, spaces, dependencies, or flows.

## Introduction Architectures

### Theorem-First Research Article

Use for concise research papers with a central theorem.

1. State the mathematical setting and the core problem.
2. Name the closest known result or standard expectation.
3. State the new theorem-level contribution early.
4. Explain the key idea or obstruction in plain prose.
5. Compare with the nearest literature.
6. Give a short route through the sections.

Good examples often place the main equivalence, fixed-point principle, comparison theorem, or construction in the first few paragraphs.

### Bridge-Between-Worlds Article

Use when the paper connects two frameworks, such as algebraic versus analytic, finite versus infinite, local versus global, or physics versus topology.

1. Present the two viewpoints.
2. Give familiar examples showing overlap.
3. State the precise bridge the paper builds.
4. Explain what machinery makes the bridge possible.
5. List applications that demonstrate the bridge's value.

Check that the introduction does not become a history essay. Every historical or contextual sentence should serve the comparison.

### Method Lecture

Use for papers built around a reusable technique rather than one theorem.

1. State the purpose of the method.
2. Give a simple first example quickly.
3. Generalize after the example.
4. Mark variants by theorem, remark, question, or exercise.
5. End sections with what the example teaches.

This works well when a reader should learn how to use a technique, not just know a result.

### Expository-Survey Route

Use for surveys, thesis background chapters, or lecture notes.

1. Begin with a familiar benchmark problem.
2. Introduce basic examples early.
3. Use examples to expose what the general theorem must explain.
4. Delay technical generality until the reader has a mental model.
5. Return periodically to the examples.

The goal is not chronological completeness. Organize by ideas and obstacles.

## Section Architectures

### Definition-To-Use

Definitions should not sit in isolation.

1. Say why the object is needed.
2. Define it with type, scope, and assumptions.
3. State a convention if notation is nonstandard.
4. Use it immediately in a lemma, proposition, example, or comparison.

If a definition will not be used soon, move it later or explain why it is being prepared now.

### Technical-Machinery Section

Use when the paper needs a toolkit before the main proof.

1. Name the local goal of the section.
2. Present only the machinery needed for the main route.
3. Separate standard facts from new lemmas.
4. Say where each nontrivial lemma will be used.
5. Close with a bridge to the main theorem.

Do not let preliminaries become a second paper.

### Main-Proof Section

Use for a long central argument.

1. Restate the inputs and desired conclusion.
2. Give a proof route before details.
3. Split the route into claims with roles.
4. Check hypotheses when invoking external theorems.
5. Reassemble the claims explicitly.
6. End with what has now been proved and what remains.

### Applications Section

Use when the main theorem has consequences.

1. Recall the main theorem in the form needed.
2. State the application setting.
3. Verify the theorem's hypotheses.
4. Derive the consequence.
5. Explain what the application adds beyond restating the theorem.

## Proof Patterns

### Quantifier-Dependency Proof

For statements with many "for all" and "there exists" clauses:

1. Introduce arbitrary inputs in the order of the statement.
2. Construct witnesses only from allowed previous data.
3. Name dependencies when helpful, such as $N_\epsilon$ or $C(X,\eta)$.
4. Prove the final property for all remaining variables.
5. Avoid reusing symbols from hypotheses for new objects.

When using a quantified hypothesis, feed it the specific input. Do not restate the entire quantified sentence with the same variable names.

### Equality-Chain Proof

A chain of equalities or inequalities is readable only when each link is justified.

- Put reasons in prose before the chain if one idea justifies the whole chain.
- Put reasons on the relevant line if different steps have different causes.
- Do not write false equalities to mean implication or transformation.
- If the chain becomes long, split it into named intermediate identities.

### Construction Paper Proof

For papers whose contribution is a construction:

1. State the universal or target property first.
2. Define the raw object.
3. Verify it is well-defined.
4. Prove structural properties in lemmas.
5. Prove the universal property or classification result.
6. Give consequences or examples.

## Style Guardrails

- Prefer concrete nouns over pronouns such as "it", "this", and "that" when the antecedent could be ambiguous.
- Keep the subject and verb close in long mathematical sentences.
- Use "we" for the author-reader path through the proof, not for unsupported authority.
- Use "such that" for conditions; use "so that" for purpose or result.
- Do not add "We now prove the following proposition" unless the sentence says why the proposition matters.
- If a proof ends with a proof symbol, do not also write a redundant proof-ending sentence.

## OCR Caution

The local exemplar Markdown contains OCR errors in names, symbols, equation layout, accents, section marks, and punctuation. Never use it as authoritative text. Use it only to infer architecture and writing moves; verify mathematical statements and bibliographic data elsewhere before citing them.
