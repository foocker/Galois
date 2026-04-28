---
id: opg-even_vs_odd_latin_squares
title: Even vs. odd latin squares
status: open
difficulty: frontier
domains:
- Combinatorics
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/even_vs_odd_latin_squares
---

# Statement

A latin square is even if the product of the signs of all of the row and column permutations is 1 and is odd otherwise.

Conjecture For every positive even integer $ n $ , the number of even latin squares of order $ n $ and the number of odd latin squares of order $ n $ are different.

# Source literature

- *[AT] N. Alon, M. Tarsi, Coloring and Orientations of Graphs. Combinatorica 12, 125-143, 1992 MathSciNet
- [D1] A. Drisko, On the number of even and odd Latin squares of order $ p+1 $ , Adv. Math. 128 (1997), no. 1, 20--35. MathSciNet
- [D2] A. Drisko, Proof of the Alon-Tarsi conjecture for $ n=2\sp rp $ . Electron. J. Combin. 5 (1998) MathSciNet.
- [HR] R. Huang and G-C Rota, On the relations of various conjectures on Latin squares and straightening coefficients. Discrete Math. 128 (1994), no. 1-3, 225--236. MathSciNet.
- [O] S. Onn, A colorful determinantal identity, a conjecture of Rota, and Latin squares. Amer. Math. Monthly 104 (1997), no. 2, 156--159. MathSciNet.
- [Z] P. Zappa, The Cayley determinant of the determinant tensor and the Alon-Tarsi conjecture. Adv. in Appl. Math. 19 (1997), no. 1, 31--44. MathSciNet.

# Progress

- For every positive integer $ n $ , let $ ELS(n) $ , ( $ OLS(n) $ ) be the number of even (odd) latin squares of order $ n $ .

The inspiration for this conjecture comes from an attempt by Alon and Tarsi to use their polynomial technique to show that the complete bipartite graph $ K_{n,n} $ is $ n $ -edge-choosable (a famous conjecture of Dinitz asserts that this is always true). They show (in [AT]) that whenever $ ELS(n) \neq OLS(n) $ , the graph $ K_{n,n} $ is $ n $ -edge-choosable. For odd integers $ n>1 $ it is easy to see that $ ELS(n) = OLS(n) $ , since interchanging the first two rows has no effect on the signs of the rows, but flips the signs of all of the columns. For even $ n $ , Alon and Tarsi checked that $ ELS(n) $ and $ OLS(n) $ were different for $ n=2,4,6 $ and conjectured that this pattern would continue. Although Dinitz' Conjecture has since been resolved, Alon and Tarsi's conjecture remains quite interesting. In particular, it has been shown by Huang and Rota [HR] that the truth of this conjecture would imply Rota's basis conjecture for even values of $ n $ (see [O] for a nice proof of this).

ELS() and OLS() appear in the The Encyclopedia of Integer Sequences as A114628 and A114629. The following chart shows the first few values. Although the data here is quite limited, $ ELS(n) > OLS(n) $ for every even $ n $ in the chart, and as far as we know, this might hold in general.

n
ELS(n)
OLS(n)

1
1
0

2
2
0

3
6
6

4
576
0

5
80640
80640

6
505958400
306892800

7
30739709952000
30739709952000

8
55019078005712486400
53756954453370470400

Drisko [D1] proved that whenever $ p $ is prime, $ ELS(p+1) - OLS(p+1) \cong (-1)^{{(p+1)}/2} p^2 $ (mod $ p^3 $ ), thus verifying the Alon-Tarsi conjecture for any even number which is one more than a prime. Shortly afterward, Zappa [Z] introduced a function $ AT() $ which compares the number of even and odd latin squares which have all diagonal entries equal to one, and proved some interesting identities concerning $ AT() $ . By utilizing these identities, Drisko [D2] proved that $ ELS(n) \neq OLS(n) $ whenever $ n $ is of the form $ 2^rp $ for a prime $ p $ .
