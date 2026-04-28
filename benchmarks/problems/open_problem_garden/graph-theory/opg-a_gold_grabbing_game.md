---
id: opg-a_gold_grabbing_game
title: A gold-grabbing game
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/a_gold_grabbing_game
---

# Statement

Setup Fix a tree $ T $ and for every vertex $ v \in V(T) $ a non-negative integer $ g(v) $ which we think of as the amount of gold at $ v $ .

2-Player game Players alternate turns. On each turn, a player chooses a leaf vertex $ v $ of the tree, takes the gold at this vertex, and then deletes $ v $ . The game ends when the tree is empty, and the winner is the player who has accumulated the most gold.

Problem Find optimal strategies for the players.

# Source literature


# Progress

- In the special case when $ T $ is a path of even length, the first player can ensure that she chooses either all of the even vertices, or all of the odd vertices. Thus, player 1 should never finish with less than player 2, and whenever the total gold on the odd vertices and the total gold on the even vertices are not equal, there is a winning strategy for player 1.
