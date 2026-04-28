---
id: opg-does_the_symmetric_chromatic_function_distinguish_trees
title: Does the chromatic symmetric function distinguish between trees?
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/does_the_symmetric_chromatic_function_distinguish_trees
---

# Statement

Problem Do there exist non-isomorphic trees which have the same chromatic symmetric function?

# Source literature

- [MMW] J. Martin, M. Morin, and J. D. Wagner, On distinguishing trees by their chromatic symmetric functions. J. Combin. Theory Ser. A 115 (2008), no. 2, 237–253. MathSciNet
- *[S] R. P. Stanley, A symmetric function generalization of the chromatic polynomial of a graph, Advances in Math. 111 (1995), 166–194.

# Progress

- Stanley [S] introduced the following symmetric function associated with a graph. Let $ x_1,x_2,\ldots $ be commuting indeterminates, and for every graph $ G=(V,E) $ let $ {\mathcal C}_G $ be the set of all proper colorings $ f: V \rightarrow {\mathbb N} $ . Then the chromatic symmetric function is defined to be \[ X_G = \sum_{f \in {\mathcal C}_G} \prod_{v \in V} x_{f(v)}. \] So, the coefficient of a term $ x_1^{d_1} x_2^{d_2} \ldots $ in $ X_G $ is precisely the number of proper colorings of $ G $ where color $ i $ appears exactly $ d_i $ times. It is immediate that $ X_G $ is homogeneous of degree $ |V| $ and is symmetric.

If we set $ x_1,x_2,\ldots,x_k = 1 $ and $ x_{k+1}, x_{k+2} \ldots = 0 $ and evaluate, we get the number of proper colorings of $ G $ using the colors $ 1,2,\ldots,k $ . Therefore, the chromatic symmetric function contains all of the information of the chromatic polynomial. In fact, the chromatic symmetric function contains strictly more information about the graph, since there exist examples of graphs which have distinct chromatic symmetric functions but have the same chromatic polynomial.

This natural problem of Stanley remains wide open. It has recently been established for some special classes of trees, namely caterpillars and spiders [MMW].
