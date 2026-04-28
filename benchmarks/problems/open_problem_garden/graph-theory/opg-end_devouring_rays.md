---
id: opg-end_devouring_rays
title: End-Devouring Rays
status: open
difficulty: graduate
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/end_devouring_rays
---

# Statement

Problem Let $ G $ be a graph, $ \omega $ a countable end of $ G $ , and $ K $ an infinite set of pairwise disjoint $ \omega $ -rays in $ G $ . Prove that there is a set $ K' $ of pairwise disjoint $ \omega $ -rays that devours $ \omega $ such that the set of starting vertices of rays in $ K' $ equals the set of starting vertices of rays in $ K $ .

# Source literature

- *[G] A. Georgakopoulos, Infinite Hamilton Cycles in Squares of Locally Finite Graphs, Preprint.

# Progress

- We say that a set of rays $ K $ devours the end $ \omega $ if every ray in $ \omega $ meets some ray in $ K $ . An end is countable if there is a countable set of rays devouring it.

If $ K $ is a finite set of rays then it is not hard to prove (see [G]) that this problem has a positive answer:

Theorem For every graph $ G $ and every countable end $ \omega $ of $ G $ , if $ G $ has a set $ K $ of $ k\in \mathcal N $ pairwise disjoint $ \omega $ -rays, then it also has a set $ K' $ of $ k $ pairwise disjoint $ \omega $ -rays that devours $ \omega $ . Moreover, $ K' $ can be chosen so that its rays have the same starting vertices as the rays in~ $ K $ .
