---
id: opg-pebbling_a_cartesian_product
title: Pebbling a cartesian product
status: open
difficulty: frontier
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/pebbling_a_cartesian_product
---

# Statement

We let $ p(G) $ denote the pebbling number of a graph $ G $ .

Conjecture $ p(G_1 \Box G_2) \le p(G_1) p(G_2) $ .

# Source literature

- *[C] F. Chung, Pebbling in hypercubes SIAM J. Disc. Math. 2 (1989), 467--472.

# Progress

- The pebbling number of a graph $ G $ , denoted $ p(G) $ , is the smallest integer $ k $ so that however $ k $ pebbles are distributed onto the vertices of $ G $ , it is possible to move a pebble to any vertex by a sequence of steps, where in each step we remove two pebbles from one vertex, and then place one on an adjacent vertex. The cartesian product of two graphs $ G_1 $ and $ G_2 $ , denoted $ G_1 \Box G_2 $ , is the graph with vertex set $ V(G_1) \times V(G_2) $ and an edge from $ (v,w) $ to $ (v',w') $ if either $ v=v' $ and $ w \sim w' $ (in $ G_2 $ ) or $ w=w' $ and $ v \sim v' $ (in $ G_1 $ ).

Graph Pebbling arose out of the study of zero-sum subsequences in groups, but has proved to be a rich and interesting topic in graph theory. See Glenn Hurlbert's wonderful graph pebbling page for much more on this topic (and this problem in particular). Graham's conjecture was stated in one of the first papers on this subject by Fan Chung [C], and has since generated considerable interest.

There are a number of partial results toward this conjecture. Chung [C] proved that $ p(P_{d_1+1} \Box P_{d_2+1} \ldots \Box P_{d_{\ell}+1}) = 2^{d_1 + d_2 \ldots + d_{\ell}} $ , thus settling the conjecture for products of paths (here $ P_n $ denotes a path with $ n $ vertices). It is also known when $ G_1,G_2 $ are both trees, both cycles, and for graphs with high minimum degree. Again, we encourage the interested reader to see the graph pebbling page for more details.
