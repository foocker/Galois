---
id: opg-bounding_the_chromatic_number_of_triangle_free_graphs_with_fixed_maximum_degree
title: Bounding the chromatic number of triangle-free graphs with fixed maximum degree
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/bounding_the_chromatic_number_of_triangle_free_graphs_with_fixed_maximum_degree
---

# Statement

Conjecture A triangle-free graph with maximum degree $ \Delta $ has chromatic number at most $ \ceil{\frac{\Delta}{2}}+2 $ .

# Source literature

- [K] Kostochka, A. V., Degree, girth and chromatic number. Combinatorics (Proc. Fifth Hungarian Colloq., Keszthely, 1976), Vol. II, pp. 679--696, Colloq. Math. Soc. János Bolyai, 18, North-Holland, Amsterdam-New York, 1978.
- *[R] Reed, B.A., $ \omega, \Delta $ , and $ \chi $ , J. Graph Theory 27 (1998) 177-212.

# Progress

- This conjecture is a special case of Reed's $ \omega $ , $ \Delta $ , and $ \chi $ conjecture, which posits that for any graph, $ \chi \leq \lceil\frac 12(\Delta+1+\omega)\rceil $ , where $ \omega $ , $ \Delta $ , and $ \chi $ are the clique number, maximum degree, and chromatic number of the graph respectively. Reed's conjecture is very easy to prove for complements of triangle-free graphs, but the triangle-free case seems challenging and interesting in its own right.

This conjecture is very much true for large values of $ \Delta $ ; Johansson proved that triangle-free graphs have chromatic number at most $ \frac{9\Delta}{\ln \Delta} $ . Surprisingly, the question appears to be open for every value of $ \Delta $ greater than four, up until Johansson's result implies the conjecture.

Kostochka previously proved that the chromatic number of a triangle-free graph is at most $ \frac{2\Delta}{3}+2 $ , and he proved that for every $ \Delta \geq 5 $ there is a $ g $ for which a graph of girth $ g $ has chromatic number at most $ \frac{\Delta}2+2 $ . Specifically, he showed that $ g \geq 4(\Delta+2)\ln \Delta $ is sufficient. In [K] he posed the general problem: "To find the best upper estimate for the chromatic number of the graph in terms of the maximal degree and density or girth."

The conjecture is implied by Brooks' Theorem for $ \Delta\leq 5 $ . The three smallest open values of $ \Delta $ offer natural entry points to this problem. The easiest seems to be:

Problem Does there exist a $ 6 $ -chromatic triangle-free graph of maximum degree 6?

Perhaps looking at graphs of girth at least five would also be a good starting point.
