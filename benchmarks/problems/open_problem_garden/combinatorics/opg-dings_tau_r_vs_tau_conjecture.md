---
id: opg-dings_tau_r_vs_tau_conjecture
title: Ding's tau_r vs. tau conjecture
status: open
difficulty: frontier
domains:
- Combinatorics
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/dings_tau_r_vs_tau_conjecture
---

# Statement

Conjecture Let $ r \ge 2 $ be an integer and let $ H $ be a minor minimal clutter with $ \frac{1}{r}\tau_r(H) < \tau(H) $ . Then either $ H $ has a $ J_k $ minor for some $ k \ge 2 $ or $ H $ has Lehman's property.

# Source literature


# Progress

- See Wikipedia's Clutter for definitions of clutter and clutter minors. The clutter $ J_k $ is the degenerate projective plane with vertex set $ \{0,1,\ldots,k\} $ and edge set $ \{ \{0,1\}, \{1,2\},\ldots,\{0,k\},\{0,1,\ldots,k\} \} $ . If $ H=(V,E) $ is a clutter, then for every positive integer $ r $ we let $ \tau_r(H) $ denote the largest multiset of vertices of $ H $ which hit every edge at least $ r $ times. Note that $ \tau(H) = \tau_1(H) $ and that $ \tau_r(H) \le r \tau(H) $ .

We say that a clutter $ H $ with $ |V(H)| = n $ , $ \tau(H) = s $ and $ \tau(b(H)) = r $ has Lehman's property if $ rs > n $ , $ E(H) = \{A_1,\ldots,A_n\} $ , $ E(b(H)) = \{B_1,\ldots,B_n\} $ , and the following properties are satisfied.

\item $ |A_i| = r $ for every $ 1 \le i \le n $ . \item $ |B_i| = s $ for every $ 1 \le i \le n $ . \item $ |A_i \cap B_i| = rs - n +1 $ for $ 1 \le i \le n $ \item $ |A_i \cap B_j| = 1 $ if $ 1 \le i,j \le n $ and $ i \neq j $ . \item every $ v \in V(H) $ lies in exactly $ r $ edges of $ H $ , $ s $ edges of $ b(H) $ , and $ rs-n+1 $ members of $ \{A_1 \cap B_1, \ldots ,A_n \cap B_n\} $ .

Although the conditions in Lehman's condition are extremely stringent, Lehman [L] showed that every minor minimal clutter with the MFMC property satisfies these properties. Since the MFMC property for $ H $ implies $ \frac{1}{r}\tau_r(H) = \tau(H) $ (and the degenerate projective planes are minor minimal without MFMC), if true, the above conjecture would be a nice extension of Lehman's theorem.

Ding [D] proved this conjecture for $ r=2 $ , but it is open for all other cases.

Bibliography

*[D] G. Ding, Clutters with tau_2=2 tau, Discrete Math. 115 (1993), no. 1-3, 141--152. MathSciNet.

[L] A. Lehman, On the width-length inequality, mimeographic notes, published 1979. Math. Program. 17, 403--417 MathSciNet.

* indicates original appearance(s) of problem.
