---
id: opg-seymours_r_graph_conjecture
title: Seymour's r-graph conjecture
status: open
difficulty: frontier
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/seymours_r_graph_conjecture
---

# Statement

An $ r $ -graph is an $ r $ -regular graph $ G $ with the property that $ |\delta(X)| \ge r $ for every $ X \subseteq V(G) $ with odd size.

Conjecture $ \chi'(G) \le r+1 $ for every $ r $ -graph $ G $ .

# Source literature

- [NK] T. Nishizeki and K. Kashiwagi, An upper bound on the chromatic index of multigraphs. Graph theory with applications to algorithms and computer science (Kalamazoo, Mich., 1984), 595--604, Wiley-Intersci. Publ., Wiley, New York, 1985. MathSciNet.
- *[S] P.D. Seymour, On multicolourings of cubic graphs, and conjectures of Fulkerson and Tutte. Proc. London Math. Soc. (3) 38 (1979), no. 3, 423--460. MathSciNet.

# Progress

- This conjecture is among the most important unsolved problems in edge coloring. It is very close in nature to Goldberg's Conjecture, and is also closely related to Rizzi's packing postman sets conjecture (see packing T-joins).

If $ G $ is an $ r $ -regular graph and there exists $ X \subseteq V(G) $ with $ |X| $ odd and $ |\delta(X)| < r $ , then it is immediate that $ G $ is not $ r $ -edge-colourable, since every perfect matching must use at least one edge from $ \delta(X) $ . This is in some sense the only obvious obstruction to $ r $ -edge-colorability that we know of. So, $ r $ -graphs are the $ r $ -regular graphs which do not fail to be $ r $ -edge-colorable for this obvious reason. Not every $ r $ -graph is $ r $ -edge-colorable, for instance Petersen's graph is a 3-graph which is not 3-edge-colorable. However, this conjecture asserts that all such graphs are still $ (r+1) $ -edge-colorable.

This conjecture has been proved for $ r \le 11 $ by Nishizeki and Kashiwagi [NK].
