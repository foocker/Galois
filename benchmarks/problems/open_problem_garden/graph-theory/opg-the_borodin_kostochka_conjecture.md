---
id: opg-the_borodin_kostochka_conjecture
title: The Borodin-Kostochka Conjecture
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/the_borodin_kostochka_conjecture
---

# Statement

Conjecture Every graph with maximum degree $ \Delta \geq 9 $ has chromatic number at most $ \max\{\Delta-1, \omega\} $ .

# Source literature

- [BK] O. V. Borodin and A. V. Kostochka. On an upper bound of a graph's chromatic number, depending on the graph's degree and density. JCTB 23 (1977), 247--250.
- [CR] D. W. Cranston and L. Rabern. Coloring claw-free graphs with $ \Delta-1 $ colors, arXiv 1206.1269, 2012.
- [R] B. A. Reed. A strengthening of Brooks’ Theorem. J. Comb. Theory Ser. B, 76:136–149, 1999.

# Progress

- The Borodin-Kostochka conjecture proposes that for any graph $ G $ with maximum degree $ \Delta $ and clique number $ \omega < \Delta $ , $ G $ is $ \Delta-1 $ colourable so long as $ \Delta $ is sufficiently large (specifically, $ \Delta\geq 9 $ ). The requirement that $ \Delta \geq 9 $ is necessary, as one can see by looking at the strong product of $ C_5 $ and $ K_3 $ .

Reed [R] proved that there exists a $ \Delta_0 $ for which the conjecture holds whenever $ \Delta \geq \Delta_0 $ . Specifically he proved that $ \Delta_0 \leq 10^{14} $ , but claims that more careful analysis could reduce $ \Delta_0 $ to 1000.

The conjecture was recently proven by Cranston and Rabern for claw-free graphs [CR]. In their paper they mention an unpublished strengthening proposed by Borodin and Kostochka, namely that one can replace the chromatic number in the statement of the conjecture with the list chromatic number.
