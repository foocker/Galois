---
id: opg-the_robustness_of_the_tensor_product_0
title: The robustness of the tensor product
status: open
difficulty: frontier
domains:
- Theoretical Comp. Sci.
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/the_robustness_of_the_tensor_product_0
---

# Statement

Problem Given two codes $ R,C $ , their Tensor Product $ R \otimes C $ is the code that consists of the matrices whose rows are codewords of $ R $ and whose columns are codewords of $ C $ . The product $ R \otimes C $ is said to be robust if whenever a matrix $ M $ is far from $ R \otimes C $ , the rows (columns) of $ M $ are far from $ R $ ( $ C $ , respectively).

The problem is to give a characterization of the pairs $ R,C $ whose tensor product is robust.

# Source literature

- *[BS] Eli Ben-Sasson, Madhu Sudan, Robust locally testable codes and products of codes, APPROX-RANDOM 2004, pp. 286-297 (See ECCC TR04-046).
- [CR] D. Coppersmith and A. Rudra, On the robust testability of tensor products of codes, ECCC TR07-061.
- [DSW] Irit Dinur, Madhu Sudan and Avi Wigderson, Robust local testability of tensor products of LDPC codes, APPROX-RANDOM 2006, pp. 304-315 (See ECCC TR06-118).
- [GM] Oded Goldreich, Or Meir, The Tensor Product of Two Good Codes Is Not Necessarily Robustly Testable, ECCC TR07-062.
- [M] Or Meir, On the Rectangle Method in proofs of Robustness of Tensor Products, ECCC TR07-061.
- [V] Paul Valiant, The Tensor Product of Two Codes Is Not Necessarily Robustly Testable, APPROX-RANDOM 2005, pp. 472-481.

# Progress

- The question is studied in the context of Locally Testable Codes.
