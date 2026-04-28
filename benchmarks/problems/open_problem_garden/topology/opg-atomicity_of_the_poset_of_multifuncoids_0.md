---
id: opg-atomicity_of_the_poset_of_multifuncoids_0
title: Atomicity of the poset of multifuncoids
status: open
difficulty: research
domains:
- Topology
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/atomicity_of_the_poset_of_multifuncoids_0
---

# Statement

Conjecture The poset of multifuncoids of the form $ (\mathscr{P}\mho)^n $ is for every sets $ \mho $ and $ n $ :

\item atomic; \item atomistic.

See below for definition of all concepts and symbols used to in this conjecture.

Refer to this Web site for the theory which I now attempt to generalize.

# Source literature

- * Algebraic General Topology

# Progress

- Definition A free star on a join-semilattice $ \mathfrak{A} $ with least element 0 is a set $ S $ such that $ 0 \not\in S $ and \[ \forall A, B \in \mathfrak{A}: \left( A \cup B \in S \Leftrightarrow A \in S \vee B \in S \right) . \]

Definition Let $ \mathfrak{A} $ be a family of posets, $ f \in \mathscr{P} \prod \mathfrak{A} $ ( $ \prod \mathfrak{A} $ has the order of function space of posets), $ i \in \ensuremath{\operatorname{dom}}\mathfrak{A} $ , $ L \in \prod \mathfrak{A}|_{\left( \ensuremath{\operatorname{dom}}\mathfrak{A} \right) \setminus \left\{ i \right\}} $ . Then \[ \left( \ensuremath{\operatorname{val}}f \right)_i L = \left\{ X \in \mathfrak{A}_i \hspace{0.5em} | \hspace{0.5em} L \cup \left\{ (i ; X) \right\} \in f \right\} . \]

Definition Let $ \mathfrak{A} $ is a family of posets. A multidimensional funcoid (or multifuncoid for short) of the form $ \mathfrak{A} $ is an $ f \in \mathscr{P} \prod \mathfrak{A} $ such that we have that:

\item $ \left( \tmop{val} f \right)_i L $ is a free star for every $ i \in \tmop{dom} \mathfrak{A} $ , $ L \in \prod \mathfrak{A}|_{\left( \tmop{dom} \mathfrak{A} \right) \setminus \left\{ i \right\}} $ .

\item $ f $ is an upper set.

$ \mathfrak{A}^n $ is a function space over a poset $ \mathfrak{A} $ that is $ a\le b\Leftrightarrow \forall i\in n:a_i\le b_i $ for $ a,b\in\mathfrak{A}^n $ .
