---
id: opg-textbf_convex_fair_partitions_of_convex_polygons
title: Convex 'Fair' Partitions Of Convex Polygons
status: open
difficulty: research
domains:
- Geometry
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/textbf_convex_fair_partitions_of_convex_polygons
---

# Statement

Basic Question: Given any positive integer n, can any convex polygon be partitioned into n convex pieces so that all pieces have the same area and same perimeter?

Definitions: Define a Fair Partition of a polygon as a partition of it into a finite number of pieces so that every piece has both the same area and the same perimeter. Further, if all the resulting pieces are convex, call it a Convex Fair Partition.

Questions: 1. (Rephrasing the above 'basic' question) Given any positive integer n, can any convex polygon be convex fair partitioned into n pieces?

2. If the answer to the above is "Not always'', how does one decide the possibility of such a partition for a given convex polygon and a given n? And if fair convex partition is allowed by a specific convex polygon for a give n, how does one find the optimal convex fair partition that minimizes the total length of the cut segments?

3. Finally, what could one say about higher dimensional analogs of this question?

Conjecture: The authors tend to believe that the answer to the above 'basic' question is "yes". In other words they guess: Every convex polygon allows a convex fair partition into n pieces for any n

# Source literature

- (*)1. The original 'mainstream' statement of this problem: http://maven.smith.edu/~orourke/TOPP/P67.html#Problem.67
- 2. Jin Akiyama, A. Kaneko, M. Kano, Gisaku Nakamura, Eduardo Rivera-Campo, S. Tokunaga, and Jorge Urrutia. Radial perfect partitions of convex sets in the plane. In Japan Conf. Discrete Comput. Geom., pages 1-13, 1998.
- 3. Jin Akiyama, Gisaku Nakamura, Eduardo Rivera-Campo, and Jorge Urrutia. Perfect divisions of a cake. In Proc. Canad. Conf. Comput. Geom., pages 114-115, 1998.
- 4. This blog maintained by the authors has tentative thoughts, examples, etc on 'Fair Partitions': http://nandacumar.blogspot.com

# Progress

- 1. The above conjecture is easily seen to hold for n=2. for n=3 and above, it is not clear.

2. The n = 2 case does not appear to allow a recursive generalization for values of n equal to powers of 2.

3. It can be shown that any polygon (not necessarily convex) allows a fair partitioning into n pieces for any n, provided the pieces need not be convex (this is not a convex fair partition). See (4) in references below.

4. It appears that the fair parition of a convex polygon which minimizes the total length of cuts (or equivalently, the sum of the perimeters of the pieces) need not be a convex fair partition.

5. There is no known work in this specific area. The problem of partitioning convex polygons into equal area convex pieces so that every piece equally shares the boundary of the input polygon has been studied (references below)
