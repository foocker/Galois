---
id: opg-diophantine_quintuple_does_not_exist
title: Diophantine quintuple conjecture
status: open
difficulty: research
domains:
- Number Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/diophantine_quintuple_does_not_exist
---

# Statement

Definition A set of m positive integers $ \{a_1, a_2, \dots, a_m\} $ is called a Diophantine $ m $ -tuple if $ a_i\cdot a_j + 1 $ is a perfect square for all $ 1 \leq i < j \leq m $ .

Conjecture (1) Diophantine quintuple does not exist.

It would follow from the following stronger conjecture [Da]:

Conjecture (2) If $ \{a, b, c, d\} $ is a Diophantine quadruple and $ d > \max \{a, b, c\} $ , then $ d = a + b + c + 2bc + 2\sqrt{(ab+1)(ac+1)(bc+1)}. $

# Source literature

- [Da] A. Dujella Diophantine $ m $ -tuples, a survey of the main problems and results concerning Diophantine m-tuples.
- [Db] A. Dujella, There are only finitely many Diophantine quintuples, J. Reine Angew. Math. 566 (2004), 183-214.
- [AHS] J. Arkin, V. E. Hoggatt and E. G. Strauss, On Euler's solution of a problem of Diophantus, Fibonacci Quart. 17 (1979), 333-339.

# Progress

- It was proved in [Db] that there are only finitely many Diophantine quintuples and no Diophantine sextuples.

Conjecture (2) is motivated by an observation of [AHS] that every Diophantine triple $ \{a,b,c\} $ can be extended to a Diophantine quadruple $ \{a,b,c,a + b + c + 2bc + 2\sqrt{(ab+1)(ac+1)(bc+1)}\}. $
