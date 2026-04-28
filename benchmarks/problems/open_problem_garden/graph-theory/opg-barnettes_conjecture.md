---
id: opg-barnettes_conjecture
title: Barnette's Conjecture
status: open
difficulty: frontier
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/barnettes_conjecture
---

# Statement

Conjecture Every 3-connected cubic planar bipartite graph is Hamiltonian.

# Source literature

- *[B] David W. Barnette, Conjecture 5, Recent progress in combinatorics (ed. W. T. Tutte), Academic Press, New York (1969) 343, MathSciNet
- [HMM] Derek A.Holton, Bennet Manvel, Brendan D. McKay, Hamiltonian cycles in cubic 3-connected bipartite planar graphs, J. Combin. Theory Ser. B 38 (1985) 279-297. MathSciNet
- [M] B. Mohar, Problem of the Month

# Progress

- (Originally appeared in [B], this discussion appears as [M].)

\item It is known that this is not true if you remove the "bipartite" condition, but the smallest 3-connected cubic planar graph which is not Hamiltonian has 38 vertices.

\item Holton, Manvel, and McKay [HMM] proved (using computers) that all graphs having fewer than 66 vertices satisfy the conjecture.

\item [A communication by Robert Aldred, Gunnar Brinkmann, and Brendan McKay (December 2002):]

A paper of Holton, Manvel and McKay [HMM] proved Barnette's conjecture for up to 64 vertices, inclusive. This is to announce that the conjecture remains true up to 84 vertices, inclusive. The method used was the same as in the 1985 paper, but took advantage of two developments. One was the new program plantri (Brinkmann and McKay, to be published) which can generate the required graphs without isomorphs at more than $ 100\,000 $ per second. The other was the advance in computers. Total cpu time was about 3 years, almost all of it taken in finding hamiltonian cycles. Specifically, for all 3-connected cubic planar bipartite graphs up to 60 vertices, and those up to 64 vertices not having a 4-face adjacent to two others, we found a hamiltonian cycle using $ x $ and avoiding $ y $ for each pair of edges $ x $ and $ y $ . There are over $ 10^{10} $ such graphs. By a theorem of Kelman's, one can build a counterexample to Barnette's conjecture when one has a 3-connected cubic planar bipartite graph with this property: for some two edges $ x $ and $ y $ on the same face, there is no hamiltonian cycle that uses $ x $ and avoids $ y $ . We did not find any such graph even where $ x $ and $ y $ are not required to be on the same face. Perhaps the path to finding a counterexample is to strengthen Kelman's method to some more complicated condition involving 3 or more edges, as then it is more likely to fail on a smaller size.

There is another conjecture of Barnette (checked by Brendan McKay and Gunnar Brinkmann up to 250 vertices).

Conjecture Every planar cubic 3-connected graph with faces only of sizes 3, 4, 5, and 6 is Hamiltonian.
