---
id: opg-a_sequence_defined_on_multisets
title: Sequence defined on multisets
status: open
difficulty: research
domains:
- Combinatorics
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/a_sequence_defined_on_multisets
---

# Statement

Conjecture Define a $ 2 \times n $ array of positive integers where the first row consists of some distinct positive integers arranged in increasing order, and the second row consists of any positive integers in any order. Create a new array where the first row consists of all the integers that occur in the first array, arranged in increasing order, and the second row consists of their multiplicities. Repeat the process. For example, starting with the array $ [1; 1] $ , the sequence is: $ [1; 1] $ -> $ [1; 2] $ -> $ [1, 2; 1, 1] $ -> $ [1, 2; 3, 1] $ -> $ [1, 2, 3; 2, 1, 1] $ -> $ [1, 2, 3; 3, 2, 1] $ -> $ [1, 2, 3; 2, 2, 2] $ -> $ [1, 2, 3; 1, 4, 1] $ -> $ [1, 2, 3, 4; 3, 1, 1, 1] $ -> $ [1, 2, 3, 4; 4, 1, 2, 1] $ -> $ [1, 2, 3, 4; 3, 2, 1, 2] $ -> $ [1, 2, 3, 4; 2, 3, 2, 1] $ , and we now have a fixed point (loop of one array).

The process always results in a loop of 1, 2, or 3 arrays.

# Source literature

- * Erickson, Martin J., "Introduction to Combinatorics," Wiley, 1996.

# Progress

- Status: open.
