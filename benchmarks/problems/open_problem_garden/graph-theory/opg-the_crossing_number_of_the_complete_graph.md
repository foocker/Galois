---
id: opg-the_crossing_number_of_the_complete_graph
title: The Crossing Number of the Complete Graph
status: open
difficulty: frontier
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/the_crossing_number_of_the_complete_graph
---

# Statement

The crossing number $ cr(G) $ of $ G $ is the minimum number of crossings in all drawings of $ G $ in the plane.

Conjecture $ \displaystyle cr(K_n) = \frac 14 \floor{\frac n2} \floor{\frac{n-1}2} \floor{\frac{n-2}2} \floor{\frac{n-3}2} $

# Source literature

- [G] R. Guy, The decline and fall of Zarankiewicz's theorem, in Proof Techniques in Graph Theory (F. Harary Ed.), Academic Press, New York (1969) 63-69.
- [K] D. Kleitman, The crossing number of $ K_{5,n} $ , J. Combin. Theory 9 (1970) 315-323.
- [M] B. Mohar, Problem of the Month

# Progress

- (This discussion appears as [M].)

A drawing of a graph $ G $ in the plane has the vertices represented by distinct points and the edges represented by polygonal lines joining their endpoints such that:

\item no edge contains a vertex other than its endpoints, \item no two adjacent edges share a point other than their common endpoint, \item two nonadjacent edges share at most one point at which they cross transversally, and \item no three edges cross at the same point.

The conjectured value for the crossing number of $ K_n $ is known to be an upper bound. This is shown by exhibiting a drawing with that number of crossings. If $ n = 2m $ , place $ m $ vertices regularly spaced along two circles of radii 1 and 2, respectively. Two vertices on the inner circle are connected by a straight line; two vertices on the outer circle are connected by a polygonal line outside the circle. A vertex on the inner circle is connected to one on the outer circle with a polygonal line segment of minimum possible positive winding angle around the cylinder. A simple count shows that the number of crossings in such a drawing achieves the conjectured minimum. For $ n = 2m-1 $ we delete one vertex from the drawing described and achieve the conjectured minimum.

The conjecture is known to be true for $ n $ at most 10 [G]. If the conjecture is true for $ n = 2m $ , then it is also true for $ n-1 $ . This follows from an argument counting the number of crossings in drawings of all $ K_{n-1} $ 's contained in an optimal drawing of $ K_n $ .

It would also be interesting to prove that the conjectured upper bound is asymptotically correct, that is, that $ \lim \frac{cr(K_n)}{\binom{n}4} = \frac38 $ .

The best known lower bound is due to Kleitman [K], who showed that this limit is at least $ 3/10 $ .
