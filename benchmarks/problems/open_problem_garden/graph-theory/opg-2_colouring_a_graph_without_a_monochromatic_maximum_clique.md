---
id: opg-2_colouring_a_graph_without_a_monochromatic_maximum_clique
title: 2-colouring a graph without a monochromatic maximum clique
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/2_colouring_a_graph_without_a_monochromatic_maximum_clique
---

# Statement

Conjecture If $ G $ is a non-empty graph containing no induced odd cycle of length at least $ 5 $ , then there is a $ 2 $ -vertex colouring of $ G $ in which no maximum clique is monochromatic.

# Source literature

- [CRS] Maria Chudnovsky, Neil Robertson, Paul Seymour, Robin Thomas: The strong perfect graph theorem, Ann. of Math. (2) 164 (2006), no. 1, 51--229. MathSciNet
- [HMcD] C.T. Hoàng, C. McDiarmid, On the divisibility of graphs, Discrete Math. 242 (1–3) (2002) 145–156.
- [BM] J. A. Bondy and U. S. R. Murty. Graph theory, volume 244 of Graduate Texts in Mathematics. Springer, New York, 2008.

# Progress

- A $ 2 $ -division of a graph $ G $ is a partitioning of $ G $ into two subgraphs, neither of which contains a maximum clique. It is known that every perfect graph admits a $ 2 $ -division. Thus, by the Strong Perfect Graph Theorem [CRS], a graph which does not contain an induced copy of an odd cycle of length at least $ 5 $ or its complement has a $ 2 $ -division. Hoàng and McDiarmid [HMcD] also prove that a claw-free graph admits a 2-division if and only if it does not contain an induced odd cycle of length at least $ 5 $ . The conjecture says that this holds for all graphs.

This problem was featured as unsolved problem #49 in Bondy and Murty's book "Graph Theory" [BM].

See also a posting on the American Institute of Mathematics website, contributed by Bruce Reed.
