---
id: opg-the_bollobas_eldridge_catlin_conjecture_on_graph_packing
title: The Bollobás-Eldridge-Catlin Conjecture on graph packing
status: open
difficulty: frontier
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/the_bollobas_eldridge_catlin_conjecture_on_graph_packing
---

# Statement

Conjecture (BEC-conjecture) If $ G_1 $ and $ G_2 $ are $ n $ -vertex graphs and $ (\Delta(G_1) + 1) (\Delta(G_2) + 1) < n + 1 $ , then $ G_1 $ and $ G_2 $ pack.

# Source literature

- *[BE] B. Bollabás and S. E. Eldridge, Maximal matchings in graphs with given maximal and minimal degrees, Congr. Numer. XV (1976), 165--168.
- *[C] P. A. Catlin, Embedding subgraphs and coloring graphs under extremal degree conditions, Ph. D. Thesis, Ohio State Univ., Columbus (1976).
- [KY1] A. V. Kostochka and G. Yu, An Ore-type analogue of the Sauer-Spencer Theorem, Graphs Combin. 23 (2007), 419--424.
- [KY2] A. V. Kostochka and G. Yu, An Ore-type graph packing problems, Combin. Probab. Comput. 16 (2007), 167--169.
- [SS] N. Sauer and J. Spencer, Edge disjoint placement of graphs, J. Combin. Theory Ser. B 25 (1978), 295--302.

# Progress

- A pair of $ n $ -vertex graphs $ G_1 $ and $ G_2 $ are said to $ {\it pack} $ if they are edge-disjoint subgraphs of the complete graph on $ n $ vertices.

The main conjecture in the area of graph packing is the abovementioned conjecture by Bollobás, Eldridge [BE] and Catlin [C].

In support of the BEC-conjecture, Sauer and Spencer [SS] proved that if $ G_1 $ and $ G_2 $ are $ n $ -vertex graphs and $ 2 \Delta(G_1) \Delta(G_2) < n $ then $ G_1 $ and $ G_2 $ pack.

Given a graph $ G $ , $ L(G) $ denotes the line graph of $ G $ and $ \Theta(G) $ denotes the number $ \Delta(L(G)) + 2 $ . Kostochka and Yu [KY1] proved that if $ G_1 $ and $ G_2 $ are two $ n $ -vertex graphs with $ \Theta(G_1) \Delta(G_2) \leq n $ , then $ G_1 $ and $ G_2 $ pack with the following exceptions: (1) $ G_1 $ is a perfect matching and $ G_2 $ is either $ K_{n/2,n/2} $ with $ n/2 $ odd or contains $ K_{n/2 + 1} $ or (2) $ G_2 $ is a perfect matching and $ G_1 $ is $ K_{r,n-r} $ with $ r $ odd or contains $ K_{n/2 + 1} $ .

Kostachka and Yu [KY2] conjectured that if $ G_1 $ and $ G_2 $ are $ n $ -vertex graphs with $ \Theta(G_1) \Theta(G_2) < 2n $ then $ G_1 $ and $ G_2 $ pack.
