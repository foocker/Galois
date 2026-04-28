---
id: opg-minimal_graphs_with_a_prescribed_number_of_spanning_trees
title: Minimal graphs with a prescribed number of spanning trees
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/minimal_graphs_with_a_prescribed_number_of_spanning_trees
---

# Statement

Conjecture Let $ n \geq 3 $ be an integer and let $ \alpha(n) $ denote the least integer $ k $ such that there exists a simple graph on $ k $ vertices having precisely $ n $ spanning trees. Then $ \alpha(n) = o(\log{n}). $

# Source literature

- [S] J. Sedlacek, On the minimal graph with a given number of spanning trees, Canad. Math. Bull. 13 (1970) 515-517.
- [A] J. Azarija, R. Skrekovski, Euler's idoneal numbers and an inequality concerning minimal graphs with a prescribed number of spanning trees, IMFM preprints 49 (2011) Link to paper
- * [C] Minimal graphs with a prescribed number of spanning trees

# Progress

- Observe that $ \alpha(n) $ is well defined for $ n \geq 3 $ since $ C_n $ has $ n $ spanning trees.

The function was introduced by Sedlacek [S] who has shown that for large enough $ n $ $ \alpha(n) \leq \frac{n+6}{3} \mbox{if } n \equiv 0 \pmod{3} $ and $ \alpha(n) \leq \frac{n+4}{3} \mbox{if } n \equiv 2 \pmod{3}. $

Using the fact that almost all positive integers $ n $ are expressible as $ n = ab+ac+bc $ for integers $ 0 < a < b < c $ it can be shown [A] that for large enough $ n $

$ \alpha(n) \leq \frac{n+4}{3} \mbox{if } n \equiv 2 \pmod{3} $ and $ \alpha(n) \leq \frac{n+9}{4} $ otherwise.

Moreover, the only fixed points of $ \alpha $ are 3, 4, 5, 6, 7, 10, 13 and 22.

The conjecture is motivated by the following graph (ploted for a very small sample of vertices)

The conjecture [C] is justifiable for highly composite numbers $ n $ since in this case one can construct the graph obtained after taking cycles $ C_{p_1}, \ldots,C_{p_k} $ for every odd prime factor $ p_i $ of $ n $ .
