---
id: opg-length_of_surreal_product
title: Length of surreal product
status: open
difficulty: graduate
domains:
- Combinatorics
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/length_of_surreal_product
---

# Statement

Conjecture Every surreal number has a unique sign expansion, i.e. function $ f: o\rightarrow \{-, +\} $ , where $ o $ is some ordinal. This $ o $ is the length of given sign expansion and also the birthday of the corresponding surreal number. Let us denote this length of $ s $ as $ \ell(s) $ .

It is easy to prove that

$$ \ell(s+t) \leq \ell(s)+\ell(t) $$

What about

$$ \ell(s\times t) \leq \ell(s)\times\ell(t) $$

?

# Source literature

- *[Gon86] Harry Gonshor, An Introduction to the Theory of Surreal Numbers, Cambridge University Press, Cambridge, 1986.

# Progress

- This is strongly conjectured to be true by Gonshor in [Gon86]. There is an easy way to prove that

$$ \ell(s\times t) \leq 3^{\ell(s)+\ell(t)} $$
