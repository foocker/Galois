---
id: opg-shannon_capacity_of_the_seven_cycle
title: Shannon capacity of the seven-cycle
status: open
difficulty: frontier
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/shannon_capacity_of_the_seven_cycle
---

# Statement

Problem What is the Shannon capacity of $ C_7 $ ?

# Source literature

- [B] Tom Bohman, A limit theorem for the Shannon capacity of odd cycles II, Proc. Amer. Math. Soc. 133 (2005), no. 2, 537-543.
- [L] László Lovász, On the Shannon capacity of a graph, IEEE Trans. Inform. Th. IT-25 (1979), 1-7.

# Progress

- Let $ \alpha(G) $ denote the independence number of the graph $ G $ , and let $ G*H $ denote the strong graph product of $ G $ and $ H $ (in which $ (g,h) $ is adjacent to $ (g',h') $ if $ g=g' $ and $ h $ is adjacent to $ h' $ , or if $ h=h' $ and $ g $ is adjacent to $ g' $ , or if $ g $ is adjacent to $ g' $ and $ h $ is adjacent to $ h' $ ). Then the Shannon capacity of $ G $ is defined by $$\theta(G) = \lim_{k\to\infty} \biggl({\alpha(G*G*\cdots*G) \over k}\biggr)^{1/k},$$ where the strong graph product is over $ k $ copies of $ G $ . The Shannon capacity is important because it represents the effective size of an alphabet in a communication model represented by $ G $ , but it is notoriously difficult to compute. Lovász [L] famously proved that the Shannon capacity of the five-cycle $ C_5 $ is $ \sqrt{5} $ , but even the Shannon capacity of $ C_7 $ remains unknown. However, Bohman [B] has shown that $$\lim_{k\to\infty}(k+(1/2)-\theta(C_{2k+1}))=0.$$
