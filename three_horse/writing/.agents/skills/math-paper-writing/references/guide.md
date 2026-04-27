# Mathematical Paper Writing Guide

Source: distilled from the local mathematical English writing book notes used to build this skill.

Purpose: provide writing rules, review checklists, product modules, and evaluation criteria for the Galois Paper Writing page. This guide is a structured extraction and product translation. It does not reproduce long passages from the source book.

## 0. Positioning

The core problem is not generic English polishing. The goal is to help a mathematician turn mathematical ideas into a paper that is readable, credible, and publishable.

For Galois, the book-derived material should become four capabilities:

1. Draft generation: guide the user from title, abstract, introduction, body, proofs, and conclusion toward a coherent manuscript.
2. Writing diagnosis: detect vague contributions, loose structure, notation conflicts, proof gaps, and reference problems.
3. Revision workflow: convert comments from reviewers, advisors, or AI review into concrete editing tasks.
4. Academic standards: enforce originality, citation, copyright, submission format, reviewer response, and proof-stage checks.

Important product premise: Paper Writing should first be an independent mathematical writing tool. It should not depend on a Galois run. Later, Galois run outputs can be imported as optional theorem, proof, computation, or search material.

## 1. Overall Standard for a Mathematical Paper

A mathematical paper must answer three questions:

1. Does it contain a new contribution?
2. Is the mathematics correct?
3. Is the exposition clear enough for the intended reader?

Novelty and correctness determine whether the paper deserves to exist. Clarity determines whether readers, referees, and later researchers can actually use it.

Galois diagnostic dimensions:

| Dimension | Core question | Product feature |
| --- | --- | --- |
| Contribution | What is new, and how does it advance the literature? | Contribution checker |
| Correctness | Are assumptions, proof chains, and formula derivations complete? | Proof gap reviewer |
| Readability | Can a reader follow the motivation, definitions, results, and proofs? | Structure reviewer |
| Conventions | Do title, abstract, keywords, references, figures, and format meet journal norms? | Submission checklist |
| Integrity | Are sources cited correctly and is improper reuse avoided? | Citation and originality guard |

## 2. Paper Structure

### 2.1 Title

A good title is accurate, concise, specific, and informative. It is neither a slogan nor a research-plan heading.

Checklist:

- It identifies the main object, method, or result.
- It is not padded with unnecessary modifiers.
- It is not too generic, such as "A study of ..." without the actual result.
- It avoids repeated technical words that make it heavy.
- It avoids unnecessary formulas, abbreviations, and internal numbering.
- It lets specialists infer the field and problem class.

Galois features:

- Title evaluator: score accuracy, concision, information density, and searchability.
- Title variants: generate 3 to 5 versions, such as object-first, method-first, result-first, and short-title variants.

### 2.2 Abstract

The abstract is a compressed version of the paper, not a stitched introduction or conclusion. It should quickly tell the reader the problem, the main idea or method, and the most important result.

Checklist:

- Self-contained, with no equation numbers, figure numbers, or citation numbers.
- Avoids excessive technical detail.
- States the core contribution instead of saying only "we study ..."
- Matches the title and does not overstate or understate the paper.
- Can be understood when indexed separately by a database.
- Fits the journal length limit.
- Avoids empty phrases such as "this result is important" without explaining why.

Useful structure:

1. Background and problem: what mathematical problem is treated and why it matters.
2. Method and idea: the key construction, estimate, algorithm, or framework.
3. Result and significance: what is proved, improved, generalized, or made applicable.

Galois features:

- Abstract builder: generate an abstract from the problem, method, main theorem, and comparison target.
- Abstract critic: check self-containment, internal references, and missing contribution statements.
- Abstract compression: reduce a 250-word abstract to a 150-word or journal-limited version.

### 2.3 Introduction

The introduction brings the reader to the problem and explains why the paper is worth reading.

Recommended structure:

1. Enter from a broad background without writing a textbook section.
2. Identify known results, difficulties, or gaps.
3. State the problem addressed by the paper.
4. Summarize the main results and methods.
5. Explain the relation to existing work.
6. Outline the paper.

Common problems:

- Background is too long and the real problem appears too late.
- Literature is piled up without explaining logical relationships.
- Existing work is described unfairly.
- Claims exceed what the paper proves.
- Readers outside the narrow subfield get too little motivation.

Galois features:

- Introduction planner: build a background -> gap -> contribution -> outline plan.
- Literature positioning: help rewrite prior work as an objective research trajectory.
- Claim calibration: check whether contribution claims exceed the theorem statements.

### 2.4 Body

The body should follow the natural order of the mathematical ideas, not mechanically pile up results.

For theoretical papers:

- Introduce definitions when they are needed.
- Use theorem, proposition, lemma, and corollary hierarchy intentionally.
- Reserve "theorem" for important results.
- Split long proofs into lemmas when that helps the reader.
- Move highly technical material to an appendix only if the main line remains complete.
- Start a section with a brief goal and end it with a short bridge when useful.

For computational or applied mathematics papers:

- State the model, assumptions, algorithm, error, complexity, and experiment setup clearly.
- Explain computational value, efficiency, stability, or range of applicability.
- Align numerical experiments with the paper's claims.
- Use figures and tables to support conclusions, not to dump data.

Galois features:

- Section outline checker: detect fragmented sections, single-subsection sections, and unbalanced headings.
- Theorem hierarchy adviser: suggest theorem, proposition, lemma, and corollary roles.
- Computation evidence checker: verify whether experiments support claims in applied or computational papers.

### 2.5 Conclusion

The conclusion is not a repeated abstract. It should close the paper by summarizing completed work and giving reasonable directions.

Checklist:

- It returns to the main result clearly.
- It does not introduce unsupported new conclusions.
- It states limitations or future questions when appropriate.
- It avoids self-promotion.
- It complements the abstract: the abstract opens the paper, the conclusion closes it.

Galois features:

- Conclusion builder: draft a conclusion from the main theorem, method, limitations, and future work.
- Abstract-conclusion overlap checker: detect conclusions that merely rewrite the abstract.

### 2.6 Acknowledgments

Acknowledgments should be specific, truthful, and restrained.

Checklist:

- Funding is acknowledged accurately.
- People who gave substantive help are named appropriately.
- Anonymous referees are thanked in revised versions when useful.
- Formulaic or exaggerated praise is avoided.

Galois feature:

- Acknowledgment checklist: generate items for funding, advisors, collaborators, referees, and host institutions that the author must confirm.

### 2.7 References

References must be complete, accurate, consistent, and relevant. They are not a display of quantity. They document sources and position the research.

Checklist:

- Every bibliography entry is cited in the text.
- Every cited important result appears in the bibliography.
- Author names, title, journal, volume, pages, and year are accurate.
- Formatting is consistent and matches the target journal.
- Original sources are cited when possible, not only secondary surveys.
- When a theorem is cited, author, theorem number, page, or section is given when useful.
- Unpublished or hard-to-access items are not used unnecessarily.

Galois features:

- Citation consistency checker: bidirectional check between manuscript citations and BibTeX entries.
- Reference formatter: normalize references for AMS, SIAM, Springer, or other styles.
- Missing-citation detector: find named theorems or methods without a source.

### 2.8 Appendix

An appendix protects the main line of the paper.

Good appendix material:

- Long or highly technical proofs.
- Standard but necessary background.
- Large calculations.
- Supplementary experiments, tables, or notation lists.
- Related material that would interrupt the main text.

Poor appendix material:

- The main idea of the main theorem.
- Definitions required immediately for the body.
- Key proof steps used to hide a logical gap.

Galois feature:

- Appendix adviser: detect long proofs, excessive preliminaries, and oversized tables, then suggest what to move or keep.

### 2.9 Keywords, MSC, and Section Headings

Keywords support search. MSC codes support classification. Section headings show the skeleton of the paper.

Checklist:

- Use a small number of meaningful keywords.
- Avoid words too broad for the paper, such as "mathematics" or generic "differential equation" when a more specific term exists.
- Prefer terminology used by the field.
- Match MSC codes to the core direction of the paper.
- Make headings reveal the route of the argument.

Galois features:

- Keyword and MSC suggester: infer candidate keywords and MSC codes from abstract, theorem statements, and references.
- Heading normalizer: standardize capitalization, numbering, terminology, and heading granularity.

## 3. Mathematical English and Proof Language

### 3.1 Mathematical Prose

A mathematical article is not a pile of symbols. Good mathematical English should feel explanatory.

Rules:

- Do not replace clear language with symbols too early.
- Embed formulas in grammatical sentences.
- Avoid abrupt sentence beginnings or endings with isolated symbols.
- Add prose between adjacent displayed formulas.
- Split long sentences, especially when subject and verb are far apart.
- Passive voice is allowed, but not when it makes the sentence heavy.
- Define or cite terms that the intended reader may not know.

Galois features:

- Math prose reviewer: flag high symbol density, long sentences, and formulas without explanation.
- Sentence splitter: divide long sentences while preserving mathematical meaning.

### 3.2 Definitions and Notation

Definitions and notation are cognitive load. Every new symbol is something the reader must remember.

Rules:

- Define new concepts only when needed.
- Use already defined concepts, or concepts assumed known by the target audience, inside definitions.
- Make definitions rigorous, concise, and understandable.
- Keep symbols and fonts consistent for the same concept.
- Do not reuse a symbol for different nearby objects.
- Prefer standard notation in the field.
- Put important notation in a notation table.
- Reintroduce notation briefly when it has not appeared for a while.

Galois features:

- Notation table: extract symbols, first-use locations, definitions, and later uses.
- Notation conflict checker: detect one symbol with multiple meanings or one concept with multiple symbols.
- Unused definition detector: identify terms or symbols that are defined but not used.

### 3.3 Formulas and Equation Numbers

Formulas should support reasoning, not become reading obstacles.

Rules:

- Number only formulas that are referenced later.
- Display long or important formulas.
- Keep short expressions inline when that improves readability.
- Add punctuation and explanation around formulas.
- Do not use equation numbers as substitutes for mathematical description.
- Align and format displayed formulas cleanly.

Galois features:

- Equation label cleaner: find unused labels and broken references.
- Formula narrative checker: check whether formulas are introduced and explained.

### 3.4 Proof Writing

The goal of a proof is not to convince the author, but to convince the reader.

Rules:

- State the proof strategy for long proofs.
- Do not hide nontrivial steps behind "obvious", "clear", or "easy".
- If the proof has steps, state each step's goal.
- Split long proofs of important results into lemmas when helpful.
- Give each lemma a clear purpose.
- Cite existing results accurately.
- Mark the end of the proof clearly.
- If a result is not proved, say whether it is standard, similar, follows from a reference, or is outside scope.

Common proof problems:

- Missing hypotheses.
- Mismatch between theorem statement and proof assumptions.
- Large reasoning jumps.
- Cited theorems used without checking hypotheses.
- Notation changes meaning inside the proof.
- Only a special case is checked while a general conclusion is claimed.

Galois features:

- Proof plan generator: decompose a theorem into a proof route.
- Proof gap reviewer: check assumptions, goals, citations, and reasoning steps.
- Obviousness checker: flag "obvious", "clear", and "easy" near nontrivial implications.

### 3.5 Transitions and Paragraphs

Mathematical writing needs logical signposts.

Paragraph rules:

- Each paragraph should have one main job.
- The first sentence should connect to the previous text or introduce a new goal.
- The last sentence may explain how the paragraph will be used later.
- Avoid long sequences of definitions, theorems, and proofs with no explanatory prose.

Transition functions:

| Function | Writing task |
| --- | --- |
| Continuation | Move from definition to proposition or from lemma to theorem |
| Contrast | Explain the limitation of existing methods |
| Causation | Explain why a condition leads to a conclusion |
| Comparison | Compare the paper's result with prior work |
| Summary | Close a section or proof |
| Preview | Tell readers what the next section does |

Galois features:

- Transition suggester: generate bridge sentences between paragraphs.
- Paragraph role labeler: label paragraphs as background, definition, result, proof, discussion, or transition.

## 4. Revision and Polishing

### 4.1 Deletion

Revision begins with deletion.

Delete candidates:

- Empty phrases.
- Repeated sentences.
- Unnecessary adjectives and adverbs.
- Unused symbols, definitions, and abbreviations.
- Equation numbers that are never referenced.
- Background unrelated to the main line.
- Tables or dense data without information value.

Galois features:

- Deletion candidates: mark removable phrases, repeated paragraphs, and unused definitions.
- Abbreviation audit: check whether abbreviations are too many or actually reduce reading cost.

### 4.2 Emphasis and Main Thread

A paper must have a main line. It should not read like a textbook, data dump, or complete lab notebook.

Rules:

- Identify one main contribution.
- Make secondary results support the main result.
- Arrange the structure around the main line.
- Organize the literature review around the paper's problem.
- Use figures and experiments to support claims.

Galois features:

- Main-thread extractor: extract the main contribution and the structure supporting it.
- Off-topic detector: flag paragraphs weakly related to the main line.

### 4.3 Structural Revision

Structural problems are often more serious than sentence-level grammar.

Checklist:

- Heading levels are logical.
- There are no tiny sections or single-subsection sections unless justified.
- Long proofs do not block the main line.
- Definitions are not dumped before they are used.
- Preliminaries are placed where readers need them.
- Motivation appears before conclusions that depend on it.

Galois features:

- Outline refactor assistant: propose a reorganized table of contents.
- Section balance chart: show words, formulas, theorems, and citations per section.

### 4.4 Figures and Tables

Figures and tables should explain mathematical or computational facts. They are not decoration.

Rules:

- Captions should be self-contained.
- Each figure or table should be explicitly connected to the text.
- Numerical results should support a stated claim.
- Symbols, line styles, colors, and units should be clear.
- Tables should not contain excessive irrelevant data.
- Third-party images require permission and citation.

Galois features:

- Figure/table checklist: inspect captions, citations, data meaning, and copyright status.
- Experiment evidence reviewer: assess coverage and persuasiveness of numerical experiments.

### 4.5 Anti-Plagiarism and Citation Standards

Mathematical writing must avoid plagiarism and improper reuse.

Rules:

- Direct text from another source requires quotation and citation.
- Changing a few words or word order can still be improper paraphrase.
- Translating another author's text still requires attribution.
- Reusing one's own published text requires caution, especially with coauthors or transferred copyright.
- Using another author's figure, table, or long proof requires permission and citation when applicable.
- When using another author's result, make attribution precise.

Galois features:

- Citation safety guard: warn about source-like sentences and standard results without citations.
- Paraphrase assistant: require a source and produce attributed rewriting, not unsupported paraphrase.

### 4.6 Pre-Submission Checklist

Final review should check:

- Title is accurate, concise, and informative.
- Abstract is self-contained and covers problem, method, and result.
- Introduction gives motivation, literature relation, contribution, and structure.
- Theorem assumptions are complete.
- Proofs do not contain unexplained jumps.
- Notation is consistent and unused symbols are removed.
- Equation numbers are necessary and referenced.
- Figures and tables are explained in the text.
- Conclusion is not a repeated abstract.
- References are complete, accurate, and consistently formatted.
- Text citations and bibliography entries match bidirectionally.
- Funding and substantive help are acknowledged correctly.
- Spelling, grammar, punctuation, and capitalization are checked.
- No unauthorized copying, improper paraphrase, or image-permission issue remains.

## 5. Submission, Refereeing, and Publication

### 5.1 Submission Preparation

Before submission, the author must judge whether the paper is publishable and choose an appropriate journal.

Journal-fit dimensions:

- Field match.
- Journal quality, readership, and rejection rate.
- Review and publication timeline.
- Length, format, and LaTeX template.
- Rules on preprints, color figures, appendices, and supplementary material.
- Requirements for MSC, keywords, and author declarations.

Galois features:

- Journal fit worksheet: collect target journal requirements and produce a pre-submission task list.
- Instructions parser: extract format requirements from pasted author guidelines.

### 5.2 Cover Letter

A cover letter should briefly state the submission intent, title, originality, no simultaneous submission, and corresponding author information. Mathematical cover letters usually do not need heavy promotion.

Galois feature:

- Cover letter generator: draft a concise cover letter from journal, title, authors, and originality statement.

### 5.3 Handling Reviewer Comments

After reviews arrive, the correct order is to understand, classify, revise, and respond.

Rules:

- Read every comment, not only the recommendation.
- Separate mathematical errors, exposition problems, citation problems, format issues, and optional suggestions.
- Modify the manuscript directly when the comment is right.
- If disagreeing, give a clear, polite, technical reason.
- Reply point by point.
- Include page, section, theorem, or equation locations where possible.
- Do not answer emotionally.

Galois features:

- Reviewer-response workbench: parse reviews into a task list.
- Response letter generator: draft "changed", "clarified", or "not changed because ..." responses.
- Revision diff summary: summarize changed locations for the response letter.

### 5.4 Proof Stage

The proof stage is for correcting typesetting, notation, spelling, missing words, and editor queries. It is not for rewriting the paper.

Checklist:

- Mathematical symbols are typeset correctly.
- Subscripts, superscripts, hats, norms, and parentheses are correct.
- Formula line breaks do not change meaning.
- Author names, affiliations, funding, and references are correct.
- Figures and tables are clear.
- Editor queries are answered one by one.
- Proofs are returned before the deadline.

Galois feature:

- Proofreading mode: line-by-line inspection of symbols, formulas, citations, figures, and author information.

## 6. Surveys, Reading Reports, and Theses

### 6.1 Survey Articles

A survey is not a list of results. It organizes the ideas, history, methods, and present state of a field.

Rules:

- Enter from concrete and accessible problems.
- Explain the development of concepts and methods.
- Give ideas, structure, and impact rather than excessive technical detail.
- For important theorems, consider proof ideas or special cases.
- Cover key original papers, important books, and recent progress.
- End with future directions and open problems.

Galois features:

- Survey planner: create a survey outline from topic, target reader, and core literature.
- Literature map: organize literature by ideas rather than mechanically by year.

### 6.2 Reading Reports

The goal of a reading report is to extract ideas, not to repeat abstracts or theorem lists.

Rules:

- Restate the problem, method, and conclusion in the writer's own words.
- Explain why the authors take their approach.
- For key proofs, give a special case or simplified route when useful.
- Evaluate the result's position in the field.
- State what the writer truly understands and what questions remain.

Galois features:

- Paper reading note: summarize a paper as problem, idea, result, proof route, risk points, and follow-up questions.
- Seminar report generator: turn reading notes into a talk or report outline.

### 6.3 Theses

A thesis must be more self-contained than a journal paper. The main readers are advisors and the defense committee, but clarity and academic standards still matter.

Typical traits:

- Format is governed by the university.
- Chapters are longer than paper sections.
- Background and preliminaries are more complete.
- Several related topics may be covered.
- A PhD thesis must demonstrate original contribution.

Recommended structure:

1. Research problem and background.
2. Literature review and state of the art.
3. Preliminaries and tools.
4. Author's method, theorem, algorithm, or model.
5. Proofs, experiments, and analysis.
6. Summary, contributions, limitations, and future work.

Galois features:

- Thesis mode: separate from paper mode, with more background, fuller preliminaries, and stricter format checks.
- Defense preparation: generate a defense outline and likely questions from the thesis.

## 7. Refereeing and Review Writing as Self-Diagnosis

Referee standards can be turned into self-review standards.

Self-review questions:

- Is the paper suitable for the target journal?
- Are the results new, correct, and meaningful?
- Are the proofs complete?
- Is the relation to existing literature clear?
- Are the title and abstract accurate?
- Is the organization clear?
- Are references accurate and complete?
- Does the English obstruct understanding?

Lessons from book reviews and paper reviews:

- Do not merely list contents. Extract ideas.
- A good review helps readers understand why a work matters.
- Evaluation of others' work must be objective and evidence-based.
- Negative judgments should be specific, careful, and verifiable.

Galois features:

- Self-referee mode: produce an accept, minor revision, major revision, or reject-style self-review.
- Paper review writer: help write reading reports, review essays, or referee reports.

## 8. Galois Paper Writing Page Design

### 8.1 Page Positioning

Recommended page name: `Paper Writing`.

Definition: an independent mathematical paper writing workspace that helps users form, revise, review, and export English mathematical manuscripts from ideas, theorems, proofs, and literature.

The first version should not depend on:

- Galois run.
- Automatic problem-solving results as the only input.
- The user already having a complete proof.

Optional inputs:

- Paper title or research problem.
- Main theorem draft.
- Proof draft.
- Literature list or BibTeX.
- LaTeX source.
- Reviewer comments.
- Journal author instructions.
- Galois run results as future optional material.

### 8.2 Workflow

Recommended workflow:

1. Project setup: choose paper, survey, thesis, reading report, or review response.
2. Outline: generate or edit title, abstract, and section structure.
3. Manuscript editor: write LaTeX or Markdown.
4. Math writing tools: local tools for title, abstract, introduction, proof, notation, equations, and figures.
5. Citation library: manage BibTeX, citation consistency, and literature positioning.
6. Review: run structure review, proof review, language review, and submission checklist.
7. Revision board: turn findings into tasks.
8. Export: produce LaTeX, PDF, BibTeX, response letter, or submission bundle.

### 8.3 Module Split

| Module | Input | Output |
| --- | --- | --- |
| Project setup | Type, field, target reader, journal | Project configuration |
| Outline planner | Topic, main result, literature | Paper outline |
| Section assistant | Current section and goal | Local draft or revision suggestions |
| Proof assistant | Theorem and proof draft | Proof route, gaps, rewrite suggestions |
| Notation manager | LaTeX source | Notation table and conflict report |
| Citation manager | BibTeX and manuscript | Citation consistency report |
| Review engine | Full manuscript | Multi-dimensional review report |
| Revision board | Review report | Actionable revision tasks |
| Submission kit | Target journal and final draft | Cover letter, checklist, export bundle |

### 8.4 MVP Scope

The first version should be small but complete:

1. Create a mathematical writing project.
2. Let users paste or edit LaTeX or Markdown drafts.
3. Provide six local checkers: title, abstract, introduction, proof, notation, and references.
4. Provide one-click self-referee report.
5. Generate revision tasks.
6. Export Markdown or LaTeX.

Defer:

- Complex collaborative editing.
- Full PDF typesetting service.
- Deep Galois run integration.
- Large-scale automatic full-text literature crawling.
- Large-scale plagiarism detection.

### 8.5 Later Enhancements

Second-stage features:

- Matlas theorem search as a theorem and definition sidebar.
- arXiv or MathSciNet-style literature search entry.
- Import theorem, proof, and result snippets from Galois run.
- Journal templates and submission bundle generation.
- Defense presentation generation.
- Reading report and survey-writing modes.

## 9. Rule Library Sketch

These rules can later become a structured review engine.

```yaml
- id: title.too_generic
  area: title
  severity: warning
  check: "Title contains generic phrases without a mathematical object, method, or result."
  message: "The title is too generic. Add the specific object, method, or main result."

- id: abstract.has_internal_reference
  area: abstract
  severity: error
  check: "Abstract references equation, table, figure, or citation numbers."
  message: "The abstract should be self-contained. Remove internal numbering and citation-number dependencies."

- id: proof.obvious_gap
  area: proof
  severity: warning
  check: "Proof uses obvious, clear, or easy near a nontrivial implication."
  message: "This may hide a proof gap. Add the missing reason or cite a precise result."

- id: notation.reused_symbol
  area: notation
  severity: error
  check: "Same symbol is assigned multiple meanings in nearby sections."
  message: "The symbol has conflicting meanings. Rename or unify the notation."

- id: equation.unused_label
  area: formula
  severity: info
  check: "Equation has a label but no references."
  message: "This equation label is not referenced later. Remove the number unless it is needed."

- id: citation.unused_bib_entry
  area: citation
  severity: warning
  check: "Bibliography entry is not cited in the manuscript."
  message: "This bibliography entry is unused. Cite it or remove it."
```

## 10. Relation to Other Retained References

`references/scientific-agent-skills` can provide general scientific-writing, literature-review, citation-management, and peer-review workflow references. Biomedical, generic science, and autonomous-agent orchestration parts should remain out of the mathematical writing core.

`references/math-ai-review-skills` is useful for review-engine standards: mathematical correctness, contribution, proof rigor, literature positioning, and clarity.

This book-derived skill should be the most concrete mathematical writing base, especially for:

- section-level checklists;
- title, abstract, and introduction generation;
- proof prose review;
- notation and equation checking;
- reviewer response workflow;
- thesis and survey modes.

The Galois Paper Writing page should use this guide as the writing-rule base, `math-ai-review-skills` as review-logic support, and selected literature and citation workflows from `scientific-agent-skills` as engineering references.

## 11. First-Screen Product Copy and Layout

The page should not feel like a generic "AI writes a paper for you" product. It should open directly into a mathematical manuscript workspace.

Recommended first screen:

- Left: project and section navigation.
- Center: manuscript editor.
- Right: writing checks, notation, citations, and revision tasks.
- Top: Paper / Survey / Thesis / Review Response mode switch.
- Bottom or side drawer: Matlas theorem search and citation search as optional tools.

Core action labels:

- `Review Draft`
- `Improve Abstract`
- `Check Proof`
- `Check Notation`
- `Check Citations`
- `Build Response Letter`
- `Export`

## 12. Product Mistakes to Avoid

- Do not make the page a vague "AI writes your paper" generator.
- Do not make Galois run the entry point; that blocks early-stage writing and independent use.
- Do not offer only grammar polishing. Mathematical writing problems are often structural, logical, notational, and bibliographic.
- Do not put all functions inside a chat box. The page needs visible sections, notation, citations, and task panels.
- Do not let AI assert that a proof is correct without explainable checks and risk points.
- Do not encourage unsourced rewriting of literature. Require citation and attribution.

## 13. Minimal Implementation Tasks

When implementation starts, split work into these tasks:

1. Define a `PaperProject` data model: title, abstract, sections, references, notation, review reports, and revision tasks.
2. Build a manuscript editor that supports Markdown or LaTeX text and section splitting.
3. Build review engine v1 using the rules in this guide.
4. Build a notation scanner for `$...$`, `\label`, `\ref`, and `\cite`.
5. Build a citation consistency checker for manuscript citations and BibTeX.
6. Build abstract and introduction assistants from user-provided topic, theorem, and method inputs.
7. Build a revision board that turns review findings into todos.
8. Build export for `.tex`, `.md`, `.bib`, and review reports.
