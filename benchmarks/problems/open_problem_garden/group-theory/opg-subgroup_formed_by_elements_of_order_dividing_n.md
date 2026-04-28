---
id: opg-subgroup_formed_by_elements_of_order_dividing_n
title: Subgroup formed by elements of order dividing n
status: open
difficulty: research
domains:
- Group Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/subgroup_formed_by_elements_of_order_dividing_n
---

# Statement

Conjecture

Suppose $ G $ is a finite group, and $ n $ is a positive integer dividing $ |G| $ . Suppose that $ G $ has exactly $ n $ solutions to $ x^{n} = 1 $ . Does it follow that these solutions form a subgroup of $ G $ ?

# Source literature

- Marshall Hall Jr., Theory of Groups, Macmillan (1959)
- Walter Feit, On a Conjecture of Frobenius, Proceedings of the American Mathematical Society, Vol.7, No. 2 (Apr. 1956), 177-187.

# Progress

- If these solutions form a subgroup, they form a characteristic (and therefore normal) subgroup of $ G $ . This easily follows from the First Sylow Theorem if $ n $ is the highest power of a prime $ p $ dividing $ |G| $ .

In a 1980 article, Feit commented that the case where $ (n, \frac{|G|}{n}) = 1 $ (i.e., $ n $ 'exactly divides' $ |G| $ ) had been reduced to considering $ G $ simple. Thus it should be resolvable using the classification of finite simple groups.

It is known that if $ n $ divides $ |G| $ , the number of solutions of $ x^{n} = 1 $ in $ G $ is a multiple of $ n $ . A generalization of this theorem, replacing $ x^{n} = 1 $ by $ x^{n} \in C $ for a conjugacy class $ C $ of $ G $ , can be found in Marshall Hall Jr.'s book.

Observation This conjecture implies the (known) theorem of Frobenius:

Theorem If $ G $ is a finite transitive permutation group in which only the identity has more than one fixed point, then the derangements of $ G $ , together with the identity, form a subgroup of $ G $ .
