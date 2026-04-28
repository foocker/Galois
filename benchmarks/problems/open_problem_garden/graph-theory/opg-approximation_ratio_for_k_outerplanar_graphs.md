---
id: opg-approximation_ratio_for_k_outerplanar_graphs
title: Approximation ratio for k-outerplanar graphs
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/approximation_ratio_for_k_outerplanar_graphs
---

# Statement

Conjecture Is the approximation ratio for the Maximum Edge Disjoint Paths (MaxEDP) or the Maximum Integer Multiflow problem (MaxIMF) bounded by a constant in $ k $ -outerplanar graphs or tree-width graphs?

# Source literature

- C. Bentz, “Disjoint paths in sparse graphs,” Discrete Appl. Math., vol. 157, no. 17, pp. 3558–3568, 2009

# Progress

- Assume a flow graph $ G = (V, E) $ with $ n $ vertices and $ m $ edges (Flow network). Each edge has a capacity function $ c: E \rightarrow \mathbb{Z}^+ $ . The graph contains a list $ \mathcal{N} $ of terminal vertices called sources ( $ s_i $ ) and sinks ( $ s_i' $ ). Each pair ( $ s_i, s_i' $ ) defines a net or commodity.

A Multiflow is a way of routing commodities from their sources to the respective sinks while ensuring that the flow of each commodity is conserved at each non-terminal vertex and that the sum of the flows of all commodities through an edge does not exceed the capacity of the edge.

The Maximum Integer Multiflow problem (MaxIMF) seeks to maximize the number of flow units routed between the nets in the graph. The Maximum Edge Disjoint Paths (MaxEDP) problem seeks to find the maximum number of disjoint paths between the sources and sinks. When the capacities for all edges are set to one, MaxIMF simplifies into the MaxEDP problem.

Is the approximation ratio (Approximation and integrality gap) for MaxEDP or MaxIMF bounded by a constant in $ k $ -outerplanar graphs (Outerplanar graphs) or tree-width graphs?
