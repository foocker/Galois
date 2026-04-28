---
id: opg-vertex_coloring_of_graph_fractional_powers
title: Vertex Coloring of graph fractional powers
status: open
difficulty: frontier
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/vertex_coloring_of_graph_fractional_powers
---

# Statement

Conjecture Let $ G $ be a graph and $ k $ be a positive integer. The $ k- $ power of $ G $ , denoted by $ G^k $ , is defined on the vertex set $ V(G) $ , by connecting any two distinct vertices $ x $ and $ y $ with distance at most $ k $ . In other words, $ E(G^k)=\{xy:1\leq d_G(x,y)\leq k\} $ . Also $ k- $ subdivision of $ G $ , denoted by $ G^\frac{1}{k} $ , is constructed by replacing each edge $ ij $ of $ G $ with a path of length $ k $ . Note that for $ k=1 $ , we have $ G^\frac{1}{1}=G^1=G $ .
Now we can define the fractional power of a graph as follows:
Let $ G $ be a graph and $ m,n\in \mathbb{N} $ . The graph $ G^{\frac{m}{n}} $ is defined by the $ m- $ power of the $ n- $ subdivision of $ G $ . In other words $ G^{\frac{m}{n}}\isdef (G^{\frac{1}{n}})^m $ .
Conjecture. Let $ G $ be a connected graph with $ \Delta(G)\geq3 $ and $ m $ be a positive integer greater than 1. Then for any positive integer $ n>m $ , we have $ \chi(G^{\frac{m}{n}})=\omega(G^\frac{m}{n}) $ .
In [1], it was shown that this conjecture is true in some special cases.

# Source literature

- [1] Iradmusa, Moharram N., On colorings of graph fractional powers. Discrete Math. 310 (2010), no. 10-11, 1551–1556.

# Progress

- Status: open.
