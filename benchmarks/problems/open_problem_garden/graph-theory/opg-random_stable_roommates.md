---
id: opg-random_stable_roommates
title: Random stable roommates
status: solved
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/random_stable_roommates
---

# Statement

Conjecture The probability that a random instance of the stable roommates problem on $ n \in 2{\mathbb N} $ people admits a solution is $ \Theta( n ^{-1/4} ) $ .

# Source literature

- [GS] D. Gale D and L. S. Shapley, College admissions and the stability of marriage, Am. Math. Mon. 69 9-15.
- [I] R. W. Irving, An efficient algorithm for the stable roommates problem, J. Algorithms 6 577-95.
- [IP] B. Pittel and R. W. Irving, An upper bound for the solvability of a random stable roommates instance, Random Struct. Algorithms 5 465-87.
- *[M] S. Mertens, Random stable matchings, J. Stat. Mech. Theory Exp. 2005, no. 10 MathSciNet
- [P] B. Pittel, The 'stable roommates' problem with random preferences, Ann. Probab. 21 1441-77

# Progress

- A system of preferences for a graph $ G $ is a family $ \{ >_v \}_{v \in V(G)} $ so that every $ >_v $ is a linear ordering of the neighbors of the vertex $ v $ . We say that $ v $ prefers $ u $ to $ u' $ if $ u >_v u' $ . A perfect matching $ M $ in $ G $ is stable if there do not exist $ uv,u'v' \in M $ so that $ u $ prefers $ v' $ to $ v $ and $ v' $ prefers $ u $ to $ u' $ .

A famous theorem of Gale-Shapley [GS] proves that every system of preferences on a complete bipartite graph $ K_{n,n} $ admits a stable perfect matching. Indeed, they provide an amusing algorithm to construct one. On complete graphs, this problem is known as either the homosexual stable marriage problem, or more commonly, the stable roommate problem. Here there does not always exist a solution (that is, a stable perfect matching), but Irving [I] constructed an algorithm which runs in polynomial time, and outputs a solution if one exists.

Let $ P_n $ denote the probability that a random instance of the stable roommates problem has a solution (so the above conjecture asserts that $ P_n = \Theta( n^{-1/4} $ ). The following are the best known asymptotic bounds for $ P_n $ (with $ n $ even) and hold for $ n $ sufficiently large. The lower bound is due to Pittel [P] and the upper bound to Pittel and Irving [IP]

\[ \frac{2 e ^{3/2} }{ \sqrt{\pi n}} \le P_n \le \frac{\sqrt{e}}{2} \]

Mertens [M] did an extensive Monte-Carlo simulation to obtain the above conjecture. Indeed, by guessing at the constant he even offers the stronger conjecture $ P_n \simeq e \sqrt{ \frac{2}{\pi} } n ^{-1/4} $ .
