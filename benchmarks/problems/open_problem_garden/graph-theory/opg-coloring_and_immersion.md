---
id: opg-coloring_and_immersion
title: Coloring and immersion
status: open
difficulty: frontier
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/coloring_and_immersion
---

# Statement

Conjecture For every positive integer $ t $ , every (loopless) graph $ G $ with $ \chi(G) \ge t $ immerses $ K_t $ .

# Source literature

- * Faisal N. Abu-Khzam and Michael A. Langston, Graph Coloring and the Immersion Order

# Progress

- Let $ G $ be a graph and let $ uv, vw \in E(G) $ . The operation of deleting the edges $ uv $ and $ vw $ and then adding a new edge between $ v $ and $ w $ is called a split. We say that a graph $ G $ immerses a graph $ H $ if a graph isomorphic to $ H $ may be obtained from $ G $ by repeatedly making splits and deleting vertices and edges.

The graph containment relations of minor and topological minor have been thoroughly studied with respect to graph coloring. In particular, there are two famous conjectures: Hajos conjectured that every graph with chromatic number $ \ge t $ contains a subdivision of the complete graph $ K_t $ as a subgraph. Hadwiger conjectured that every graph with chromatic number $ \ge t $ contains $ K_t $ as a minor. While Hajos' Conjecture is false for $ t \ge 8 $ (indeed it is actually false on average), Hadwiger's Conjecture remains open, and is one of the outstanding problems in Graph Theory.

On the other hand, the relationship between graph coloring and immersions seems to have been largely ignored until Abu-Khzam and Langston made the above conjecture. In addition to formulating this conjecture, they proved it for $ t \le 4 $ and showed that a minimal counterexample to it must be 4-connected and $ t $ -edge-connected. Recently, DeVos, Kawarabayashi, Mohar, and Okamura have resolved the conjecture for $ t \le 7 $ .
