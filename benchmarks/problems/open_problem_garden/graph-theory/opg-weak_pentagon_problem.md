---
id: opg-weak_pentagon_problem
title: Weak pentagon problem
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/weak_pentagon_problem
---

# Statement

Conjecture If $ G $ is a cubic graph not containing a triangle, then it is possible to color the edges of $ G $ by five colors, so that the complement of every color class is a bipartite graph.

# Source literature


# Progress

- This conjecture has several reformulations: the conclusion of the conjecture can be replaced by either of the following:

\item $ G $ has a homomorphism to the Clebsch graph. \item there is a cut-continuous mapping from $ G $ to $ C_5 $ .

For the latter variant, few definitions are in place. A cut-continuous mapping from a graph~ $ G $ to a graph~ $ H $ is a mapping $ f : E(G) \to E(H) $ such that the preimage of every cut in~ $ H $ is a cut in~ $ G $ . Here, by a cut in~ $ H $ we mean the edge-set of a spanning bipartite subgraph of~ $ H $ ---less succinctly, it is the set of all edges leaving some subset of vertices of~ $ H $ .

Cut-continuous mappings are closely related with graph homomorphisms (see [DNR], [S]). In particular, every homomorphism from~ $ G $ to~ $ H $ naturally induces a cut-continuous mapping from~ $ G $ to~ $ H $ ; thus, the presented conjecture can be thought of as a weaker version of Nesetril's Pentagon problem.

We mention a generalization of the conjecture, that deals with longer cycles/larger number of colors. The $ n $ -dimensional projective cube, denoted $ PQ_n $ , is the simple graph obtained from the $ (n+1) $ -dimensional cube~ $ Q_{n+1} $ by identifying pairs of antipodal vertices (vertices that differ in all coordinates). Note that $ PQ_4 $ is the Clebsch graph.

Question What is the largest integer $ k $ with the property that all cubic graphs of sufficiently high girth have a homomorphism to $ PQ_{2k} $ ?

Again, the question has several reformulations due to the following simple proposition.

Proposition For every graph $ G $ and nonnegative integer $ k $ , the following properties are equivalent.

\item There exists a coloring of~ $ E(G) $ by $ 2k+1 $ colors so that the complement of every color class is a bipartite graph. \item $ G $ has a homomorphism to $ PQ_{2k} $ \item $ G $ has a cut-continuous mapping to~ $ C_{2k+1} $

There are high-girth cubic graphs with the largest cut of size less then $ 0.94\cdot |E| $ . Such graphs do not admit a homomorphism to $ PQ_{2k} $ for any $ k \ge 8 $ , so there is indeed some largest integer~ $ k $ in the above question. To bound this largest~ $ k $ from below, recall that every cubic graph maps homomorphically to $ K_4 = PQ_2 $ . Moreover, it is known [DS] that cubic graphs of girth at least 17 admit a homomorphism to $ PQ_4 $ (the Clebsch graph). This shows $ k\ge 2 $ (and also provides a support for the main conjecture).

Related problems
Pentagon problem

Bibliography

[DNR] Matt DeVos, Jaroslav Nesetril and Andre Raspaud: On edge-maps whose inverse preserves flows and tensions, \MRref{MR2279171}

*[DS] Matt Devos, Robert Samal: \arXiv[High Girth Cubic Graphs Map to the Clebsch Graph}{math.CO/0602580}

[S] Robert Samal, On XY mappings, PhD thesis, Charles University 2006, tech. report

* indicates original appearance(s) of problem.
