---
id: opg-caccetta_haggkvist_conjecture
title: Caccetta-Häggkvist Conjecture
status: open
difficulty: frontier
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/caccetta_haggkvist_conjecture
---

# Statement

Conjecture Every simple digraph of order $ n $ with minimum outdegree at least $ r $ has a cycle with length at most $ \lceil n/r\rceil $

# Source literature


# Progress

- It is one of the most famous conjectures in graph theory. It has many alternative formulations and lots of work have been done around it. Many interesting conjectures are related to it. See [Sul]. It is in particular implied by a conjecture of Thomassé and Hoàng-Reed Conjecture.

The Caccetta-Häggkvist Conjecture is a generalization of an earlier conjecture of Behzad, Chartrand, and Wall, who conjectured it only for diregular digraphs. Caccetta-H äggkvist Conjecture has been proved for $ r\leq \sqrt{n/2} $ by Shen [She1]. For $ r\geq n/2 $ it is trivial. But already for $ r=n/3 $ , it is still open as well as Behzad-Chartrand-Wall Conjecture

Conjecture Every simple $ n $ -vertex digraph with minimum outdegree at least $ r/3 $ and minimum indegree at least $ r/3 $ has a cycle with length at most $ 3 $ .

This conjecture would be implied by Seymour's Second Neighbourhood Conjecure.

Shen [She2] also proved the following approximate version.

Theorem Every simple digraph of order $ n $ with minimum outdegree at least $ r $ has a cycle with length at most $ n/r + 73 $ .

Bollobás and Scott [BS] proposed a weighted version of the Caccetta-Häggkvist Conjecture.

Conjecture Let $ w:E(D) \rightarrow [0,1] $ be a weight function on the arcs of a digraph $ D $ . If $ \sum_{u\in N^-(v)} w(uv) \geq 1 $ and $ \sum_{u\in N^+(v)} w(vu) \geq 1 $ for all $ v\in V(D) $ , then there is a directed cycle in $ D $ of total weight at least 1.

They gave a nice proof that there is a directed path of total weight at least 1.

Related problems
Seymour's Second Neighbourhood Conjecture
Directed path of length twice the minimum outdegree
Hoàng-Reed Conjecture

Bibliography

[BCW] M. Behzad, G. Chartrand, and C. Wall. On minimal regular digraphs with given girth. Fundamenta Mathematicae, 69:227–231, 1970.

[BS] B. Bollobás and A. D. Scott, A proof of a conjecture of {B}ondy concerning paths in weighted digraphs. J. Combin. Theory Ser. B, 66:283-292, 1996.

*[CH] L. Caccetta and R. Häggkvist. On minimal digraphs with given girth. Congressus Numerantium, XXI, 1978

[She1J. Shen. On the girth of digraphs. Discrete Math, 211(1-3):167–181, 2000.

[She2] J. Shen. On the Caccetta-Häggkvist conjecture. Graphs and Combinatorics, 18(3):645–654, 2002.

[Sul] Blair D. Sullivan: A Summary of Problems and Results related to the Caccetta-Häggkvist Conjecture

* indicates original appearance(s) of problem.

add new comment
