---
id: opg-friendly_partitions
title: Friendly partitions
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/friendly_partitions
---

# Statement

A friendly partition of a graph is a partition of the vertices into two sets so that every vertex has at least as many neighbours in its own class as in the other.

Problem Is it true that for every $ r $ , all but finitely many $ r $ -regular graphs have friendly partitions?

# Source literature


# Progress

- Let me say at the start, that I (M. DeVos) suspect this problem has been considered previously, so I await a more correct attribution.

An unfriendly partition of a graph is a partition of the vertices into two sets so that every vertex has at least as many neighbours in the opposite class as its own. It is an easy fact that every (finite) graph has an unfriendly partition; for instance, any maximum size edge-cut gives a partition with this property.

Finding friendly partitions appears to be considerably more difficult. Perhaps one reason why is that there exist graphs without unfriendly partitions. For instance, $ K_{2n} $ and $ K_{2n+1,2n+1} $ have no unfriendly partitions. However, it appears possible that the only graphs which fail to have friendly partitions are fairly dense.

When $ r=3 $ , the above problem is fairly easy to solve, as it reduces to the problem of finding two vertex disjoint cycles. Every cubic graph other than $ K_4 $ or $ K_{3,3} $ has two disjoint cycles, and thus has a friendly partition. The case when $ r=4 $ is also not terribly complicated. However, the next step up, $ r=5 $ looks like a tricky problem which requires something new.
