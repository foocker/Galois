---
id: opg-seagull_problem
title: Seagull problem
status: open
difficulty: frontier
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/seagull_problem
---

# Statement

Conjecture Every $ n $ vertex graph with no independent set of size $ 3 $ has a complete graph on $ \ge \frac{n}{2} $ vertices as a minor.

# Source literature

- [KPT] K. Kawarabayashi, M. Plummer, and B. Toft, Improvements of the theorem of Duchet and Meynial's theorem on Hadwiger's Conjecture, J. Combin. Theory Ser. B. 95 (2005) 152-167.

# Progress

- This conjecture is significant because it is an interesting unproved consequence of Hadwiger's conjecture (this implication is proved next). In fact, some experts have suggested that this problem might hold the key to finding a counterexample to Hadwiger. I (M. DeVos) have attributed this conjecture to Seymour, but I believe that it may have been independently suggested by Mader and by others. Its curious title will be explained later in this discussion.

Hadwiger's conjecture (every loopless graph with chromatic number $ \ge n $ has $ K_n $ as a minor) is one of the outstanding problems in graph theory. This conjecture has been resolved for small values of $ n $ ; when $ n \le 4 $ it is relatively easy, for $ n=5,6 $ it has been proven to be equivalent to the Four color theorem. The Seagull problem concerns the other extreme - when the size of the chromatic number is close to the order of the graph. If $ G $ is an $ n $ vertex graph with no independent set of size 3, then $ \chi(G) \ge \frac{n}{2} $ since each color class has size $ \le 2 $ . If Hadwiger's conjecture holds for $ G $ , it must then have a minor which is a complete graph on $ \ge \frac{n}{2} $ vertices. This is precisely the statement of the Seagull problem.

The (essentially) best known bound for the conjecture is that every $ n $ vertex graph $ G $ with no independent set of size 3 has a complete graph on $ \ge \frac{n}{3} $ vertices as a minor. This argument is where the name of this conjecture arises. Let us call a seagull of $ G $ an induced subgraph which is a 2-edge path (such a subgraph may be drawn suggestively as a seagull). Then, for every seagull $ S $ and every vertex $ v $ not in $ S $ , there must be an edge between $ v $ and one of the two endpoints of $ S $ (this follows from the assumption that $ G $ has no independent set of size 3). This feature makes seagulls especially useful for constructing complete graphs as minors - as we now demonstrate. Choose a maximal collection $ {\mathcal S} $ of pairwise disjoint seagulls of $ G $ . The graph $ G' $ obtained from $ G $ by deleting every vertex which appears in a seagull in $ {\mathcal S} $ cannot have any two vertices at distance 2 from one another (since this would yield a seagull), so $ G' $ must be a disjoint union of complete graphs. Since $ G' $ has no independent set of size 3, it is in fact a disjoint union of at most two complete graphs. By deleting every vertex in the smaller complete subgraph of $ G' $ from $ G $ and then contracting both edges in every seagull in $ {\mathcal S} $ , we obtain a complete graph minor of $ G $ with size $ \ge \frac{n}{3} $ .

Kawarabayashi, Plummer, and Toft have improved this bound slightly by showing that $ G $ must have a complete graph minor of size $ \ge \frac{n + \omega(G)}{3} $ , but it looks very difficult to get much more out of this type of argument.
