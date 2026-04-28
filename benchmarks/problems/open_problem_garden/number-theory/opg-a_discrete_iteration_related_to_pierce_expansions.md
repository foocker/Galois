---
id: opg-a_discrete_iteration_related_to_pierce_expansions
title: A discrete iteration related to Pierce expansions
status: open
difficulty: research
domains:
- Number Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/a_discrete_iteration_related_to_pierce_expansions
---

# Statement

Conjecture Let $ a > b > 0 $ be integers. Set $ b_1 = b $ and $ b_{i+1} = {a \bmod {b_i}} $ for $ i \geq 0 $ . Eventually we have $ b_{n+1} = 0 $ ; put $ P(a,b) = n $ .

Example: $ P(35, 22) = 7 $ , since $ b_1 = 22 $ , $ b_2 = 13 $ , $ b_3 = 9 $ , $ b_4 = 8 $ , $ b_5 = 3 $ , $ b_6 = 2 $ , $ b_7 = 1 $ , $ b_8 = 0 $ .

Prove or disprove: $ P(a,b) = O((\log a)^2) $ .

# Source literature

- [ES] P. Erd\"os and J. Shallit, ``New bounds on the length of finite Pierce and Engel series'', S\'eminaire de Th\'eorie des Nombres de Bordeaux 3 (1991), 43--53.

# Progress

- The best upper bound is currently $ P(a,b) = O(a^{1/3}) $ . For more information, see [ES].
