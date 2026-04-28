---
id: opg-order_invariant_queries
title: Order-invariant queries
status: open
difficulty: research
domains:
- Logic
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/order_invariant_queries
---

# Statement

Question

\item Does $ {<}\text{-invariant\:FO} = \text{FO} $ hold over graphs of bounded tree-width? \item Is $ {<}\text{-invariant\:FO} $ included in $ \text{MSO} $ over graphs? \item Does $ {<}\text{-invariant\:FO} $ have a 0-1 law? \item Are properties of $ {<}\text{-invariant\:FO} $ Hanf-local? \item Is there a logic (with an effective syntax) that captures $ {<}\text{-invariant\:FO} $ ?

# Source literature

- [AMSS10] Matthew Anderson, Dieter van Melkebeek, Nicole Schweikardt, and Luc Segoufin, Locality of queries definable in invariant first-order logic with arbitrary built-in predicates. In ICALP'11.
- [BS09] Michael Benedikt and Luc Segoufin, Towards a characterization of order-invariant queries over tame graphs. J. Symb. Log. 74(1), 2009. Pages 168-186.
- [GS00] Martin Grohe and Thomas Schwentick, Locality of order-invariant first-order formulas. ACM Trans. Comput. Log. 1(1), 2000. Pages 112-130.
- [N05] Hannu Niemistö, On Locality and Uniform Reduction, LICS'05.
- [SS10] Nicole Schweikardt and Luc Segoufin, Addition-Invariant FO and regularity, LICS'10.

# Progress

- We describe the problem over finite vertex-colored graphs which we call graphs in the sequel. An ordered graph is a graph together with a linear order on its vertices. A property $ p $ of ordered graphs is said to be order-invariant if it is independent of the linear order. I.e. $ G,<_1 \models p $ iff $ G,<_2 \models p $ for all graphs $ G $ and all linear orders $ <_1,<_2 $ on $ G $ . Therefore, we now view an order-invariant property as a property over (unordered) graphs.

We denote by $ {<}\text{-invariant\:FO} $ , the set of order-invariant first-order definable properties over graphs, where the first-order signature contains the vocabulary for graphs but also a linear order predicate. Note that it is undecidable whether a first-order query is order-invariant. In terms of expressive power, Gurevich showed that $ {<}\text{-invariant\:FO} $ is strictly more expressive than $ \text{FO} $ . However it is known that queries expressible in $ {<}\text{-invariant\:FO} $ are Gaifman-local~[GS00]. It is also known that $ {<}\text{-invariant\:FO} = \text{FO} $ over finite trees~[BS09] (see also~[N05]).

A glimpse beyond

One can view the linear order on top of the graph as a bijection between the vertices of the graph and an ordered prefix of the positive natural numbers. With this point of view, being order-invariant corresponds to being independent from the choice of the bijection. We could imagine allowing more predicates on the numerical side, and not just the linear order. Typically addition and multiplication. When both these predicates are present we denote by $ (+,*)\text{-invariant\:FO} $ the properties definable in first-order independently of the bijection. It was shown in~[AMSS10] that those properties are Gaifman local but with a polylog radius for the neighborhoods, and this polylog is tight. However the case when only addition is present is unclear. On top of all the questions above we could add:

Question Is $ +\text{-invariant\:FO} $ Gaifman-local?

The question of the inclusion of $ +\text{-invariant\:FO} $ in $ \text{MSO} $ is already relevant over words:

Question Can $ +\text{-invariant\:FO} $ define non-regular languages over words?

See~[SS10] for more background about this question.
