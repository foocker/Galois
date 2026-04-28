---
id: opg-cube_simplex_conjecture
title: Cube-Simplex conjecture
status: open
difficulty: frontier
domains:
- Geometry
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/cube_simplex_conjecture
---

# Statement

Conjecture For every positive integer $ k $ , there exists an integer $ d $ so that every polytope of dimension $ \ge d $ has a $ k $ -dimensional face which is either a simplex or is combinatorially isomorphic to a $ k $ -dimensional cube.

# Source literature

- [MKK] G. Meisinger, P. Kleinschmidt, and G. Kalai, Three theorems, with computer-aided proofs, on three-dimensional faces and quotients of polytopes. The Branko Grünbaum birthday issue. Discrete Comput. Geom. 24 (2000), no. 2-3, 413--420. MathSciNet
- *[K] G. Kalai, On low-dimensional faces that high-dimensional polytopes must have. Combinatorica 10 (1990), no. 3, 271--280. MathSciNet

# Progress

- It is an easy consequence of Euler's formula that every 3-polytope has a face which is either a triangle, a quadrilateral, or a pentagon. The 120-cell is a 4-polytope in which every 2-face is a pentagon (in fact every 3-face is a regular dodecahedron). Perles and Shephard asked whether there exist higher dimensional polytopes in which all 2-faces have at least 5 vertices. This question was answered in the negative by Kalai [K] who showed that every 5-polytope has a 2-face with at most 4 vertices. So, if we define $ f(k) $ to be the smallest integer $ d $ satisfying the above conjecture for $ k $ , or $ \infty $ if none exists, then $ f(2) = 5 $ .

This conjecture is still open for simple polytopes. However, it is known that for every positive integer $ k $ , there exists an integer $ d $ so that every simple polytope of dimension $ \ge d $ either has a 2-dimensional face which is a triangle, or a $ k $ -dimensional face which is combinatorially isomorphic to a cube. This was proved by Kalai [K] using some earlier results of Nikulin and of Blind and Blind. Actually, something much stronger holds here: simple polytopes of sufficiently high dimension without 2-faces which are triangles must have most $ k $ -dimensional faces combinatorially isomorphic to the $ k $ -cube.

The following is an interesting weakening of the above conjecture.

Conjecture For every positive integer $ k $ , there exists an integer $ d $ and a finite list $ L $ of $ k $ -dimensional polytopes, so that every polytope of dimension $ \ge d $ has a $ k $ -dimensional face which appears in $ L $ .

Defining $ h(k) $ to be the smallest integer $ d $ satisfying this conjecture for $ k $ , or $ \infty $ if none exists, we find that $ h(2) = 3 $ (by the consequence of Euler's formula in the first paragraph). Meisinger, Kleinschmidt, and Kalai [MKK] proved that $ h(3) \le 9 $ with the help of FLAGTOOL, a computer program which can compute linear relations for $ f $ -vectors. This weaker conjecture is known to be true for simple polytopes.
