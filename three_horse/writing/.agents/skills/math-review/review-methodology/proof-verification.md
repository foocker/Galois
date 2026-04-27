# Proof Verification

Use this file when theorem statements, lemmas, propositions, proof sketches, derivations, or mathematical definitions are central.

## Universal Checks

- Extract all main theorem claims, definitions, hypotheses, conclusions, and dependency lemmas.
- Compare theorem assumptions with proof assumptions.
- Build an assumption-use table for substantial proofs: assumption, first use, later use, and whether it is stated in the theorem.
- Mark hidden compactness, regularity, measurability, boundedness, separability, independence, convergence, characteristic, ramification, boundary, or finiteness assumptions.
- Verify key equalities and inequalities step by step when the requested depth permits.
- Scan formulas for sign, exponent, subscript, superscript, constant, norm, and indexing consistency.
- Challenge parametric conditions: are they sharp, technical, or inconsistent with the proof?
- Check full-paper terminology and notation consistency.
- Flag unexplained uses of "clear", "obvious", "standard", "well known", or "by routine argument".
- Separate structural proof review from line-by-line verification.

Line-by-line verification cannot be replaced by a high-level logical-structure pass. If full checking was not performed, write: "structural logic check; no full line-by-line verification performed." Do not write "the proof is correct" unless a suitable formal verifier or independent complete check established it.

## Branch-Specific Checks

### Analysis and PDE

- Check approximation, truncation, Galerkin, projection, or finite-dimensional schemes for consistency of nonlinear terms.
- Confirm weak solution spaces, test function spaces, compactness arguments, and convergence modes match.
- For kinetic or mean-field derivations, check whether stochastic conventions and limiting arguments are formal or rigorous.

### Algebra and Number Theory

- Verify compatibility of rings, modules, ideals, fields, and base changes.
- Check characteristic-dependent steps, separability, Frobenius behavior, ramification, and Galois group actions.
- Test special cases where the statement may degenerate.

### Geometry and Topology

- Check local-to-global compatibility, chart overlaps, transition functions, regularity assumptions, boundary conditions, and orientation conventions.
- Verify exact sequences, connecting homomorphisms, fibrations, foliations, and homotopy or homology arguments use the correct hypotheses.

### Combinatorics, Probability, and Discrete Mathematics

- Check bijections, double-counting, inclusion-exclusion boundaries, graph conventions, labeling conventions, and edge cases.
- Verify independence assumptions, concentration inequalities, Lovasz Local Lemma hypotheses, and random-model definitions.

### Cross-Disciplinary Papers

- Verify that imported theorems satisfy their original preconditions in the new context.
- Check that notation and parameter meanings agree with the source field rather than only the target application.
