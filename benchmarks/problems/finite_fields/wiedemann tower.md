Problem.

Wiedemann introduced a binary quadratic tower
$$
E_{-1}=\mathbb{F}_2,\qquad x_{-1}=1,
$$
and for $i \ge -1$,
$$
E_{i+1}=E_i(x_{i+1}),\qquad x_{i+1}^2+x_i x_{i+1}+1=0.
$$
Thus
$$
\mathbb{F}_2=E_{-1}\subset E_0\subset E_1\subset E_2\subset \cdots,
$$
with $|E_i|=2^{2^{i+1}}$.

Let
$$
N_i=2^{2^i}+1
$$
be the $i$-th Fermat number, and define
$$
u_r=\prod_{i=0}^r x_i.
$$

Wiedemann's questions.

1. Is the multiplicative order of $x_i$ equal to $N_i$ for every $i \ge 0$?
2. If so, then $u_r$ is primitive in $E_r$; more generally, can one obtain an efficient description of the minimal polynomial of $u_r$ over $\mathbb{F}_2$?

Known basic facts.

1. Wiedemann proved that $x_i^{N_i}=1$, so the order $O(x_i)$ always divides $N_i$.
2. Since the Fermat numbers are pairwise coprime, if $O(x_i)=N_i$ for all $0 \le i \le r$, then
$$
O(u_r)=\prod_{i=0}^r N_i=|E_r^\times|,
$$
so $u_r$ is primitive in $E_r$.

Status of Question 1.

This is still best treated as an open problem in general.

Known progress:

1. Popovych proved that $O(x_i)=N_i$ for $0 \le i \le 11$.
2. Consequently, $u_r$ is primitive in $E_r$ for $0 \le r \le 11$.
3. For $i \ge 12$, Popovych proved the lower bound
$$
O(x_i)\ge 7\cdot 2^{i+2}+1.
$$
4. Earlier, Voloch obtained a nontrivial lower bound of the shape $\exp(2^{i\delta})$ for some absolute constant $\delta$, but without determining the exact order.

Status of Question 2.

This needs interpretation.

1. In the literal computational sense, the minimal polynomial of any explicitly represented element of a finite field can be computed by standard finite-field algorithms, so the problem is not one of mere existence of an algorithm.
2. The interesting issue is whether there is a simple recursive or especially efficient tower-specific algorithm, or even a closed description, for the minimal polynomial of $u_r$.
3. I did not locate a standard published closed formula or canonical recursive algorithm for this specific problem, so it is best recorded as an open-ended algorithmic question rather than as a solved theorem.

Conway comparison tower.

The comparison tower usually attributed to Conway is
$$
L_{-1}=\mathbb{F}_2,\qquad c_{-1}=1,
$$
and for $i \ge -1$,
$$
L_{i+1}=L_i(c_{i+1}),\qquad c_{i+1}^2+c_{i+1}+\prod_{j=-1}^i c_j=0.
$$
Equivalently, if
$$
a_i=\prod_{j=0}^i c_j,
$$
then $c_{i+1}$ satisfies
$$
c_{i+1}^2+c_{i+1}+a_i=0.
$$

Remark.

The recurrence above uses a product, not a sum. Since $|L_i|=|E_i|=2^{2^{i+1}}$, abstract field isomorphisms
$$
E_i \cong L_i
$$
always exist by uniqueness of finite fields of a given order. So the nontrivial question is not existence of an isomorphism, but construction of an explicit one compatible with the recursive generators.

Known results for the Conway tower.

1. $c_0$ is primitive in $L_0$, and $c_1$ is primitive in $L_1$.
2. Lenstra showed that for $i>2$, the element $c_i$ is not primitive in $L_i$.
3. Popovych proved that for $2 \le i \le 11$,
$$
O(c_i)=O(a_i)=\prod_{j=1}^i N_j.
$$
4. Hence, for $2 \le i \le 11$, the elements $c_ic_0$ and $a_i a_0$ are primitive in $L_i$.

Status of the explicit isomorphism question.

Because $E_i$ and $L_i$ are finite fields of the same cardinality, an abstract $\mathbb{F}_2$-isomorphism always exists. However, I did not locate a standard published explicit recursive formula constructing such an isomorphism directly from the designated generators $x_i$ and $c_i$. So this is best kept as a structural or algorithmic problem, not as a theorem.

Practical assessment.

This item is more specialized than the other finite-field problems in this folder. It is not a good candidate for a quick full solution, but it is a good topic for:

1. studying high-order elements in recursive binary towers;
2. computing primitive elements in specific tower fields;
3. searching for explicit conversion maps between different recursive tower models.

References.

D. Wiedemann, An iterated quadratic extension of GF(2), Fibonacci Quart. 26 (1988), 290-295.

R. Popovych, On the multiplicative order of elements in Wiedemann's towers of finite fields, Carpathian Math. Publ. 7 (2015), 220-225.

R. Popovych, Multiplicative orders of elements in Conway's towers of finite fields, Algebra Discrete Math. 25 (2018), 137-146.

H. W. Lenstra, Nim multiplication, 1978.
