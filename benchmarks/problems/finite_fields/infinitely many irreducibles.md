Problem.

Let
$$
F(X,Y)=A_0(X)+A_1(X)Y+\cdots+A_m(X)Y^m \in \mathbb{F}_q[X,Y]
$$
be irreducible over $\mathbb{F}_q$. For polynomials $g(X) \in \mathbb{F}_q[X]$, consider the specialization
$$
F(X,g(X)) \in \mathbb{F}_q[X].
$$

Question 1.

Are there infinitely many polynomials $g(X) \in \mathbb{F}_q[X]$ such that $F(X,g(X))$ is irreducible in $\mathbb{F}_q[X]$?

Question 2.

Can one require in addition that $F(X,g(X))$ be primitive, in the sense that if $\deg F(X,g(X))=N$, then any root of $F(X,g(X))$ generates the multiplicative group of $\mathbb{F}_{q^N}$?

Status.

The first question is natural but delicate as stated. There are strong positive results in the direction of irreducible specializations, especially when the field size is allowed to be sufficiently large relative to the degrees involved, or when one restricts to special classes of substitutions such as linear polynomials $g(X)=aX+b$. However, the blanket statement above for an arbitrary fixed finite field $\mathbb{F}_q$ should be treated with caution unless additional hypotheses are imposed.

What is known in the direction of Question 1.

1. Function-field analogues of Hilbert irreducibility imply that irreducible specializations should be abundant under suitable geometric hypotheses.
2. Over sufficiently large finite fields, results of Bary-Soroker and collaborators prove irreducibility for many specializations, and even asymptotic formulas in families.
3. There are results for linear substitutions $Y=aX+b$ showing that many such specializations are irreducible when $q$ is large enough compared with the total degree and certain separability conditions hold.
4. These results strongly suggest that irreducible values occur infinitely often in many natural settings, but they do not justify writing the unrestricted fixed-$q$ statement as a solved theorem.

Why the formulation needs care.

The behavior of $F(X,g(X))$ depends not only on irreducibility of $F(X,Y)$ in two variables, but also on geometric properties such as separability and the arithmetic monodromy of the corresponding cover. Over finite fields, unlike over infinite Hilbertian fields, one must also distinguish between:

1. fixing $q$ and letting $\deg g$ grow;
2. letting $q$ grow with the degrees fixed;
3. restricting $g$ to a special family such as $aX+b$.

Different theorems address different regimes.

Safe takeaway for Question 1.

It is reasonable to record this as an open-ended problem or research direction rather than a solved theorem. If one wants a theorem-level statement, it should be rewritten with extra hypotheses, for example:

1. restrict to linear substitutions $g(X)=aX+b$;
2. assume $q$ is sufficiently large relative to $\deg F$;
3. impose explicit separability and non-composition conditions.

Status of Question 2.

The primitive version is substantially stronger. I did not find a clean general theorem that would justify stating that there are always infinitely many $g(X)$ for which $F(X,g(X))$ is primitive. This should therefore be treated as a harder speculative extension of Question 1, not as a standard solved result.

Practical assessment.

This item is best treated as a broad research problem with several rigorous partial results nearby. It is not as cleanly formulated as the primitive normal or completely normal problems. If kept in the dataset, it would benefit from narrowing to a more precise theorem-shaped question.

Suggested narrower versions.

1. For fixed irreducible $F(X,Y) \in \mathbb{F}_q[X,Y]$, are there infinitely many linear polynomials $g(X)=aX+b$ such that $F(X,g(X))$ is irreducible?
2. For fixed total degree, give explicit lower bounds on $q$ that guarantee the existence of irreducible specializations.
3. Study special classes of $F(X,Y)$ for which one can prove infinitely many irreducible values over a fixed small field.

References.

L. Bary-Soroker, Irreducible values of polynomials, Adv. Math. 229 (2012), 854-874.

L. Bary-Soroker and R. Rosenzweig, Irreducible specializations of polynomials over finite fields, Israel J. Math. 225 (2018), 469-493.

L. Bary-Soroker, A. Pollack, and O. Schlank, Bateman-Horn and Schinzel type theorems over large finite fields, Int. Math. Res. Not. IMRN 2020, no. 23, 8283-8316.

D. B. Leep and C. L. Stewart, Explicit Hilbert irreducibility over function fields, J. Number Theory 202 (2019), 1-27.
