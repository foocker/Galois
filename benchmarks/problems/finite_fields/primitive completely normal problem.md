

Problem.

Let $q$ be a prime power and let $n \ge 2$. Does there exist an irreducible polynomial $f(x) \in \mathbb{F}_q[x]$ of degree $n$ such that any root $\alpha$ of $f$ in $\mathbb{F}_{q^n}$ is simultaneously:

1. primitive, that is, $\alpha$ generates the multiplicative group $\mathbb{F}_{q^n}^*$;
2. completely normal over $\mathbb{F}_q$, that is, $\alpha$ is normal over every intermediate field $\mathbb{F}_{q^d}$ with $d \mid n$?

Equivalently, does every extension $\mathbb{F}_{q^n}/\mathbb{F}_q$ admit a primitive completely normal element?

Standard name.

This is the primitive completely normal problem, usually referred to as the Morgan-Mullen conjecture.

Terminology.

Older papers often use the terms completely free and primitive completely free instead of completely normal and primitive completely normal. In the finite-field setting these formulations refer to the same phenomenon: normality over every intermediate subfield.

Why the polynomial formulation is equivalent.

If $\alpha \in \mathbb{F}_{q^n}$ is primitive and completely normal over $\mathbb{F}_q$, then its minimal polynomial over $\mathbb{F}_q$ is irreducible of degree $n$, all its roots are Galois conjugates of $\alpha$, hence they are again primitive and completely normal. So the element version and the polynomial version are equivalent.

Relation to classical existence theorems.

Two separate existence theorems are already known:

1. the Primitive Normal Basis Theorem: for every $q$ and $n$, there exists an element of $\mathbb{F}_{q^n}$ that is both primitive and normal over $\mathbb{F}_q$;
2. the Completely Normal Basis Theorem: for every $q$ and $n$, there exists an element of $\mathbb{F}_{q^n}$ that is completely normal over $\mathbb{F}_q$.

The Morgan-Mullen conjecture asks whether these two properties can always be imposed simultaneously.

Status.

This problem is not known in full generality. It has been proved in many infinite families and in many explicit finite cases, but as of 2025 the general conjecture still appears to be open.

Selected proven families.

1. Morgan and Mullen introduced the conjecture and exhibited many explicit examples computationally.
2. Hachenberger proved in 2001 that primitive completely normal elements exist for the large class of regular extensions, under an additional mild parity condition when $q$ is odd and $n$ is even.
3. Hachenberger proved in 2015 asymptotic and effective existence results. In particular, one has $PCN_n(q)>0$ whenever $q \ge n^{7/2}$ and $n \ge 7$, or whenever $q \ge n^3$ and $n \ge 37$.
4. Garefalakis and Kapetanakis proved in 2018 that primitive completely normal elements exist whenever
$$
n=p^\ell m,\qquad (m,p)=1,\qquad q>m.
$$
5. Garefalakis and Kapetanakis proved in 2019 that the conjecture holds for all $n \le q$, and more generally obtained asymptotic and effective existence results in parts of the range $q \le n \le O(q^\varepsilon)$, with $\varepsilon=2$ asymptotically and $\varepsilon=1.25$ effectively. For even $n$ they assume $q-1 \nmid n$ in that argument.
6. In 2025, Garefalakis and Kapetanakis introduced a translate method for completely normal elements and showed that it resolves some previously unresolved cases, but not the full conjecture.

How to read these results.

The literature shows a clear pattern:

1. when $q$ is large compared with $n$, the conjecture is known in many regions;
2. when the extension has additional arithmetic structure, such as regularity, one can often prove existence;
3. the difficult cases are concentrated among relatively small $(q,n)$ pairs where global character-sum arguments are too weak and one must use sharper estimates or direct computation.

Heuristic difficulty.

Primitive is a multiplicative condition, while completely normal is simultaneously an additive-linear condition over every intermediate subfield. Each condition alone is abundant, but controlling their intersection uniformly in all extensions is delicate. The standard proofs combine character sums, estimates for the number of completely normal elements, and case-by-case treatment of small exceptional pairs.

More concretely, complete normality is much stronger than ordinary normality: instead of asking that the Frobenius orbit of $\alpha$ span $\mathbb{F}_{q^n}$ over $\mathbb{F}_q$, one asks the analogous spanning condition over every $\mathbb{F}_{q^d}$. That means the additive constraints must survive simultaneously across all divisor levels of $n$, while primitivity asks that the multiplicative order be exactly $q^n-1$. These two requirements are governed by different character-theoretic detectors, and making the main term dominate uniformly is the hard part.

Useful equivalent counting viewpoint.

Let $\mathrm{PCN}_q(n)$ denote the set of primitive completely normal elements of $\mathbb{F}_{q^n}$ over $\mathbb{F}_q$. Then the conjecture is equivalent to the statement
$$
|\mathrm{PCN}_q(n)| > 0
$$
for every prime power $q$ and every integer $n \ge 2$.

A common proof strategy is:

1. count or lower-bound the number of completely normal elements;
2. use multiplicative and additive characters to detect primitive completely normal elements;
3. show the main term dominates the error term except possibly for finitely many explicit pairs $(q,n)$;
4. resolve the remaining pairs by sharper estimates or computation.

Why the remaining cases are stubborn.

The standard lower-bound method is strongest when the number of completely normal elements is already relatively large. It degrades in small fields and for degrees with many divisors, because complete normality must be checked against many intermediate layers. As a result, the difficult part of the conjecture is not the generic asymptotic regime but the finite list of exceptional low-parameter configurations left after the analytic estimates are applied.

What is currently safe to say.

It is safe to treat this as a genuine hard problem rather than a solved theorem. It is also safe to say that a large part of the parameter space is settled, especially when $q$ is not too small relative to $n$, but one should not state the full conjecture as proved without checking the latest literature case by case.

Practical summary for this project.

If this problem is kept in the dataset, it should be labeled as an open problem with substantial partial progress. It is not a good candidate for a quick complete solution, but it is a good candidate for:

1. a survey-style note explaining the known parameter ranges;
2. a computational project on unresolved small pairs $(q,n)$;
3. a literature-guided reduction to special families such as regular extensions or low-divisor-degree cases.

Full-solve objective.

If one insists on solving the full Morgan-Mullen problem, the exact target statement is:

For every prime power $q$ and every integer $n \ge 2$, there exists an element
$$
\alpha \in \mathbb{F}_{q^n}
$$
that is simultaneously primitive and completely normal over $\mathbb{F}_q$.

Equivalently:

For every prime power $q$ and every integer $n \ge 2$, there exists an irreducible polynomial
$$
f(x)\in \mathbb{F}_q[x]
$$
of degree $n$ such that every root of $f$ in $\mathbb{F}_{q^n}$ is primitive and completely normal over $\mathbb{F}_q$.

What would count as a complete solution.

Any one of the following would qualify:

1. a proof of the statement above for all prime powers $q$ and all $n \ge 2$;
2. a reduction of the conjecture to finitely many explicit exceptional pairs $(q,n)$ together with a complete resolution of every remaining pair;
3. a counterexample, namely one explicit pair $(q,n)$ for which no primitive completely normal element exists.

Current status of the full objective.

As of April 20, 2026, this still appears to be an open problem. The 2025 preprint of Garefalakis and Kapetanakis explicitly says it covers some yet unresolved cases, which is evidence that the full conjecture was still not settled on September 27, 2025. Therefore, asking Rethlas to fully solve the problem means asking it to attack a genuine research problem, not to reproduce a known theorem.

Suggested Rethlas subproblem.

For computational experimentation, the best concrete version is the following.

Subproblem.

For a fixed small prime power $q$, enumerate small integers $n>q$ and determine for each pair $(q,n)$ whether there exists an element $\alpha \in \mathbb{F}_{q^n}$ that is simultaneously primitive and completely normal over $\mathbb{F}_q$.

Why this is a good computational target.

1. The range $n \le q$ is already covered by known theory, so the first unexplored-looking regime starts at $n>q$.
2. Complete normality and primitivity are both algorithmically testable for explicit elements of $\mathbb{F}_{q^n}$.
3. Even a negative search at bounded size is still useful: it produces a table of verified positive cases, candidate hard pairs, and example primitive completely normal polynomials.
4. This aligns with how the literature attacks the conjecture after the asymptotic estimates are exhausted: one isolates small exceptional pairs and treats them computationally.

Recommended first task.

Fix $q=2$ or $q=3$, and search degrees
$$
q<n\le 20
$$
for primitive completely normal elements.

Concrete decision problem.

For each pair $(q,n)$ in the chosen range:

1. construct $\mathbb{F}_{q^n}$;
2. sample or enumerate generators $\alpha$;
3. test whether $\alpha$ is primitive;
4. for every divisor $d \mid n$, test whether $\alpha$ is normal over $\mathbb{F}_{q^d}$;
5. if successful, output the minimal polynomial of $\alpha$ over $\mathbb{F}_q$.

Equivalent complete-normality test.

For each divisor $d \mid n$, the element $\alpha$ is normal over $\mathbb{F}_{q^d}$ if and only if the set
$$
\{\alpha,\alpha^{q^d},\alpha^{q^{2d}},\dots,\alpha^{q^{(n/d-1)d}}\}
$$
is linearly independent over $\mathbb{F}_{q^d}$.

Expected outputs.

1. a table of pairs $(q,n)$ tested;
2. for each successful pair, one explicit primitive completely normal polynomial;
3. for each unsuccessful pair within the search budget, a record that no example was found by the chosen strategy;
4. empirical statistics on how rare primitive completely normal elements appear to be.

Why this is better than asking Rethlas for a proof.

The full conjecture is too large and too literature-dependent for a first end-to-end run. The bounded search problem above is self-contained, checkable, and can still lead to mathematically meaningful artifacts:

1. explicit examples;
2. candidate exceptional pairs;
3. data to guide a later theorem attempt.

Stretch goal.

After building a search pipeline, specialize to a thin family of candidate elements, for example:

1. roots of sparse irreducible polynomials;
2. elements with prescribed trace;
3. translates $\alpha+c$ of completely normal elements, inspired by the 2025 translate method.

This gives a realistic path from brute-force search to pattern discovery.

References.

I. H. Morgan and G. L. Mullen, Completely normal primitive basis generators of finite fields, Utilitas Math. 49 (1996), 21-43.

D. Hachenberger, Primitive complete normal bases for regular extensions, Glasgow Math. J. 43 (2001), 383-398.

D. Hachenberger, The existence of primitive completely free elements in finite fields, J. Algebra 321 (2009), 667-684.

D. Hachenberger, Asymptotic existence results for primitive completely normal elements in extensions of Galois fields, Des. Codes Cryptogr. 79 (2016), 555-567.

S. Garefalakis and I. E. Kapetanakis, On the existence of primitive completely normal bases of finite fields, J. Pure Appl. Algebra 223 (2019), 909-921.

S. Garefalakis and I. E. Kapetanakis, Further results on the Morgan-Mullen conjecture, Des. Codes Cryptogr. 87 (2019), 1363-1375.

S. Garefalakis and I. E. Kapetanakis, Translates of completely normal elements and the Morgan-Mullen conjecture, preprint, 2025.
