---
id: opg-partial_list_coloring_0
title: Partial List Coloring
status: open
difficulty: frontier
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/partial_list_coloring_0
---

# Statement

Let $ G $ be a simple graph, and for every list assignment $ \mathcal{L} $ let $ \lambda_{\mathcal{L}} $ be the maximum number of vertices of $ G $ which are colorable with respect to $ \mathcal{L} $ . Define $ \lambda_t = \min{ \lambda_{\mathcal{L}} } $ , where the minimum is taken over all list assignments $ \mathcal{L} $ with $ |\mathcal{L}| = t $ for all $ v \in V(G) $ .

Conjecture [2] Let $ G $ be a graph with list chromatic number $ \chi_\ell $ and $ 1\leq r\leq s\leq \chi_\ell $ . Then \[\frac{\lambda_r}{r}\geq\frac{\lambda_s}{s}.\]

# Source literature

- [1] M. Albertson, S. Grossman and R. Haas, Partial list colouring, Discrete Math., 214(2000), pp. 235-240.
- [2] Moharram N. Iradmusa, A Note on Partial List Colorings, Australasian Journal of Combinatorics, Vol.46, 2010, $ 19-24 $ .

# Progress

- As you see this conjecture in the special case $ s=\chi_\ell $ , is the conjecture of Albertson, Grossman and Haas [1]: $ \lambda_t\geq\frac{tn}{\chi_\ell} $ for any $ 0\leq t\leq \chi_\ell $ .
