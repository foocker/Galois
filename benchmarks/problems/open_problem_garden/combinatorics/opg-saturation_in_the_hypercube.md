---
id: opg-saturation_in_the_hypercube
title: Saturation in the Hypercube
status: open
difficulty: research
domains:
- Combinatorics
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/saturation_in_the_hypercube
---

# Statement

Question What is the saturation number of cycles of length $ 2\ell $ in the $ d $ -dimensional hypercube?

# Source literature

- [CG] S. Choi and P. Guan, Minimum critical squarefree subgraph of a hypercube, Proceedings of the Thirty-Ninth Southeastern International Conference on Combinatorics, Graph Theory and Computing, vol. 189, 2008, pp. 57–64.
- [EHM] P. Erdős, A. Hajnal, and J. W. Moon, A problem in graph theory, Amer. Math. Monthly 71 (1964), 1107–1110.
- [JP] J. R. Johnson and T. Pinto, Saturated subgraphs of the hypercube, arXiv:1406.1766v1, preprint, June 2014.
- [MNS] N. Morrison, J. A. Noel and A. Scott, Saturation in the Hypercube and Bootstrap Percolation, arXiv:1408.5488v2, June 2015.

# Progress

- Let $ G $ and $ H $ be graphs. Say that a spanning subgraph $ F $ of $ G $ is $ (G,H) $ -saturated if $ F $ contains no copy of $ H $ but $ F+e $ contains a copy of $ H $ for every edge $ e\in E(G)\setminus E(F) $ . Let $ \text{sat}(G,H) $ denote the minimum number of edges in a $ (G,H) $ -saturated graph. Saturation was introduced by Erdős, Hajnal and Moon [EHM] who proved the following:

Theorem (Erdős, Hajnal and Moon) For $ n\geq k\geq2 $ we have $ \text{sat}(K_n,K_k) = \binom{n}{2} = \binom{n-k+2}{2} $ .

Let $ Q_d $ denote the $ d $ -dimensional hypercube. Saturation of $ 4 $ -cycles in the hypercube has been studied by Choi and Guan [CG] who proved that $ \text{sat}(Q_d,C_4)\leq \left(\frac{1}{4} + o(1)\right)|E(Q_d)| $ . This was drastically improved by Johnson and Pinto [JP] to $ \text{sat}(Q_d,C_4) < 10\cdot 2^d $ . The saturation number for longer cycles in the hypercube is not known, though. The question above addresses this.

Another open problem is to determine the saturation number of sub-hypercubes in $ Q_d $ . This was first considered by Johnson and Pinto [JP] who proved that $ \text{sat}(Q_d,Q_m) = o\left(|E(Q_d)|\right) $ for fixed $ m $ and $ d\to \infty $ . This upper bound was improved to $ (1+o(1))72m^2 2^d $ by Morrison, Noel and Scott [MNS]. The best known lower bound on $ \text{sat}(Q_d,Q_m) $ for fixed $ m $ and large $ d $ , also due to [MNS], is $ (m-1-o(1))2^d $ .

Problem Improve the upper and lower bounds on $ \text{sat}(Q_d,Q_m) $ for fixed $ m $ and large $ d $ .

The results of [MNS] show that $ \text{sat}(Q_d,Q_m) = \Theta(2^d) $ for fixed $ m $ . Howver, the precise asymptotic behaviour of this quantity is unknown.

Question (Morrison, Noel and Scott) For fixed $ m\geq 2 $ , is it true that $ \frac{\text{sat}(Q_d,Q_m)}{2^d} $ converges as $ d\to \infty $ ?
