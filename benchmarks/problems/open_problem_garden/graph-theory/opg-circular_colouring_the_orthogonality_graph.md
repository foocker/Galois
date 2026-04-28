---
id: opg-circular_colouring_the_orthogonality_graph
title: Circular colouring the orthogonality graph
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/circular_colouring_the_orthogonality_graph
---

# Statement

Let $ {\mathcal O} $ denote the graph with vertex set consisting of all lines through the origin in $ {\mathbb R}^3 $ and two vertices adjacent in $ {\mathcal O} $ if they are perpendicular.

Problem Is $ \chi_c({\mathcal O}) = 4 $ ?

# Source literature


# Progress

- In the problem statement, $ \chi_c $ denotes the circular chromatic number.

Coloring properties of $ {\mathcal O} $ are, rather surprisingly, of interest in quantum mechanics. If the spins of certain particles are measured in three orthogonal directions, then these measurements always return one $ 0 $ and two values which are $ \pm 1 $ . If such a particle has "decided" in advance how it will respond to any possible measurement, then the set of directions in which it will respond $ 0 $ must be an independent set in the orthogonality graph $ {\mathcal O} $ which meets every triangle. Kochen and Specker have shown that $ {\mathcal O} $ (even certain finite subgraphs of it) does not have any independent set meeting every triangle, thus exhibiting a rather mysterious property of these particles. In some sense, if the person doing the measurement has the free will to decide in which directions to measure, then the particle must have some free will to decide how it will respond.

The property that $ {\mathcal O} $ has no independent set which meets every triangle shows that $ \chi({\mathcal O}) \ge 4 $ . On the other hand, if we center a regular octahedron at the origin, and assign a color to each line $ L $ depending on which pair of opposite faces it passes through (if $ L $ meets more than one pair of opposite faces, just choose one) we get a proper 4-coloring of $ {\mathcal O} $ . Therefore, $ \chi({\mathcal O}) = 4 $ .

These bounds prove that $ 3 \le \chi_c({\mathcal O}) \le 4 $ . By investigating certain finite subgraphs of $ {\mathcal O} $ , DeVos, Ghebleh, Goddyn, Mohar, and Naserasr have shown that $ \chi_c({\mathcal O}) \ge 3.5 $ .
