---
id: opg-high_connectivity_no_k_n
title: Highly connected graphs with no K_n minor
status: open
difficulty: frontier
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/high_connectivity_no_k_n
---

# Statement

Problem Is it true for all $ n \ge 0 $ , that every sufficiently large $ n $ -connected graph without a $ K_n $ minor has a set of $ n-5 $ vertices whose deletion results in a planar graph?

# Source literature


# Progress

- A famous conjecture of Jorgensen asserts that every 6-connected graph without a $ K_6 $ -minor is apex (planar plus one vertex). If true, Jorgensen's conjecture does not generalize (naively) to higher connectivities, since for sufficiently large $ n $ , there do exist $ n $ -connected graphs which are not close to planar in the sense we are considering (many more than $ n-5 $ vertices must be deleted to leave a planar graph). This conjecture of Thomas asserts that all such graphs are small in size.

For $ n \le 6 $ this conjecture is true. For $ n \le 4 $ this conjecture is trivial, since any graph without a $ K_4 $ -minor is planar. The $ n=5 $ case follows from a theorem of Wagner which gives a construction for all graphs without $ K_5 $ -minors (and from which it follows that every 4-connected graph with no $ K_5 $ minor is planar). The $ n=6 $ case was recently resolved by DeVos, Hegde, Kawarabayashi, Norine, Thomas, and Wollan. The difficulties associated with finding $ K_n $ minors in graphs make this conjecture appear daunting, but if true, it would yield powerful insight into the structure of graphs.
