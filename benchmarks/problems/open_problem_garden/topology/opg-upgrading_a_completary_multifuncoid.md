---
id: opg-upgrading_a_completary_multifuncoid
title: Upgrading a completary multifuncoid
status: open
difficulty: research
domains:
- Topology
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/upgrading_a_completary_multifuncoid
---

# Statement

Let $ \mho $ be a set, $ \mathfrak{F} $ be the set of filters on $ \mho $ ordered reverse to set-theoretic inclusion, $ \mathfrak{P} $ be the set of principal filters on $ \mho $ , let $ n $ be an index set. Consider the filtrator $ \left( \mathfrak{F}^n ; \mathfrak{P}^n \right) $ .

Conjecture If $ f $ is a completary multifuncoid of the form $ \mathfrak{P}^n $ , then $ E^{\ast} f $ is a completary multifuncoid of the form $ \mathfrak{F}^n $ .

See below for definition of all concepts and symbols used to in this conjecture.

Refer to this Web site for the theory which I now attempt to generalize.

# Source literature

- * Conjecture: Upgrading a multifuncoid

# Progress

- Definition A filtrator is a pair $ \left( \mathfrak{A}; \mathfrak{Z} \right) $ of a poset $ \mathfrak{A} $ and its subset $ \mathfrak{Z} $ .

Having fixed a filtrator, we define:

Definition $ \ensuremath{\operatorname{up}}x = \left\{ Y \in \mathfrak{Z} \hspace{0.5em} | \hspace{0.5em} Y \geqslant x \right\} $ for every $ X \in \mathfrak{A} $ .

Definition $ E^{\ast} K = \left\{ L \in \mathfrak{A} \hspace{0.5em} | \hspace{0.5em} \ensuremath{\operatorname{up}}L \subseteq K \right\} $ (upgrading the set $ K $ ) for every $ K \in \mathscr{P} \mathfrak{Z} $ .

Definition Let $ \mathfrak{A} $ is a family of join-semilattice. A completary multifuncoid of the form $ \mathfrak{A} $ is an $ f \in \mathscr{P} \prod \mathfrak{A} $ such that we have that:

\item $ L_0 \cup L_1 \in f \Leftrightarrow \exists c \in \left\{ 0, 1 \right\}^n : \left( \lambda i \in n : L_{c \left( i_{} \right)} i \right) \in f $ for every $ L_0, L_1 \in \prod \mathfrak{A} $ .

\item If $ L \in \prod \mathfrak{A} $ and $ L_i = 0^{\mathfrak{A}_i} $ for some $ i $ then $ \neg f L $ .

$ \mathfrak{A}^n $ is a function space over a poset $ \mathfrak{A} $ that is $ a\le b\Leftrightarrow \forall i\in n:a_i\le b_i $ for $ a,b\in\mathfrak{A}^n $ .

For finite $ n $ this problem is equivalent to Upgrading a multifuncoid .

It is not hard to prove this conjecture for the case $ \ensuremath{\operatorname{card}}n \leqslant 2 $ using the techniques from this my article. But I failed to prove it for $ \ensuremath{\operatorname{card}}n = 3 $ and above.
