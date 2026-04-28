---
id: opg-diagonal_ramsey_numbers
title: Diagonal Ramsey numbers
status: open
difficulty: frontier
domains:
- Combinatorics
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/diagonal_ramsey_numbers
---

# Statement

Let $ R(k,k) $ denote the $ k^{th} $ diagonal Ramsey number.

Conjecture $ \lim_{k \rightarrow \infty} R(k,k) ^{\frac{1}{k}} $ exists.

Problem Determine the limit in the above conjecture (assuming it exists).

# Source literature

- [E] P. Erdos, Some remarks on the theory of graphs, Bull. Amer. Math. Soc. 53 (1947), 292–294. MathSciNet
- [ESz] P. Erdos and G. Szekeres, A combinatorial problem in geometry, Compositio Math. 2 (1935), 463–470.
- [G] W. T. Gowers, Rough structure and classification, GAFA 2000 (Tel Aviv, 1999). Geom. Funct. Anal. 2000, Special Volume, Part I, 79--117. MathSciNet
- [S] J. Spencer, Ramsey’s theorem—a new lower bound, J. Comb. Theory Ser. A 18 (1975), 108–115. MathSciNet
- [T] A. Thomason, An upper bound for some Ramsey numbers, J. Graph Theory 12 (1988), 509–517. MathSciNet

# Progress

- Erdos offered $100 for a solution to the highlighted conjecture and $250 for a solution to the associated problem (these prizes are now provided by Graham).

Classic results of Erdos [E] and Erdos-Szekeres [ESz] give bounds on $ R(k,k) $ which show that if $ \lim_{k \rightarrow \infty} R(k,k)^{\frac{1}{k}} $ exists, then it is in the interval $ [\sqrt{2},4] $ . Although these arguments are quite basic, little progress has been made in improving these bounds. The best known lower bound on $ R(k,k) $ is due to Spencer [S] and the best known upper bound is due to Thomason [T]. They are as follows: $$(1 + o(1)) \frac{ \sqrt 2 }{e} k 2 ^{k/2} < R(k,k) < k^{-1/2 + c / \sqrt{ \log k}} {2k-2 \choose k-1}. $$

Gowers [G] has suggested that resolving these problems might require a rough structure theorem.
