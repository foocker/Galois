---
id: opg-turans_problem_for_hypergraphs
title: Turán's problem for hypergraphs
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/turans_problem_for_hypergraphs
---

# Statement

Conjecture Every simple $ 3 $ -uniform hypergraph on $ 3n $ vertices which contains no complete $ 3 $ -uniform hypergraph on four vertices has at most $ \frac12 n^2(5n-3) $ hyperedges.

Conjecture Every simple $ 3 $ -uniform hypergraph on $ 2n $ vertices which contains no complete $ 3 $ -uniform hypergraph on five vertices has at most $ n^2(n-1) $ hyperedges.

# Source literature

- *[T] P. Turán, Eine Extremalaufgabe aus der Graphentheorie. Mat. Fiz. Lapok 48 (1941), 436--452.

# Progress

- Let $ V $ be an $ n $ -set. A $ k $ -uniform hypergraph $ (V,{\cal F}) $ is complete if $ {\cal F}={V \choose k} $ , the set of all $ {n\choose{k}} $ $ k $ -subsets of $ V $ .

Let $ \{X,Y,Z\} $ be a partition of $ V $ into three sets which are as nearly equal in size as possible, and let $ {\cal F} $ be the union of $ \{\{x,y,z\}:x\in X, y\in Y, z\in Z\} $ , $ \{\{x_1,x_2,y\}:x_1\in X, x_2\in X, y\in Y\} $ , $ \{\{y_1,y_2,z\}:y_1\in Y, y_2\in Y, z\in Z\} $ , and $ \{\{z_1,z_2,x\}:z_1\in Z, z_2\in Z, x\in X\} $ . This $ 3 $ -uniform hypergraph has $ \frac12 n^2(5n-3) $ hyperedges and contains no complete $ 3 $ -uniform hypergraph on four vertices. Hence the first conjecture asserts that this hypergraph is extremal with this prpoerty.

Let $ \{X,Y\} $ be a partition of $ V $ into two sets which are as nearly equal in size as possible, and let $ {\cal F} $ be the set of all $ 3 $ -subsets of $ V $ which intersect both $ X $ and $ Y $ . This $ 3 $ -uniform hypergraph has $ n^2(n-1) $ hyperedges and contains no complete $ 3 $ -uniform hypergraph on five vertices. Hence the second conjecture asserts that this hypergraph is extremal with this property.
