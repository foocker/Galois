---
id: opg-list_total_colouring_conjecture
title: List Total Colouring Conjecture
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/list_total_colouring_conjecture
---

# Statement

Conjecture If $ G $ is the total graph of a multigraph, then $ \chi_\ell(G)=\chi(G) $ .

# Source literature


# Progress

- The list chromatic number of a graph $ G $ , denoted $ \chi_\ell(G) $ , is defined here. Given a multigraph $ H $ , the total graph $ T(H) $ of $ H $ is a graph on vertex set $ V(T(H)):=V(H)\cup E(H) $ where

\item two elements of $ V(H) $ are adjacent in $ T(H) $ if and only if they are adjacent in $ H $ ; \item two elements of $ E(H) $ are adjacent in $ T(H) $ if and only if they share an endpoint; \item an element of $ V(H) $ is adjacent to an element of $ E(H) $ in $ T(H) $ if it is incident with it.

This problem is related to the List (Edge) Colouring Conjecture as well as the Total Colouring Conjecture.

Kostochka and Woodall [KW] conjectured that $ \chi_\ell(G^2)=\chi(G^2) $ for every graph $ G $ ; this was known as the List Square Colouring Conjecture. It is stronger than the List Total Colouring Conjecture since, given a multigraph $ H $ , the total graph of $ H $ can be obtained by subdividing each edge of $ H $ and taking the square. Moreover, the graph obtained from $ H $ by subdividing each edge is bipartite and one part of the bipartition consists of vertices of degree $ 2 $ . Thus, the List Total Colouring Conjecture corresponds to this (very) special case of the List Square Colouring Conjecture.

However, the List Square Colouring Conjecture is not true in general. For a family of counterexamples, see the paper of Kim and Park [KP].

Related problems
Edge list coloring conjecture
Total Colouring Conjecture
Choosability of Graph Powers

Bibliography

*[BKW] O. V. Borodin, A. V. Kostochka, and D. R. Woodall. List edge and list totalcolourings of multigraphs. J. Combin. Theory Ser. B, 71(2):184–204, 1997.

[KW] A. V. Kostochka and D. R. Woodall. Choosability conjectures and multicircuits. Discrete Math., 240(1-3):123–143, 2001.

[KP] Seog-Jin Kim and Boram Park: Counterexamples to the List Square Coloring Conjecture, submitted.

* indicates original appearance(s) of problem.
