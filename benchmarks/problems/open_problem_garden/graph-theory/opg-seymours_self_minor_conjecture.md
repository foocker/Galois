---
id: opg-seymours_self_minor_conjecture
title: Seymour's self-minor conjecture
status: open
difficulty: frontier
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/seymours_self_minor_conjecture
---

# Statement

Conjecture Every infinite graph is a proper minor of itself.

# Source literature

- [T] R. Thomas, A counterexample to "Wagner's conjecture" for infinite graphs. Math. Proc. Cambridge Philos. Soc. 103 (1988), no. 1, 55--57. MathSciNet

# Progress

- Robertson and Seymour famously proved that the set of all finite graphs is well-quasi-ordered by the minor relation. More precisely, if we let $ G_1,G_2,\ldots $ be an infinite sequence of graphs, then there exist $ i < j $ so that $ G_i $ is a minor of $ G_j $ . Their theory also gives us a rough structure theorem for the family of graphs without a fixed minor - a powerful tool for studying minors in finite graphs.

On the other hand, there are still large gaps in our understanding of minors of infinite graphs. For instance, while it is known that Wagner's conjecture does not hold in general for infinite graphs [T], it is possible that countably infinite graphs are well quasi-ordered.

The conjecture highlighted above is especially interesting, because (if true) it would imply the well quasi-ordering of finite graphs. Indeed, the well quasi-ordering of finite graphs is equivalent to the statement that every infinite set $ \Omega $ of finite graphs contains two distinct members, one of which is a minor of the other. This latter statement follows from the above conjecture, since we may form a single infinite graph $ G $ from the disjoint union of the graphs in $ \Omega $ , and the proper self-minor of $ G $ gives us a pair of graphs in $ \Omega $ with one a minor of the other.
