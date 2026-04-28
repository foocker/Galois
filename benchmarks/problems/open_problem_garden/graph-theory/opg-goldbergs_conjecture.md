---
id: opg-goldbergs_conjecture
title: Goldberg's conjecture
status: open
difficulty: frontier
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/goldbergs_conjecture
---

# Statement

The overfull parameter is defined as follows: \[ w(G) = \max_{H \subseteq G} \left\lceil \frac{ |E(H)| }{ \lfloor \tfrac{1}{2} |V(H)| \rfloor} \right\rceil. \]

Conjecture Every graph $ G $ satisfies $ \chi'(G) \le \max\{ \Delta(G) + 1, w(G) \} $ .

# Source literature


# Progress

- This important problem remains open despite considerable attention. The same conjecture was independently discovered by Andersen and Seymour.

Vizing's Theorem, one of the cornerstones of graph colouring, shows that $ \chi'(G) \le \Delta(G) + 1 $ for every simple graph $ G $ . So, in particular, every simple graph satisfies Goldberg's conjecture. Graphs with parallel edges need not satisfy Vizing's bound. For instance, if $ G $ is the graph obtained from a triangle by adding an extra $ k-1 $ edges in parallel with each existing one, then $ \Delta(G) = 2k $ but $ \chi'(G) = 3k $ . More generally, if $ H $ is a subgraph of $ G $ , then every colour can appear on at most $ \lfloor \frac{1}{2}|V(H)| \rfloor $ edges of $ H $ , so $ \chi'(G) \ge |E(H)| / \lfloor \tfrac{1}{2} |V(H)| \rfloor $ . Thus, $ w(G) $ , our overfull parameter, is a natural lower bound on $ \chi'(G) $ , and Goldberg's conjecture asserts that whenever $ \chi'(G) $ exceeds $ \Delta(G)+1 $ , then it is equal to this lower bound.

Although the statement of the conjecture may appear to be the most natural formulation, there are a couple of related conjectures with similar lower bounds. For instance, Seymour's r-graph conjecture is equivalent to the statement that $ \chi'(G) \le \max \{\Delta(G), w(G) \} + 1 $ . Goldberg also conjectured that $ \chi'(G) \le \max\{ \Delta(G), w(G) + 1\} $ .

In addition to simple graphs, Goldberg's Conjecture is known to hold for any graph $ G $ which satisfies one of the following

\item $ \Delta(G) \le 11 $ \item $ G $ has no minor isomorphic to $ K_5 $ minus an edge. \item $ \Delta(G) $ is sufficiently large in comparison with $ |V(G)| $ .

$ \quad $

Packers And Movers Chandigarh
Packers And Movers Hyderabad
Packers And Movers Bangalore

Related problems
Seymour's r-graph conjecture

Bibliography

*[G] M. K. Goldberg, Multigraphs with a chromatic index that is nearly maximal. (Russian) A collection of articles dedicated to the memory of Vitaliĭ Konstantinovič Korobkov. Diskret. Analiz No. 23 (1973), 3--7, 72. MathSciNet

* indicates original appearance(s) of problem.
