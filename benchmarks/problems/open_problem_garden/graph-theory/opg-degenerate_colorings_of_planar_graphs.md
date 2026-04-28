---
id: opg-degenerate_colorings_of_planar_graphs
title: Degenerate colorings of planar graphs
status: open
difficulty: frontier
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/degenerate_colorings_of_planar_graphs
---

# Statement

A graph $ G $ is $ k $ -degenerate if every subgraph of $ G $ has a vertex of degree $ \le k $ .

Conjecture Every simple planar graph has a 5-coloring so that for $ 1 \le k \le 4 $ , the union of any $ k $ color classes induces a $ (k-1) $ -degenerate graph.

# Source literature

- *[B] O. V. Borodin, A proof of B. Grünbaum's conjecture on the acyclic $ 5 $ -colorability of planar graphs. Dokl. Akad. Nauk SSSR 231 (1976), no. 1, 18--20. MathSciNet
- [R] D. Rautenbach, A conjecture of Borodin and a coloring of Grünbaum. Fifth Cracow Conference on Graph Theory USTRON '06, 187--194 Electron. Notes Discrete Math., 24, Elsevier, Amsterdam, 2006.

# Progress

- An acyclic coloring of a graph $ G $ is a proper coloring with the added property that the union of any two color classes induces a forest. Grunbaum famously conjectured that every simple planar graph has an acyclic 5-coloring. Following a sequence of partial results, Borodin [B] resolved this conjecture with an impressive and detailed argument. In the same paper, Borodin made the above conjecture, which, if true, would give a stronger result (as forests are precisely the 1-degenerate graphs).

A degenerate coloring of a graph $ G $ is a proper coloring with the added property that the union of any $ k $ color classes induces a $ (k-1) $ -degenerate graph. A planar graph of minimum degree 5 cannot have a degenerate 5-coloring, but if the above conjecture holds, something just short of this is true. Rautenbach [R] proved that every planar graph has a degenerate 18-coloring, and recently, Mohar, Spacepan, and Zhu showed that every planar graph has a degenerate 9-coloring.
