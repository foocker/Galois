---
id: opg-p_vs_bpp
title: P vs. BPP
status: open
difficulty: frontier
domains:
- Theoretical Comp. Sci.
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/p_vs_bpp
---

# Statement

Conjecture Can all problems that can be computed by a probabilistic Turing machine (with error probability < 1/3) in polynomial time be solved by a deterministic Turing machine in polynomial time? That is, does P = BPP?

# Source literature

- Andrea E. F. Clement, Jose D. P. Rolim, and Luca Trevisan, Recent Advances Towards Proving P = BPP (1998).
- Oded Goldreich, In a World of BPP=P, Studies in complexity and cryptography, Lecture Notes in Comput. Sci., 6650, Springer, Heidelberg, 2011, pp. 191-–232. See also the presentation.
- Russell Impagliazzo and Avi Wigderson, P=BPP unless E has sub-exponential circuits: derandomizing the XOR Lemma, following STOC '97.
- Ryan Williams, Towards NEXP versus BPP?, Computer Science---Theory and Applications, Lecture Notes in Computer Science Volume 7913 (2013), pp. 174--182.

# Progress

- BPP has long been considered tractable. Many problems in BPP have been derandomized, showing that they are in fact in P. Is this true for all problems in BPP? All that is known at the moment is $ P\subseteq BPP\subseteq NEXP. $

This problem has been shown to have deep connections to circuit complexity (see for example Impagliazzo & Wigderson). It is folklore that the existence of appropriate pseudorandom generators suffices to give P = BPP; Goldreich shows that their existence also follows from P = BPP.
