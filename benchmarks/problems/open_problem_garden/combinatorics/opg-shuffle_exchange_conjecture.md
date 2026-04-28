---
id: opg-shuffle_exchange_conjecture
title: Shuffle-Exchange Conjecture
status: open
difficulty: frontier
domains:
- Combinatorics
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/shuffle_exchange_conjecture
---

# Statement

Given integers $ k,n\ge2 $ , let $ d(k,n) $ be the smallest integer $ d\ge2 $ such that the symmetric group $ \frak S $ on the set of all words of length $ n $ over a $ k $ -letter alphabet can be generated as $ \frak S = (\sigma \frak G)^d:=\sigma\frak G \sigma\frak G \dots \sigma\frak G $ ( $ d $ times), where $ \sigma\in \frak S $ is the shuffle permutation defined by $ \sigma(x_1 x_2 \dots x_{n}) = x_2 \dots x_{n} x_1 $ , and $ \frak G $ is the exchange group consisting of all permutations in $ \frak S $ preserving the first $ n-1 $ letters in the words.

Problem (SE) Evaluate $ d(k,n) $ .

Conjecture (SE) $ d(k,n)=2n-1 $ , for all $ k,n\ge2 $ .

# Source literature


# Progress

- This beautiful and difficult problem arises in switching networks theory and has important applications in parallel processing, sorting networks, card shuffling, etc. In this area it is perhaps the most famous open question which is at the center of the quest to understand the phenonemon of network rearrangeability. Both the problem and conjecture are referred to as Shuffle-Exchange (SE) ones. The case $ k=2 $ of SE problem (but not the conjecture) can be traced back to the work of Stone [S71], where he showed that $ d(2,n)\le n^2 $ . The upper bound $ d(k,n)\le 2n-1 $ is the central case of Beneš conjecture [B75], while the lower bound $ d(k,n)\ge 2n-1 $ can be easily seen (it is also a special case of the stronger version [B75] of Beneš conjecture, which turned out to be generally false). Since 1975 SE conjecture, especially its case $ k=2 $ , has received a lot of attention, mostly in the context of switching networks, with rather modest results.

Note that $ d(k,n)\le m $ is equivalent to $ \frak S = (\sigma \frak G)^m $ , for any integer $ m\ge2 $ . Furthermore, it is easy to see that the latter decomposition is equivalent to $ \frak S = \frak G_1 \frak G_2\dots \frak G_{m} $ , where $ \frak G_i:=\sigma^{i} \frak G \sigma^{-i} $ is the subgroup of $ \frak S $ consisting of all permutations which may only change the letters on the position $ i-1\ (\text{mod } n) + 1 $ in the words.

Also, the case $ n=2 $ of SE conjecture can be reformulated as the following

Theorem ( $ \star $ ) Every permutation of entries of a square matrix can be obtained in 3 steps as follows: first by permuting entries in the columns, then - in the rows, and then - in the columns again. Moreover, some permutations cannot be obtained in less than 3 of such steps.

(The parameter $ k $ in the case $ n=2 $ of SE conjecture corresponds to the size $ k\times k $ of a matrix in the theorem.) Moreover, the general case of SE conjecture can be reformulated as a straightforward generalization of Theorem ( $ \star $ ) to the $ n $ -dimensional cubic matrices (of size $ k\times\dots\times k $ ) stating that every permutation of entries of such a matrix can be obtained in $ 2n-1 $ steps in a similar way, and this number is generally a precise lower bound.

Theorem ( $ \star $ ) holds as being easily equivalent to the special case of the following classical result when each part of the multigraph has size $ k $ :

Theorem (König) A $ k $ -regular bipartite multigraph is $ k $ -edge-colorable.

The function $ d(k,n) $ admits 3 main interpretations (that are not immediately equivalent), "group-theoretic" (presented in the beginning), "combinatorial" (below), and "graph-theoretic", each of which provides its own framework for SE problem and suggests its own interesting natural generalizations and extensions. Accordingly, there are 3 equivalent forms of SE problem/conjecture. Although the group-theoretic interpretation of $ d(k,n) $ is the shortest and most elegant among the three, it seems the least natural when it comes to proving the known results and studying SE problem more deeply. I believe that SE problem is very deep and combinatorial by nature. I also strongly believe in the validity of SE conjecture.

2. Combinatorial form of SE problem/conjecture

Given a pure abstract simplicial complex $ \Delta $ of rank $ n\ge2 $ and a positive integer $ \ell $ , an $ \ell $ -transition is a map that assigns to evey pair of ordered facets, $ x_1,\dots,x_{n} $ and $ y_1,\dots,y_{n} $ , a sequence of vertices $ z_1,\dots,z_{\ell} $ such that every $ n $ -segment of the sequence $ x_1,\dots,x_{n},z_1,\dots,z_{\ell}, y_1,\dots,y_{n} $ forms a facet. Let $ \text{tr}(\Delta) $ be the smallest $ \ell $ , or $ \infty $ if none exists, for which there exists an $ \ell $ -transition. Note that $ \text{tr}(\Delta)\le \ell $ is equivalent to the existence of $ \ell $ -transition for $ \Delta $ , for any $ \ell\ge 1 $ .

Given integers $ k,n\ge2 $ , let $ \Delta_{k,n} $ be the pure abstract simplicial complex of rank $ n $ whose vertex set is the set $ V_{k,n} $ of all uniform $ k $ -partitions (i.e., ones consisting of $ k $ equal-sized blocks) of a $ k^n $ -set, and whose facets are all $ n $ -subsets of $ V_{k,n} $ with zero infinum. Using normal reasoning, it is not hard to show [L04] the following

Theorem $ d(k,n) = \text{tr}(\Delta_{k,n})+n $ .

Thus, the combinatorial forms of SE problem and conjecture can be formulated as to find $ \text{tr}(\Delta_{k,n}) $ and that $ \text{tr}(\Delta_{k,n})=n-1 $ , respectively.

The infinum (or meet) of two partitions $ \mathbf{a} $ and $ \mathbf{b} $ of a set $ E $ is the partition of $ E $ defined by $$ \mathbf{a\wedge b} := \big\{\, a\cap b\ne\varnothing \ | \ a\in\mathbf{a} \ \&\ b\in\mathbf{b} \,\big\}. $$ Note that together with the operation $ \wedge $ , the collection of all partitions of $ E $ forms a semilattice (i.e., a commutative and idempotent semigroup) with the identity and zero being the partitions $ \mathbf{1}_E:=\{E\} $ and $ \mathbf{0}_E:=\big\{\{x\} \ | \ x\in E \big\} $ , respectively.

Observe that the complex $ \Delta_{k,n} $ is non-matroidal for all $ (k,n)\ne (2,2) $ .

3. Constructive version of SE problem/conjecture

Application-wise it is important not only to establish a certain decomposition $ \frak S = (\sigma \frak G)^m $ or, equivalently, rearrangeability of the graph $ (\text{SE}(k,n))^{m-1} $ or, equivalently, the existence of an $ (m-n) $ -transition for the complex $ \Delta_{k,n} $ , but also to find a corresponding efficient factorization/routing/transition algorithm.

Given an identity $ A = A_1A_2\dots A_m $ , where all $ A_i $ are subsets of a multiplicative group, a factorization algorithm finds for every $ a\in A $ an $ m $ -tuple $ (a_1,\dots,a_m)\in A_1\times \dots \times A_m $ such that $ a = a_1a_2\dots a_m $ . Given a rearrangeable graph $ (\text{SE}(k,n))^{m-1} $ , a routing algorithm takes a mask of the graph as input and returns a corresponding routing. Given a pure simplicial complex $ \Delta $ with $ \text{tr}(\Delta)\le r $ , an $ r $ -transition algorithm realizes an $ r $ -transition for $ \Delta $ . It is not hard to prove

Theorem Any factorization algorithm for $ \frak S = (\sigma \frak G)^m $ translates into a routing algorithm for $ (\text{SE}(k,n))^{m-1} $ and into an $ (m-n) $ -transition algorithm for $ \Delta_{k,n} $ of the same complexity, and vise versa. Consequently, $ D^{*}(k,n) = R^{*}(k,n) = T^{*}(k,n) $ .

Here $ D^*(k,n) $ , $ R^*(k,n) $ , and $ T^{*}(k,n) $ are the sets of all $ m\ge 2 $ , respectively, for which there exists an efficient polynomial-time (in $ k^n $ ) factorization/routing/transition algorithm mentioned in the above theorem (we will also write $ A \buildrel{*}\over= A_1A_2\dots A_m $ to indicate the existence of such a factorization algorithm for $ A = A_1A_2\dots A_m $ , where each $ A_i\subseteq \frak S $ ). Clearly, $$ d^*(k,n)\ge d(k,n)= r(k,n)=\text{tr}(\Delta_{k,n})+n, $$ where $ d^*(k,n):= \min D^*(k,n) $ with the usual convention $ \min\varnothing :=\infty $ , and $ r(k,n) $ is defined here.

It is easy to see that $ d\in D^*(k,n) $ implies $ [d,\infty)\subseteq D^*(k,n) $ (equivalently, the same is true for $ R^*(k,n) $ and $ T^{*}(k,n) $ ). Consequently, $ d^*(k,n)\le m $ is equivalent to $ \frak S \buildrel{*}\over= (\sigma \frak G)^m $ .

Problem (CSE) Evaluate $ d^*(k,n) $ and specify the corresponding factorization/routing/transition algorithm for the upper bound.

Conjecture (CSE) $ d^*(k,n)=2n-1 $ .

Both the problem and conjecture are referred here to as Constructive Shuffle-Exchange (CSE) ones. The conjecture was proposed in [L04]. Clearly, CSE conjecture implies SE one as $ 2n-1\le d(k,n)\le d^*(k,n) $ .

4. Main results

So far SE/CSE conjecture has been only settled in the following 3 cases: $ n=2 $ , $ (k,n)=(2,3) $ , and $ (k,n)=(2,4) $ . That is, the following 3 identities holds:

$$ (1)\ d(k,2) = d^*(k,2) = 3,\ \ (2)\ d(2,3) = d^*(2,3) = 5,\ \ (3)\ d(2,4) = d^*(2,4) = 7. $$

Also, there are 2 the following major results on SE/CSE problem:

(4) $ d(k,n)\ge 2n-1 $ .

(5) $ d^{(*)}(k,n)\le d^{(*)}(k,r)+3(n-r) $ , for all $ n > r\ge2 $ .

The lower bound (4) follows immediately from the obvious observation that $ \text{tr}(\Delta) \ge \dim(\Delta) $ , for any pure complex $ \Delta $ .

Note that (4) reduces SE (CSE) conjecture to $ d^{(*)}(k,n)\le 2n-1 $ which is equivalent to $ \frak S \buildrel{(*)}\over= (\sigma \frak G)^{2n-1} $ . In fact, the main reason why SE/CSE conjecture is widely believable, apart from results (1-4), is a close similarity between the latter decomposition and the following well known result [B65, L04] (that is not hard to derive from the constructive version of the König's theorem):

Theorem (Beneš) $ \frak S \buildrel{*}\over= (\frak G\sigma^{-1})^{n-1}\frak G(\sigma \frak G)^{n-1} $ .

Combining (1) and (3) with (5) yields respectively the following 2 best known upper bounds (in addition to (2)) for both $ d(k,n) $ and $ d^*(k,n) $ :

$ (6)\quad d(k,n)\le d^*(k,n)\le 3n-3 $ , for all $ k\ge3 $ and $ n\ge2 $

$ (7)\quad d(2,n)\le d^*(2,n)\le 3n-5 $ , for all $ n\ge4 $ .

As it was mentioned earlier, the case $ n=2 $ of SE conjecture is easily equivalent to the following case of the Konig's theorem: a $ k $ -regular bipartite multigraph $ B $ with $ k $ -vertex parts is $ k $ -edge-colorable. Moreover, any $ k $ -edge-coloring algorithm for the graph $ B $ easily translates into a factorization/routing/1-transition algorithm of the same complexity for $ \frak S = (\sigma \frak G)^3 $ (at $ n=2 $ ) or the graph $ (\text{SE}(k,2))^{2} $ or the complex $ \Delta_{k,2} $ , respectively, and vise versa. Consequently, as there are many efficient polynomial-time (in $ k^2 $ ) $ k $ -edge-coloring algorithms well known for the graph $ B $ , the case $ n=2 $ of CSE conjecture also holds.

There are at least 6 alternative proofs proposed for the case $ (k,n)=(2,3) $ of CSE conjecture. Although they may look quite different, each proof is essentially based on either of 3 similar short and elegant algorithms which we refer to as A1 [RV87, LT89, L04], A2 [ND00, L04] and A3 [KR91]. Each algorithm is based on a 2-edge-coloring algorithm for a 2-regular bipartite multigraph with 4-vertex parts. Namely, A1 uses 2, A2 uses at most 2, and A3 uses 1 application(s) of such an algorithm. Each algorithm Ai deals with 2 cases in which the procedure is especially simple. The algorithms A1 and A2 are very efficient (with A2 being slightly faster than A1), while A3 is not so (contrary to what is claimed in [KR91]) as it relies on an exhausting search to determine the case for each input permutation. However, A3 has some theoretical advantage over A1 and A2 as its 2 cases partition the symmetric group $ S_8 $ into 2 classes that do not depend on a realization of the algorithm. In [L04], both algorithms A1 and A2 are explicitly described as 2-transition algorithms for the complex $ \Delta_{2,3} $ , and the corresponding 2 proofs for the statement $ \text{\rm tr}(\Delta_{2,3})=2 $ are particularly transparent. Moreover, the latter statement, the algorithms and the proofs are straightforwardly generalized [L05] to a wide class of 2-dimensional pure abstract simplicial complexes.

A brute force verification for the case $ (k,n)=(2,4) $ of SE conjecture was first reported in [R95]. The first theoretical proof for such case of CSE conjecture was proposed (in graph-theoretic terms) in [ND00]. Although the ideas behind the underlying algorithm for this proof are simple, the algorithm deals with a huge and intricate tree of cases and is substantially more complicated (and not so elegant) than that of the case $ (k,n)=(2,3) $ . As a result, the proof is very tedious, hard to verify, and leaves little hope for using a similar approach to prove the next case $ (k,n)=(2,5) $ of CSE conjecture. An essentially similar but slightly better organized algorithm and proof for (3) were proposed in [DS08] (with no reference to [ND00]).

The upper bound (5) was first obtained in [VR88] for the case $ k=2 $ and (i) $ d^{(*)}(k,r)=2r-1 $ . In other words, it was shown that (i) at $ k=2 $ implies $ d^{(*)}(2,n)\le 3n-r-1 $ , if $ n > r $ . A much simpler proof of (5) for the case $ r=2,3 $ and (i) appeared in [LT89]. The latter proof was easily extended [ND00] to an arbitrary $ r\ge2 $ . A transparent combinatorial proof in terms of the complex $ \Delta_{k,n} $ for the general case of (5) was proposed in [L04]. This proof (together with its underlying transition algorithm) was generalized [L05] to a wide class of pure abstract simplicial complexes of arbitrary dimensions. Namely, it was shown that, given a complex $ \Delta $ in this class and an integer $ 1\le m<\dim(\Delta) $ ,

$$ :\qquad\qquad \text{tr}(\Delta) \le 2m + \max \big\{ \text{tr}(\Delta/F) \mid F\in\Delta,\ |F|=m \big\} $$

and, moreover, that any $ \ell $ -transition algorithm for the complexes $ \Delta/F $ can be efficiently used to make a $ (2m+\ell) $ -transition algorithm for $ \Delta $ . Note that (5) can be easily obtained as an instance of the latter result. Here $ \Delta/ F $ is the link of a face $ F $ in $ \Delta $ , i.e., a subcomplex of $ \Delta $ defined by

$$ :\qquad\qquad \Delta/ F := \{ A\in \Delta \ | \ A\cap F = \varnothing \ \&\ A\cup F\in\Delta \big\}. $$

It is worth noting that there are many flawed proofs for SE conjecture in the literature. Most notably, in [Ba01] (the general case) and [C03] (the case $ k=2 $ ). The latter proof was first refuted in [BHL06], while the former remains unrefuted in the literature.

Related problems
Shuffle-Exchange Conjecture (graph-theoretic form)
Beneš Conjecture
Beneš Conjecture (graph-theoretic form)

Bibliography

[B65] V.E. Benes, Mathematical theory of connecting networks and telephone traffic, Academic Press, New York, 1965.

*[S71] H.S. Stone, Parallel processing with the perfect shuffle, IEEE Trans. on Computers C-20 (1971), 153-161.

*[B75] V.E. Beneš, Proving the rearrangeability of connecting networks by group calculation, Bell Syst. Tech. J. 54 (1975), 421-434.

[RV87] C.S. Raghavendra, A. Varma, Rearrangeability of 5-stage shuffle/exchange network for N=8, IEEE Trans. on Commun. COM-35 (1987), 808-812.

[VR88] A. Varma, C.S. Raghavendra, Rearrangeability of multistage shuffle/exchange networks, IEEE Trans. on Commun. 36 (1988), 1138-1147.

[LT89] N. Linial, M. Tarsi, Interpolation between bases and the shuffle-exchange networks, European J. of Combinatorics, 10(1) (1989), 29-39.

[KR91] K. Kim, C.S. Raghavendra, A Simple Algorithm to Route Arbitrary Permutations on 8-input 5-stage Shuffle/Exchange Network, Proc. 5th International Parallel Processing Symposium (1991), 398-403.

[R95] C.S. Raghavendra, On the rearrangeability conjecture of $ (2\log_2 N -1) $ -stage shuffle/exchange network, IEEE Computer Society, Tech. Committee on Comp. Arch. Newsletter, Position paper (Winter 1995), 10-12.

[ND00] H.Q. Ngo, D.Z. Du, On the rearrangeability of shuffle-exchange networks, Tech. Report TR00-045, Dept. of Computer Science, Univ. of Minnesota (2000)

[Ba01] R.E. Bashirov, On the rearrangeability of 2s-1 stage networks employing uniform interconnection pattern Calcolo, Springer Verlag, 38(2) (2001), 85-97.

[C03] H. Cam, Rearrangeability of (2n-1)-stage shuffle-exchange networks, SIAM J. on Computing 32(3) (2003), 557-585.

[L04] V. Lioubimov, Decomposition of symmetric group into product of stabilizers and Shuffle-Exchange problem, manuscript (2004).

[L05] V. Lioubimov, Facet transitions in abstract simplicial complexes, manuscript (2005).

[BHL06] X. Bao, F.K. Hwang, Q. Li, Rearrangeability of bit permutation networks, Theoretical Computer Science, 352(1) (2006), 197-214.

[DS08] H. Dai, X. Shen, Rearrangeability of 7-stage 16x16 shuffle-exchange networks, Frontiers of Electrical and Electronic Engineering in China, 3(4) (2008), 440-458.

* indicates original appearance(s) of problem.

add new comment
