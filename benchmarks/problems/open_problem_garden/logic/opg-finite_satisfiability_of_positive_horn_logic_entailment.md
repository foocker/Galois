---
id: opg-finite_satisfiability_of_positive_horn_logic_entailment
title: Finite entailment of Positive Horn logic
status: open
difficulty: research
domains:
- Logic
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/finite_satisfiability_of_positive_horn_logic_entailment
---

# Statement

Question Positive Horn logic (pH) is the fragment of FO involving exactly $ \exists, \forall, \wedge, = $ . Does the fragment $ pH \wedge \neg pH $ have the finite model property?

# Source literature

- [CMM08] Hubie Chen, Florent R. Madelaine, Barnaby Martin: Quantified Constraints and Containment Problems. LICS 2008: 317-328

# Progress

- It doesn't really matter whether or not equality is allowed, as it may mostly be propagated out by substitution. The question is whether there an infinity axiom of the form $ \phi \wedge \neg \psi $ , for $ \phi, \psi $ in pH?

In [CMM08] it is proved that entailment of pH sentences is decidable. I.e. input, $ \phi, \psi $ in pH and return yes if $ \phi \rightarrow \psi $ is true on all models. The question is whether this is the same as asking if entailment of pH is equivalent to finite entailment, i.e. if $ \phi \rightarrow \psi $ is true on all models iff it is true on all finite models.

For the positive equality-free fragment of FO (bigger than pH), finite entailment and general entailment do not coincide, and the latter problem is undecidable. For existential positive logic, (smaller than pH), finite entailment and general entailment do coincide, and of course both are decidable. At present, the question as to whether finite entailment of pH is decidable is also open.
