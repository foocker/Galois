---
id: opg-complexity_of_the_h_factor_problem
title: Complexity of the H-factor problem.
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/complexity_of_the_h_factor_problem
---

# Statement

An $ H $ -factor in a graph $ G $ is a set of vertex-disjoint copies of $ H $ covering all vertices of $ G $ .

Problem Let $ c $ be a fixed positive real number and $ H $ a fixed graph. Is it NP-hard to determine whether a graph $ G $ on $ n $ vertices and minimum degree $ cn $ contains and $ H $ -factor?

# Source literature

- [HK] P. Hell and D.G. Kirkpatrick, On the complexity of general graph factor problems, SIAM J. Computing 12 (1983), 601-609.
- [KO06] D. Kühn and D. Osthus, Critical chromatic number and the complexity of perfect packings in graphs, Proceedings of the 17th ACM-SIAM Symposium on Discrete Algorithms (SODA), 2006.
- *[KO09] D. Kühn and D. Osthus, The minimum degree threshold for perfect graph packings, Combinatorica 29 (2009), 65-107.

# Progress

- The answer is positive for cliques and a few other graphs [KO06].

If we remove the minimum degree condition, the problem is NP-complete if and only if $ H $ has a component which contains at least 3 vertices, as shown by Hell and Kirkpatrick [HK].
