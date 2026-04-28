---
id: opg-acyclic_edge_coloring
title: Acyclic edge-colouring
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/acyclic_edge_coloring
---

# Statement

Conjecture Every simple graph with maximum degree $ \Delta $ has a proper $ (\Delta+2) $ -edge-colouring so that every cycle contains edges of at least three distinct colours.

# Source literature

- [AMR] N. Alon, C. McDiarmid and B. Reed, Acyclic colouring of graphs, Random Structures and Algorithms 2 (1991), 277-288. MathSciNet
- [ASZ] N. Alon, B. Sudakov and A. Zaks, Acyclic edge-colorings of graphs, J. Graph Theory 37 (2001), 157-167. MathSciNet
- [EP] L. Esperet and A. Parreau, Acyclic edge-coloring using entropy compression, arXiv:1206.1535 [math.CO].

# Progress

- An edge-colouring with the property that every cycle contains edges of at least three distinct colours is called an acyclic edge-colouring. It is known (see [AMR]) that every graph of maximum degree $ \Delta $ has an acyclic edge-colouring of size $ O(\Delta ) $ . The best upper bound so far is $ 4\Delta -4 $ and is due to Esperet and Parreau [EP]. It is also known (see [ASZ]) that this conjecture is true for graphs with girth at least $ C \Delta \log(\Delta ) $ (for some fixed constant $ C $ ).
