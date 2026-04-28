---
id: opg-the_crossing_number_of_the_hypercube
title: The Crossing Number of the Hypercube
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/the_crossing_number_of_the_hypercube
---

# Statement

The crossing number $ cr(G) $ of $ G $ is the minimum number of crossings in all drawings of $ G $ in the plane.

The $ d $ -dimensional (hyper)cube $ Q_d $ is the graph whose vertices are all binary sequences of length $ d $ , and two of the sequences are adjacent in $ Q_d $ if they differ in precisely one coordinate.

Conjecture $ \displaystyle \lim \frac{cr(Q_d)}{4^d} = \frac{5}{32} $

# Source literature

- *[EG] P. Erdős and R.K. Guy, Crossing number problems, Amer. Math. Monthly 80 (1973) 52-58.
- [FF] L. Faria, C.M.H. de Figueiredo, On Eggleton and Guy's conjectured upper bound for the crossing number of the $ n $ -cube, Math. Slovaca 50 (2000) 271-287.
- [M] T. Madej, Bounds for the crossing number of the $ n $ -cube, J. Graph Theory 15 (1991) 81-97.
- [SV] O. Sykora and I. Vrto, On crossing numbers of hypercubes and cube connected cycles, BIT 33 (1993) 232-237.

# Progress

- It is known that $ cr(Q_d) = 0 $ for $ d = 1,2,3 $ and that $ cr(Q_4) = 8 $ . No other exact values are known. Madej [M] proved that $ cr(Q_d) \le 4^d/6 + o(4^d/6) $ . Faria and de Figueiredo [FF] improved the upper bound to $ (165/1024) 4^d $ . Sykora and Vrto [SV] proved that $ 4^d/20 + o(4^d/20) $ is a lower bound on $ cr(Q_d) $ .
