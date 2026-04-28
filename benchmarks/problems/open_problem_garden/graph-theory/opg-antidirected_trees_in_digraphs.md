---
id: opg-antidirected_trees_in_digraphs
title: Antidirected trees in digraphs
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/antidirected_trees_in_digraphs
---

# Statement

An antidirected tree is an orientation of a tree in which every vertex has either indegree 0 or outdergree 0.

Conjecture Let $ D $ be a digraph. If $ |A(D)| > (k-2) |V(D)| $ , then $ D $ contains every antidirected tree of order $ k $ .

# Source literature


# Progress

- The value $ k-2 $ would be best possible, since the oriented tree consisting of a vertex dominating $ k-1 $ other vertices is not contained in any digraph in which every vertex has outdegree $ k-2 $ . The condition on the trees be antidirected cannot be suppressed. In a bipartite digraph $ D $ with bipartition $ (A,B) $ such that all arcs are directed from $ A $ to $ B $ , all the trees contained in $ D $ are antidirected.

This conjecture for symmetric digraphs is equivalent to the celebrated Erdös-Sos conjecture for undirected graphs. (see [E]).

Conjecture Let $ G $ be a graph. If $ |E(G)| > \frac{1}{2} (k-2) |V(G)| $ , then $ G $ contains every tree of order $ k $ .

Addario-Berry et al. Conjecture also implies Burr's conjecture (see Oriented trees in n-chromatic digraphs) for antidirected trees, since every digraph with chromatic number $ 2k-2 $ contains a colour-critical digraph has minimum degree at least $ 2k-3 $ , and so whose number of vertices is at least $ \frac{2k-3}{2}|V(D)| $ , which exceeds $ (k-2) |V(D)| $ .

This conjecture has only been proved [AHL+] for antidirected trees of diameter at most $ 3 $ .

Related problems
Oriented trees in n-chromatic digraphs

Bibliography

*[AHL+] L. Addario-Berry, F. Havet, C. Linhares Sales, B. Reed, and S. Thomassé. Oriented trees in digraphs. Discrete Mathematics, 313(8):967-974, 2013.

[E] P. Erdös, Some problems in graph theory, Theory of Graphs and Its Applications, M. Fielder, Editor, Academic Press, New York, 1965, pp. 29--36.

* indicates original appearance(s) of problem.
