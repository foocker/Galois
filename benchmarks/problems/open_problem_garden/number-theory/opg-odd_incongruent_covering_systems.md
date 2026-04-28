---
id: opg-odd_incongruent_covering_systems
title: Odd incongruent covering systems
status: open
difficulty: frontier
domains:
- Number Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/odd_incongruent_covering_systems
---

# Statement

Conjecture There is no covering system whose moduli are odd, distinct, and greater than 1.

# Source literature

- [BFF1] M. A. Berger, A. Felzenbaum and A. S. Fraenkel, Necessary condition for the existence of an incongruent covering system with odd moduli, Acta. Arith. 45 (1986), 375–379
- [BFF2] M. A. Berger, A. Felzenbaum and A. S. Fraenkel, Necessary condition for the existence of an incongruent covering system with odd moduli. II, Acta Arith. 48 (1987), 73–79.
- [GS] Song Guo and Zhi-Wei Sun: On odd covering systems with distinct moduli; Adv. Appl. Math. 35(2005), 182–187
- [SZ] R. J. Simpson and D. Zeilberger, Necessary conditions for distinct covering systems with square-free moduli, Acta. Arith. 59 (1991), 59–70.

# Progress

- Let $ a(n) $ denote the residue class $ \{a+nt \mid t \in \Z\} $ . A covering system (defined by Paul Erdos in early 1930's) is a finite collection $ \{a_1(n_1), \dots, a_k(n_k) \} $ of residue classes whose union covers all the integers. Such systems are easy to find if the moduli are allowed to repeat, or if we allow even numbers. The covering system is called incongruent if all the moduli are distinct.

Partial results are known. Berger, Felzenbaum and Fraenkel ([BFF1], [BFF2]) show (among else) that if covering system with odd distinct moduli (greater than 1) exists, $ N $ is the least common multiple of $ n_1 $ , \dots, $ n_t $ , and $ p_1 $ , \dots, $ p_s $ are all distinct prime divisors of~ $ N $ , then $$ \prod_{i=1}^s \frac{p_i -1}{p_i-2} - \sum_{i=1}^s \frac {1}{p_i-2} > 2 \,. $$

Simpson and Zeilberger [SZ] proved that if in addition $ n_1 $ , \dots , $ n_k $ are square-free, then $ N $ has at least 18 prime divisors.

Guo and Sun [GS] recently improved this to show that if $ N $ is square-free, then it has at least 22 prime divisors.
