---
id: opg-bene_conjecture
title: Beneš Conjecture
status: open
difficulty: frontier
domains:
- Combinatorics
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/bene_conjecture
---

# Statement

Let $ E $ be a non-empty finite set. Given a partition $ \bf h $ of $ E $ , the stabilizer of $ \bf h $ , denoted $ S(\bf h) $ , is the group formed by all permutations of $ E $ preserving each block of $ \mathbf h $ .

Problem ( $ \star $ ) Find a sufficient condition for a sequence of partitions $ {\bf h}_1, \dots, {\bf h}_\ell $ of $ E $ to be complete, i.e. such that the product of their stabilizers $ S({\bf h}_1) S({\bf h}_2) \dots S({\bf h}_\ell) $ is equal to the whole symmetric group $ \frak S(E) $ on $ E $ . In particular, what about completeness of the sequence $ \bf h,\delta(\bf h),\dots,\delta^{\ell-1}(\bf h) $ , given a partition $ \bf h $ of $ E $ and a permutation $ \delta $ of $ E $ ?

Conjecture (Beneš) Let $ \bf u $ be a uniform partition of $ E $ and $ \varphi $ be a permutation of $ E $ such that $ \bf u\wedge\varphi(\bf u)=\bf 0 $ . Suppose that the set $ \big(\varphi S({\bf u})\big)^{n} $ is transitive, for some integer $ n\ge2 $ . Then $$ \frak S(E) = \big(\varphi S({\bf u})\big)^{2n-1}. $$

# Source literature

- *[B75] V.E. Beneš, Proving the rearrangeability of connecting networks by group calculation, Bell Syst. Tech. J. 54 (1975), 421-434.

# Progress

- This conjecture was essentially proposed by Václav E. Beneš in 1975 [B75] and bears his name. It remains open for all $ n\ge3 $ .

A partition of a set is uniform if all its blocks have the same size. Given a subset $ P $ of a multiplicative group and a positive integer $ m $ , by $ P^m $ we mean the product $ PP\dots P $ ( $ m $ times). A set $ T\subseteq\frak S(E) $ is transitive if for every $ x,y\in E $ there exists a permutation $ \tau\in T $ such that $ \tau(x)=y $ . The infinum of two partitions $ \bf a $ and $ \bf b $ of $ E $ is the partition of $ E $ defined by

$$ : \qquad\qquad\qquad {\bf a\wedge b} := \big\{\, a\cap b\ne\varnothing \ | \ a\in{\bf a} \ \&\ b\in{\bf b} \,\big\}. $$

The partition $ \bf 0 $ of $ E $ is defined by $ {\bf 0}:={\bf 0}_E:=\big\{\{x\} \ | \ x\in E \big\} $ . So the condition $ {\bf h}\wedge\delta({\bf h})={\bf 0} $ is equivalent to saying that for every pair of blocks $ a,b\in{\bf h} $ , the intersection $ a\cap\delta(b) $ consists of at most one element.

Observe that the decomposition $ \frak S(E) = \big(\delta S({\bf h})\big)^{\ell} $ is equivalent to completeness of the sequence $ {\bf h},\delta({\bf h}),\dots,\delta^{\ell-1}({\bf h}) $ due to the obvious identity $ \delta S({\bf h}) \delta^{-1} = S(\delta{\bf h}) $ . Thus Problem ( $ \star $ ) is indeed underlying for Beneš conjecture.

Problem ( $ \star $ ) is a special case of a broader fundamental problem of description of product of stabilizers on a finite set. The latter problem, which I believe is combinatorial by nature, is of great interest in switching network study. However, despite many years of extensive research on its various cases in the context of switching networks, this fascinating problem remains unsolved in all but a very few interesting instances. Very little is understood about such products beyond what is obvious. In particular, it is unclear how to efficiently compute their cardinalities. Even for some rather simple sequences of partitions, the product of their stabilizers is surprisingly difficult to describe. Beneš conjecture, if proven (even under some additional assumptions on $ E,{\bf u},\varphi $ ), would provide a very useful and easy-to-check sufficient condition for completeness of the sequences $ {\bf u},\varphi({\bf u}),\dots,\varphi^{\ell-1}({\bf u}) $ that are of particular interest.

Another important and interesting problem related to ( $ \star $ ) is to find an efficient polynomial-time (in $ |E| $ ) factorization algorithm for the identity $ \frak S(E) = S({\bf h}_1) S({\bf h}_2) \dots S({\bf h}_\ell) $ . Given an identity $ A = A_1A_2\dots A_\ell $ , where all $ A_i $ are subsets of a multiplicative group, a factorization algorithm finds for every $ a\in A $ an $ \ell $ -tuple $ (a_1,\dots,a_\ell)\in A_1\times \dots \times A_\ell $ such that $ a = a_1a_2\dots a_\ell $ .

Beneš conjecture is mainly famous for its central case, Shuffle-Exchange (SE) conjecture, stating essentially that $ \frak S(\tilde X) = \big(\sigma S({\bf g})\big)^{2n-1} $ , where $ (\tilde X,{\bf g},\sigma) $ is an instance of $ (E,{\bf u},\varphi) $ defined, given arbitrary integer parameters $ k,n\ge2 $ , as follows:

$ \bullet $ $ \tilde X $ is the set of all words of length $ n $ over a $ k $ -letter alphabet $ X $ .

$ \bullet $ $ \bf g $ is the $ k^{n-1} $ -partition of $ \tilde X $ formed by the equivalence relation $ \sim $ on $ \tilde X $ defined by

$ :\qquad\qquad x_1\dots x_{n} \sim y_1\dots y_{n} : \Leftrightarrow x_1\dots x_{n-1}=y_1\dots y_{n-1} $ .

$ \bullet $ $ \sigma $ is the shuffle permutation of $ \tilde X $ defined by $ \sigma(x_1 x_2 \dots x_{n}) := x_2 \dots x_{n} x_1 $ .

Whereas SE conjecture, especially its case $ k=2 $ , has received enormous attention in the study of switching networks with relatively little progress, the general case of Beneš conjecture, despite importance of Problem ( $ \star $ ) in that area, has virtually generated no literature and had no progress. While I strongly believe in the validity of SE conjecture, I am not so sure about the general case of Beneš conjecture and even do not rule out that it could be disproved by a low-scale counterexample. On the other hand, I cannot rule out that Beneš conjecture (possibly under some mild additional assumptions on $ E,{\bf u},\varphi $ ) may be reduced to SE conjecture.

It is easy to see that the case $ n=2 $ of Beneš conjecture coincides with that of SE conjecture. The latter case is well known to be valid (discussed here).

Unlike completeness of a sequence of partitions of $ E $ , the condition of transitivity of the product of their stabilizers is very easy to check. In particular, transitivity of the set $ \big(\delta S({\bf h})\big)^{n} $ with $ n\ge2 $ is equivalent to the following assertion:

$$ :\qquad\qquad \forall\,h_1,h_n\in{\bf h} \ \exists\,h_2,\dots,h_{n-1}\in{\bf h} \ \forall\, i\in[n-1]: h_i\cap \delta(h_{i+1}) \ne \varnothing. $$

Beneš conjecture (as well as its underlying Problem ( $ \star $ ) and a broader problem of description of product of stabilizers on a finite set) admits a nice equivalent graph-theoretic form.

Counterexamples

In what follows we present 3 counterexamples showing that certain stronger versions of Beneš conjecture are false.

Counterexample 1. The condition $ {\bf u}\wedge\varphi({\bf u})={\bf 0} $ is necessary for Beneš conjecture. This can be shown by the following simple counterexample:

$$ :\qquad\qquad E := \{1,2,3,4,5,6\}, \ {\bf u} := \big\{\{1,2,3\}, \{4,5,6\}\big\}, \text{ and } \varphi:= (3,4). $$

Indeed, $ {\bf u}\wedge\varphi({\bf u}) \ne {\bf 0} $ as $ \{1,2,3\}\cap\varphi\{1,2,3\} = \{1,2\} $ . Also, the set $ \big(\varphi S({\bf u})\big)^{2} $ is obviously transitive. However, it can be easily seen that any permutation $ \alpha $ of $ E $ satisfying $ \alpha \{1,2,3\} = \{4,5,6\} $ does not belong to $ S({\bf u})\varphi S({\bf u})\varphi S({\bf u}) $ . Thus, $ \frak S(E) \ne \big(\varphi S({\bf u})\big)^{3} $ . In fact, the condition $ {\bf u}\wedge\varphi({\bf u})={\bf 0} $ is missing in the original statement [B75] of Beneš conjecture (however, such condition is commonly (but not always) assumed in the context of switching networks).

Counterexample 2. Beneš conjecture is not directly generalizable to the products of stibilizers of the form $ P:=S({\bf u})\varphi_1 S({\bf u})\dots\varphi_{n-1} S({\bf u}) $ . More precisely, transitivity of $ P $ does not always imply $ \frak S(E) = P^2 $ , where $ {\bf u} $ is a uniform partition of $ E $ and all $ \varphi_i $ are permutations of $ E $ such that $ {\bf u}\wedge\varphi_i({\bf u})={\bf 0} $ (while Beneš conjecture states that this implication is always true as long as $ \varphi_1=\dots=\varphi_{n-1} $ ). For that I constructed the following counterexample:

$$ :\qquad\qquad E := \{1,2,\dots,12\}, \ {\bf u} := \big\{\{1,2\}, \{3,4\},\dots,\{11,12\}\big\}, \ \varphi_1:= (2,3)(6,7)(10,11) \text{ and } \varphi_2:= (2,7)(4,9)(6,11). $$

Indeed, it is obvious that both permutations $ \varphi_1, \varphi_2 $ are satisfying $ {\bf u}\wedge\varphi_i({\bf u})={\bf 0} $ and the set $ Q:=S({\bf u})\varphi_1 S({\bf u})\varphi_2 S({\bf u})\varphi_1S({\bf u}) $ is transitive. However, $ \frak S(E) \ne Q^2 $ as, in particular, it can be easily seen that any permutation $ \alpha $ of $ E $ satisfying $ \alpha \{1,2,3,4\} = \{5,6,7,8\} $ does not belong to $ Q^2 $ .

Counterexample 3. In the same paper [B75], Beneš also proposed the following

Conjecture ( $ \diamond $ ) Let $ \bf u $ be a uniform partition of $ E $ and $ \varphi $ be a permutation of $ E $ such that $ \bf u\wedge\varphi(\bf u)=\bf 0 $ . Suppose that $ n\ge2 $ is the smallest integer such that the set $ \big(\varphi S({\bf u})\big)^{n} $ is transitive. Then $ \frak S(E) \ne \big(\varphi S({\bf u})\big)^{2n-2} $ .

In other words, this conjecture together with Beneš one, asserts that if $ n\ge2 $ is the smallest integer such that $ \big(\varphi S({\bf u})\big)^{n} $ is transitive, then $ 2n-1 $ is the the smallest integer $ \ell $ such that $ \frak S(E) = \big(\varphi S({\bf u})\big)^{\ell} $ . However, Conjecture ( $ \diamond $ ) turned out to be generally false as I found the following counterexample for it:

$$ :\qquad\qquad E := \{1,2,\dots,8\}, \ {\bf u} := \big\{\{1,2\}, \{3,4\}, \{5,6\}, \{7,8\}\big\}, \text{ and } \varphi:= (2,3)(4,5,6,7). $$

Indeed, it is easy to verify that $ {\bf u}\wedge\varphi({\bf u})={\bf 0} $ and the set $ \big(\varphi S({\bf u})\big)^{4} $ is transitive while $ \big(\varphi S({\bf u})\big)^{3} $ is not as, in particular, $ \{4,7\} \cap \big(\varphi S({\bf u})\big)^{3}\{1,2\} =\varnothing $ . However, a brute force verification confirmed that $ \frak S(E) = \big(\varphi S({\bf u})\big)^{6} $ .
