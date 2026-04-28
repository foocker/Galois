---
id: opg-crossing_sequences
title: Crossing sequences
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/crossing_sequences
---

# Statement

Conjecture Let $ (a_0,a_1,a_2,\ldots,0) $ be a sequence of nonnegative integers which strictly decreases until $ 0 $ .

Then there exists a graph that be drawn on a surface with orientable (nonorientable, resp.) genus $ i $ with $ a_i $ crossings, but not with less crossings.

# Source literature

- *[ABS] Dan Archdeacon, C. Paul Bonnington, and Jozef Siran, Trading crossings for handles and crosscaps, J.Graph Theory 38 (2001), 230--243.
- [DMS] Matt DeVos, Bojan Mohar, Robert Samal, Unexpected behaviour of crossing sequences, in preparation
- [S] Jozef Siran, The crossing function of a graph, Abh. Math. Sem. Univ. Hamburg 53 (1983), 131--133.

# Progress

- This actually are two conjectures, one for the orientable case and another for nonorientable one. For sequences $ (a_0,a_1,0) $ the nonorientable case was resolved in [ABS] and the orientable one in [DMS].

The conclusion also holds (for the orientable case) whenever the sequence $ (a_i) $ is convex [S], that is whenever $ a_i - a_{i-1} $ is nonincreasing. It might seem that this condition is also necessary: For the most extreme sequence $ (N,N-1,0) $ (suggested by Salazar) one needs to construct a graph for which adding one handle saves just one crossing, while adding another saves many -- but then why not add the second handle first? Somewhat surprisingly, graphs with this counterintuitive property exist, at least for sequences $ (a_0,a_1,0) $ .

An interesting open case is to consider sequences for which $$ a_0 - a_s < \varepsilon (a_s - a_{s+1}) $$ for some $ s $ and small $ \varepsilon $ .
