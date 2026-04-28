---
id: opg-non_edges_vs_feedback_edge_sets_in_digraphs
title: Non-edges vs. feedback edge sets in digraphs
status: open
difficulty: frontier
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/non_edges_vs_feedback_edge_sets_in_digraphs
---

# Statement

For any simple digraph $ G $ , we let $ \gamma(G) $ be the number of unordered pairs of nonadjacent vertices (i.e. the number of non-edges), and $ \beta(G) $ be the size of the smallest feedback edge set.

Conjecture If $ G $ is a simple digraph without directed cycles of length $ \le 3 $ , then $ \beta(G) \le \frac{1}{2} \gamma(G) $ .

# Source literature

- *[CSS] M. Chudnovsky, P.D. Seymour, and B. Sullivan, Cycles in dense digraphs.

# Progress

- If $ G $ satisfies $ \gamma(G) = 0 $ , then $ G $ is a tournament, and it is easy to check that $ G $ will have a directed cycle of length three unless it is acyclic, in which case $ \beta(G) = 0 $ . So in this case, the conjecture holds. More generally, it is natural to suspect that a digraph with few non-edges and no directed triangles should be close to acyclic. Indeed, this conjecture asserts a precise relationship of this form.

If true, the above conjecture is essentially tight for a number of examples. We noted above that it is tight for transitive tournaments. Here is another basic class: let $ G_k $ be the circulant digraph obtained by placing $ 3k+1 $ vertices in a circle, and adding an edge directed from $ u $ to $ v $ whenever $ v $ is distance $ \le k $ from $ u $ in the clockwise order. Such examples may be nested to obtain new ones.

Chudnovsky, Seymour, and Sullivan [CSS] utilized a clever double counting argument to prove that $ \beta(G) \le \gamma(G) $ always holds. They also proved their conjecture in the case when $ V(G) $ is the union of two cliques, and when $ G $ is a circular interval digraph.
