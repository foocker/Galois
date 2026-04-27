---
name: math-paper-writing
description: Use when drafting or revising English mathematical papers, surveys, theses, abstracts, introductions, proof prose, notation, equations, conclusions, cover letters, or reviewer responses.
---

# Math Paper Writing

This skill is the primary writing layer for Galois Paper Writing. It integrates the local mathematical-English writing guide and adapts it into an executable agent workflow.

## Supporting References

This skill has local supporting files:

- `references/principles.md`: compact principles for quick checks.
- `references/guide.md`: detailed mathematical paper-writing guide with section rules, revision workflow, submission workflow, and product module design.
- `references/case-library.md`: parsed Markdown case cards replacing raw PDF dependence.

Use them deliberately:

- For a short local rewrite, use this `SKILL.md` and `principles.md`.
- For a full manuscript, abstract, introduction, proof, revision, or submission task, consult `guide.md`.
- For title, abstract, proof, revision, cover-letter, response-letter, survey, or review examples, consult `case-library.md`.
- Never require PDF files. Never copy long passages from source books or papers.

## Core Standard

Mathematical writing is not generic English polishing. A good mathematical paper answers:

1. What is new?
2. Why is it mathematically credible?
3. Can the intended reader follow the definitions, results, proofs, and context?

Preserve mathematical claims. Do not strengthen theorem statements, hide assumptions, invent novelty, or fabricate citations. When the draft is incomplete, write around the gap honestly and turn the missing information into revision tasks.

## Paper Structure

### Title

Evaluate title candidates by accuracy, concision, specificity, and searchability.

- Identify the main object, method, or result.
- Avoid generic forms such as "A study of ..." unless the object and result are explicit.
- Avoid unnecessary formulas, internal numbering, abbreviations, and padded modifiers.
- Generate variants when useful: object-first, method-first, result-first, short-title.
- If the title says only the topic, add the actual result, object, obstruction, or method.
- If the title contains a formula, ask whether a named object or phrase would be clearer for indexing.

Output when asked to improve a title:

1. One recommended title.
2. Three alternatives with different emphasis.
3. A one-line reason for each.
4. A warning if the current title overclaims.

### Abstract

The abstract is a compressed version of the paper, not a stitched introduction.

- State background/problem, method or core idea, result, and significance.
- Keep it self-contained: no citation numbers, equation numbers, figure references, or theorem labels that require the body.
- Do not overclaim beyond the theorem statements.
- Compress to target length when requested.
- Do not start with empty phrases such as "In this paper, we study..." unless the next words immediately identify the precise problem and contribution.
- Do not mention proof details, definitions, table numbers, theorem numbers, or internal section references unless the target venue explicitly permits it.

Build an abstract from these slots:

1. Problem: the object and question.
2. Gap: what previous methods/results do not cover.
3. Method: the construction, estimate, framework, algorithm, or comparison idea.
4. Result: the strongest precise statement the draft supports.
5. Significance: what assumption is weakened, conclusion strengthened, class enlarged, constant sharpened, or obstacle resolved.

When criticizing an abstract, check: self-containment, missing result, missing method, mismatch with title, unsupported significance, excessive technical detail, and length.

### Introduction

Use a background -> gap -> problem -> contribution -> relation-to-literature -> outline structure.

- Keep background short enough that the research problem appears early.
- Explain logical relationships among prior results, not just a citation list.
- Calibrate novelty claims to what the manuscript proves.
- Avoid unfair descriptions of prior work.
- Add a paper outline only when it helps navigation.
- Do not write a textbook-style background section. Every background paragraph should move toward the paper's problem.
- Do not stack citations without explaining the mathematical relation among them.
- Avoid "to the best of our knowledge" unless the literature check supports it.

Concrete introduction plan:

1. Opening paragraph: field and concrete problem, not broad ceremonial history.
2. Known results: name the closest results and their assumptions/conclusions.
3. Difficulty/gap: state the obstruction or missing case.
4. Main contribution: state theorem-level contribution in plain prose.
5. Method: explain the new idea enough that the reader sees why it works.
6. Literature position: compare against direct predecessors.
7. Organization: brief map of sections.

### Body and Results

Organize by the mathematical route of the argument.

- Introduce definitions only when needed.
- Use theorem/proposition/lemma/corollary hierarchy intentionally.
- Reserve "Theorem" for central results.
- Split long proofs into lemmas when it clarifies dependency structure.
- Use appendices for long technical details, standard background, or large calculations, not for hiding the main idea.
- Start each major section with its local goal.
- End a difficult section with a bridge sentence explaining what was established and how it will be used.
- Avoid single-subsection sections unless the journal style or exposition really needs them.
- Do not dump preliminaries before the reader knows why they matter; move definitions near first use when possible.

For computational or applied mathematics, require clear model assumptions, algorithms, error or complexity claims, experiment setup, and evidence that computations support stated claims.

### Proof Prose

Proofs must be readable arguments, not symbol dumps.

- Start long proofs with strategy.
- State where each hypothesis is used.
- Explain nontrivial steps; do not rely on "clear", "obvious", or "standard" without support.
- Embed displayed equations in grammatical prose.
- Put prose between adjacent displays.
- Label only equations referenced later.
- Cite external theorems precisely, preferably with theorem number, section, or page.
- For a long proof, first write a proof route: inputs, intermediate claims, final mechanism.
- If the proof uses cases, name the purpose of each case.
- If the proof invokes compactness, convergence, regularity, density, boundedness, measurability, or independence, say where the hypothesis comes from.
- If only a special case is proved, do not write the general theorem as proved.

Do not do these:

- Do not write "obvious", "clear", "easily follows", or "standard" at a nontrivial implication without giving the reason or citation.
- Do not let notation change meaning inside the proof.
- Do not use equation numbers as the explanation of the argument.
- Do not end a proof with an unintroduced symbol or unexplained limit.

### Definitions and Notation

Treat every symbol as cognitive load.

- Define symbols at first use and reuse them consistently.
- Avoid overloaded notation unless the convention is standard and harmless.
- Make definitions rigorous but not needlessly verbose.
- Reintroduce old notation after long gaps.
- Flag notation conflicts in the review report.
- Build a notation table when the manuscript has many symbols. Columns: symbol, meaning, first use, scope, later conflicts.
- Delete definitions and abbreviations that are never used.
- Prefer standard field notation unless the manuscript explains a deliberate departure.

Run a notation table pass when revising a full draft:

1. Extract every new symbol, operator, space, index set, norm, and abbreviation.
2. Record first-use definition.
3. Check whether the same symbol has multiple meanings.
4. Check whether one concept has multiple symbols.
5. Return conflicts as revision tasks.

### Formulas and Equations

Use formulas to support reading, not to replace prose.

- Display long, central, or multi-line formulas.
- Keep short expressions inline when this preserves flow.
- Introduce every important display before it appears.
- Explain what follows from the display after it appears.
- Punctuate formulas as parts of sentences.
- Align multi-line displays around the mathematical relation.

Run an equation label audit:

1. Find every label or numbered equation.
2. Check whether it is referenced later.
3. Remove numbers for unreferenced formulas unless the venue requires numbering.
4. Find broken references.
5. Replace "from (3.2)" alone with a sentence explaining what (3.2) gives.

### Conclusion

The conclusion closes the paper; it does not repeat the abstract.

- Return to the main result and method.
- State limitations or future questions when appropriate.
- Do not introduce unsupported new conclusions.
- Avoid self-promotion.
- Do not use the conclusion to announce results that were not proved.
- Mention limitations and future questions only if they follow naturally from the work.

### Acknowledgments

Keep acknowledgments specific and restrained.

- Confirm funding names and grant numbers.
- Thank people for concrete help when known.
- Thank anonymous referees in revised versions when appropriate.
- Do not invent institutional support or exaggerated praise.

### Appendix

Use appendices to protect the main line.

Good appendix material: long technical proofs, standard background, large calculations, supplementary experiments, notation lists, and related material that interrupts the main text.

Bad appendix material: the main idea of the main theorem, definitions required immediately in the body, or key proof steps hidden to avoid explaining a gap.

### References, Keywords, MSC

- Every bibliography entry should be cited or marked as background.
- Every cited important result should appear in the bibliography.
- Prefer original sources for core theorems.
- Keywords should be specific field terms, not broad labels like "mathematics".
- MSC suggestions must be labeled as candidates unless verified.
- When citing a theorem, include author and theorem/section/page when possible.
- Do not cite hard-to-access unpublished material when a published source is available.
- Keep bibliography quantity meaningful; references document sources and position the work, not status.

## Paragraph and Transition Rules

Run a paragraph transitions pass on dense sections:

1. Label each paragraph as background, definition, result, proof, discussion, comparison, summary, or transition.
2. Check that each paragraph has one main job.
3. Add a first sentence when the paragraph changes goal.
4. Add a closing sentence when the result will be used later.
5. Insert bridges between definition -> proposition, lemma -> theorem, proof -> consequence, and prior work -> contribution.

Use transitions for these functions:

- Continuation: "We now pass from local estimates to the global argument."
- Contrast: "The preceding argument fails without compactness because ..."
- Causation: "This bound implies tightness, which is the only point where ..."
- Comparison: "Unlike [prior result], the present theorem removes ..."
- Summary: "Thus the construction gives the required extension."
- Preview: "The next section verifies the hypotheses of ..."

Do not leave long sequences of definitions, theorems, and proofs with no explanatory prose.

## Revision and Polishing Procedure

### Deletion Pass

Always run a deletion pass before sentence polishing.

Delete or flag:

- empty phrases;
- repeated sentences;
- unnecessary adjectives and adverbs;
- unused symbols, definitions, and abbreviations;
- equation numbers that are never referenced;
- background unrelated to the main line;
- tables or dense data without information value;
- claims that repeat the abstract without adding information.

If deletion might remove mathematical content, move it to a revision task instead of deleting silently.

### Main Thread Pass

Identify the manuscript's main contribution in one sentence. Then check every section against it.

- Secondary results should support the main result.
- Literature review should be organized around the problem, not chronology alone.
- Figures, examples, and computations should support stated claims.
- Off-topic paragraphs should be moved, compressed, or removed.

### Structural Revision Pass

Check:

- heading levels are logical;
- there are no tiny sections unless justified;
- definitions are not dumped too early;
- preliminaries appear where readers need them;
- long proofs do not block the main line;
- motivation appears before conclusions that depend on it.

Output a revised table of contents when structure is the main problem.

### Figure and Table Pass

Figures and tables are evidence, not decoration.

- Captions should be self-contained.
- Every figure/table should be mentioned in the text.
- Symbols, colors, line styles, and units should be defined.
- Numerical tables should support a claim.
- Third-party images require permission and citation.

### Integrity Pass

Check for:

- direct text reused without quotation and citation;
- close paraphrase of a source;
- translated source text without attribution;
- reuse of the author's published text without caution;
- copied figures, tables, or proof blocks without permission or citation.

Do not produce unsourced literature prose. Require source material or mark `lookup_needed`.

## Submission and Publication Workflow

### Submission Checklist

Before submission, verify:

- title is accurate and informative;
- abstract is self-contained and states problem, method, and result;
- introduction gives motivation, literature relation, contribution, and structure;
- theorem assumptions are complete;
- proofs do not contain unexplained jumps;
- notation is consistent and unused symbols are removed;
- equation numbers are necessary and referenced;
- figures and tables are explained in the text;
- conclusion is not a repeated abstract;
- references are complete, accurate, and consistently formatted;
- text citations and bibliography match bidirectionally;
- funding and acknowledgments are accurate;
- no unauthorized copying, improper paraphrase, or image-permission issue remains.

### Journal Fit

Run a journal fit pass when target journal information is provided:

1. Check field match and readership.
2. Check paper length and article type.
3. Check LaTeX template and bibliography style.
4. Check rules on preprints, color figures, appendices, supplementary material, MSC, keywords, and author declarations.
5. Create formatting and submission tasks.

Do not invent journal requirements. If author instructions are absent, ask for them or mark `lookup_needed`.

### Cover Letter

A mathematical cover letter should be concise:

- title;
- article type;
- originality/no simultaneous submission statement if requested;
- brief contribution statement;
- corresponding author details;
- optional suggested editors/referees only when requested.

Do not oversell the paper with vague praise.

### Reviewer Response Matrix

When reviewer comments are provided, create a reviewer response matrix:

| Comment | Type | Manuscript change | Response stance | Location | Remaining risk |
| --- | --- | --- | --- | --- | --- |

Types: mathematical error, exposition, citation, format, optional suggestion, misunderstanding.

Response stances:

- accepted and changed;
- clarified in manuscript;
- partially changed;
- not changed with technical reason;
- requires author decision.

Write responses point by point. Stay technical and calm. Include page, section, theorem, or equation locations when available.

### Proof Stage

The proof stage is for typesetting and factual corrections, not rewriting the paper.

Check:

- symbols, subscripts, superscripts, hats, norms, and parentheses;
- formula line breaks;
- author names, affiliations, funding, and references;
- figure/table clarity;
- editor queries one by one;
- deadline and return instructions.

Do not introduce new arguments or restructure the paper at proof stage unless the editor explicitly permits it.

## Special Document Types

### Survey Mode

A survey is not a list of results.

- Organize by ideas, methods, and historical development.
- Explain why definitions and theorems matter.
- Include key original papers, important books, and recent progress.
- For central theorems, give proof ideas or special cases when helpful.
- End with future directions and open problems.

### Reading Report

A reading report extracts ideas.

- Restate problem, method, and conclusion in the writer's own words.
- Explain why the authors use their approach.
- Give simplified proof routes or special cases for key arguments.
- State the result's position in the field.
- Mark what is understood and what questions remain.

Do not merely repeat the abstract or list theorem statements.

### Thesis Mode

A thesis is more self-contained than a journal paper.

- Provide fuller background and preliminaries.
- Follow university formatting requirements.
- Connect chapters into one research program.
- Make original contributions explicit.
- Include limitations and future work.

Typical thesis structure: problem/background, literature review, preliminaries, author's method/results, proofs/experiments, summary/contributions/limitations/future work.

## Revision Modes

### Generate

When generating a section from theorem/proof notes:

1. Extract claims, assumptions, objects, methods, and dependencies.
2. Build a section outline before prose.
3. Draft polished English with LaTeX math.
4. Mark missing proof/citation data as explicit assumptions or revision tasks.

### Revise

When revising user prose:

1. Diagnose the issue first: structure, contribution, proof clarity, notation, English, or citation.
2. Preserve claims and notation unless clearly erroneous.
3. Rewrite only the requested surface.
4. Mention any mathematical risks separately in `review_report.md`.

### Reviewer Response

For reviewer comments:

- Answer point by point.
- Separate accepted changes, clarifications, and technical disagreements.
- Keep technical disagreements precise and polite.
- Cite changed manuscript locations when available.
- Convert unresolved issues into revision tasks.

## Output Rules

- Write complete paragraphs for manuscript prose.
- Use Markdown headings and LaTeX math.
- Inline math uses `$...$`; display math uses `$$...$$`.
- Do not include workflow diary, hidden reasoning, or process notes in `manuscript_draft.md`.
- If the user asks only for review, keep `manuscript_draft.md` short and say no rewrite was requested.
