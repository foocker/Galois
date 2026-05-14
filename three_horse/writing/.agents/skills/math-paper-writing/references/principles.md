# Mathematical Paper Writing Principles

This reference condenses `references/guide.md` for skill use.

## Paper Structure

- Title: precise object/method/result; no empty phrases.
- Abstract: a mini-paper; problem, method, result; no equation numbers, figure numbers, or citation numbers.
- Introduction: background, gap, contribution, relation to literature, paper outline.
- Body: introduce definitions only when needed; use theorem/proposition/lemma/corollary hierarchy intentionally.
- Resolution ladder: title, abstract, introduction, and body each describe the whole paper at increasing resolution.
- Conclusion: use only when it adds perspective, limitations, or future directions; do not repeat the abstract.
- References: complete, accurate, consistent, and cited in text.
- Appendix: long technical proofs, standard background, supplemental computations.

## Mathematical Prose

- Prefer readable prose over dense symbolic shorthand.
- Embed formulas in grammatical sentences.
- Define symbols on first use and keep notation consistent.
- Define the type and role of important objects, not only their symbols.
- Make quantifiers and dependencies explicit.
- Avoid unnecessary abbreviations.
- Split long sentences when the subject and verb are far apart.
- Reintroduce old notation if it has not appeared for a while.
- Do not start sentences with symbols, and do not use blackboard abbreviations such as WLOG, iff, s.t., or standalone logical symbols in prose.
- Do not switch from "there exists an object" to "the object" unless a specific object has been constructed or selected.

## Proof Writing

- State the proof strategy for long proofs.
- Do not hide nontrivial steps behind "obvious", "clear", or "easy".
- A reader reaching a period should know why every claim in that sentence is justified, or should be warned that the justification follows.
- Check that every cited theorem's hypotheses are satisfied.
- Use lemmas to break long arguments.
- If only one result in a section is needed later, say so.
- Move purely technical details to an appendix only if the main line remains complete.
- Do not hide the hardest step behind "clear", "by definition", "a computation", "standard", or a proof-ending symbol.

## Equations

- Use `=` only for equality, not for implication or "next step".
- Punctuate displayed equations as sentence parts.
- Number only formulas referenced later.
- Attach reasons to the relevant lines in long chains of equalities or inequalities.
- Prefer words over `forall`, `exists`, `implies`, or arrows in prose unless formal logic is being discussed.

## Revision

- Delete empty phrases, repeated sentences, unused symbols, unused definitions, and unreferenced equation numbers.
- Check section balance and merge tiny sections.
- Make figures and tables support a claim; do not dump data.
- Run the Serre anti-pattern pass in `references/anti-patterns.md` when a draft is hard to read despite appearing mathematically correct.
- Verify title, abstract, introduction, theorem statements, proof steps, notation, references, and acknowledgments before submission.

## Reviewer Response

- Parse every reviewer comment into tasks.
- Modify directly where the comment is right.
- If disagreeing, give a specific mathematical reason.
- Reply point by point and cite page/section/equation locations.
