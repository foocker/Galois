---
id: opg-unit_vector_flows
title: Unit vector flows
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/unit_vector_flows
---

# Statement

Conjecture For every graph $ G $ without a bridge, there is a flow $ \phi : E(G) \rightarrow S^2 = \{ x \in {\mathbb R}^3 : |x| = 1 \} $ .

# Source literature

- [BJJ] J.C. Bermond, B. Jackson, and F. Jaeger, Shortest covering of graphs with cycles, J. Combinatorial Theory Ser. B 35 (1983), 297-308. MRhref{0735197}
- [T54] W.T. Tutte, A Contribution on the Theory of Chromatic Polynomials, Canad. J. Math. 6 (1954) 80-91. MathSciNet
- [T66] W.T. Tutte, On the Algebraic Theory of Graph Colorings, J. Combinatorial Theory 1 (1966) 15-50. MathSciNet

# Progress

- The main interest in these two conjectures is that together they imply Tutte's 5-flow conjecture. This follows easily from the fact that the 5-flow conjecture can be reduced to cubic graphs without bridges, and for such a graph $ G $ , the composition of the maps $ \phi $ and $ q $ (given by the above conjectures) is a nowhere-zero 5-flow.

There are a couple of easy partial results toward the first conjecture which follow from well-known flow/cycle-cover results. First, Tutte showed that every graph with a nowhere-zero 4-flow has a list of three 2-flows $ f_1,f_2,f_3 : E(G) \to \{-1,0,1\} $ so that every edge is in the support of exactly two of these flows. Combining these flows and normalizing appropriately gives an $ S^2 $ -flow. Bermond, Jackson, and Jaeger [BJJ] showed that every graph with no bridge has a list of seven 2-flows so that every edge is in the support of exactly four of these flows. Combining these and normalizing appropriately gives an $ S^6 $ -flow.

It seems likely that a graph has an $ S^1 $ -flow if and only if it has a nowhere-zero 3-flow. The "if" direction of this implication isn't hard to show and the "only if" direction looks quite possible.

A dual concept to that of a flow is that of a tension. Observe that a graph $ G $ has a $ S^n $ tension if and only if can be embedded in $ {\mathbb R}^{n+1} $ so that all edges are unit length line segments. Such embeddings have received some attention over the years. In particular, there is considerable interest in finding the best possible upper bound on the chromatic number of graphs which embed in $ {\mathbb R}^2 $ in this manner. This is Hadwinger-Nelson problem on coloring the plane.
