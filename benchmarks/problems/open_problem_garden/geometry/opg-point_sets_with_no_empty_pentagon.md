---
id: opg-point_sets_with_no_empty_pentagon
title: Point sets with no empty pentagon
status: open
difficulty: graduate
domains:
- Geometry
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/point_sets_with_no_empty_pentagon
---

# Statement

Problem Classify the point sets with no empty pentagon.

# Source literature

- Z. Abel, B. Ballinger, P. Bose, S. Collette, V. Dujmovic, F. Hurtado, S. D. Kominers, S. Langerman, A. Pór, D. R. Wood. Every large point set contains many collinear points or an empty pentagon, Graphs and Combinatorics 27(1):47-60, 2011.
- Eppstein, David. Happy endings for flip graphs. J. Computational Geometry 1(1):3-28, 2010. MathSciNet
- Kára, Jan; Pór, Attila; Wood, David R. On the chromatic number of the visibility graph of a set of points in the plane. Discrete Comput. Geom. 34(3):497-506, 2005. MathSciNet
- Pfender, Florian. Visibility graphs of point sets in the plane. Discrete Comput. Geom. 39 (2008), no. 1-3, 455–459. MathSciNet
- Rabinowitz, Stanley. Consequences of the pentagon property. Geombinatorics 14:208-220, 2005.

# Progress

- Let $ P $ be a finite set of points in the plane (not necessarily in general position). Two points $ x,y\in P $ are visible if the line segment $ xy $ contains no other point in $ P $ . The visibility graph of $ P $ has vertex set $ P $ , where two vertices are adjacent if and only if they are visible. An empty pentagon in $ P $ consists of 5 points in $ P $ that are the vertices of a strictly convex pentagon whose interior contains none of the points in $ P $ .

Consider the following three closely related classes of point sets:

$ A := $ point sets with no empty pentagon (called a 5-hole),
$ B := $ point sets with no 5 pairwise visible points,
$ C := $ point sets whose visibility graph is 4-colourable.

By definition, $ C \subseteq B \subseteq A $ , and it is easy to show that $ A \neq B $ and $ B \neq C $ .

A key example of a point set in $ C $ is the planar grid (intersected with a convex set so that it is finite): colour each grid point $ (x,y) $ by $ (x \bmod 2, y \bmod 2) $ . If $ (x,y) $ and $ (v,w) $ receive the same colour then $ |x-v| $ and $ |y-w| $ are both even, and thus the midpoint of $ (x,y) $ and $ (v,w) $ is a blocker. Hence the visibility graph of the grid is 4-colourable. [This result and proof is folklore.] Many other examples of point sets in these classes can be found in the references.

Consider the following open problems:

\item Classify the point sets in $ A $ , $ B $ , or $ C $
(i.e. list all examples; this is easy for point sets with no empty quadrilateral, or no 4 pairwise visible points).
\item Does the visibility graph of every point set in $ A $ have bounded chromatic number?
\item Does the visibility graph of every point set in $ A $ have bounded clique number?
\item Does the visibility graph of every point set in $ B $ have bounded chromatic number?

Kára-Pór-Wood gave an example of a point set in $ B $ with chromatic number $ 5 $ .
