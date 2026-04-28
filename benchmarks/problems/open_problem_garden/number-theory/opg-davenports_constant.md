---
id: opg-davenports_constant
title: Davenport's constant
status: open
difficulty: frontier
domains:
- Number Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/davenports_constant
---

# Statement

For a finite (additive) abelian group $ G $ , the Davenport constant of $ G $ , denoted $ s(G) $ , is the smallest integer $ t $ so that every sequence of elements of $ G $ with length $ \ge t $ has a nontrivial subsequence which sums to zero.

Conjecture $ s( {\mathbb Z}_n^d) = d(n-1) + 1 $

# Source literature


# Progress

- Davenport's original motivation for introducing the constant $ s(G) $ concerned prime ideal decompositions in algebraic number fields. However, determining this constant even for some very restricted families of groups has proved to be an interesting combinatorial problem. Indeed, the highlighted conjecture is considered to be one of the most important unsolved problems concerning finite abelian groups. I (M. DeVos) have reguarded this conjecture as folklore, but I await correction here.

It is easy to see that $ s( {\mathbb Z}_{n_1} \times {\mathbb Z}_{n_2} \ldots \times {\mathbb Z}_{n_{\ell}} ) \ge 1 + \sum_{i=1}^\ell (n_i - 1) $ because the sequence constructed by taking $ n_i - 1 $ copies of the element with a $ 1 $ in the $ i^{th} $ position and $ 0 $ 's elsewhere has no nontrivial subsequence which sums to zero. There is also an easy upper bound of $ s(G) \le |G| $ . To see this, assume $ |G| = n $ , let $ a_1,\ldots,a_n $ be a sequence of elements from $ G $ , and consider the terms $ a_1, a_1 + a_2, \ldots, a_1 + a_2 + \ldots a_n $ . If these terms are distinct, then one must be 0 (giving us a zero sum subseqence). Otherwise two of them must be equal, so we have $ a_1 + \ldots a_i = a_1 + \ldots a_j $ for some $ i < j $ , but then $ a_{i+1} + a_{i+1} \ldots + a_j = 0 $ .

For cyclic groups, our trivial upper and lower bound match, so we have $ s({\mathbb Z}_n) = n $ . However, the situation gets much more difficult as soon as we go any further. The following theorem summarizes two classic results of Olson which remain state of the art.

Theorem (Olson)

\item $ s( {\mathbb Z}_a \times {\mathbb Z}_b ) = a + b - 1 $ if $ a|b $ . \item if $ p $ is prime, $ s( {\mathbb Z}_{p^{d_1}} \times {\mathbb Z}_{p^{d_2}} \ldots \times {\mathbb Z}_{p^{d_{\ell}}}) = 1 + \sum_{i=1}^{\ell} (p^{d_i} - 1) $

Although there does not even exist a conjecture as to the value of $ s(G) $ for a general $ G $ , recently a number of authors have proved theorems which give upper bounds on $ s(G) $ under some structural assumptions. For instance, Caro has proved that $ s(G) \le \frac{|G|}{3} + 1 $ for every $ G $ which is not cyclic and not of the form $ {\mathbb Z}_2 \times {\mathbb Z}_m $ .
