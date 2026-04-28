---
id: opg-oriented_trees_in_n_chromatic_digraphs
title: Oriented trees in n-chromatic digraphs
status: open
difficulty: frontier
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/oriented_trees_in_n_chromatic_digraphs
---

# Statement

Conjecture Every digraph with chromatic number at least $ 2k-2 $ contains every oriented tree of order $ k $ as a subdigraph.

# Source literature


# Progress

- The conjectured bound is best possible, because a regular tournament of order $ 2k-3 $ does not contain the oriented tree consisting of a vertex dominating $ k-1 $ leaves.

Let $ f $ be the function $ f $ such that every oriented tree of order $ k $ is $ f(k) $ -universal, that is contained in every digraph with chromatic number at least $ f(k) $ . Burr proved that $ f(k) \leq (k-1)^2 $ . This was slightly improved by Addario-Berry et al. [AHL+] who proved $ f(k)\leq k^2/2-k/2+1 $ .

Burr's conjecture has been proved only in few particular cases of digraphs: tournaments, and acyclic digraphs. Kühn, Mycroft, and Osthus [KMS] showed that every oriented tree of order $ k $ is contained in every tournament of order $ 2k-2 $ for all sufficiently large $ k $ (so proving a Conjecture of Sumner); Addario-Berry et al. [AHL+] proved that every acyclic digraph with chromatic number $ k $ contains every oriented tree of order $ k $ .

Burr's conjecture or some approximation have been also proved for special classes of trees. Gallai-Roy's celebrated theorem states that every directed path of order $ k $ is $ k $ -universal; El-Sahili [E] proved that every oriented path of order $ 4 $ is $ 4 $ -universal and that the antidirected path of order $ 5 $ is $ 5 $ -universal; Addario-Berry, Havet, and Thomassé [AHT] showed that every oriented path of order $ k $ whose vertex set can be partioned into two directed paths is $ k $ -universal; Addario-Berry et al. [AHL+] showed that antidirected trees (oriented trees in which every vertex has in-degree $ 0 $ or out-degree $ 0 $ ) are $ 5k $ -universal.

Havet, generalizing a conjecture of Havet and Thomassé (see [H]) on tournaments, conjectured that the following could also be true.

Conjecture Every digraph with chromatic number at least $ k+\ell+1 $ contains every oriented tree of order $ k $ with $ k $ leaves.

Bibliography

[AHL+] L. Addario-Berry, F. Havet, C. Linhares Sales, B. Reed, and S. Thomassé. Oriented trees in digraphs. Discrete Mathematics, 313(8):967-974, 2013.

[AHT] L. Addario-Berry, F. Havet, and S. Thomassé, Paths with two blocks in $ n $ -chromatic digraphs, J. of Combinatorial Theory Ser. B, 97 (2007), 620--626.

* [B] A. Burr, Subtrees of directed graphs and hypergraphs, Proceedings of the Eleventh Southeastern Conference on Combinatorics, Graph Theory and Computing, Boca Raton, Congr. Numer., 28 (1980), 227--239.

[H] F. Havet, Trees in tournaments. Discrete Mathematics 243 (2002), no. 1-3, 121--134.

[KOM] D. Kühn, D. Osthus, and R. Mycroft, A proof of Sumner's universal tournament conjecture for large tournaments, Proceedings of the London Mathematical Society 102 (2011), 731--766.

* indicates original appearance(s) of problem.
