---
id: opg-crossing_numbers_and_coloring
title: Crossing numbers and coloring
status: open
difficulty: frontier
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/crossing_numbers_and_coloring
---

# Statement

We let $ cr(G) $ denote the crossing number of a graph $ G $ .

Conjecture Every graph $ G $ with $ \chi(G) \ge t $ satisfies $ cr(G) \ge cr(K_t) $ .

# Source literature

- [BT] J. Barat and G. Toth, Towards the Albertson Conjecture

# Progress

- This conjecture is an interesting weakening of the disproved Hajos Conjecture which asserted that $ \chi(G) \ge t $ implies that $ G $ contains a subdivision of $ K_t $ .

A minimal counterexample to Albertson's conjecture is critical, with minimum degree $ \ge t $ . Using this and the crossing lemma, Albertson, Cranston and Fox showed that a minimum counterexample has at most $ 4t $ vertices. They then analyzed small cases to show that the conjecture holds for $ t \le 12 $ . More recently, Barat and Toth [BT] sharpened these arguments to show that the conjecture holds for $ t \le 16 $ .
