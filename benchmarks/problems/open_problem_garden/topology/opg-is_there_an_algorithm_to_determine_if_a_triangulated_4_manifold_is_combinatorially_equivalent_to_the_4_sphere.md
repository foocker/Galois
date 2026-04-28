---
id: opg-is_there_an_algorithm_to_determine_if_a_triangulated_4_manifold_is_combinatorially_equivalent_to_the_4_sphere
title: Is there an algorithm to determine if a triangulated 4-manifold is combinatorially
  equivalent to the 4-sphere?
status: open
difficulty: frontier
domains:
- Topology
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/is_there_an_algorithm_to_determine_if_a_triangulated_4_manifold_is_combinatorially_equivalent_to_the_4_sphere
---

# Statement

Problem Is there an algorithm which takes as input a triangulated 4-manifold, and determines whether or not this manifold is combinatorially equivalent to the 4-sphere?

# Source literature

- [CL] Chernavsky, A. V, and Leskine, V. P., Unrecognizability of manifolds, Annals of Pure and Applied Logic 141 (2006) 325--335.
- [N] Novikov, P.S., On the algorithSSSR 85 (5) (19552) 709--712 (in Russian). Algorithmic unsolvability of the problem of identity, Dokl. Akad. Nauk SSSR 85 (5) (1952) 709--712 (in Russian).
- [T] Thompson, A. Thin position and the recognition problem for $ S^3 $ . MRL (1994).

# Progress

- A 4-manifold triangulation admits a unique smoothing up to diffeomorphism, so this problem is equivalent to asking for an algorithm to determine if a 4-manifold is diffeomorphic to the 4-sphere (with standard differentiable structure). "Combinatorial equivalence" refers to the ability to pass from one triangulation to another via a sequence of Pachner moves.

Rubinstein has an algorithm to determine if a triangulated 3-manifold is combinatorially equivalent to the 3-sphere. A consequence of his algorithm is that there is an algorithm to determine if a 4-dimensional simplicial complex is a 4-manifold triangulation.

It's known that no algorithms exist to determine if a triangulated 4-manifold has a trivial fundamental group, as there is a procedure to construct a compact 4-manifold with any finitely presented fundamental group.

In dimensions 5 and higher, Novikov proved that there is no algorithm to decide whether a given triangulated $ n $ -manifold is combinatorially equivalent to the $ n $ -sphere is undecidable [N, CL]. Also, it is undecidable whether a given triangulated 4-manifold is combinatorially equivalent to a connect sum of 14 copies of $ S^2 \times S^2 $ .
