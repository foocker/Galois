---
id: opg-convex_equipartitions_with_extreme_perimeter
title: Convex Equipartitions with Extreme Perimeter
status: open
difficulty: research
domains:
- Geometry
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/convex_equipartitions_with_extreme_perimeter
---

# Statement

To divide a given 2D convex region C into a specified number n of convex pieces all of equal area (perimeters could be different) such that the total perimeter of pieces is (1) maximized (2) minimized.

Remark: It appears maximizing the total perimeter is the easier problem.

# Source literature

- Online Reference (the only one known to the author): http://nandacumar.blogspot.in/2015/08/another-convex-equi-partition-problem.html (*)

# Progress

- Conjecture 1: It appears that for convex equipartition with maximum total cut length, the cut lines should not meet in the interior of C.

Conjecture 1a: for n=3, it appears conjecture 1 can be proved by proving the following subconjecture: If from a point P in the interior of C, three rays originate and divide C into three equal area pieces and if p_0 is the sum of the perimeters of the three pieces, then from at least one of the three points (call them A, B, C) where the three rays from P cut the boundary of C, there originate 2 rays which equipartition region C into three equal area pieces such that the perimeter sum of the three pieces is necessarily greater than p_0.

Conjecture 2: If conjecture 1 holds, one could have a greedy algorithm to achieve maximum perimeter sum as follows:

- From C, first cut out a convex region with 1/n of the total area such that the separating cut is the longest possible, then repeat the same process on the remaining piece and so on until we have n equal area pieces) appears to give the optimal answer

Generalizations: One could think of partitioning a convex regions into convex pieces with specified different areas and minimize/maximize the total perimter. Higher dimensional analgs too could be considered.
