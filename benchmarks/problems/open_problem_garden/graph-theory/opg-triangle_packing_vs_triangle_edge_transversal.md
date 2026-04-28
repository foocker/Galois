---
id: opg-triangle_packing_vs_triangle_edge_transversal
title: Triangle-packing vs triangle edge-transversal.
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/triangle_packing_vs_triangle_edge_transversal
---

# Statement

Conjecture If $ G $ has at most $ k $ edge-disjoint triangles, then there is a set of $ 2k $ edges whose deletion destroys every triangle.

# Source literature

- [H] P.Haxell, Packing and covering triangles in graphs, Discrete Mathematics 195 (1999), no. 1–3, 251–254.
- [K] M. Krivelevich, On a conjecture of Tuza about packing and covering of triangles Discrete Mathematics 142 (1995), 281-286.
- *[T] Z. Tuza, A conjecture on triangles of graphs. Graphs Combin. 6 (1990), 373-380.

# Progress

- This conjecture may be rephrased in terms of packing and edge-transversal. A triangle packing is a set of pairwise edge-disjoint triangles. A triangle edge-tranversal is a set of edges meeting all triangles. Denote the maximum size of a triangle packing in $ G $ by $ \nu(G) $ and the minimum size of a triangle edge-transversal of $ G $ by $ \tau(G) $ . Clearly $ \nu(G) \leq \tau(G) $ . The conjecture translates in $ \tau(G)\leq 2\nu(G) $ .

This conjecture, if true, is best possible as can be seen by taking, say $ G=K_4 $ or $ G=K_5 $ . Trivially, $ \tau(G)\leq 3\nu(G) $ , since the set of edges of a maximum triangle packing is a triangle edge-transversal. Haxell [H] proved that $ \tau(G) \leq (3-\frac{3}{23})\nu(G) $ edges whose deletion destroys every triangle.

As usual, one can define fractional packing and fractional transversal. Let $ {\cal T} $ be the set of triangles of $ G $ . A fractional triangle packing is a function $ f:{\cal T}\rightarrow \mathbb{R}^+ $ such that $ \sum_{T\ni e} \leq 1 $ for every edge $ e $ . A fractional triangle edge-transversal is a function $ g:E\rightarrow \mathbb{R}^+ $ such that $ \sum_{e\in T} g(e)\geq 1 $ for every triangle $ T\in {\cal T} $ . We denote by $ \nu^*(G) $ the maximum of $ \sum_{T\in {\cal T}} f(T) $ over all fractional triangle packing and by $ \tau^*(G) $ the minimum of $ \sum_{e\in E(G)} g(e) $ over all fractional edge-transversals. By duality of linear programming $ \tau^*(G) = \nu^*(G) $ . Krivelevich [K] proved two fractional versions of the conjecture:

$ \tau(G) \leq 2\nu^*(G) $ and $ \tau^*(G)\leq 2\nu(G) $ .
