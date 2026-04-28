---
id: opg-complete_bipartite_subgraphs_of_perfect_graphs
title: Complete bipartite subgraphs of perfect graphs
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/complete_bipartite_subgraphs_of_perfect_graphs
---

# Statement

Problem Let $ G $ be a perfect graph on $ n $ vertices. Is it true that either $ G $ or $ \bar{G} $ contains a complete bipartite subgraph with bipartition $ (A,B) $ so that $ |A|, |B| \ge n^{1 - o(1)} $ ?

# Source literature

- [F] J. Fox, A Bipartite Analogue of Dilworth’s Theorem, Order 23 (2006), 197-209.

# Progress

- Every perfect graph on $ n $ vertices either has a clique or an independent set of size $ \ge n^{1/2} $ , so weakening the bound on $ |A| $ , $ |B| $ to $ \lfloor \frac{1}{2} n^{1/2} \rfloor $ gives a true statement. Jacob Fox [F] has proved that every comparability graph $ G $ on $ n $ vertices has a complete bipartite subgraph of size $ \ge c \frac{n}{\log n} $ , and (up to the constant) this is best possible.
