---
id: opg-waring_rank_of_determinant
title: Waring rank of determinant
status: open
difficulty: research
domains:
- Algebra
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/waring_rank_of_determinant
---

# Statement

Question What is the Waring rank of the determinant of a $ d \times d $ generic matrix?

For simplicity say we work over the complex numbers. The $ d \times d $ generic matrix is the matrix with entries $ x_{i,j} $ for $ 1 \leq i,j \leq d $ . Its determinant is a homogeneous form of degree $ d $ , in $ d^2 $ variables. If $ F $ is a homogeneous form of degree $ d $ , a power sum expression for $ F $ is an expression of the form $ F = \ell_1^d+\dotsb+\ell_r^d $ , the $ \ell_i $ (homogeneous) linear forms. The Waring rank of $ F $ is the least number of terms $ r $ in any power sum expression for $ F $ . For example, the expression $ xy = \frac{1}{4}(x+y)^2 - \frac{1}{4}(x-y)^2 $ means that $ xy $ has Waring rank $ 2 $ (it can't be less than $ 2 $ , as $ xy \neq \ell_1^2 $ ).

The $ 2 \times 2 $ generic determinant $ x_{1,1}x_{2,2}-x_{1,2}x_{2,1} $ (or $ ad-bc $ ) has Waring rank $ 4 $ . The Waring rank of the $ 3 \times 3 $ generic determinant is at least $ 14 $ and no more than $ 20 $ , see for instance Lower bound for ranks of invariant forms, Example 4.1. The Waring rank of the permanent is also of interest. The comparison between the determinant and permanent is potentially relevant to Valiant's "VP versus VNP" problem.

# Source literature


# Progress

- Status: open.
