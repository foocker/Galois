---
id: opg-partial_list_coloring
title: Partial List Coloring
status: open
difficulty: frontier
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/partial_list_coloring
---

# Statement

Conjecture Let $ G $ be a simple graph with $ n $ vertices and list chromatic number $ \chi_\ell(G) $ . Suppose that $ 0\leq t\leq \chi_\ell $ and each vertex of $ G $ is assigned a list of $ t $ colors. Then at least $ \frac{tn}{\chi_\ell(G)} $ vertices of $ G $ can be colored from these lists.

# Source literature

- *[AGH] M. Albertson, S. Grossman and R. Haas, Partial list colouring, Discrete Math., 214(2000), pp. 235-240.

# Progress

- Albertson, Grossman, and Haas introduce this interesting question in [AGH], and prove some partial results. For instance, they show that under the above assumptions, at least $ (1 - (\frac{ \chi(G) - 1}{\chi(G)} )^t) \cdot n $ vertices of $ G $ can be colored from the lists.
