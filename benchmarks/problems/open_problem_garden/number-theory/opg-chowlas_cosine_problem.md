---
id: opg-chowlas_cosine_problem
title: Chowla's cosine problem
status: open
difficulty: frontier
domains:
- Number Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/chowlas_cosine_problem
---

# Statement

Problem Let $ A \subseteq {\mathbb N} $ be a set of $ n $ positive integers and set \[m(A) = - \min_x \sum_{a \in A} \cos(ax).\] What is $ m(n) = \min_A m(A) $ ?

# Source literature

- [B] J. Bourgain, Sur le minimum d'une somme de cosinus, Acta Arith. 45 (1986), 381--389. MathSciNet
- *[C] S. Chowla, Some applications of a method of A. Selberg. J. Reine Angew. Math. 217 (1965) 128--132. MathSciNet
- [R] I.Z. Ruzsa, Negative values of cosine sums. Acta Arith. 111 (2004), no. 2, 179--186. MathSciNet

# Progress

- It is easy to see that $ m(A) > 0 $ , since the average value of the sum of the cosines is zero. Bourgain [B] proved that $ m(n) > e^{(\log n)^c} $ for some $ c>0 $ and $ n $ sufficiently large. Recently, Ruzsa [R] tightened this argument, proving that $ m(n) > c_1 e^{c_2 \sqrt{ \log n}} $ where $ c_2 = \sqrt{ (\log 2)/ 8} $ . The proof utilizes a clever manipulation of norms to reveal a (somewhat surprising) additive structure to the problem.

It seems the only known upper bound is $ m(n) \ll \sqrt{n} $ .
