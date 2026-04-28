---
id: opg-the_crossing_number_of_the_complete_bipartite_graph
title: The Crossing Number of the Complete Bipartite Graph
status: open
difficulty: frontier
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/the_crossing_number_of_the_complete_bipartite_graph
---

# Statement

The crossing number $ cr(G) $ of $ G $ is the minimum number of crossings in all drawings of $ G $ in the plane.

Conjecture $ \displaystyle cr(K_{m,n}) = \floor{\frac m2} \floor{\frac {m-1}2} \floor{\frac n2} \floor{\frac {n-1}2} $

# Source literature

- [G] R. Guy, The decline and fall of Zarankiewicz's theorem, in Proof Techniques in Graph Theory (F. Harary Ed.), Academic Press, New York (1969) 63-69.
- [K] D. Kleitman, The crossing number of K_{5,n} , J. Combin. Theory 9 (1970) 315-32
- [M] B. Mohar, Problem of the Month

# Progress

- (This discussion appears as [M].)

A drawing of a graph $ G $ in the plane has the vertices represented by distinct points and the edges represented by polygonal lines joining their endpoints such that:

\item no edge contains a vertex other than its endpoints, \item no two adjacent edges share a point other than their common endpoint, \item two nonadjacent edges share at most one point at which they cross transversally, and \item no three edges cross at the same point.

This problem is also known as Turan's Brickyard Problem (since it was formulated by Turan when he was working at a brickyard - the edges of the drawing would correspond to train tracks connecting different shipping depots, and fewer crossings would mean smaller chance for collision of little trains and smaller chance for their derailing).

This conjectured value for the crossing number of $ K_{m,n} $ can be realized by the following drawing. Place $ \ceil{n/2} $ vertices on the positive $ x $ -axis and $ \floor{n/2} $ vertices on the negative $ x $ -axis. Similarly, place $ \ceil{m/2} $ and $ \floor{m/2} $ along the positive and negative $ y $ -axis. Now connect each pair of vertices on different axes with straight line segments.
