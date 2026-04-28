---
id: opg-approximation_ratio_for_maximum_edge_disjoint_paths_problem
title: Approximation Ratio for Maximum Edge Disjoint Paths problem
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/approximation_ratio_for_maximum_edge_disjoint_paths_problem
---

# Statement

Conjecture Can the approximation ratio $ O(\sqrt{n}) $ be improved for the Maximum Edge Disjoint Paths problem (MaxEDP) in planar graphs or can an inapproximability result stronger than $ \mathcal{APX} $ -hardness?

# Source literature

- Cédric Bentz, Edge disjoint paths and max integral muliflow/min multicut theorems in planar graphs, Electronic Notes in Discrete Mathematics 22 (2005), 55–60

# Progress

- Assume a flow graph $ G = (V, E) $ with $ n $ vertices and $ m $ edges. Each edge has a capacity function $ c: E \rightarrow \mathbb{Z}^+ $ (Flow network). The graph contains a list $ \mathcal{N} $ of terminal vertices called sources ( $ s_i $ ) and sinks ( $ s_i' $ ). Each pair ( $ s_i, s_i' $ ) defines a net or commodity.

A Multiflow is a way of routing commodities from their sources to the respective sinks while ensuring that the flow of each commodity is conserved at each non-terminal vertex and that the sum of the flows of all commodities through an edge does not exceed the capacity of the edge.

The Maximum Integer Multiflow problem (MaxIMF) seeks to maximize the number of flow units routed between the nets in the graph. The Maximum Edge Disjoint Paths (MaxEDP) problem seeks to find the maximum number of disjoint paths between the sources and sinks. When the capacities for all edges are set to one, MaxIMF simplifies into the MaxEDP problem.

Bentz provides an algorithm to find the MaxEDP with a proven approximation ratio (Approximation and integrality gap) of $ O(\sqrt{n}) $ . Can the approximation ratio be improved for MaxEDP in planar graphs, or can an inapproximability result stronger than $ \mathcal{APX} $ -hardness be proved for this problem? And what about the general graphs?
