---
id: opg-fibonacci_divisibility
title: Wall-Sun-Sun primes and Fibonacci divisibility
status: open
difficulty: research
domains:
- Number Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/fibonacci_divisibility
---

# Statement

Conjecture For any prime $ p $ , there exists a Fibonacci number divisible by $ p $ exactly once.

Equivalently:

Conjecture For any prime $ p>5 $ , $ p^2 $ does not divide $ F_{p-\left(\frac p5\right)} $ where $ \left(\frac mn\right) $ is the Legendre symbol.

# Source literature

- [EJ] Andreas-Stephan Elsenhansand and Jörg Jahnel, The Fibonacci sequence modulo p^2
- [R] Marc Renault, Properties of the Fibonacci Sequence Under Various Moduli
- *[W] D. D. Wall, Fibonacci Series Modulo m, American Mathematical Monthly, 67 (1960), pp. 525-532.

# Progress

- Let $ p $ be an odd prime, and let $ \nu_p(n) $ denote the $ p $ -adic valuation of $ n $ . Let $ F_{k(p)} $ be the smallest Fibonacci number that is divisible by $ p $ (which must exist by a simple counting argument). A well-known result says that $ \nu_p(F_n)=0 $ unless $ k(p) $ divides $ n $ , and $ \nu_p(F_{k(p)m}) = \nu_p(F_{k(p)}) + \nu_p(m) $ . This conjecture asserts that $ \nu_p(F_{k(p)})=1 $ for all $ p $ . This has been verified up to at least $ p<10^{14} $ . [EJ]

This conjecture is equivalent to non-existence of Wall-Sun-Sun primes.
