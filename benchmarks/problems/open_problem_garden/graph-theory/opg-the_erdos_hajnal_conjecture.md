---
id: opg-the_erdos_hajnal_conjecture
title: The Erdös-Hajnal Conjecture
status: open
difficulty: frontier
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/the_erdos_hajnal_conjecture
---

# Statement

Conjecture For every fixed graph $ H $ , there exists a constant $ \delta(H) $ , so that every graph $ G $ without an induced subgraph isomorphic to $ H $ contains either a clique or an independent set of size $ |V(G)|^{\delta(H)} $ .

# Source literature

- [APS] N. Alon, J. Pach, and J. Solymosi, Ramsey-type theorems with forbidden subgraphs, Combinatorica 21 (2001), 155-170.
- [EH] P. Erdös and A. Hajnal, Ramsey-type theorems, Discrete Appl. Math. 25 (1989), 37-52 MathSciNet

# Progress

- There are numerous interesting classes of graphs which are based upon forbidding one or more induced subgraphs. For instance: chordal graphs, split graphs, and claw-free graphs. Numerous other natural classes of graphs have been proved to have such characterizations, most famously perfect graphs, but also line graphs and comparability graphs. All of these classes are very well structured (far from random) and their members all either have large cliques or independent sets. On the flip side of this are random graphs. It is well known that a random graph on $ n $ vertices has both clique and independence number highly concentrated around $ 2 \log_2 n $ . The Erdos-Hajnal conjecture suggests a fundamental separation between these two worlds in terms of independence/clique sizes.

Erdös and Hajnal proved that this conjecture is true for the recursive class of graphs $ {\mathcal C} $ defined as follows. The one vertex graph is in $ {\mathcal C} $ , and if $ G_1 $ and $ G_2 $ lie in $ {\mathcal C} $ , then the disjoint union of $ G_1 $ and $ G_2 $ lies in $ {\mathcal C} $ , as does the graph obtained from the disjoint union by adding an edge between $ v_1 $ and $ v_2 $ for every $ v_1 \in V(G_1) $ and $ v_2 \in V(G_2) $ . More generally, Alon, Pach, and Solymosi proved that if $ F $ is a graph with $ V(F) = \{v_1,v_2,\ldots,v_n\} $ for which the Erdös-Hajnal conjecture holds, and $ H_1,\ldots,H_n $ are graphs for which the Erdos-Hajnal conjecture holds, then the graph obtained from $ F $ by blowing up each vertex $ v_i $ with a copy of $ H_i $ (more precisely, starting from the disjoint union of $ H_1,H_2,\ldots,H_n $ , we add all possible edges between the vertices of $ V(H_i) $ and $ V(H_j) $ if $ ij \in E(F) $ ) also satisfies the Erdos-Hajnal conjecture.

The Erdös-Hajnal property is known to hold for a number of small graphs (and using the above result this may be easily bootstrapped). For instance, the conjecture is known to hold when $ H $ is a path of three edges, and recently M. Chudnovsky and S. Safra have announced a proof when $ H $ is a bull (a triangle plus two pendant edges). However, our knowledge here is still quite limited. In particular, Lovasz has suggested the following very special case which remains open.

Question Is the Erdös-Hajnal conjecture true when $ H \cong C_5 $ ?
