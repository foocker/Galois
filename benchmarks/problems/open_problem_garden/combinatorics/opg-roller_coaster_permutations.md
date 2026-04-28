---
id: opg-roller_coaster_permutations
title: Roller Coaster permutations
status: open
difficulty: frontier
domains:
- Combinatorics
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/roller_coaster_permutations
---

# Statement

Let $ S_n $ denote the set of all permutations of $ [n]=\set{1,2,\ldots,n} $ . Let $ i(\pi) $ and $ d(\pi) $ denote respectively the number of increasing and the number of decreasing sequences of contiguous numbers in $ \pi $ . Let $ X(\pi) $ denote the set of subsequences of $ \pi $ with length at least three. Let $ t(\pi) $ denote $ \sum_{\tau\in X(\pi)}(i(\tau)+d(\tau)) $ .

A permutation $ \pi\in S_n $ is called a Roller Coaster permutation if $ t(\pi)=\max_{\tau\in S_n}t(\tau) $ . Let $ RC(n) $ be the set of all Roller Coaster permutations in $ S_n $ .

Conjecture For $ n\geq 3 $ ,

\item If $ n=2k $ , then $ |RC(n)|=4 $ . \item If $ n=2k+1 $ , then $ |RC(n)|=2^j $ with $ j\leq k+1 $ .

Conjecture (Odd Sum conjecture) Given $ \pi\in RC(n) $ ,

\item If $ n=2k+1 $ , then $ \pi_j+\pi_{n-j+1} $ is odd for $ 1\leq j\leq k $ . \item If $ n=2k $ , then $ \pi_j + \pi_{n-j+1} = 2k+1 $ for all $ 1\leq j\leq k $ .

# Source literature

- *[AS] Tanbir Ahmed, Hunter Snevily, Some properties of Roller Coaster permutations. To appear in Bull. Institute of Combinatorics and its Applications, 2013.

# Progress

- Status: open.
