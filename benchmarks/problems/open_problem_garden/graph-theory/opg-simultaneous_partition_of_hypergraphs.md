---
id: opg-simultaneous_partition_of_hypergraphs
title: Simultaneous partition of hypergraphs
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/simultaneous_partition_of_hypergraphs
---

# Statement

Problem Let $ H_1 $ and $ H_2 $ be two $ r $ -uniform hypergraph on the same vertex set $ V $ . Does there always exist a partition of $ V $ into $ r $ classes $ V_1, \dots , V_r $ such that for both $ i=1,2 $ , at least $ r!m_i/r^r -o(m_i) $ hyperedges of $ H_i $ meet each of the classes $ V_1, \dots , V_r $ ?

# Source literature

- *[KO] D. Kühn and D. Osthus, Maximizing several cuts simultaneously, Combinatorics, Probability and Computing 16 (2007), 277-283.

# Progress

- The bound on the number of hyperedges is what one would expect for a random partition. For graphs, the question was answered in the affirmative in [KO]. Keevash and Sudakov observed that the answer is negative if we consider many hypergraphs instead of just 2 (see [KO] for the example).
