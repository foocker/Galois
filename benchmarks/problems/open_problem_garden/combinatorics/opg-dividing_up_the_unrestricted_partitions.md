---
id: opg-dividing_up_the_unrestricted_partitions
title: Dividing up the unrestricted partitions
status: open
difficulty: research
domains:
- Combinatorics
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/dividing_up_the_unrestricted_partitions
---

# Statement

Begin with the generating function for unrestricted partitions:

(1+x+x^2+...)(1+x^2+x^4+...)(1+x^3+x^6+...)...

Now change some of the plus signs to minus signs. The resulting series will have coefficients congruent, mod 2, to the coefficients of the generating series for unrestricted partitions. I conjecture that the signs may be chosen such that all the coefficients of the series are either 1, -1, or zero.

# Source literature

- Andrews, George E., The Theory of Partitions, Cambridge University Press (1984)

# Progress

- I've been thinking about this problem since about 1970. Emory Starke thought that it was a good problem, but not suitable for the Problems section of the AMM, because it was unsolved. George Andrews and Freeman Dyson also thought that it is a good problem, but neither had any ideas how to solve it.

I've found choices of sign which yield series with coefficients 1, -1, or 0 for all exponents about as high as 110 using computer searches. One thing which mitigates against finding a meaningful solution is that there is no known pattern for the number of unrestricted partitions modulo 2.
