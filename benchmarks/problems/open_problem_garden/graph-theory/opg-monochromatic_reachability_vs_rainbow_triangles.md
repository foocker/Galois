---
id: opg-monochromatic_reachability_vs_rainbow_triangles
title: Monochromatic reachability or rainbow triangles
status: open
difficulty: frontier
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/monochromatic_reachability_vs_rainbow_triangles
---

# Statement

In an edge-colored digraph, we say that a subgraph is rainbow if all its edges have distinct colors, and monochromatic if all its edges have the same color.

Problem Let $ G $ be a tournament with edges colored from a set of three colors. Is it true that $ G $ must have either a rainbow directed cycle of length three or a vertex $ v $ so that every other vertex can be reached from $ v $ by a monochromatic (directed) path?

# Source literature

- *[SSW] B. Sands, N. Sauer, R. Woodrow, On monochromatic paths in edge-coloured digraphs. J. Combin. Theory Ser. B 33 (1982), no. 3, 271--275. MathSciNet.

# Progress

- This problem was raised in a paper by Sands, Sauer, and Woodrow [SSW] where they prove that every tournament with 2-colored edges has a vertex $ v $ so that every other vertex can be reached from $ v $ by a monochromatic path.

Galeana-Sanchez and Rojas-Monroy found a tournament on 6 vertices with 4-colored edges which has no rainbow triangle and does not have a vertex $ v $ which has monochromatic paths to all remaining vertices. However, the following generalization of the above conjecture looks plausible.

Problem Does every edge-colored tournament have either a rainbow directed cycle or a vertex $ v $ so that every other vertex can be reached from $ v $ by a monochromatic path?
