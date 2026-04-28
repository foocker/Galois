---
id: opg-forcing_a_2_regular_minor
title: Forcing a 2-regular minor
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/forcing_a_2_regular_minor
---

# Statement

Conjecture Every graph with average degree at least $ \frac{4}{3}t-2 $ contains every 2-regular graph on $ t $ vertices as a minor.

# Source literature

- [CH] Keresztely Corradi and Andras Hajnal. On the maximal number of independent circuits of a graph. Acta Math. Acad. Sci. Hungar., 14:423–443, 1963.
- *[RW] Bruce Reed and David R. Wood. Forcing a sparse minor, arXiv:1402.0272, 2013.
- [HW] Daniel J. Harvey and David R. Wood. Cycles of given size in a dense graph. SIAM J. Discrete Math. 29.4:2336–2349, 2015.
- [CNLWY] E. Csóka, S. Norin, I. Lo, H. Wu and L. Yepremyan. The extremal function for disconnected minors. J. Comb. Theory B 126 (2017), 162-174.

# Progress

- Reed and Wood [RW] explained that a result of Corradi and Hajnal [CH] implies that if $ H $ is the graph consisting of $ k $ disjoint triangles, then every graph with average degree at least $ 4k-2 $ contains $ H $ as a minor. Moreover, the bound of $ 4k-2 $ is best possible since the complete bipartite graph $ K_{2k-1,n} $ contains no $ H $ -minor, but has average degree tending to $ 4k-2 $ (as $ n\rightarrow\infty $ ). Thus the conjecture would generalise this result.

Update: There has been a lot of recent progress on this conjecture [HW,CNLWY].
