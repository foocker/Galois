---
id: opg-matching_cut_and_girth
title: Matching cut and girth
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/matching_cut_and_girth
---

# Statement

Question For every $ d $ does there exists a $ g $ such that every graph with average degree smaller than $ d $ and girth at least $ g $ has a matching-cut?

# Source literature

- [C84] V. Chvátal, Recognizing decomposable graphs, J Graph Theory 8 (1984), 51–53
- [BFP11] P. Bonsma, A. Farley, A. Proskurowski, Extremal graphs having no matching cuts, J Graph Theory (2011)

# Progress

- Let $ G=(V,E) $ be a graph. A matching $ M $ is a matching-cut if there exists a set $ S\subset V $ such that $ M = E(S:V\setminus S) $ . Graphs having a matching-cut are called decomposable.

It is known that every graph with $ |E| < 3(|V|-1)/2 $ is decomposable [BFP11].
