---
id: opg-jones_conjecture
title: Jones' conjecture
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/jones_conjecture
---

# Statement

For a graph $ G $ , let $ cp(G) $ denote the cardinality of a maximum cycle packing (collection of vertex disjoint cycles) and let $ cc(G) $ denote the cardinality of a minimum feedback vertex set (set of vertices $ X $ so that $ G-X $ is acyclic).

Conjecture For every planar graph $ G $ , $ cc(G)\leq 2cp(G) $ .

# Source literature

- *[KLL] Ton Kloks, Chuan-Min Lee, and Jiping Liu, New Algorithms for $ k $ -Face Cover, $ k $ -Feedback Vertex Set, and $ k $ -Disjoint Cycles on Plane and Planar Graphs, in Proceedings of the 28th International Workshop on Graph-Theoretic Concepts in Computer Science (WG2002), LNCS 2573, pp. 282--295, 2002.

# Progress

- In [KLL], the authors mention that there exists a family of nonplanar graphs for which $ cc(G) = \Theta( cp(G) \log cp(G) ) $ , so no such result could hold for general graphs. They also point out that the conjecture is tight for wheels, and they prove it for the special case of outerplanar graphs.
