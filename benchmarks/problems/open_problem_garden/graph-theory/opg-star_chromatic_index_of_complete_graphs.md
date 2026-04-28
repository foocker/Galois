---
id: opg-star_chromatic_index_of_complete_graphs
title: Star chromatic index of complete graphs
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/star_chromatic_index_of_complete_graphs
---

# Statement

Conjecture Is it possible to color edges of the complete graph $ K_n $ using $ O(n) $ colors, so that the coloring is proper and no 4-cycle and no 4-edge path is using only two colors?

Equivalently: is the star chromatic index of $ K_n $ linear in $ n $ ?

# Source literature

- *[DMS] Dvořák, Zdeněk; Mohar, Bojan; Šámal, Robert: Star chromatic index, arXiv:1011.3376.

# Progress

- The star chromatic index $ \chi_s'(G) $ of a graph $ G $ is the minimum number of colors needed to properly color the edges of $ G $ so that no path or cycle of length four is bi-colored. An equivalent definition is that $ \chi_s'(G) $ is the star chromatic number of the line graph $ L(G) $ .

Dvořák, Mohar, and Šámal [DMS] show that $ \chi_s'(G) \ge (2+o(1))n $ . On the other hand, the best known upper bound (also in \cite{DMS]) is superlinear: $$ \chi_s'(K_n) \le n \cdot \frac{ 2^{ 2\sqrt2(1+o(1)) \sqrt{\log n} } }{(\log n)^{1/4}} \,. $$

It may be possible to decrease the upper bound by elementary methods.
