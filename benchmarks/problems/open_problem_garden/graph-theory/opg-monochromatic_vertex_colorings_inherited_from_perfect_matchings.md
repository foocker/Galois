---
id: opg-monochromatic_vertex_colorings_inherited_from_perfect_matchings
title: Monochromatic vertex colorings inherited from Perfect Matchings
status: open
difficulty: frontier
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/monochromatic_vertex_colorings_inherited_from_perfect_matchings
---

# Statement

Conjecture For which values of $ n $ and $ d $ are there bi-colored graphs on $ n $ vertices and $ d $ different colors with the property that all the $ d $ monochromatic colorings have unit weight, and every other coloring cancels out?

# Source literature

- Questions on the Structure of Perfect Matchings inspired by Quantum Physics

# Progress

- Background: This and many related questions are directly inspired from quantum physics, and their solutions would directly contribute to new understanding in quantum physics.

Bi-Colored Graph: A bi-colored weighted graph $ G=(V(G),E(G)) $ , on $ n $ vertices with $ d $ colors is an undirected, not necessarily simple graph where there is a fixed ordering of the vertices $ V(G)=v_1, \ldots, v_n $ and to each edge $ e \in E(G) $ there is a complex weight $ w_e $ and an ordered pair of (not necessarily different) colors $ (c_1(e),c_2(e)) $ associated with it from the $ d $ possible colors. We say that an edge is monochromatic if the associated pair of colors are not different, otherwise the edge is bi-chromatic. Moreover, if $ e $ is an edge incident to the vertices $ v_i,v_j \in V(G) $ with $ i<j $ and the associated ordered pair of colors to $ e $ is $ (c_1(e),c_2(e)) $ then we say that $ e $ is colored $ c_1 $ at $ v_i $ and $ c_2 $ at $ v_j $ .

We will be interested in a special coloring of this graph:

Inherited Vertex Coloring: Let $ G $ be a bi-colored weighted graph and $ PM $ denote a perfect matching in $ G $ . We associate a coloring of the vertices of G with PM in the natural way: for every vertex $ v_i $ there is a single edge $ e(v_i) \in PM $ that is incident to $ v_i $ , let the color of $ v_i $ be the color of $ e(v_i) $ at $ v_i $ . We call this coloring $ c $ , the inherited vertex coloring (IVC) of the perfect matching PM.

Now we are ready to define how constructive and destructive interference during an experiment is governed by perfect matchings of a bi-colored graph.

Weight of Vertex Coloring: Let $ G $ be a bi-colored weighted graph. Let $ \mathcal{M} $ be the set of perfect matchings of $ G $ which have the coloring $ c $ as their inherited vertex coloring. We define the weight of $ c $ as $$w(c) := \sum_{PM \in \mathcal{M}} \prod_{e \in PM}w_e. $$ Moreover, if $ w(c) $ =1 we say that the coloring gets unit weight, and if $ w(c) $ =0 we say that the coloring cancels out.
