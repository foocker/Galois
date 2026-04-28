---
id: opg-what_is_the_smallest_number_of_disjoint_spanning_trees_made_a_graph_hamiltonian
title: What is the smallest number of disjoint spanning trees made a graph Hamiltonian
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/what_is_the_smallest_number_of_disjoint_spanning_trees_made_a_graph_hamiltonian
---

# Statement

We are given a complete simple undirected weighted graph $ G_1=(V,E) $ and its first arbitrary shortest spanning tree $ T_1=(V,E_1) $ . We define the next graph $ G_2=(V,E\setminus E_1) $ and find on $ G_2 $ the second arbitrary shortest spanning tree $ T_2=(V,E_2) $ . We continue similarly by finding $ T_3=(V,E_3) $ on $ G_3=(V,E\setminus \cup_{i=1}^{2}E_i) $ , etc. Let k be the smallest number of disjoint shortest spanning trees as defined above and let $ T^{k}=(V,\cup_{i=1}^{k}E_i) $ be the graph obtained as union of all $ k $ disjoint trees.

Question 1. What is the smallest number of disjoint spanning trees creates a graph $ T^{k} $ containing a Hamiltonian path.

Question 2. What is the smallest number of disjoint spanning trees creates a graph $ T^{k} $ containing a shortest Hamiltonian path?

Questions 3 and 4. Replace in questions 1 and 2 a shortest spanning tree by a 1-tree. What is the smallest number of disjoint 1-trees creates a Hamiltonian graph? What is the smallest number of disjoint 1-trees creates a graph containing a shortest Hamiltonian cycle?

# Source literature

- M. Chrobak and S. Poljak. On common edges in optimal solutions to travelling salesman and other optimization problems, Discrete Applied Mathematics 20 (1988) 101-111.

# Progress

- These questions are induced by the following paper Chrobak and Poljak. On common edges in optimal solutions to travelling salesman and other optimization problems, Discrete Applied Mathematics 20 (1988) 101-111.
