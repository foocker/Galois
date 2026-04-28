---
id: opg-rysers_conjecture
title: Ryser's conjecture
status: open
difficulty: frontier
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/rysers_conjecture
---

# Statement

Conjecture Let $ H $ be an $ r $ -uniform $ r $ -partite hypergraph. If $ \nu $ is the maximum number of pairwise disjoint edges in $ H $ , and $ \tau $ is the size of the smallest set of vertices which meets every edge, then $ \tau \le (r-1) \nu $ .

# Source literature

- [A] R. Aharoni, Ryser's conjecture for tripartite 3-graphs. Combinatorica 21 (2001), no. 1, 1--4. MathSciNet
- [AH] R. Aharoni and P. Haxell, Hall's theorem for hypergraphs. J. Graph Theory 35 (2000), no. 2, 83--88. MathSciNet
- [F] Z. Füredi, Maximum degree and fractional matchings in uniform hypergraphs, Combinatorica 1 (1981), 155--162. MathSciNet
- [K] D. König, Theorie der endlichen und unendlichen Graphen, Leipzig, 1936.
- [L] L. Lovász, On minimax theorems of combinatorics, Ph.D thesis, Matemathikai Lapok 26 (1975), 209--264 (in Hungarian). MathSciNet

# Progress

- Definitions: A (vertex) cover is a set of vertices which meets (has nonempty intersection with) every edge, and we let $ \tau(H) $ denote the size of the smallest vertex cover of $ H $ . A matching is a collection of pairwise disjoint edges, and we let $ \nu(H) $ denote the size of the largest matching in $ H $ . When the hypergraph is clear from context, we just write $ \tau $ or $ \nu $ .

It is immediate that $ \nu \le \tau $ , since every cover must contain at least one point from each edge in any matching. For $ r $ -uniform hypergraphs, $ \tau \le r \nu $ , since the union of the edges from any maximal matching is a set of at most $ r \nu $ vertices that which meets every edge. Ryser's conjecture is that this second bound can be improved if $ H $ is $ r $ -uniform and $ r $ -partite (the vertices may be partitioned into $ r $ sets $ V_1,V_2,\ldots,V_r $ so that every edge contains exactly one element of each $ V_i $ ).

In the special case when $ r=2 $ our trivial inequality yields $ \nu \le \tau $ and the conjecture implies $ \tau \le \nu $ , so we should have $ \nu = \tau $ . In fact this is true, it is König's theorem on bipartite graphs [K]. Indeed, Ryser's conjecture is probably easiest to view as a high dimensional generalization of this early result of König. Recently, Aharoni [A] has applied the "Hall's theorem for hypergraphs" result of Aharoni and Haxell [AH] to prove this conjecture for $ r=3 $ . However the case $ r=4 $ is still wide open.

Some other interesting work on this problem concerns fractional covers and fractional matchings. A fractional cover of $ H = (V,E) $ is a weighting $ a : V \rightarrow {\mathbb R}^+ $ so that $ \sum_{x \in S} a(x) \ge 1 $ for every $ S \in E $ , and the weight of this cover is $ \sum_{x \in V} a(x) $ . The fractional cover number, denoted $ \tau^* $ is the infimum of the set of weights of covers. Similarly, a fractional matching is an edge-weighting $ b : E \rightarrow {\mathbb R}^+ $ so that $ \sum_{S \ni x} b(S) \le 1 $ for every $ x \in V $ , and the weight of this matching is $ \sum_{S \in E} b(S) $ . The fractional matching number, denoted $ \nu^* $ is the supremum of the set of weights of fractional matchings. Fractional covers and matchings are the usual fractional relaxations, and by LP-duality, they satisfy $ \nu^* = \tau^* $ for every hypergraph. For $ r $ -regular $ r $ -partite hypergraphs, Füredi [F] has proved that $ \tau^* \le (r-1)\nu $ and Lovasz [L] has shown $ \tau \le \frac{1}{2} r \nu^* $ .
