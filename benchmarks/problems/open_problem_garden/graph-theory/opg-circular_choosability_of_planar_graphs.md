---
id: opg-circular_choosability_of_planar_graphs
title: Circular choosability of planar graphs
status: open
difficulty: graduate
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/circular_choosability_of_planar_graphs
---

# Statement

Let $ G = (V, E) $ be a graph. If $ p $ and $ q $ are two integers, a $ (p,q) $ -colouring of $ G $ is a function $ c $ from $ V $ to $ \{0,\dots,p-1\} $ such that $ q \le |c(u)-c(v)| \le p-q $ for each edge $ uv\in E $ . Given a list assignment $ L $ of $ G $ , i.e.~a mapping that assigns to every vertex $ v $ a set of non-negative integers, an $ L $ -colouring of $ G $ is a mapping $ c : V \to N $ such that $ c(v)\in L(v) $ for every $ v\in V $ . A list assignment $ L $ is a $ t $ - $ (p,q) $ -list-assignment if $ L(v) \subseteq \{0,\dots,p-1\} $ and $ |L(v)| \ge tq $ for each vertex $ v \in V $ . Given such a list assignment $ L $ , the graph G is $ (p,q) $ - $ L $ -colourable if there exists a $ (p,q) $ - $ L $ -colouring $ c $ , i.e. $ c $ is both a $ (p,q) $ -colouring and an $ L $ -colouring. For any real number $ t \ge 1 $ , the graph $ G $ is $ t $ - $ (p,q) $ -choosable if it is $ (p,q) $ - $ L $ -colourable for every $ t $ - $ (p,q) $ -list-assignment $ L $ . Last, $ G $ is circularly $ t $ -choosable if it is $ t $ - $ (p,q) $ -choosable for any $ p $ , $ q $ . The circular choosability (or circular list chromatic number or circular choice number) of G is $$cch(G) := \inf\{t \ge 1 : G \text{ is circularly $t$-choosable}\}.$$

Problem What is the best upper bound on circular choosability for planar graphs?

# Source literature

- [HKMS] F. Havet, R. J. Kang, T. Müller, and J.-S. Sereni. Circular choosability. J. Graph Theory 61 (2009), no. 4, 241--270.
- [T] C. Thomassen. Every planar graph is 5-choosable. J. Combinatorial Theory B 62 (1994) 180--181

# Progress

- The problem was first posed in 2003 by Mohar (Problem 4 of link*) who suggested the answer should be between 4 and 5.

Some time later, Havet, Kang, Müller, and Sereni [HKMS] showed that in fact the answer is somewhere between 6 and 8. The upper bound extends a celebrated planar choosability proof due to Thomassen [T]. The lower bound is by way of an elementary, though rather large, construction.
