---
id: opg-3_decomposition_conjecture
title: 3-Decomposition Conjecture
status: open
difficulty: frontier
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/3_decomposition_conjecture
---

# Statement

Conjecture (3-Decomposition Conjecture) Every connected cubic graph $ G $ has a decomposition into a spanning tree, a family of cycles and a matching.

# Source literature

- [1] Arthur Hoffmann-Ostenhof, Tomáš Kaiser, Kenta Ozeki, \arXiv[Decomposing planar cubic graphs] 1609.05059 [math.CO]
- [2] Arthur Hoffmann-Ostenhof, Kenta Ozeki, \arXiv[On HISTs in Cubic Graphs] 1507.07689 [math.CO]
- [3] F. Abdolhosseini, S. Akbari, H. Hashemi, M.S. Moradian, \arXiv[Hoffmann-Ostenhof's conjecture for traceable cubic graphs] 1607.04768[math.CO]
- [4] Anna Bachstein, Dong Ye (talk): www.rwoodroofe.math.msstate.edu/workshop2014/bachstein_slides.pdf
- [5] Arthur Hoffmann-Ostenhof (talk): www.iti.zcu.cz/plzen15/talks/1-2a-Arthur-Survey_decomposition.ppt
- [6] Yingqian Wang, Qijun Zhang, Discrete Mathematics 311 (2011) 844–849, Decomposing a planar graph with girth at least 8 into a forest and a matching
- [7] Kenta Ozeki, Dong Ye, Decomposing plane cubic graphs, European Journal of Combinatorics 52 (2016) 40-46.

# Progress

- We state the conjecture in a more precise manner:

Let $ G $ be a connected cubic graph. Then $ G $ contains a spanning tree $ H_1 $ , a $ 2 $ -regular subgraph $ H_2 $ and a matching $ H_3 $ (where only $ H_3 $ and not $ H_1 $ or $ H_2 $ may be empty) such that $ E(H_1) \cup E(H_2) \cup E(H_3) = E(G) $ and $ E(H_i) \cap E(H_j) =\emptyset $ for every $ \{i,j\} \subseteq \{1,2,3\} $ with $ i\not=j $ .

The conjecture holds for all hamiltionian cubic graphs and for all connected planar cubic graphs, see [1] and see also [7].

Every cubic graph G which has a spanning tree T such that every vertex of T has degree three or one (such spanning tree T is called a HIST) obviously satisfies this conjecture. But not every connected cubic graph has a HIST, see [2].

The 3-Decomposition Conjecture has been shown to be equivalent to the following conjecture:

Conjecture (2-Decomposition Conjecture) Let $ G $ be connected graph where every vertex has degree two or three. Suppose that for every cycle $ C $ of $ G $ , $ G-E(C) $ is disconnected, then $ G $ has a decomposition into a spanning tree $ T $ and a matching $ M $ , i.e $ G-M=T $ .

Note that every cycle $ C $ which passes through a vertex of degree two satisfies the condition that G-E(C) is disconnected.

Remark: The 3-Decomposition Conjecture has also been shown to hold for other classes of cubic graphs, see for instance [3,4]. A survey on the 3-Decompostion conjecture has been given by the author 2015 in Pilsen (at that time the planar case was still open) see iti.zcu.cz/plzen15/talks/1-2a-Arthur-Survey_decomposition.ppt (and press play if you find the play button). Note that there are several papers on the problem whether a planar graph $ G $ has a matching $ M $ such that $ G-M $ is acyclic, see for instance [6].
