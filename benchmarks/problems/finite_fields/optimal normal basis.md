Problem.

Let $\mathbb{F}_{q^n}/\mathbb{F}_q$ be a finite field extension. For a normal basis
$$
\mathcal{B}=\{\alpha,\alpha^q,\alpha^{q^2},\dots,\alpha^{q^{n-1}}\},
$$
the complexity of $\mathcal{B}$ is the number of nonzero entries in the multiplication table for multiplication by $\alpha$. A normal basis has complexity at least $2n-1$, and those attaining this lower bound are called optimal normal bases.

Question.

If an optimal normal basis does not exist, how small can the complexity of a normal basis be?

Standard conjectural form.

The standard version in the literature is the binary case:

If there is no optimal normal basis of $\mathbb{F}_{2^n}$ over $\mathbb{F}_2$, then every normal basis has complexity at least $3n-3$.

Equivalently, for binary extensions, the conjecture says that there is a gap between the optimal value $2n-1$ and the next possible minimum value, namely $3n-3$.

General-$q$ remark.

One sometimes sees broader formulations for arbitrary $q$, but the clean and widely cited conjecture is the binary one above. For general $q$, the landscape is less uniform, and the value $3n-3$ should not be stated as a universal next minimum without qualification.

Status.

This is an open problem. It is a classical conjecture in the theory of normal bases and is still listed as unresolved in standard references.

Evidence and partial results.

1. The general lower bound $2n-1$ is classical, and characterizes optimal normal bases.
2. Various constructions produce normal bases of complexity close to $3n$, which suggests that $3n-3$ is the right candidate for the next minimum in the binary case.
3. The duals of type I optimal normal bases provide explicit examples of low-complexity normal bases: their complexity is $3n-3$ when $q$ is even and $3n-2$ when $q$ is odd.
4. Computational searches support the binary conjecture for many degrees; the literature records verification at least for $n \le 39$.
5. A closely related open problem is to classify all normal bases of complexity at most $3n$, which would in particular clarify whether any complexity strictly between $2n-1$ and $3n-3$ can occur in the binary case.

Why this problem is hard.

This is not just an existence question. One must rule out all intermediate complexities between the optimal bound $2n-1$ and the conjectural next value $3n-3$. That makes the problem closer to a structural classification problem for low-complexity multiplication tables than to a direct construction problem.

Practical assessment.

This is a genuine hard open problem. It is not a good candidate for a quick solution. It is better suited to:

1. a survey on low-complexity normal bases;
2. a computational search for small binary degrees;
3. a classification project for special families of normal bases.

References.

S. Gao, Normal Bases over Finite Fields, PhD thesis, University of Waterloo, 1993.

D. Jungnickel and A. Pott, Perfect and almost perfect normal bases, Discrete Appl. Math. 88 (1998), 149-158.

J. von zur Gathen and I. Shparlinski, Orders of Gauss periods in finite fields, Appl. Algebra Engrg. Comm. Comput. 9 (1998), 15-24.

S. Hachenberger and D. Jungnickel, Topics in Galois Fields, 2020. See the discussion around Conjecture 8.6.25.

G. L. Mullen and D. Panario, Handbook of Finite Fields, 2013. See Conjecture 2.2.13 and the surrounding discussion on low-complexity normal bases.
