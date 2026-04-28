---
id: opg-a_diagram_about_funcoids_and_reloids
title: A diagram about funcoids and reloids
status: open
difficulty: research
domains:
- Topology
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/a_diagram_about_funcoids_and_reloids
---

# Statement

Define for posets with order $ \sqsubseteq $ :

$ \Phi_{\ast} f = \lambda b \in \mathfrak{B}: \bigcup \{ x \in \mathfrak{A} \mid f x \sqsubseteq b \} $ ;

$ \Phi^{\ast} f = \lambda b \in \mathfrak{A}: \bigcap \{ x \in \mathfrak{B} \mid f x \sqsupseteq b \} $ .

Note that the above is a generalization of monotone Galois connections (with $ \max $ and $ \min $ replaced with suprema and infima).

Then we have the following diagram:

What is at the node "other" in the diagram is unknown.

Conjecture "Other" is $ \lambda f\in\mathsf{FCD}: \top $ .

Question What repeated applying of $ \Phi_{\ast} $ and $ \Phi^{\ast} $ to "other" leads to? Particularly, does repeated applying $ \Phi_{\ast} $ and/or $ \Phi^{\ast} $ to the node "other" lead to finite or infinite sets?

See Algebraic General Topology for definitions of used concepts.

The known part of the diagram is considered in this file.

Bibliography

Blog post

* indicates original appearance(s) of problem.

add new comment

The value of node "other"

On November 29th, 2016 porton says:

It seems that the node "other" is not $ \lambda f\in\mathsf{FCD}: \top $ .

I conjecture $ \langle \Phi_{\ast} (\mathsf{RLD})_{\operatorname{out}} \rangle f = (\mathsf{FCD}) f $ where $ f $ is the reloid defined by the cofinite filter on $ A \times B $ and thus $ \langle (\mathsf{FCD}) f \rangle \{ x \} = \bot $ for all singletons $ \{ x \} $ and $ \langle (\mathsf{FCD}) f \rangle p = \top $ for every nontrivial atomic filter $ p $ .

This is my very recent thoughts and yet needs to be checked.

-- Victor Porton - http://www.mathematics21.org

reply

The diagram was with an error

On November 26th, 2016 porton says:

My diagram was with an error. I have uploaded a corrected version of the diagram.

--

Victor Porton - http://www.mathematics21.org

reply

Comment viewing options

Flat list - collapsedFlat list - expandedThreaded list - collapsedThreaded list - expanded

Date - newest firstDate - oldest first

10 comments per page30 comments per page50 comments per page70 comments per page90 comments per page150 comments per page200 comments per page250 comments per page300 comments per page

Select your preferred way to display the comments and click "Save settings" to activate your changes.

# Source literature


# Progress

- Status: open.
