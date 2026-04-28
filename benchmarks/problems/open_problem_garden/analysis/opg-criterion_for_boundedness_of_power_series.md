---
id: opg-criterion_for_boundedness_of_power_series
title: Criterion for boundedness of power series
status: open
difficulty: graduate
domains:
- Analysis
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/criterion_for_boundedness_of_power_series
---

# Statement

Question Give a necessary and sufficient criterion for the sequence $ (a_n) $ so that the power series $ \sum_{n=0}^{\infty} a_n x^n $ is bounded for all $ x \in \mathbb{R} $ .

# Source literature


# Progress

- Consider a power series $ \sum_{n=0}^{\infty} a_n x^n $ that is convergent for all $ x \in {\mathbb R} $ , thus defining a function $ f: {\mathbb R} \to {\mathbb R} $ . Are there criteria to decide whether $ f $ is bounded (which e.g. is the case for the series with $ a_n = (-1)^k/(2k)! $ for $ n = 2k $ and $ a_n = 0 $ for n odd)? Some general remarks:

\item A necessary condition for $ \sum_n a_n x^n $ to be bounded is that $ a_0 $ is the only non-zero $ a_n $ or there are infinitely many non-zero $ a_n $ 's which change sign infinitely many times. \item Changing a finite set of $ a_n $ 's (except $ a_0 $ ) does leave the subspace of bounded power series. \item The subspace of bounded power series is "large" in the sense that it is both a linear subspace (closed under sums and scalar multiples) and an algebra (closed under products). It includes all functions of the form $ a \cos( f(x)) $ , where $ f $ is any entire function $ \mathbb{R} \to \mathbb{R} $ . The question whether the subspace of bounded power series contains only these functions seems to be open.
