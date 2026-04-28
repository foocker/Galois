---
id: opg-weak_saturation_of_the_cube_in_the_clique
title: Weak saturation of the cube in the clique
status: open
difficulty: graduate
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/weak_saturation_of_the_cube_in_the_clique
---

# Statement

Problem

Determine $ \text{wsat}(K_n,Q_3) $ .

# Source literature

- [MNS] N. Morrison, J. A. Noel, A. Scott. Saturation in the hypercube and bootstrap percolation. To appear in Combin. Probab. Comput.

# Progress

- Given graphs $ G $ and $ H $ , let $ \text{wsat}(G,H) $ denote the minimum number of edges in a subgraph $ F $ of $ G $ such that the edges of $ E(G)\setminus E(F) $ can be added to $ F $ , one edge at a time, so that each edge completes a copy of $ H $ when it is added.

Of course, if one can solve the problem above, then a natural next step is to determine $ \text{wsat}(K_n,Q_m) $ for all $ n $ and $ m $ .

Morrison, Noel and Scott [MNS] solved the related problem of determining $ \text{wsat}(Q_d,Q_m) $ for all $ d $ and $ m $ .
