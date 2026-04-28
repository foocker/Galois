---
id: opg-geodesic_cycles_and_tuttes_theorem
title: Geodesic cycles and Tutte's Theorem
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/geodesic_cycles_and_tuttes_theorem
---

# Statement

Problem If $ G $ is a $ 3 $ -connected finite graph, is there an assignment of lengths $ \ell: E(G) \to \mathb R^+ $ to the edges of $ G $ , such that every $ \ell $ -geodesic cycle is peripheral?

# Source literature

- *[GS] Angelos Georgakopoulos, Philipp Sprüssel: Geodesic topological cycles in locally finite graphs. Preprint 2007.
- [T] W.T. Tutte, How to draw a graph. Proc. London Math. Soc. 13 (1963), 743–768.

# Progress

- A cycle $ C $ is $ \ell $ -geodesic if for every two vertices $ x,y $ on $ C $ there is no $ x $ - $ y $ ~path in $ G $ shorter, with respect to $ \ell $ , than both $ x $ - $ y $ ~arcs on $ C $ .

It is not hard to prove [GS] that for every finite graph $ G $ and every assignment of edge lengths $ \ell: E(G) \to \mathb R^+ $ the $ \ell $ -geodesic cycles of $ G $ generate its cycle space. Thus, a positive answer to the problem would imply a new proof of Tutte's classical theorem [T] that the peripheral cycles of a $ 3 $ -connected finite graph generate its cycle space.
