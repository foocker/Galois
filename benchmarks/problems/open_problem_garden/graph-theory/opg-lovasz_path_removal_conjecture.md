---
id: opg-lovasz_path_removal_conjecture
title: Lovász Path Removal Conjecture
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/lovasz_path_removal_conjecture
---

# Statement

Conjecture There is an integer-valued function $ f(k) $ such that if $ G $ is any $ f(k) $ -connected graph and $ x $ and $ y $ are any two vertices of $ G $ , then there exists an induced path $ P $ with ends $ x $ and $ y $ such that $ G-V(P) $ is $ k $ -connected.

# Source literature


# Progress

- It follows from a theorem of Tutte that any 3-connected graph contains a non-separating path connecting any two vertices, and consequently, $ f(1)=3 $ . When $ k=2 $ , it was independently shown by Chen, Gould, and Yu [CGY] and Kriesell [K] that $ f(2) = 5 $ .

Anwering a conjecture of Kriesell, Kawarabayashi et al. [KLRW] proved the following weaker statement, in which one only removes the edges of the path.

Theorem There exists a function $ f(k) $ such that for every $ f(k) $ -connected graph $ G $ and any two vertices $ x $ and $ y $ of $ G $ , there exists an induced path $ P $ with ends $ x $ and $ y $ such that $ G\setminus E(P) $ is $ k $ -connected.

Bibliography

[CGY] G. Chen, R. Gould, X. Yu, Graph connectivity after path removal, Combinatorica 23 (2003) 185--203.

[KLRW] K. Kawarabayashi, O. Lee, B. Reed, and P. Wollan, A weaker version of Lovasz's path removal conjecture, Journal of Combinatorial Theory, Series B 98 (2008) 972--979.

[K] M. Kriesell, Induced paths in 5-connected graphs, J. of Graph Theory, 36 (2001), 52--58.

*[T] C. Thomassen, Graph decompositions with applications to subdivisions and path systems modulo k, J. of Graph Theory, 7 (1983), 261--271.

* indicates original appearance(s) of problem.
