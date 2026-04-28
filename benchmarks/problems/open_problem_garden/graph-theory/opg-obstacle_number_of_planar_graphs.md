---
id: opg-obstacle_number_of_planar_graphs
title: Obstacle number of planar graphs
status: open
difficulty: graduate
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/obstacle_number_of_planar_graphs
---

# Statement

Does there exist a planar graph with obstacle number greater than 1? Is there some $ k $ such that every planar graph has obstacle number at most $ k $ ?

# Source literature

- [AKL] Hannah Alpert, Christina Koch, and Joshua D. Laison: Obstacle numbers of graphs. Discrete Comput. Geom. (2010) 44:223-244.

# Progress

- A $ k $ -obstacle drawing of a graph $ G $ is a mapping of the vertices of $ G $ to points in the plane, along with a set of polygonal obstacles $ P_1,\ldots, P_k $ , such that two vertices are adjacent precisely if the line segment connecting their corresponding points in $ \mathbb R^2 $ does not intersect any obstacle. The {\em obstacle number} of a graph $ G $ is the minimum $ k $ such that $ G $ has a $ k $ -obstacle drawing.

This invariant was recently introduced by Alpert, Koch, and Laison [AKL], who proved that every outerplanar graph has obstacle number 1. The next question, then, follows naturally: what is the obstacle number of a planar graph? So far no planar graph has been proved to have obstacle number greater than 1. Alpert, Koch, and Laison specifically ask what the obstacle numbers of the icosahedron and dodecahedron are [AKL].
