---
id: opg-small_universal_point_sets_for_planar_graphs
title: Universal point sets for planar graphs
status: open
difficulty: frontier
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/small_universal_point_sets_for_planar_graphs
---

# Statement

We say that a set $ P \subseteq {\mathbb R}^2 $ is $ n $ -universal if every $ n $ vertex planar graph can be drawn in the plane so that each vertex maps to a distinct point in $ P $ , and all edges are (non-intersecting) straight line segments.

Question Does there exist an $ n $ -universal set of size $ O(n) $ ?

# Source literature

- [CH] M. Chrobak and H.Karloff. A lower bound on the size of universal sets for planar graphs. SIGACT News, 20:83-86, 1989.
- [dFPP] H. de Fraysseix, J. Pach, and R. Pollack. How to draw a planar graph on a grid. Combinatorica, 10(1):41-51, 1990. MathSciNet
- [S] W. Schnyder. Embedding planar graphs on the grid. In Proc. 1st ACM-SIAM Sympos. Discrete Algorithms, pages 138-148, 1990.

# Progress

- More generally, if we let $ f(n) $ denote the size of the smallest $ n $ -universal set, we are interested in the behaviour of $ f $ . The best known upper bound is $ f(n) = O(n^2) $ . Indeed, every $ n $ -vertex planar graph can be drawn as required in the $ n \times n $ grid [dFPP], [S]. On the flip side, it is known that $ f(n) \ge 1.098n $ for sufficiently large $ n $ [CH].
