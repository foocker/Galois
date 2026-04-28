---
id: opg-decomposing_an_even_tournament_in_directed_paths
title: Decomposing an even tournament in directed paths.
status: open
difficulty: frontier
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/decomposing_an_even_tournament_in_directed_paths
---

# Statement

Conjecture Every tournament $ D $ on an even number of vertices can be decomposed into $ \sum_{v\in V}\max\{0,d^+(v)-d^-(v)\} $ directed paths.

# Source literature


# Progress

- This conjecture is clearly tight, because in a decomposition of a directed graph in directed paths, at least $ \max \{0,d^+(v)-d^-(v)\} $ directed paths must start at vertex $ v $ .

Observe that the analogue is trivially false for odd tournament: in regular tournament $ d^+(v)=d^-(v) $ for every vertex $ v $ , so $ \sum_{v\in V}\max\{0,d^+(v)-d^-(v)\}=0 $ . For a tournament of even order $ n $ , $ \sum_{v\in V}\max\{0,d^+(v)-d^-(v)\}\geq n/2 $ . Since a directed path may have up to $ n-1 $ arcs, it might be possible to cover the $ n(n-1)/2 $ arcs of the tournament if $ n $ is even. If the tournament is almost regular (i.e. $ |d^+(v)-d^-(v)|=1 $ for all vertex $ v $ ), the conjecture asserts that it can be decomposed into directed Hamilton paths.

This conjecture for almost regular tournaments would imply the following one due to Kelly.

Conjecture Every regular tournament of order $ n $ can be decomposed into $ (n-1)/2 $ Hamilton directed cycles.

To see this, consider a regular tournament $ T $ and a vertex $ v $ of $ T $ . The tournament $ T-v $ has even order, and in $ T-v $ , $ \max \{0,d^+(v)-d^-(v)\}=0 $ unless $ v $ is an outneighbour of $ v $ in $ T $ in which case $ \max \{0,d^+(v)-d^-(v)\}=0 $ . Hence $ \sum_{v\in V}\max\{0,d^+(v)-d^-(v)\}=(n-1)/2 $ . Now if Alspach-Mason-Pulman conjecture holds, $ T-v $ can be decomposed into $ (n-1)/2 $ directed paths. These paths must start at distinct outneighbours of $ v $ in $ T $ and ends at distinct inneighbours of $ v $ in $ T $ . Hence, we can complete each directed path in a Hamilton directed cycle in $ T $ to obtain a decomposition of $ T $ into $ (n-1)/2 $ Hamilton cycles.

Kelly's conjecture has been proved for tournaments of sufficiently large order by Kühn and Osthus [KO].

Related problems
Edge-disjoint Hamilton cycles in highly strongly connected tournaments.

Bibliography

*[AMP] Brian Alspach, David W. Mason, Norman J. Pullman, Path numbers of tournaments, Journal of Combinatorial Theory, Series B, 20 (1976), no. 3, June 1976, 222–228

[KO] Daniela Kühn and Deryk Osthus, Hamilton decompositions of regular expanders: a proof of Kelly's conjecture for large tournaments, Advances in Mathematics 237 (2013), 62-146.

* indicates original appearance(s) of problem.
