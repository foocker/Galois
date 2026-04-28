---
id: opg-earth_moon_problem
title: Earth-Moon Problem
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/earth_moon_problem
---

# Statement

Problem What is the maximum number of colours needed to colour countries such that no two countries sharing a common border have the same colour in the case where each country consists of one region on earth and one region on the moon ?

# Source literature


# Progress

- In term of graphs, it can be rephrased as follows. What is the maximum chromatic number of a graph $ G $ which is the union of two planar graphs (on the same vertex set)?

If a graph $ G $ on $ n $ vertices is the union of two planar graphs, then it has at most $ 2(3n-6) $ edges, and so it is has a vertex of degree at most $ 11 $ . An easy induction shows that $ G $ is 12-colourable, as observed by Heawood [He]. Gardner [G] reported an example requiring 9 colours (the join of $ C_5 $ and $ K_6 $ ). It is not known if configurations exist requiring 10, 11, or 12 colours.

More generally, one may ask for the maximum chromatic number of the union of $ k $ planar graphs.

Problem What is the maximum chromatic number of a graph $ G $ which is the union of $ k $ planar graphs?

The same reasoning as above shows that $ 6k $ colours are always sufficient. The minimum number of planar graphs to decompose a complete graph [BW] gives a lower bound of $ 6k-2 $ for $ k \ne 2 $ .

Bibliography

[BW] L. W. Beineke and A. T. White, Topological Graph Theory, Selected Topics in Graph Theory, L. W. Beineke and R. J. Wilson, eds., Academic Press, 15-50, 1978.

[G] M. Gardner, Mathematical Recreations: The Coloring of Unusual Maps Leads Into Uncharted Territory. Sci. Amer. 242, 14-22, 1980.

[He] P.J. Heawood, Map Colour Theorems. Quart. J. Pure Appl. Math. 24, 332-338, 1890.

*[R] G. Ringel, Färbungsprobleme auf Flachen und Graphen. Berlin: Deutsche Verlag der Wissenschaften, 1959.

* indicates original appearance(s) of problem.
