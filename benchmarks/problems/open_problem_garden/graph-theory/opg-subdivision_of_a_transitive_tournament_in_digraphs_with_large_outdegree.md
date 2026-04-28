---
id: opg-subdivision_of_a_transitive_tournament_in_digraphs_with_large_outdegree
title: Subdivision of a transitive tournament in digraphs with large outdegree.
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/subdivision_of_a_transitive_tournament_in_digraphs_with_large_outdegree
---

# Statement

Conjecture For all $ k $ there is an integer  $ f(k) $ such that every digraph of minimum outdegree at least  $ f(k) $ contains a subdivision of a transitive tournament of order $ k $ .

# Source literature

- [BT] B. Bollobás and A. Thomason, Proof of a conjecture of Mader, Erdös and Hajnal on topological complete subgraphs, European Journal of Combinatorics 19 (1998), 883–887.
- [DMMS] M. DeVos, J. McDonald, B. Mohar, and D. Scheide, Immersing complete digraphs, European Journal of Combinatorics, 33 (2012), no 6, 1294-1302.
- [KS] J. Komlós and E. Szemerédi, Topological Cliques in Graphs II, Combinatorics, Probability and Computing 5 (1996), 70–90.
- [M1] W. Mader, Homomorphieeigenschaften und mittlere Kantendichte von Graphen, Math. Annalen 174 (1967), 265–268.
- * [M2] W. Mader, Degree and Local Connectivity in Digraphs, Combinatorica 5 (1985), 161–165.
- [M3] W. Mader, On Topological Tournaments of order 4 in Digraphs of Outdegree 3, Journal of Graph Theory 21 (1996), 371–376.
- [T] C. Thomassen, Even Cycles in Directed Graphs, European Journal of Combinatorics 6 (1985), 85–89.

# Progress

- A fundamental result of Mader [M1] states that for every integer $ k $ there is a smallest $ g(k) $ so that every graph of average degree at least $ g(k) $ contains a subdivision of a complete graph on $ k $ vertices. Bollobás and Thomason [BT] as well as Komlós and Szemerédi [KS] showed that $ g $ is quadratic in $ k $ .

The above conjecture is a digraph analogue of this result. However one cannot replace the minimum outdegree in this conjecture by the average degree as in Mader's analogue for graphs: consider the complete bipartite graph $ K_{n,n} $ and orient all edges from the first to the second class. The resulting digraph has average degree $ n $ but not even a transitive tournament on 3 vertices.

One might be tempted to conjecture that large minimum outdegree would even force the existence of a subdivision of a large complete digraph. However, for all $ n $ Thomassen [T] constructed a digraph on $ n $ vertices whose minimum outdegree is at least $ \frac{1}{2} \log_2 n $ but which does not contain an even directed cycle (and thus no complete digraph on 3 vertices). A simpler construction was found by DeVos et al. [DMMS].

It is easy to see that  $ f(1)=0 $ and $ f(2)=1 $ . Mader [M3] showed that $ f(4) = 3 $ . Even the existence of  $ f(5) $ is not known.
