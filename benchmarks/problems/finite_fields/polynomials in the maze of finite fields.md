Problem.

Solve the structured sparse polynomial system from the Polynomials in the Maze of Finite Fields challenge over the given finite field substantially faster than brute force or generic Gr\"obner basis methods.

Context.

Barbero, Freij-Hollanti, Hollanti, Raddum, Ytrehus, and Oygarden study this challenge problem and show that its structured sparsity can be exploited by successive resultant computations, reducing the system to a univariate polynomial in the associated ideal and then recovering the solutions from that elimination step.

Benchmark formulation.

Given the challenge system, design an exact elimination pipeline that uses the sparsity pattern to derive a univariate polynomial, recover all solutions, and analyze the running time relative to the structure of the input equations.

References.

\AA{}. Barbero, R. Freij-Hollanti, C. Hollanti, H. Raddum, \O{}. Ytrehus, and M. \Oygarden, Attacking the Polynomials in the Maze of Finite Fields problem, arXiv:2603.05054.
