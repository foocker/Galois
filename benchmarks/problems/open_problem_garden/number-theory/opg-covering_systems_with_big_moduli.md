---
id: opg-covering_systems_with_big_moduli
title: Covering systems with big moduli
status: open
difficulty: research
domains:
- Number Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/covering_systems_with_big_moduli
---

# Statement

Problem Does for every integer $ N $ exist a covering system with all moduli distinct and at least equal to~ $ N $ ?

# Source literature

- [FFKPY] Michael Filaseta, Kevin Ford, Sergei Konyagin, Carl Pomerance, Gang Yu: Sieving by large integers and covering systems of congruences, J. Amer. Math. Soc. 20 (2007), 495-517.

# Progress

- Let $ a(n) $ denote the residue class $ \{a+nt \mid t \in \Z\} $ . A covering system (defined by Paul Erdos in early 1930's) is a finite collection $ \{a_1(n_1), \dots, a_k(n_k) \} $ of residue classes whose union covers all the integers.

Such systems are easy to find if the moduli are allowed to repeat. They are known for many lower bounds $ N $ on the size of moduli: e.g. $ \{0(2), 0(3), 1(4), 5(6), 7(12) \} $ is such system for $ N=2 $ . Choi proved that it is possible to give an example for N = 20.

On the other hand, recently it was shown [FFKPY] that if such systems exist for arbitrary large $ N $ , then $ \sum_{i=1}^k \frac 1{n_i} $ is not bounded.
