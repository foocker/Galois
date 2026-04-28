---
id: opg-limiting_subsequence_sums_in_z_n_x_z_n
title: Few subsequence sums in Z_n x Z_n
status: open
difficulty: research
domains:
- Number Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/limiting_subsequence_sums_in_z_n_x_z_n
---

# Statement

Conjecture For every $ 0 \le t \le n-1 $ , the sequence in $ {\mathbb Z}_n^2 $ consisting of $ n-1 $ copes of $ (1,0) $ and $ t $ copies of $ (0,1) $ has the fewest number of distinct subsequence sums over all zero-free sequences from $ {\mathbb Z}_n^2 $ of length $ n-1+t $ .

# Source literature


# Progress

- Definition: Given a sequence $ \bf a $ of elements from an additive abelian group, we call a subsequence sum any group element expressable as a sum of some nontrivial subsequence of $ \bf a $ . We say that $ \bf a $ is zero-free if $ 0 $ is not a subsequence sum.

It is easy to see that every sequence $ a_1,\ldots,a_n $ of elements from $ {\mathbb Z}_n $ has a nontrivial subsequence which sums to zero (actually this holds for every group of order $ n $ ). Just consider the elements $ a_1 $ , $ a_1 + a_2 $ , $ \ldots $ , $ a_1 + \ldots, a_n $ . If these elements are distinct, we have a zero sum. Otherwise, we have $ a_1 + \ldots + a_j = a_1 + \ldots + a_k $ for some $ 1 \le j < k \le n $ , but then $ a_{j+1} + a_{j+2} + \ldots a_k = 0 $ . The same argument shows that whenever $ 0 \le t \le n-1 $ , every zero-free sequence of $ t $ elements of $ {\mathbb Z}_n $ must have at least $ t $ distinct subsequence sums. In other words, the sequence consisting of $ t $ copies of $ 1 $ has the fewest number of distinct subsequence sums over all zero-free sequences in $ {\mathbb Z}_n $ of length $ t $ .

In the group $ {\mathbb Z}_n^2 $ , a theorem of Olsen shows that every sequence of length $ \ge 2n-1 $ has a nontrivial subsequence which sums to zero. However, we do not know what the minimum number of distinct subsequence sums is for a zero-free sequence of a given length. The above conjecture would appear to be the natural optimum.
