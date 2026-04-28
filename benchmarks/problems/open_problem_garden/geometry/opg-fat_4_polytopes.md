---
id: opg-fat_4_polytopes
title: Fat 4-polytopes
status: open
difficulty: frontier
domains:
- Geometry
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/fat_4_polytopes
---

# Statement

The fatness of a 4-polytope $ P $ is defined to be $ (f_1 + f_2)/(f_0 + f_3) $ where $ f_i $ is the number of faces of $ P $ of dimension $ i $ .

Question Does there exist a fixed constant $ c $ so that every convex 4-polytope has fatness at most $ c $ ?

# Source literature


# Progress

- The $ f $ -vector of a $ d $ -dimensional polytope $ P $ is the vector $ (f_0,f_1,\ldots,f_{d-1}) $ where $ f_i $ is the number of faces of dimension $ i $ . Let us denote by $ {\mathcal F}_d $ the collection of all $ f $ -vectors of convex $ d $ -dimensional polytopes. Steinitz proved that the set $ {\mathcal F}_3 $ is completely characterized by the following three conditions:

\item $ f_0 - f_1 + f_2 = 2 $ , \item $ f_2 \le 2f_0 - 4 $ , \item $ f_0 \le 2f_2 - 4 $ .

The first of these conditions is Euler's formula. The second and third are easy inequalities which are tight for simplicial (all faces triangles) and simple (all vertices of degree 3) polytopes, respectively.

In sharp contrast to this, the situation for $ {\mathcal F}_4 $ seems to be quite complicated. For instance, it has been shown that $ {\mathcal F}_4 $ does not contain all elements of $ {\mathbb Z}^4 $ which lie in the convex hull of $ {\mathcal F}_4 $ ; i.e., $ {\mathcal F}_4 $ has "holes" in it. For the extreme examples of simple and simplicial polytopes, the $ g $ -theorem of Billera-Lee and Stanley gives a complete description of all possible $ f $ -vectors, but in general very little is known.
