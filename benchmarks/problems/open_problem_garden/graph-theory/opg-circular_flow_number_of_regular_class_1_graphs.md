---
id: opg-circular_flow_number_of_regular_class_1_graphs
title: Circular flow number of regular class 1 graphs
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/circular_flow_number_of_regular_class_1_graphs
---

# Statement

A nowhere-zero $ r $ -flow $ (D(G),\phi) $ on $ G $ is an orientation $ D $ of $ G $ together with a function $ \phi $ from the edge set of $ G $ into the real numbers such that $ 1 \leq |\phi(e)| \leq r-1 $ , for all $ e \in E(G) $ , and $ \sum_{e \in E^+(v)}\phi(e) = \sum_{e \in E^-(v)}\phi(e), \textrm{ for all } v \in V(G) $ . The circular flow number of $ G $ is inf $ \{ r | G $ has a nowhere-zero $ r $ -flow $ \} $ , and it is denoted by $ F_c(G) $ .

A graph with maximum vertex degree $ k $ is a class 1 graph if its edge chromatic number is $ k $ .

Conjecture Let $ t \geq 1 $ be an integer and $ G $ a $ (2t+1) $ -regular graph. If $ G $ is a class 1 graph, then $ F_c(G) \leq 2 + \frac{2}{t} $ .

# Source literature

- [ES_2001] E. Steffen, Circular flow numbers of regular multigraphs, J. Graph Theory 36, 24 – 34 (2001)
- *[ES_2015] E. Steffen, Edge-colorings and circular flow numbers on regular graphs, J. Graph Theory 79, 1–7, 2015

# Progress

- The conjecture is true for $ t=1 $ , i.e. for cubic graphs. It says, that the circular flow number of $ (2t+1) $ -regular class 1 graphs is bounded by the circular flow number of the complete graph on $ 2t+2 $ vertices.
