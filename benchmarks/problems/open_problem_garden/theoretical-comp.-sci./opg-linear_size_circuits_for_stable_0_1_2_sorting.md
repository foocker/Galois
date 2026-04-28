---
id: opg-linear_size_circuits_for_stable_0_1_2_sorting
title: Linear-size circuits for stable $0,1 < 2$ sorting?
status: open
difficulty: research
domains:
- Theoretical Comp. Sci.
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/linear_size_circuits_for_stable_0_1_2_sorting
---

# Statement

Problem Can $ O(n) $ -size circuits compute the function $ f $ on $ \{0,1,2\}^* $ defined inductively by $ f(\lambda) = \lambda $ , $ f(0x) = 0f(x) $ , $ f(1x) = 1f(x) $ , and $ f(2x) = f(x)2 $ ?

# Source literature


# Progress

- This function moves all 2s in $ x $ flush-right, leaving the sequence of 0s and 1s the same, and represents stable topological sort of the partial order $ 0,1 < 2 $ . It is linear-time computable in any model that supports the operations of a double-ended queue in $ O(1) $ time, including multi-tape Turing machines, but is to me the "easiest" function for which I do not know linear-size circuits. By contrast sorting $ 0 < 1 < 2 $ , called the "Dutch National Flag Problem", has $ O(n) $ -size circuits by counting. It suffices to compute $ f(x) $ when $ |x| $ is a power of $ 2 $ and exactly half the entries are $ 2 $ . For this and more see my Computational Complexity blog item, PDF file here.
