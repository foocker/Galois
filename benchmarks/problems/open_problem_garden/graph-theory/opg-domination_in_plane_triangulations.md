---
id: opg-domination_in_plane_triangulations
title: Domination in plane triangulations
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/domination_in_plane_triangulations
---

# Statement

Conjecture Every sufficiently large plane triangulation $ G $ has a dominating set of size $ \le \frac{1}{4} |V(G)| $ .

# Source literature

- [MT] L. R. Matheson, R. E. Tarjan, Dominating sets in planar graphs. European J. Combin. 17 (1996), no. 6, 565--568. MathSciNet

# Progress

- Motivated by some problems in multigrid computations, Matheson and Tarjan [MT] considered the problem of finding small dominating sets in plane triangulations. They proved that every such graph $ G $ has a dominating set of size $ \le \frac{1}{3} |V(G)| $ and posed the above question.

The Octahedron is a triangulation with 6 vertices for which every dominating set has size $ \ge 2 $ , so no constant better than $ \frac{1}{3} $ can be achieved in general. However, it appears that one can do better for larger graphs. The most extreme examples here (also from [MT]) are constructed as follows: Start with $ n $ disjoint copies of $ K_4 $ embedded in the plane, and then add edges to complete this graph to a triangulation (with $ 4n $ vertices). Now each of the original copies of $ K_4 $ has an inner vertex which has degree 3 in the final graph, and in order to cover it, one must take at least one vertex from this $ K_4 $ . It follows that every dominating set has size $ \ge n $ .

Since the Matheson-Tarjan proof is short and instructive, we sketch it here. In fact, we shall prove (as they did) the stronger statement that every near-triangulation (a graph embedded in the plane with all finite faces of size three) has a (possibly improper) 3-coloring so that each color class is a dominating set and so that the subgraph induced by those vertices incident with the infinite face is properly colored. This stronger fact we prove by induction. If the infinite face is not bounded by a cycle or the infinite face is bounded by a cycle which has a chord, then the graph may be written as the union of two near-triangulations $ G_1,G_2 $ where $ G_1 $ and $ G_2 $ either share one vertex or two adjacent vertices and one edge. In either case, the result follows by applying induction to $ G_1 $ and $ G_2 $ . Otherwise, choose a vertex $ v $ on the infinite face, delete $ v $ and apply induction. Since the neighbors of $ v $ are all on the infinite face, and do not form an independent set, there are at least two colors, say $ 1 $ and $ 2 $ , which appear on the neighbors of $ v $ . Now giving $ v $ the color $ 3 $ gives a solution.
