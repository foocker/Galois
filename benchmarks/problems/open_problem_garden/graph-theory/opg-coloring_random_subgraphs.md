---
id: opg-coloring_random_subgraphs
title: Coloring random subgraphs
status: open
difficulty: research
domains:
- Graph Theory
source: Open Problem Garden
source_url: http://www.openproblemgarden.org/op/coloring_random_subgraphs
---

# Statement

If $ G $ is a graph and $ p \in [0,1] $ , we let $ G_p $ denote a subgraph of $ G $ where each edge of $ G $ appears in $ G_p $ with independently with probability $ p $ .

Problem Does there exist a constant $ c $ so that $ {\mathbb E}(\chi(G_{1/2})) > c \frac{\chi(G)}{\log \chi(G)} $ ?

# Source literature

- *[B] Boris Bukh's problem page.

# Progress

- It is a classical result that the above problem has a positive answer when $ G $ is the complete graph. More generally, the lower bound $ {\mathbb E}(\chi(G_{1/2})) \ge c \frac{\chi(G)}{\log |V(G)|} $ is known.

It is easy to obtain the bound $ {\mathbb E}(\chi(G_{1/2})) \ge (\chi(G))^{1/2} $ , since we may imagine forming two random subgraphs $ H,H' $ of $ G $ by putting each edge of $ G $ in either $ H $ or $ H' $ independently with probability $ 1/2 $ . Then $ \chi(H) \chi(H') \ge \chi(G) $ and this gives the desired bound. A similar argument with three subgraphs shows that $ {\mathbb E}(\chi(G_{1/3})) \ge (\chi(G))^{1/3} $ , however these arguments all seem to require integer multiples, so the best known lower bound on $ {\mathbb E}(\chi(G_{49/100})) $ of this form is $ (\chi(G))^{1/3} $ .
