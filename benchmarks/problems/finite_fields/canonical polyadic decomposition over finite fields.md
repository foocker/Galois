Problem.

Let $T \in \mathbb{F}^{n_0 \times \cdots \times n_{D-1}}$ be a tensor over a finite field $\mathbb{F}$, and let $R \ge 1$. Determine whether $T$ has a rank-$R$ canonical polyadic decomposition
$$
T=\sum_{r=1}^R \bigotimes_{d=0}^{D-1} a_d^{(r)},
$$
and produce such a decomposition if it exists.

Context.

Yang studies exact algorithms for tensor CPD over finite fields, motivated in part by tensor-rank questions from fast matrix multiplication. The work develops an exact rank-$R$ search algorithm, a border-CPD variant, and new upper and lower bounds for maximum tensor rank.

Benchmark formulation.

Given $(\mathbb{F},T,R)$, either output an exact rank-$R$ CPD of $T$ or certify that none exists. For small tensor shapes, also investigate the maximum possible rank over $\mathbb{F}$.

References.

J. Yang, New results in canonical polyadic decomposition over finite fields, 2025.
