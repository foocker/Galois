---
id: opg-lucas_numbers_modulo_m
title: Lucas Numbers Modulo m
status: solved
difficulty: research
domains:
- Number Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/lucas_numbers_modulo_m
---

# Statement

Conjecture The sequence {L(n) mod m}, where L(n) are the Lucas numbers, contains a complete residue system modulo m if and only if m is one of the following: 2, 4, 6, 7, 14, 3^k, k >=1.

# Source literature

- S. A. Burr, "On Moduli for Which the Fibonacci Sequence Contains a Complete System of Residue", Fibonacci Quarterly, December 1971, pp. 497-504.

# Progress

- The Lucas numbers are defined by L(0)=2, L(1)=1, and L(n)=L(n-1)+L(n-2), for n >=2. Thus the sequence is 2, 1, 3, 4, 7, 11, 18, 29, 47, ... .

Example: If m = 5, then we have the sequence 2, 1, 3, 4, 2, 1, ..., and since the sequence repeats we never obtain 0 mod 5.

Example: If m = 6, then we have 2, 1, 3, 4, 1, 5, 0, ..., and we obtain a complete residue system mod 6.

The corresponding problem for the Fibonacci sequence was solved by S. A. Burr. The sequence {F(n) mod m} contains a complete residue system mod m if and only if m is one of the following: 5^k, 2.5^k, 4.5^k, 3^j.5^k, 6.5^k, 7.5^k, 14.5^k.
