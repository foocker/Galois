---
id: opg-bases_of_many_weights
title: Bases of many weights
status: open
difficulty: frontier
domains:
- Combinatorics
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/bases_of_many_weights
---

# Statement

Let $ G $ be an (additive) abelian group, and for every $ S \subseteq G $ let $ {\mathit stab}(S) = \{ g \in G : g + S = S \} $ .

Conjecture Let $ M $ be a matroid on $ E $ , let $ w : E \rightarrow G $ be a map, put $ S = \{ \sum_{b \in B} w(b) : B \mbox{ is a base} \} $ and $ H = {\mathit stab}(S) $ . Then $$|S| \ge |H| \left( 1 - rk(M) + \sum_{Q \in G/H} rk(w^{-1}(Q)) \right).$$

# Source literature

- [C] A.L. Cauchy, Recherches sur les nombers, J. Ecole Polytechniques, 9 (1813), 99-123.
- [D] H. Davenport, On the addition of residue classes, J. London Math. Soc., 10 (1935), 30-32.
- [K] M. Kneser, Abschätzung der aymptotischen dichte von summenmengen, Math. Z. (1953) 459-484.
- [N] M.B. Nathanson, Additive Number Theory, GTM 165, Springer, 1996.
- *[SS] A. Schrijver and P.D. Seymour, Spanning trees of different weights. Polyhedral combinatorics, DIMACS Ser. Discrete Math. Theoret. Comp. Sci., 1, 281-288.

# Progress

- Although this conjecture may look a bit technical, it is in fact very natural, and important.

There is an interesting branch of combinatorial number theory which begins with the Cauchy-Davenport theorem, and M. Kneser's generelization of this theorem. We highlight these two theorems below. For a positive integer $ n $ , we let $ {\mathbb Z}_n = {\mathbb Z} / n {\mathbb Z} $ .

Theorem (Cauchy-Davenport) If $ p $ is prime and $ A,B \subseteq {\mathbb Z}_p $ are nonempty, then $ |A+B| \ge \min\{p, |A| + |B| - 1 \} $ .

Theorem (Kneser) Let $ A,B \subseteq G $ be finite and nonempty, and let $ H = {\mathit stab}(A+B) $ . Then $ |A+B| \ge |A+H| + |B+H| - |H| $ .

In a somewhat underappreciated paper of Schrijver and Seymour, they find a generalization of the Cauchy-Davenport theorem to matroids. Namely, they prove the following.

Theorem (Schrijver, Seymour) Let $ M $ be a matroid on $ E $ , let $ p $ be prime, and let $ w : E \rightarrow {\mathbb Z}_p $ be a map. Then $ \#\{ \sum_{b \in B} w(b) : B \mbox{ is a base} \} \ge \min \{p, \sum_{g \in {\mathbb Z}_p} rk(w^{-1}(g)) \} $ .

The special case of this theorem when the underlying matroid is obtained from the free matroid on two elements by adding parallel edges is exactly the Cauchy-Davenport theorem. Further, their conjecture is precisely the common generalization of their theorem and Kneser's theorem.

DeVos, Goddyn, and Mohar have proved this conjecture in the special case when the underlying matroid is obtained from a uniform matroid by adding parallel elements, but apart from that, little is known.
