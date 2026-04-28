---
id: opg-intersecting_two_perfect_matchings
title: The intersection of two perfect matchings
status: solved
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/intersecting_two_perfect_matchings
---

# Statement

Conjecture Every bridgeless cubic graph has two perfect matchings $ M_1 $ , $ M_2 $ so that $ M_1 \cap M_2 $ does not contain an odd edge-cut.

# Source literature

- * Edita Macajova, Martin Skoviera, Fano colourings of cubic graphs and the Fulkerson conjecture. Theoret. Comput. Sci. 349 (2005), no. 1, 112--120. MathSciNet

# Progress

- Let $ G = (V,E) $ be a bridgeless cubic graph. A binary cycle (henceforth called cycle) is a set $ C \subseteq E $ so that every vertex of $ (V,C) $ has even degree (equivalently, a cycle is any member of the binary cycle space). A postman join is a set $ J \subseteq E $ so that $ E \setminus J $ is a cycle. Note that since $ G $ is cubic, every perfect matching is a postman join. Next we state a well-known theorem of Jaeger in three equivalent forms.

Theorem (Jaeger's 8-flow theorem)

\item $ G $ has a nowhere-zero flow in the group $ {\mathbb Z}_2^3 $ . \item $ G $ has three cycles $ C_1,C_2,C_3 $ so that $ C_1 \cup C_2 \cup C_3 = E $ . \item $ G $ has three postman joins $ J_1,J_2,J_3 $ so that $ J_1 \cap J_2 \cap J_3 = \emptyset $ .

The last of these statements is interesting, since The Berge Fulkerson Conjecture (if true) implies the following:

Conjecture $ G $ has three perfect matchings $ M_1,M_2,M_3 $ so that $ M_1 \cap M_2 \cap M_3= \emptyset $ .

So, we know that $ G $ has three postman joins $ J_1,J_2,J_3 $ with empty intersection, and it is conjectured that $ J_1,J_2,J_3 $ may be chosen so that each is a perfect matching, but now we see two statements in between the theorem and the conjecture. Namely, is it true that $ J_1,J_2,J_3 $ may be chosen so that one is a perfect matching? or two? The first of these was solved recently.

Theorem (Macajova, Skoviera) $ G $ has two postman sets $ J_1,J_2 $ and one perfect matching $ M $ so that $ M \cap J_1 \cap J_2 = \emptyset $

The second of these asks for two perfect matchings $ M_1,M_2 $ and one postman join $ J $ so that $ M_1 \cap M_2 \cap J = \emptyset $ . It is an easy exercise to show that a set $ S \subseteq E $ contains a postman join if an only if $ S $ has nonempty intersection with every odd edge-cut. Therefore, finding two perfect matchings and one postman join with empty common intersection is precisely equivalent to the conjecture at the start of this page - find two perfect matchings whose intersection contains no odd edge-cut.
