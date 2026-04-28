---
id: opg-reeds_omega_delta_and_chi_conjecture
title: Reed's omega, delta, and chi conjecture
status: open
difficulty: frontier
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/reeds_omega_delta_and_chi_conjecture
---

# Statement

For a graph $ G $ , we define $ \Delta(G) $ to be the maximum degree, $ \omega(G) $ to be the size of the largest clique subgraph, and $ \chi(G) $ to be the chromatic number of $ G $ .

Conjecture $ \chi(G) \le \ceil{\frac{1}{2}(\Delta(G)+1) + \frac{1}{2}\omega(G)} $ for every graph $ G $ .

# Source literature

- *[R] B. Reed, $ \omega, \Delta $ , and $ \chi $ , J. Graph Theory 27 (1998) 177-212.

# Progress

- Perhaps the two most trivial bounds on $ \chi(G) $ are $ \chi(G) \ge \omega(G) $ and $ \chi(G) \le \Delta(G) + 1 $ . The above conjecture roughly asserts that the (rounded-up) average of $ \Delta(G)+1 $ and $ \omega(G) $ should again be an upper bound on $ \chi(G) $ .

The conjecture is easy to verify when $ \omega(G) $ is very large. It is trivial when $ \omega(G) \ge \Delta(G) $ , and it follows from Brook's theorem if $ \omega(G) = \Delta(G)-1 $ . On the other hand, if $ \omega(G) = 2 $ , so $ G $ is triangle free, then the conjecture is also true for $ \Delta $ sufficiently large. Indeed, Johannsen proved the much stronger fact that there exists a fixed constant $ c $ so that $ \chi(G) \le \frac{c \Delta(G)}{\log \Delta(G)} $ for every triangle free graph $ G $ .

Reed showed that the conjecture holds when $ \Delta(G) = |V(G)| - 1 $ by way of matching theory. More interestingly, he proved (using probabilistc methods) that the conjecture is true provided that $ \Delta $ is sufficiently large, and $ \omega $ is sufficiently close to $ \Delta $ . More precisely, he proves the following:

Theorem There exists a fixed constant $ \Delta_0 $ such that for every $ \Delta \ge \Delta_0 $ , if $ G $ is a graph of maximum degree $ \Delta $ with no clique of size $ >k $ for some $ k \ge (1 - \frac{1}{70000000}) \Delta $ then $ \chi(G) \le \frac{\Delta + 1 + k}{2} $ .

It is known that the conjecture is true fractionally (that is with $ \chi(G) $ replaced by $ \chi_f(G) $ , the fractional chromatic number of~ $ G $ ).
