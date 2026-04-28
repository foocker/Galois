---
id: opg-bouchets_6_flow_conjecture
title: Bouchet's 6-flow conjecture
status: open
difficulty: frontier
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/bouchets_6_flow_conjecture
---

# Statement

Conjecture Every bidirected graph with a nowhere-zero $ k $ -flow for some $ k $ , has a nowhere-zero $ 6 $ -flow.

# Source literature

- [B] A. Bouchet, Nowhere-Zero Integral Flows on a Bidirected Graph, J. Combinatorial Theory Ser. B 34 (1983) 279-292. MathSciNet
- [D] M. DeVos, Flows on Bidirected Graphs, preprint.
- [K] A. Khelladi, Nowhere-Zero Integral Chains and Flows in Bidirected Graphs, J. Combinatorial Theory Ser. B 43 (1987) 95-115. MathSciNet
- [Z] O. Zyka, Bidirected Nowhere-Zero Flows, Thesis, Charles University, Praha (1988).

# Progress

- Definition: A bidirected graph is a graph in which every edge has two arrowheads, one next to each endpoint. If the edge $ e $ has ends $ u $ and $ v $ , then the arrowheads nearest $ u $ and $ v $ may point either toward $ u $ or toward $ v $ (giving four possibilities in all). If $ G $ is a bidirected graph, a $ k $ -flow of G is a map $ \phi:E(G)\to \{-(k-1),...,-1,0,1,...,k-1\} $ with the property that at every vertex, the sum of $ \phi $ on the edges whose ends at $ v $ are directed into $ v $ is equal to the sum of $ \phi $ on the edges whose ends at $ v $ are directed out of $ v $ . We say that $ \phi $ is nowhere-zero if $ \phi(e) \neq 0 $ for every $ e \in E(G) $ (see nowhere-zero flows).

A bidirected Orientation of the Petersen graph

Flows on bidirected graphs arise naturally as duals of local-tensions on a non-orientable surface. For more on this relationship, see [B]. Bouchet proved that the above conjecture is true with 6 replaced by 216, and exhibited a bidirected Petersen graph as above which shows that 6 is the best value possible. Zyka [Z] and independently Fouquet improved upon this result proving that the above conjecture is true with 6 replaced by 30. Khelladi [K] proved that for 4-connected graphs, the above conjecture is true with 6 replaced by 18. DeVos [D] proved that the above conjecture holds with 6 replaced by 12, and showed that every 4-edge-connected bidirected graph with a nowhere-zero integer flow also has a nowhere-zero 4-flow.
