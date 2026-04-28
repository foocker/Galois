---
id: opg-general_position_subsets
title: General position subsets
status: open
difficulty: research
domains:
- Geometry
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/general_position_subsets
---

# Statement

Question What is the least integer $ f(n) $ such that every set of at least $ f(n) $ points in the plane contains $ n $ collinear points or a subset of $ n $ points in general position (no three collinear)?

# Source literature

- *[G] Timothy Gowers, A geometric Ramsey problem.
- [PW] Michael Payne, David R. Wood. On the general position subset selection problem, SIAM J. Discrete Math. 27.4:1727-1733, 2013.
- [R] K. F. Roth, On a problem of Heilbronn, J. London Mathematical Society 26.3:198–204, 1951.

# Progress

- The $ n\times n $ grid contains no set of $ n+1 $ collinear points and no subset of $ 2n+1 $ points in general position, implying $ f(n)\geq \Omega(n^2) $ .

To see that $ f(n)\leq O(n^3) $ , consider a set $ P $ of points that contain no $ n $ collinear points, and contain no subset of $ n $ points in general position. Let $ S $ be a maximal subset of $ P $ in general position. Every point in $ P-S $ is on one of the $ \binom{|S|}{2} $ lines determined by $ S $ . Each such line contains at most $ n-3 $ points in $ P-S $ . Thus $ |P|\leq |S|+\binom{|S|}{2}(n-3) \leq (n-1)+\binom{n-1}{2}(n-3)\leq O(n^3) $ .

Payne and Wood [PW] improved this upper bound to $ f(n)\leq O(n^2\log n) $ . The proof is based on the Szemerédi-Trotter Theorem and Spencer's Lemma about independent sets in hypergraphs.

It is reasonable to think that the grid is the extremal example, and $ f(n)\leq O(n^2) $ . This would be an elegant generalisation of a result by Erdős [R] who proved that the $ n\times n $ grid contains a subset of $ n-o(n) $ points in general position (the no-three-in-line problem).
