# Mathematical Writing Anti-Patterns

This reference is a reverse checklist distilled from Jean-Pierre Serre's lecture "How to write mathematics badly" and the local mathematical writing notes. Use it to find places where a paper is easy for the author but hard for the reader.

Local source: `mathematics writting/md/How to write mathematics badly.md`

## When To Use

Run this pass when:

- a proof feels technically correct but hard to follow;
- the title, abstract, or introduction seems vague;
- notation appears before it is defined;
- references are too broad to check;
- theorems switch between existence and chosen objects;
- a manuscript uses many symbols, diagrams, abbreviations, or "obvious" steps;
- the user asks for a harsh clarity review.

## Serre Pass

Read the draft adversarially and ask: where has the writer made their own life easy by moving work to the reader?

Return findings as concrete revision tasks. Each task should name the location, the anti-pattern, why it is dangerous, and the fix.

## Anti-Pattern Checklist

### 1. Empty Title

Symptoms:

- Title names only a broad topic, a famous theorem, or "a proof of ..." without the actual contribution.
- Title hides the object, method, or result.
- Title uses an author's name as a substitute for mathematical content.

Fix:

- Name the object, hypothesis, result, method, obstruction, or comparison theorem.
- Remove padded phrases unless the genre requires them.

### 2. Undefined Private Notation

Symptoms:

- Theorem statements use abbreviations, objects, or adjectives before they are defined.
- The writer assumes readers know the notation in the writer's head.
- A term has several standard meanings and the manuscript does not disambiguate.

Fix:

- Define notation before the theorem or postpone the theorem until notation is ready.
- State object type, scope, and assumptions.
- Prefer a short notation paragraph over a cryptic theorem.

### 3. Uncheckable Reference

Symptoms:

- Citation points to a long book or series without theorem, section, page, or precise location.
- Citation uses private communication, forthcoming work, or unavailable notes for a central claim.
- A reference is given long after the term or theorem is first used.

Fix:

- Cite a precise theorem, proposition, section, page, arXiv version, DOI, or stable source.
- If the source is unavailable, mark `lookup_needed` or give a self-contained proof.

### 4. Hard Part Hidden In A Lemma

Symptoms:

- Easy lemmas are fully proved, but the difficult lemma is dismissed.
- The proof says "a computation", "by definition", "standard", "obvious", or "clear" at the only nontrivial point.
- A proof-ending symbol appears where an argument should be.

Fix:

- Expand the missing argument or cite a precise result.
- If the computation is long, outline the route and move details to an appendix.
- State exactly which definitions imply the claim.

### 5. Existence-To-Choice Switch

Symptoms:

- A theorem says "there exists an isomorphism" and later prose refers to "the isomorphism".
- A subsequent theorem assigns properties to an object that was only asserted to exist.
- A statement with parts (a) and (b) does not clarify whether (b) holds for some witness from (a), all witnesses from (a), or a constructed witness.

Fix:

- Construct or select the object before discussing its properties.
- Rewrite as "there exists an object satisfying both ..." or "every such object satisfies ...".
- If the proof constructs a particular object, refer to "the object constructed in the proof".

### 6. Symbol As Verb

Symptoms:

- The main assertion is buried in a long formula and the reader must discover which symbol acts as the verb.
- The sentence starts with a symbol or formula.
- Logical symbols replace prose in running text.

Fix:

- Rewrite the assertion in words before or after the display.
- Add a noun phrase before a symbol at sentence start.
- Use "is rational", "is injective", "there exists", and "for all" in prose.

### 7. Comma Doing Logic

Symptoms:

- A sentence uses commas to mean both "and" and "therefore".
- In an "if" sentence, the condition and conclusion are separated only by punctuation.
- The scope of hypotheses is ambiguous.

Fix:

- Use "if ... then ...", "and", "so", "hence", or separate sentences.
- Split long conditional statements.
- Make quantifier scope explicit.

### 8. Abbreviation Fog

Symptoms:

- Blackboard abbreviations appear in polished prose: WLOG, iff, s.t., w.r.t., c.m., or unexplained acronyms.
- Dots or punctuation create ambiguity.
- Symbols such as `forall` and `exists` appear outside formulas.

Fix:

- Spell out abbreviations in prose unless they are standard field acronyms and defined.
- Keep formal symbols inside formulas.
- Prefer clarity over compactness.

### 9. Diagram Or Picture As Proof

Symptoms:

- The proof says "see the picture" without specifying what feature matters.
- A diagram has unlabeled arrows or ambiguous commutativity.
- A topology/geometric argument depends on a visual feature not stated in prose.

Fix:

- State the exact property the figure shows.
- Label all objects and arrows used in the argument.
- If a diagram commutes, state which compositions are equal or cite the naturality result that gives commutativity.

### 10. Hidden Constant Dependencies

Symptoms:

- The manuscript says "there is a constant $C$" but does not say what $C$ may depend on.
- Big-O notation lacks the limiting regime or threshold.
- An analytic estimate fixes an object with "let" and then implicitly claims uniformity over it.

Fix:

- State dependencies in prose or notation, such as $C=C(d,\epsilon)$.
- State the limiting variable and threshold for asymptotic notation.
- Distinguish pointwise, uniform, local, and global estimates.

### 11. Unnamed Identification

Symptoms:

- Several natural embeddings or identifications exist, but the manuscript silently uses one.
- Two objects are treated as equal when only an isomorphism has been specified.
- A comparison depends on a sign, orientation, convention, or functorial choice.

Fix:

- Name the map or convention when more than one natural choice exists.
- Use "identify via ..." once, then keep the convention consistent.
- Flag sign and orientation conventions before they matter.

### 12. Missing Final Implication

Symptoms:

- Every written line is true, but the final step from the written argument to the theorem is not supplied.
- The proof stops after proving a related statement.
- The reader must reconstruct why the established claims imply the theorem.

Fix:

- Add a final paragraph reassembling the argument.
- Restate the theorem's target and check each component has been proved.
- If a gap remains, convert it to a revision task instead of polishing around it.

## Output Format

Use this compact report:

```text
Serre anti-pattern pass

1. [Location] Anti-pattern: [name]
   Risk: [why the reader may be misled or blocked]
   Fix: [specific rewrite or proof task]
```

If no serious anti-patterns are found, say which checks were run and note any remaining proof or citation verification still needed.
