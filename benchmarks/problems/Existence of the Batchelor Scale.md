### Problem 4: Existence of the Batchelor Scale

This is actually a problem directly from my another project. In that project, we use argue by contradiction to prove a limsup is greater than zero, but I'm more curious on whether it has a limit or not.

**Problem 4**

Prove that in \cite{huang2025exponential}, Corollary 2.1, the limsup can be changed to liminf. On the other words:

Consider the advection diffusion equation in $\mathbb{T}^2$:
$$
\partial_t \rho + U(t,y)\,\partial_x \rho = \Delta \rho.
$$

Assume that $0\neq \rho(0,\cdot) \in L^2_{x,y}$ is mean-zero and that 
$$
\|U\|_{L^{\infty}_t L^2_y} < \infty.
$$

Then we have for the weak solution $\rho$,
$$
\liminf\limits_{t\rightarrow\infty}\frac{\|\rho(t)\|_{\dot{H}^{-1}}}{\|\rho(t)\|_{L^2}}>0.
$$