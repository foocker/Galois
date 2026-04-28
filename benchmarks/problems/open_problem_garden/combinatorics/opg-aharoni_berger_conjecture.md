---
id: opg-aharoni_berger_conjecture
title: Aharoni-Berger conjecture
status: open
difficulty: frontier
domains:
- Combinatorics
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/aharoni_berger_conjecture
---

# Statement

Conjecture If $ M_1,\ldots,M_k $ are matroids on $ E $ and $ \sum_{i=1}^k rk_{M_i}(X_i) \ge \ell (k-1) $ for every partition $ \{X_1,\ldots,X_k\} $ of $ E $ , then there exists $ X \subseteq E $ with $ |X| = \ell $ which is independent in every $ M_i $ .

# Source literature

- [A] R. Aharoni, Ryser's conjecture for tripartite 3-graphs, Combinatorica 21 (2001), 1-4. MathSciNet
- *[AB] R. Aharoni, E. Berger, The intersection of a matroid with a simplicial complex. Trans. Amer. Math. Soc. 358 (2006), no. 11 MathSciNet

# Progress

- Let us begin by stating two classic results. For a graph (or hypergraph) we let $ \tau $ denote the size of the smallest (vertex) cover and we let $ \nu $ denote the size of the largest matching.

Theorem (König) $ \nu = \tau $ for every bipartite graph.

Theorem (Matroid Intersection) If $ M_1,M_2 $ are matroids on $ E $ and $ rk_{M_1}(X_1) + rk_{M_2}(X_2) \ge \ell $ for every partition $ \{X_1,X_2\} $ of $ E $ , then there exists $ X \subseteq E $ with $ |X| = \ell $ which is independent in both $ M_1 $ and $ M_2 $ .

The matroid intersection theorem is exactly the $ k=2 $ case of the above conjecture, but it may also be viewed as a generalization of König's theorem. To see this, let $ G $ be a bipartite graph with edge set $ E $ and bipartition $ \{A_1,A_2\} $ and for $ i=1,2 $ let $ M_i $ be the (uniform) matroid on $ E $ where a subset $ S \subseteq E $ is independent if no two edges in $ S $ share an endpoint in $ A_i $ . Then $ rk_{M_i}(S) $ is the number of vertices in $ A_i $ which are incident with an edge in $ S $ , so $ rk_{M_1}(X_1) + rk_{M_2}(X_2) $ has minimum value $ \tau $ , and a set of edges is independent in both $ M_1 $ and $ M_2 $ if and only if it is a matching, so the size of the largest such set is $ \nu $ .

A famous conjecture of Ryser suggests a generalization of König's theorem to hypergraphs. It claims that every $ k $ -partite $ k $ -uniform hypergraph satisfies $ \tau \le (k-1) \nu $ . The above conjecture is the common generalization of this conjecture of Ryser and the matroid intersection theorem. Aharoni [A] proved the 3-partite 3-uniform case of Ryser's conjecture, and this was extended by Aharoni-Berger [AB] to the $ k=3 $ case of the above conjecture. The conjecture remains open for $ k \ge 4 $ .
