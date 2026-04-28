---
id: opg-the_riemann_hypothesis
title: The Riemann Hypothesis
status: solved
difficulty: frontier
domains:
- Number Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/the_riemann_hypothesis
---

# Statement

The zeroes of the Riemann zeta function that are inside the Critical Strip (i.e. the vertical strip of the complex plane where the real part of the complex variable is in ]0;1[), are actually located on the Critical line ( the vertical line of the complex plane with real part equal to 1/2)

# Source literature

- [R] Bernhard Riemann, "Ueber die Anzahl der Primzahlen unter einer gegebenen Grösse", (1859) Monatsberichte der Berliner Akademie.
- [T] E.C. Titchmarsh, "The theory of the Riemann zeta function", Oxford. Univ Press
- [P] G. Polya, "Bemerkung ueber die Integraldarstellung der Riemannsche zeta-Funktion", Acta Math. 48 (1926), 305-317.
- [B] D. Bump, K.K. Choi, P. Kurlberg, J. Vaaler, "A Local Riemann Hypothesis'', Math. Zeit. 233 (2000) p1-19.
- [H] H. Hamburger, "Ueber die Riemannsche Funktionalgleichung der zeta-Funktion", Math. Zeit. 10 (1921), 240-254.
- [V] A. Karatsuba, Voronin S., "The Riemann Zeta function'', De Gruyter Exposition of Mathematics, Transl. Neil Koeblitz (1975) p212.
- [F] J. Faraut, A. Koranyi, "Function spaces and reproducing kernels on bounded symmetric domains'', J. Funct. An. 88 (1990) p64-89.

# Progress

- The Riemann zeta serie is the function of the complex variable $ s $ defined by $ \zeta(s) = \sum_{n=1}^\infty \frac{1}{n^s} $ . It is defined only for a real part of $ s $ greater than 1. It is an analytic function on this domain, and there exists a unique analytic function defined over the whole complex plane (except at 1) that coincides with zeta when $ Re(s)>1 $ . This function is the analytic continuation of the Riemann zeta serie, and is called the Riemann zeta function, on which is based the Riemann Hypothesis. It was stated by Bernhard Riemann in 1859 and is still open. The zeta function and the Riemann Hypothesis are closely related to number theory and the distribution of prime numbers, as is well described in wikipedia. For that reason this item could also lie under the "Number Theory" category of this website.

A lot of variants and extensions of the Riemann hypothesis have been raised till today. The location on the Critical line of the so-called "non trivial zeroes" of zeta (the ones in the Critical Strip, by opposition to the trivial ones that are negative even integers and are well known) is supposed to be also valid for the analytic continuation of Dirichlet L-series associated to a primitive Dirichlet character $ \chi $ : $ L(s) = \sum_{n=1}^\infty \frac{\chi(n)}{n^s} $ . It is also believed to be valid for Dedekind zeta functions (generalization of zeta related to number fields, that is a finite dimensional extension of the field of rational numbers), also for Hecke L-functions associated to Hecke Grossencharacters (generalization to number fields of the Dirichlet L-functions), for Artin L-functions etc... The list of various generalizations is now long. Today, the largest class of functions that are expected to obey a Riemann Hypothesis are functions in the Selberg Class, even though zeta functions for motives over schemes are also candidates.

There exists a few variants of the Riemann Hypothesis for which the hypothesis is now solved: For the zeta functions of elliptic curves over finite fields, the problem was solved by André Weil (1950). For zeta functions associated to local fields it has been proved by Daniel Bump, Eugene Ng, Jeffrey Vaaler, Stephen Choi, Par Kurlberg [B] in the real Case (= the Mellin transform of the hermite functions behave like zeta), by Par Kurlberg in the non-archimedean case with odd residue characteristics and recently par Oloffson (2006) in the complex case even though it was previously believed it was wrong in that case. It is remarkable that the local (archimedean) results also apply to the Mellin transform of the laguerre functions, thanks to the properties of the second order differential equation fulfilled by the Laguerre functions. It supports (if necessary) the link between this problem and Harmonic Analysis (see also publications by Davidson, Olafson, Faraut [F] etc on representations of conformal groups underlying Jordan algebras on bounded symmetric domains). Polya [P] succeeded around 1926 to proove that some approximations of zeta do actually have their zeroes on the Critical Line, However his results cannot be directly generalized to zeta itself (see [T]). But there are actually a lot of ways to explore the Riemann Hypothesis, from pure Number Theory to Random Matrices or Non-Commutative Geometry, which makes this problem one of the most difficult mathematical problem today.

The zeta function is also amazing, since it is the first explicit function discovered to be "Universal" (in the sense that any analytic function that does not vanish in a small disk can be uniformly approximated by zeta up to a suitable translation of zeta in the complex plane). This result was proved in 1975 by Voronin, and Karatsuba generalized the result to a finite set of L-functions approximating a finite set of analytic functions. Before this discovery, the existence of a universal function was proven in the 50's by a construction requiring the use of the axiom of choice. This result has an impact in the context of the Riemann hypothesis, because it shows that any linear combination of some Dirichlet L-functions (with non-vanishing coefficients) do not follow the Riemann Hypothesis (such a linear combination actually vanishes infinitely many times in any vertical strip inside the Critical Strip). This result is even more important when specializing to a special kind of linear combinations of Dirichlet L-functions, the prototype of which is the Davenport Heilbronn L-function. This specific linear combination share a symmetry property with individual Dirichlet L-functions (a symmetry by the change of variable $ s \mapsto 1-s $ ) which is expressed by the so-called "functional equation" fulfilled by zeta as well as Dirichlet L-functions, Hecke L-functions etc.. This functional equation is very important in this problem since in the specific case of zeta it exactly characterizes the zeta function, and with additional conditions it characterizes also Dirichlet L-functions (these are the so-called "Converse theorems", the first of which was proven by Hans Hamburger [H]). The example of the Davenport Heilbronn L-functions shows that the exact form of the functional equation is essential in the context of the Riemann Hypothesis (the functional equation of the Davenport Heilbronn L-function is almost the same as the one of a single Dirichlet L-function but there is a slight difference). However, the functional equation $ \xi(1-s)=\xi(s) $ where $ \xi(s) = s(1-s)\pi^{s/2}\Gamma(s/2)\zeta(s) $ (and similarly for L-functions), is far from beeing sufficient to prove that the non trivial zeroes are located on the Critical Line, and it is widely agreed that the missing information will require to imagine new mathematical concepts.

See also the article of Peter Sarnak on the Clay Institute website, as well as the link about the Millenium Prize.

E.C.
