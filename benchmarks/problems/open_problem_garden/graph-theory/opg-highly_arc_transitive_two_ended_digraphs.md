---
id: opg-highly_arc_transitive_two_ended_digraphs
title: Highly arc transitive two ended digraphs
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/highly_arc_transitive_two_ended_digraphs
---

# Statement

Conjecture If $ G $ is a highly arc transitive digraph with two ends, then every tile of $ G $ is a disjoint union of complete bipartite graphs.

# Source literature

- *[CPW] P. J. Cameron, C. E. Praeger, and N. C. Wormald, Infinite highly arc transitive digraphs and universal covering digraphs. Combinatorica 13 (1993), no. 4, 377--396. MathSciNet.
- [D] M. J. Dunwoody, Cutting up graphs. Combinatorica 2 (1982), no. 1, 15--23. MathSciNet

# Progress

- It follows from a theorem of Dunwoody [D] that every vertex transitive graph $ G $ with two ends has a system of imprimitivity $ \{ X_i : i \in {\mathbb Z} \} $ with finite blocks so that the cyclic order $ \ldots X_{-2}, X_{-1},X_0,X_1,X_2,\ldots $ is preserved by the automorphism group (of $ G $ ). If $ G $ is edge-transitive, then every edge of $ G $ must have its ends in two consecutive blocks, so in this case $ G $ is an edge-disjoint union of the (isomorphic) bipartite graphs $ G[X_i,X_{i+1}] $ for $ i \in {\mathbb Z} $ - which we shall call tiles. Note that the tiles are edge-transitive.

This gives us a good description of edge-transitive graphs with two ends; each is made up by gluing together copies of a tile in a linear order. If $ G $ is a 2-arc transitive digraph with two ends, then all edges in each tile must be oriented consistently, so by possibly reordering, we may assume that every edge in $ G[X_i,X_{i+1}] $ is oriented from $ X_i $ to $ X_{i+1} $ . The above conjecture asserts that under the added symmetry condition of high arc transitivity, each tile has a simple structure - namely it is a union of (consistently oriented) complete bipartite graphs.

It is easy to construct a highly arc transitive two ended graph by simply using the complete bipartite graph $ K_{n,n} $ (with all edges oriented consistently) as a tile. Mckay and Praeger found the following pretty construction of a highly arc transitive digraph with tiles isomorphic to a disjoint union of complete bipartite graphs: Let $ S $ be a finite set, let $ n $ be a positive integer, and define $ G $ to be the digraph with vertex set $ {\mathbb Z} \times S^n $ and an edge from $ (i, \mathbf{x}, y) $ to $ (i+1, z, \mathbf{x}) $ if $ i \in {\mathbb Z} $ , $ \mathbf{x} \in S^{n-1} $ , and $ y,z \in S $ . A generalized (twisted) version of this construction was introduced by Cameron, Praeger, and Wormald [CPW], but again, every tile in this construction is a disjoint unions of bipartite graphs, and it looks hard to do anything else.
