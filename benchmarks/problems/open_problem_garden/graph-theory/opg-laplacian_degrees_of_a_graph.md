---
id: opg-laplacian_degrees_of_a_graph
title: Laplacian Degrees of a Graph
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/laplacian_degrees_of_a_graph
---

# Statement

Conjecture If $ G $ is a connected graph on $ n $ vertices, then $ c_k(G) \ge d_k(G) $ for $ k = 1, 2, \dots, n-1 $ .

# Source literature

- [GM] R. Grone, R. Merris, The Laplacian spectrum of a graph II, SIAM J. Discrete Math.7 (1994) 221-229. MathSciNet
- [LP] J.S. Li, Y.L. Pan, A note on the second largest eigenvalue of the Laplacian matrix of a graph, Linear Multilin. Algebra 48 (2000) 117-121. MathSciNet
- *[G] J.-M. Guo, On the third largest Laplacian eigenvalue of a graph, Linear Multilin. Algebra 55 (2007) 93-102. MathSciNet
- [M] B. Mohar, Problem of the Month

# Progress

- (Reproduced from [M].)

Let $ L = D - A $ be the Laplacian matrix of a graph $ G $ of order $ n $ . Let $ t_k $ be the $ k $ -th largest eigenvalue of $ L $ ( $ k = 1,\dots,n $ ). For the purpose of this problem, we call the number $$ c_k = c_k(G) = t_k + k - 2 $$ the $ k $ -th Laplacian degree of $ G $ . In addition to that, let $ d_k(G) $ be the $ k $ -th largest (usual) degree in $ G $ . It is known that every connected graph satisfies $ c_k(G) \ge d_k(G) $ for $ k = 1 $ [GM], $ k = 2 $ [LP] and for $ k = 3 $ [G].
