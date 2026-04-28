---
id: opg-infinite_uniquely_hamiltonian_graphs
title: Infinite uniquely hamiltonian graphs
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/infinite_uniquely_hamiltonian_graphs
---

# Statement

Problem Are there any uniquely hamiltonian locally finite 1-ended graphs which are regular of degree $ r > 2 $ ?

# Source literature

- [D] R. Diestel, Graph Theory, Third Edition, Springer, 2005.
- *[M] Bojan Mohar, Problem of the Month

# Progress

- (Originally appeared as [M].)

Let $ G $ be a locally finite infinite graph and let $ I(G) $ be the set of ends of~ $ G $ . The Freudenthal compactification of $ G $ is the topological space $ |G| $ which is obtained from the usual topological space of the graph, when viewed as a 1-dimensional cell complex, by adding all points of $ I(G) $ and setting, for each end $ t \in I(G) $ , the basic set of neighborhoods of $ t $ to consist of sets of the form $ C(S, t) \cup I(S,t) \cup E'(S,t) $ , where $ S $ ranges over the finite subsets of $ V(G) $ , $ C(S, t) $ is the component of $ G - S $ containing all rays in $ t $ , the set $ I(S,t) $ contains all ends in $ I(G) $ having rays in $ C(S, t) $ , and $ E'(S,t) $ is the union of half-edges $ (z,y] $ , one for every edge $ xy $ joining $ S $ and $ C(S,t) $ . We define a hamilton circle in $ |G| $ as a homeomorphic image $ C $ of the unit circle $ S^1 $ into $ |G| $ such that every vertex (and hence every end) of $ G $ appears in $ C $ . More details about these notions can be found in [D].

A graph $ G $ (finite or infinite) is said to be uniquely hamiltonian if it contains precisely one hamilton circle.

For finite graphs, the celebrated Sheehan's conjecture states that there are no $ r $ -regular uniquely hamiltonian graphs for $ r>2 $ ; this is known for all odd $ r $ and even $ r > 23 $ . For infinite graphs this is false even for odd $ r $ (e.g. for the two-way infinite ladder), but each of the known counterexamples has at least 2 ends, leading to the problem stated.

Another way to extend Sheehan's conjecture to infinite graphs is to define degree of an end $ t \in I(G) $ to be the maximal number of disjoint rays in $ t $ and ask the following:

Problem Are there any uniquely hamiltonian locally finite graphs where every vertex and every end has the same degree $ r > 2 $ ?
