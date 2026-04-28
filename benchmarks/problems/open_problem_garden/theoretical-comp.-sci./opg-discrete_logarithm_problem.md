---
id: opg-discrete_logarithm_problem
title: Discrete Logarithm Problem
status: open
difficulty: frontier
domains:
- Theoretical Comp. Sci.
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/discrete_logarithm_problem
---

# Statement

If $ p $ is prime and $ g,h \in {\mathbb Z}_p^* $ , we write $ \log_g(h) = n $ if $ n \in {\mathbb Z} $ satisfies $ g^n = h $ . The problem of finding such an integer $ n $ for a given $ g,h \in {\mathbb Z}^*_p $ (with $ g \neq 1 $ ) is the Discrete Log Problem.

Conjecture There does not exist a polynomial time algorithm to solve the Discrete Log Problem.

# Source literature

- [RR] Alexander A. Razborov and Steven Rudich, Natural proofs, Journal of Computer and System Sciences 55 (1997), 24–35.

# Progress

- The Discrete Logarithm Problem is a critical problem in number theory, and is similar in many ways to the integer factorization problem. If it were possible to compute discrete logs efficiently, it would be possible to break numerous thought-to-be unbreakable cryptographic schemes. However, although most mathematicians and computer scientists believe that the DLP is unsolvable, this conjecture is difficult to establish, because such a proof would imply that P != NP...which is the most difficult open problem in theoretical computer science.

Avi Wigderson has shown that there is no ``natural proof'' (in the sense of [RR]) that the DLP requires circuits of greater than half-exponential size. The key idea is that a natural proof that the DLP is hard would yield a method for breaking discrete-log-based cryptosystems, and this is a contradiction. Of course, it could still be that DLP is provably hard, but by a proof that is not ``natural.''
