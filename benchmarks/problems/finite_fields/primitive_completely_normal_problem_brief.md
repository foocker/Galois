Problem: Primitive Completely Normal Problem

Let $q$ be a prime power and let $n \ge 2$. The question is whether there always exists an element
$$
\alpha \in \mathbb{F}_{q^n}
$$
such that:

1. $\alpha$ is primitive, meaning that it generates the multiplicative group $\mathbb{F}_{q^n}^{\times}$;
2. $\alpha$ is completely normal over $\mathbb{F}_q$, meaning that for every divisor $d \mid n$, the element $\alpha$ is normal for the extension $\mathbb{F}_{q^n}/\mathbb{F}_{q^d}$.

Equivalently, one may ask whether there always exists an irreducible polynomial
$$
f(x)\in \mathbb{F}_q[x]
$$
of degree $n$ such that every root of $f$ in $\mathbb{F}_{q^n}$ is both primitive and completely normal.

This is the problem usually known as the Morgan-Mullen conjecture.

What is known:

1. If one only asks for a primitive normal element, this is known to be always possible.
2. If one only asks for a completely normal element, this is also known to be always possible.
3. However, requiring both properties simultaneously is much harder, and only many partial results are known.
4. The problem is known to be solved when $n \le q$. There are also several asymptotic results, results for regular extensions, and many explicit small-parameter cases.

Why it is difficult:

Primitivity is a multiplicative condition, while complete normality is an additive and linear condition that must hold simultaneously over every intermediate subfield. Each condition alone is common, but proving that they must always occur together for every pair $(q,n)$ is very difficult.

As of April 20, 2026, this should still be regarded as an open problem.
