Problem: Finiteness Problem for Small Diophantine Equations

Source:

- Epoch AI FrontierMath Open Problems, "Finiteness Problem for Diophantine Equations"
- URL: https://epoch.ai/frontiermath/open-problems/small-diophantine
- Contributors listed by Epoch AI: Bogdan Grechuk and Tetiana Grechuk
- Accessed: April 20, 2026

## Problem Statement

For each of the following Diophantine equations, determine whether it has
infinitely many integer solutions. Equivalently, for benchmark purposes, try
to find three distinct integer solutions $(x,y,z)$ with $|x|>10^{50}$ and
with three distinct values of $x$.

The equations are:

1. $z^2+y^2z+x^3-2=0$.
2. $z^2+y^2z+x^3-x-1=0$.
3. $z^2+y^2z+x^3+x-1=0$.
4. $z^2+y^2z+x^3+x+1=0$.
5. $z^2+y^2z+x^3-3=0$.
6. $z^2+y^2z+x^3+3=0$.
7. $z^2+y^2z+x^3-x-2=0$.
8. $z^2+y^2z+x^3-x+2=0$.
9. $z^2+y^2z-z+x^3+2=0$.

## Background

Epoch AI describes the size of a Diophantine equation by substituting $2$ for
all variables and using absolute values for coefficients. The page states that
these were the size $\le 24$ equations for which the finiteness problem was
open in the source problem set. Numerical evidence suggests infinitely many
solutions, but the general resolution is not supplied in the problem statement.

## Source Update To Preserve

Epoch AI's page includes an update dated March 5, 2026:

- GPT-5.4 Pro solved two of the nine equations by direct substitution:
  $z^2+y^2z-z+x^3+2=0$ and $z^2+y^2z+x^3+x+1=0$.
- The problem authors then adapted one of those substitutions to solve
  $z^2+y^2z+x^3+x-1=0$ as well.
- The page still presents the full set as the benchmark problem and says the
  authors expect the full resolution to require a genuinely new approach.

## Suggested Agent Task

Treat this as an open-problem research task, not as a routine exercise. A
complete solution should either:

1. prove infinitely many integer solutions for each equation still unresolved
   by the source update, or
2. produce explicit parameterized infinite families or enough distinct large
   solutions to meet the benchmark prompt for each requested equation.

Do not claim the full FrontierMath problem is solved unless every required
equation has been handled and the resulting proof or constructions have been
verified.
