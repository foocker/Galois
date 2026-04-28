---
id: opg-subset_sums_equality
title: Subset-sums equality (pigeonhole version)
status: open
difficulty: frontier
domains:
- Theoretical Comp. Sci.
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/theoretical_computer_science/subset_sums_equality
---

# Statement

Problem Let $ a_1,a_2,\ldots,a_n $ be natural numbers with $ \sum_{i=1}^n a_i < 2^n - 1 $ . It follows from the pigeon-hole principle that there exist distinct subsets $ I,J \subseteq \{1,\ldots,n\} $ with $ \sum_{i \in I} a_i = \sum_{j \in J} a_j $ . Is it possible to find such a pair $ I,J $ in polynomial time?

# Source literature


# Progress

- This is one of a class of search problems for which a positive solution is garaunteed (so the corresponding decision problem is trivial) based on a theoretical property of the problem. Another such problem is given a Hamiltonian cycle in a cubic graph, find a second Hamiltonian cycle (here a theorem of Smith guarantee's a positive solution). The above problem is particularly attractive, since the proof that a pair $ I,J $ must exist is quite simple, but it gives no insight into how to find the pair $ I,J $ .

It seems to be consensus among the cryptography community that this problem is hard.
