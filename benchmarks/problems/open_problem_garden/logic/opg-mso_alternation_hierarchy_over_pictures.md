---
id: opg-mso_alternation_hierarchy_over_pictures
title: MSO alternation hierarchy over pictures
status: open
difficulty: research
domains:
- Logic
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/mso_alternation_hierarchy_over_pictures
---

# Statement

Question Is the MSO-alternation hierarchy strict for pictures that are balanced, in the sense that the width and the length are polynomially (or linearly) related.

# Source literature


# Progress

- In [MST02], Matz, Schweikardt, and Thomas, proved that the MSO-alternation hierarchy is strict over the class of 2-dimensional rectangular pictures (and, as a consequence, is also strict over the class of finite graphs).

The proof of this hierarchy strictness is essentially based on the fact that, for any positive integer $ k $ , there is a function $ f_k: \mathbb{N}\to \mathbb{N} $ (defined as a fixed height tower of exponentials) such that the set of rectangular grids of format $ n\times f_k(n) $ (i.e, of width $ n $ and length $ f_k(n) $ ) can be defined by some $ \Sigma_k $ MSO sentence but cannot be defined by some $ \Sigma_{k-1} $ MSO sentence.

So, the hierarchy result essentially rests on the (more than exponential) imbalance between the two dimensions of the rectangular grid.

In view of this result a natural question is as follows.

Question Is the MSO-alternation hierarchy strict for more well-balanced pictures, for example, if it is required that the width and the length of the pictures are polynomially (resp. linearly) related?

For example, for square picture languages (or equivalently, rectangular picture languages for which the width and the length of the pictures are linearly related), the only thing we know is that EMSO (that is Existential or $ \Sigma_1 $ MSO) over square pictures is not closed under complement.

Oliver Matz (personal communication) thinks it is possible that any MSO sentence over square pictures be equivalent to a Boolean combination of existntial MSO sentences.

Bibliography

[MST02] O. Matz, N. Schweikardt and W. Thomas, The Monadic Quantifier Alternation Hierarchy over Grids and Graphs, Information and Computation 179(2002), 356-383.

* indicates original appearance(s) of problem.
