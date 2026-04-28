---
id: opg-minimum_number_of_transitive_subtournaments_of_order_3_in_a_tournament
title: Minimum number of arc-disjoint transitive subtournaments of order 3 in a tournament
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/minimum_number_of_transitive_subtournaments_of_order_3_in_a_tournament
---

# Statement

Conjecture If $ T $ is a tournament of order $ n $ , then it contains $ \left \lceil n(n-1)/6 - n/3\right\rceil $ arc-disjoint transitive subtournaments of order 3.

# Source literature

- [KY] M. Kabiya and R. Yuster. Packing transitive triples in a tournament. Ann. Comb. 12 (2008), no. 3, 291–-306.
- *[Y] R. Yuster. The number of edge-disjoint transitive triples in a tournament. Discrete Math. 287 (2004). no. 1-3,187--191.

# Progress

- If true the conjecture would be tight as shown by any tournament whose vertex set can be decomposed into $ 3 $ sets $ V_1, V_2, V_3 $ of size $ \lceil n/3 \rceil $ or $ \lfloor n/3\rfloor $ and such that $ V_1\rightarrow V_2 $ , $ V_2\rightarrow V_3 $ and $ V_3\rightarrow V_1 $ .

Let $ TT_3 $ denote the transitive tournament of order 3. A $ TT_3 $ -packing of a digraph $ D $ is a set of arc-disjoint copies of $ TT_3 $ subgraphs of $ D $ .

Let $ f(n) $ be the minimum size of a $ TT_3 $ -packing over all tournaments of order $ n $ . The conjecture and its tightness say $ f(n)= \left \lceil n(n-1)/6 - n/3\right\rceil $ .

The best lower bound for $ f(n) $ so far is due to Kabiya and Yuster [KY] proved that $ f(n) > \frac{41}{300} n^2(1+o(1)) $ .
