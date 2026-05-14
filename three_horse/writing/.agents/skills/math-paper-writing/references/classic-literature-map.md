# Classic Mathematical Literature Map

This file indexes local classic-paper Markdown as reference models for mathematical writing. Use these papers as architecture and style references, not as text to copy.

## Use Rules

- Use this map before selecting exemplar papers for a manuscript, introduction, survey, thesis chapter, or proof rewrite.
- Match by mathematical direction, paper type, and writing problem.
- Load only the specific local Markdown files that fit the task.
- Do not imitate archaic typography, outdated notation, or source-specific quirks unless the user explicitly wants historical style.
- Do not copy long passages. Extract structure, sequencing, and rhetorical moves.

## Quick Selection

| Writing Need | Suggested Models |
| --- | --- |
| Bridge two theories or categories | Serre GAGA; Grothendieck Tohoku; Witten Morse theory |
| Introduce a reusable method | Serre finite fields; Huber-Sturmfels polyhedral method; Ball convex geometry |
| Present a construction with universal property | Milnor universal bundles I-II; Kapranov-Sturmfels-Zelevinsky toric quotients |
| Build a long technical proof route | Katz nilpotent connections; Serre FAC; Grothendieck Tohoku |
| Write a survey or lecture-style exposition | Ball convex geometry; Tate elliptic curves; Serre finite fields |
| Explain cross-field mathematics | Witten Morse theory; Einstein relativity papers |
| State arithmetic geometry motivation and consequences | Zhang small points; Katz p-curvature/Hodge filtration; Tate elliptic curves |
| Organize computational or algorithmic mathematics | Huber-Sturmfels sparse systems; finite field problem lectures |
| Run a reverse clarity review | Serre "How to write mathematics badly" |

## Direction Map

### Algebraic Geometry and Complex Analytic Geometry

**Serre, GAGA**
Local file: `great-math-paper/md/serre_gaga_algebraic_geometry_and_analytic_geometry_english.md`

- Direction: algebraic geometry, analytic geometry, coherent sheaves, comparison theorem.
- Paper type: bridge-between-worlds research article.
- Use when: a manuscript compares two categories, proves an equivalence, or wants an introduction that starts from two viewpoints and then states the precise bridge.
- Writing lesson: name both viewpoints early, give familiar overlap examples, then state the comparison theorem and applications.

**Serre, FAC / Coherent Algebraic Sheaves**
Local file: `great-math-paper/md/serre_fac_coherent_algebraic_sheaves_english.md`

- Direction: coherent sheaves, projective varieties, cohomology.
- Paper type: foundational theory-building paper.
- Use when: a paper introduces a large technical framework with many definitions, propositions, and consequences.
- Writing lesson: keep definitions systematic, number results for navigation, and let the theory build through reusable formal statements.

**Grothendieck, Tohoku / Some Aspects of Homological Algebra**
Local file: `great-math-paper/md/grothendieck_tohoku_some_aspects_homological_algebra_english.md`

- Direction: abelian categories, derived functors, sheaf cohomology.
- Paper type: unifying framework paper.
- Use when: a manuscript abstracts several existing theories into a common formalism.
- Writing lesson: state the motivating analogy first, then explain the general framework and list applications and omissions.

**Kleiman, Transversality of a General Translate**
Local file: `great-math-paper/md/kleiman_transversality_of_a_general_translate.md`

- Direction: algebraic geometry, transversality, group actions.
- Paper type: focused theorem paper.
- Use when: a paper has one central geometric statement and needs a concise introduction plus clean theorem-proof flow.
- Writing lesson: keep the surrounding exposition tight; let hypotheses and theorem statements carry the precision.

**Kapranov-Sturmfels-Zelevinsky, Quotients of Toric Varieties**
Local file: `great-math-paper/md/kapranov_sturmfels_zelevinsky_quotients_of_toric_varieties.md`

- Direction: toric varieties, quotient fans, GIT, Chow quotients, fiber polytopes.
- Paper type: construction-and-comparison paper.
- Use when: a manuscript constructs objects and compares several quotient notions.
- Writing lesson: organize by construction first, then relations to existing frameworks.

### Arithmetic Geometry and Number Theory

**Tate, Arithmetic of Elliptic Curves**
Local file: `great-math-paper/md/tate_arithmetic_of_elliptic_curves.md`

- Direction: elliptic curves, local/global fields, L-series, Galois action.
- Paper type: lecture/survey with theorem-driven exposition.
- Use when: a survey or thesis chapter needs to move from basic models to local, global, and arithmetic consequences.
- Writing lesson: section titles should reflect the mathematical route; examples can anchor abstract theory.

**Zhang, Small Points and Adelic Metrics**
Local file: `great-math-paper/md/zhang_equidistribution_small_points_abelian_varieties.md`

- Direction: abelian varieties, heights, adelic metrics, Bogomolov-type problems.
- Paper type: conjecture-driven arithmetic geometry paper.
- Use when: a manuscript begins from a conjecture, proves a special case, and develops technical infrastructure.
- Writing lesson: state the conjectural setting, state the proved case, then explain the machinery and positivity mechanism.

**Katz, Algebraic Solutions of Differential Equations / p-Curvature and Hodge Filtration**
Local file: `great-math-paper/md/katz_algebraic_solutions_differential_equations_p_curvature_hodge_filtration.md`

- Direction: arithmetic differential equations, p-curvature, Hodge filtration.
- Paper type: deep technical research paper.
- Use when: a paper connects arithmetic criteria to geometric structures and needs careful setup of assumptions.
- Writing lesson: separate problem statement, technical framework, main theorem, and proof infrastructure.

**Katz, Nilpotent Connections and the Monodromy Theorem**
Local file: `great-math-paper/md/katz_nilpotent_connections_monodromy_turrittin.md`

- Direction: connections, monodromy, de Rham cohomology, arithmetic proof methods.
- Paper type: problem-to-mechanism paper.
- Use when: a paper proves a known-looking theorem by a new arithmetic or structural route.
- Writing lesson: reinterpret the classical theorem, list the reductions in order, and mark which sections supply which ingredients.

**Serre, How to Use Finite Fields for Problems Concerning Infinite Fields**
Local file: `great-math-paper/md/HOW TO USE FINITE FIELDS FOR PROBLEMS.md`

- Direction: finite fields, algebraic geometry, reduction arguments, group actions.
- Paper type: method lecture.
- Use when: a paper or exposition explains transfer from finite to infinite settings.
- Writing lesson: start with a simple theorem, prove the transparent finite case, then explain reduction and variants.

### Topology and Geometry

**Milnor, Construction of Universal Bundles I**
Local file: `great-math-paper/md/milnor_construction_of_universal_bundles_I.md`

- Direction: topology, CW-complexes, universal bundles, topological groups.
- Paper type: construction paper.
- Use when: a manuscript constructs an object satisfying a universal property.
- Writing lesson: state the target property early, then verify the construction through lemmas.

**Milnor, Construction of Universal Bundles II**
Local file: `great-math-paper/md/milnor_construction_of_universal_bundles_II.md`

- Direction: topology, joins, universal bundles, countable CW-groups.
- Paper type: sequel and extension paper.
- Use when: a paper extends a previous construction and needs to keep continuity with an earlier part.
- Writing lesson: identify what is inherited from the first paper and what new obstacle is solved.

**Ball, An Elementary Introduction to Modern Convex Geometry**
Local file: `great-math-paper/md/ball_elementary_introduction_modern_convex_geometry.md`

- Direction: convex geometry, asymptotic geometry, concentration.
- Paper type: expository lecture notes.
- Use when: a survey needs accessible entry, examples, and conceptual themes before technical results.
- Writing lesson: begin with simple objects and recurring themes; use examples to train intuition before general theorems.

### Mathematical Physics and Cross-Field Exposition

**Witten, Supersymmetry and Morse Theory**
Local file: `great-math-paper/md/witten_supersymmetry_and_morse_theory.md`

- Direction: Morse theory, supersymmetry, quantum mechanics, topology.
- Paper type: cross-field bridge paper.
- Use when: a paper introduces an external framework to a mathematical audience.
- Writing lesson: define foreign concepts through the role they play in the mathematical argument, then return to the theorem.

**Einstein, On the Electrodynamics of Moving Bodies**
Local file: `great-math-paper/md/einstein_on_the_electrodynamics_of_moving_bodies_english.md`

- Direction: relativity, electrodynamics, coordinate transformations.
- Paper type: principle-to-consequence physics paper.
- Use when: an exposition begins from a small set of principles and derives many consequences.
- Writing lesson: make assumptions explicit, then let consequences unfold section by section.

**Einstein, Does the Inertia of a Body Depend Upon Its Energy Content?**
Local file: `great-math-paper/md/einstein_does_inertia_depend_upon_energy_content_english.md`

- Direction: relativity, mass-energy relation.
- Paper type: short consequence note.
- Use when: a manuscript is a concise derivation of a striking consequence from an existing framework.
- Writing lesson: keep the note narrow; do not inflate a small argument into a broad survey.

**Einstein, The Foundation of the Generalised Theory of Relativity**
Local file: `great-math-paper/md/einstein_foundation_generalised_theory_relativity_english.md`

- Direction: general relativity, tensor calculus, gravitational field equations.
- Paper type: foundational theory exposition.
- Use when: a long paper must build formal language before stating field equations or governing laws.
- Writing lesson: sequence conceptual motivation, formal definitions, special cases, and governing equations.

### Computational and Algorithmic Mathematics

**Huber-Sturmfels, A Polyhedral Method for Solving Sparse Polynomial Systems**
Local file: `great-math-paper/md/huber_sturmfels_polyhedral_method_sparse_polynomial_systems.md`

- Direction: sparse polynomial systems, mixed subdivisions, homotopy, algorithms.
- Paper type: method plus algorithm paper.
- Use when: a paper introduces an algorithmic method with definitions, theorem support, examples, and implementation concerns.
- Writing lesson: organize as introduction, core combinatorial structure, deformation method, algorithm, worked example, appendix.

### Reverse Models and Anti-Patterns

**Serre, How to Write Mathematics Badly**
Local file: `mathematics writting/md/How to write mathematics badly.md`

- Direction: mathematical writing, exposition, proof clarity.
- Paper type: reverse model / anti-pattern lecture.
- Use when: a manuscript needs adversarial clarity review rather than a positive exemplar.
- Writing lesson: find places where the author has saved effort by making the reader infer notation, references, choices, constants, diagram commutativity, or missing implications.
- Operational reference: use `anti-patterns.md` for the concise checklist.

## Paper-Type Map

### Bridge Paper

Goal: show that two viewpoints, theories, or categories correspond.

Models:

- Serre GAGA.
- Grothendieck Tohoku.
- Witten Morse theory.

Writing moves:

- Name both worlds early.
- Give familiar overlap examples.
- State the bridge theorem or dictionary before the machinery.
- Use applications to show that the bridge is useful.

### Method Paper

Goal: teach and justify a reusable method.

Models:

- Serre finite fields.
- Huber-Sturmfels polyhedral method.
- Ball convex geometry.

Writing moves:

- Start with a clean motivating example.
- State the general method.
- Work through a representative application.
- End sections with what the method has achieved.

### Foundation Paper

Goal: build a formal framework other papers can use.

Models:

- Serre FAC.
- Grothendieck Tohoku.
- Einstein general relativity.

Writing moves:

- State motivation and scope.
- Separate definitions from theorems and applications.
- Use precise numbering and cross-reference discipline.
- Include omissions or limitations when the framework is intentionally incomplete.

### Construction Paper

Goal: construct a mathematical object with a universal, classification, or comparison property.

Models:

- Milnor universal bundles.
- Kapranov-Sturmfels-Zelevinsky toric quotients.

Writing moves:

- State the desired object and property first.
- Build the object.
- Verify well-definedness and structural properties.
- Derive the universal or comparison result.

### Conjecture-Driven Paper

Goal: start from a conjectural landscape and prove a meaningful case.

Models:

- Zhang small points.
- Katz p-curvature/Hodge filtration.

Writing moves:

- State the conjecture or expected principle.
- Identify the case solved.
- Explain why the case is not formal from known results.
- Develop exactly the machinery needed for the proof.

## Choosing a Model

Before borrowing a model, answer:

1. Is the user's paper closer to a theorem, method, construction, foundation, survey, or conjecture-driven paper?
2. Is the target reader a specialist, adjacent mathematician, graduate student, or cross-field reader?
3. Does the paper's main difficulty lie in motivation, definitions, proof route, literature position, or technical detail?
4. Which local model has the same difficulty without imposing irrelevant style?

Then load only the matching local Markdown file and extract:

- introduction shape;
- section order;
- theorem/lemma hierarchy;
- proof routing;
- handling of examples, remarks, applications, and appendices.

Do not extract:

- exact prose;
- old typographic conventions;
- obsolete terminology unless historically necessary.
