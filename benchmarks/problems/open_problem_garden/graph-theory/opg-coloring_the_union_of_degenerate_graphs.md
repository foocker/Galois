---
id: opg-coloring_the_union_of_degenerate_graphs
title: Coloring the union of degenerate graphs
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/coloring_the_union_of_degenerate_graphs
---

# Statement

Conjecture The union of a $ 1 $ -degenerate graph (a forest) and a $ 2 $ -degenerate graph is $ 5 $ -colourable.

# Source literature


# Progress

- A graph is $ k $ -degenerate if it can be reduced to $ K_1 $ (the graph with a unique vertex) by repeatedly deleting vertices of degree at most $ k $ . A $ 1 $ -degenerate graph $ G_1 $ admits a proper $ 2 $ -colouring $ c_1 $ , and a $ 2 $ -degenerate graph $ G_2 $ admits a proper $ 3 $ -colouring $ c_2 $ . Thus, $ (c_1,c_2) $ is a proper $ 6 $ -colouring of $ G_1 $ and $ G_2 $ .

The conjecture is tigth because $ K_5 $ is the union of a $ 1 $ -degenerate graph and a $ 2 $ -degenerate graph.

Based on a decompostion of the complete graph, Klein and Schönheim [KlSc93] generalised this conjecture to $ (m_1, \dots, m_s) $ -composed graphs, which are unions of $ s $ graphs $ G_1, \dots , G_s $ such that $ G_i $ is $ m_i $ -degenerate, $ 1\leq i\leq s $ .

Conjecture Every $ (m_1, \dots, m_s) $ -composed graph is $ \left(\sum_{i=1}^s m_i+\bigg\lfloor\frac{1}{2}\bigg(1+\sqrt{1+8\sum_{1\leq i<j\leq s}m_i m_j}\bigg)\bigg\rfloor\right) $ -colourable.

Partial results towards this conjecture are obtained in [KlSc95].

Bibliography

*[K] R. Klein. On the colorability of { $ m $ }-composed graphs. Discrete Math. 133 (1994), 181--190.

[KlSc93] R. Klein and J. Schönheim. Decomposition of { $ K_n $ } into degenerate graphs. In Combinatorics and graph theory (Hefei, 1992), pages 141--155. World Sci. Publ., River Edge, NJ, 1993.

[KlSc95] R. Klein and J. Schönheim. On the colorability of graphs decomposable into degenerate graphs with specified degeneracy. Australas. J. Combin., 12:201--208, 1995.

* indicates original appearance(s) of problem.
