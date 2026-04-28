---
id: opg-complexity_of_square_root_sum
title: Complexity of square-root sum
status: open
difficulty: research
domains:
- Theoretical Comp. Sci.
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/complexity_of_square_root_sum
---

# Statement

Question What is the complexity of the following problem?

Given $ a_1,\dots,a_n; k $ , determine whether or not $ \sum_i \sqrt{a_i} \leq k. $

# Source literature

- [G] Michal Goemans, Semidefinite Programming and Combinatorial Optimization

# Progress

- As of a 1998 survey, the complexity of this problem was unknown. I'm not sure if that's still the case. But I wanted to see how easy it was to make a page about it.

This is the key to determining if semi-definite programming is truly solvable in polynomial time (it can be approximated to within $ \varepsilon $ using the interior point method or the ellipsoid algorithm in time polynomial in the size of the instance and $ \log 1/\varepsilon $ .
