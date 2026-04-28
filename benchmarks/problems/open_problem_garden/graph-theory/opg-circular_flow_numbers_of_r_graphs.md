---
id: opg-circular_flow_numbers_of_r_graphs
title: Circular flow numbers of $r$-graphs
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/circular_flow_numbers_of_r_graphs
---

# Statement

A nowhere-zero $ r $ -flow $ (D(G),\phi) $ on $ G $ is an orientation $ D $ of $ G $ together with a function $ \phi $ from the edge set of $ G $ into the real numbers such that $ 1 \leq |\phi(e)| \leq r-1 $ , for all $ e \in E(G) $ , and $ \sum_{e \in E^+(v)}\phi(e) = \sum_{e \in E^-(v)}\phi(e), \textrm{ for all } v \in V(G) $ .

A $ (2t+1) $ -regular graph $ G $ is a $ (2t+1) $ -graph if $ |\partial_G(X)| \geq 2t+1 $ for every $ X \subseteq V(G) $ with $ |X| $ odd.

Conjecture Let $ t > 1 $ be an integer. If $ G $ is a $ (2t+1) $ -graph, then $ F_c(G) \leq 2 + \frac{2}{t} $ .

# Source literature

- *[ES_2015]E. Steffen, Edge-colorings and circular flow numbers on regular graphs, J. Graph Theory 79, 1–7, 2015

# Progress

- Since every $ (2t+1) $ -regular class 1 graph is a $ (2t+1) $ -graph, the truth of this conjecture would imply the truth of the conjecture on the circular flow number of regular class 1 graphs. If it is true for even $ t $ , say $ t=2t' $ , then Jaeger's modular orientation conjecture is true for $ (4t'+1) $ -regular graphs and hence, by a result of Jaeger, it would imply the truth of Tutte's 5-flow conjecture. For $ t=2 $ it is Tutte's 3-flow conjecture.
