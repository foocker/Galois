---
id: opg-perfect_2_error_correcting_codes_over_arbitrary_finite_alphabets
title: Perfect 2-error-correcting codes over arbitrary finite alphabets.
status: open
difficulty: research
domains:
- Combinatorics
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/perfect_2_error_correcting_codes_over_arbitrary_finite_alphabets
---

# Statement

Conjecture Does there exist a nontrivial perfect 2-error-correcting code over any finite alphabet, other than the ternary Golay code?

# Source literature


# Progress

- Very few perfect codes are known to exist over any alphabet. The trivial examples are codes with 1 or 2 codewords, or q-ary (n, M, d) codes with all of the q^n vectors being codewords. Other than this, we have an infinite family of perfect 1-error-correcting Hamming codes, and two unique Golay codes, the binary one which corrects 1 error, the ternary one which corrects 2 errors. Recent research activity has discovered a large number of previously unknown perfect 1-error correcting codes which are not isomorphic to the Hamming codes.

It is well known (see Van Lint) that the answer is negative for codes over alphabets of size equal to a power of a prime number. Further results (see Hong, Best) establish that there are no perfect t-error-correcting codes for any t > 2 over any finite alphabet, which establishes the fact that 2 is the largest number of errors which any new perfect code could possibly correct. Lloyd's theorem plays a key role in ruling out t > 2, but provides less information than needed in the t = 2 case. Establishing the result in the negative would likely require an ad-hoc combinatorial argument, while establishing it in the positive could be done by any clever construction.
