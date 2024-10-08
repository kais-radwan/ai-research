<h1 style="text-align: center">
Kais Radwan's Research In Artificial Intelligence
</h1>



<h2 style="text-align: center">
Algorithms
</h2>

---

### search algorithms

#### depth-first search (DFS)

search algorithm that always expands the deepest node in the frontier.

uses a stack data structure.

#### breadth-first search (BFS)

search algorithm that always expands the shallowest node in the frontier.

uses a queue data structure.

#### greedy best-first search

search algorithm that expands the node that is closest to the goal. as estimated by a heuristic function `h(n)`

A* search

search algorithm that expands node with lowest value of:
$$
g(n) + h(n)
$$
where:

`g(n)` = cost to reach node

`h(n)` = estimated cost to goal

optimal if:

`h(n)` is admissible (never overestimates the true cost), and

`h(n)` is consistent, which means for every node `n` and successor `n'` with step cost `c`:
$$
h(n) <= h(n') + c
$$

#### minimax

**MAX** (X) aims to maximize score.

**MIN** (O) aims to minimize score.

<h2 style="text-align: center">
Problems
</h2>

---

### Search problems

built up of:

- initial state
- actions
- transition model
- goal test
- path cost function

#### Approach

start with a frontier that contains the initial state.

start with an empty explored set.

repeat:

​	if the frontier is empty, then no solution.

​	remove a node from the frontier.

​	if node contains goal state, return the solution.

​	Add node to the explored set

​	expand node, add resulting nodes to the frontier if they aren't already in the frontier or the explored set.

<h2 style="text-align: center">
Search Terms
</h2>

---

### agent

entity that perceives its environment and acts upon that environment.

### state

a configuration of the agent and its environment.

### initial state

the state in which the agent begins

### actions

choices that can be made in a state.
$$
ACTIONS(s: state): actions
$$
`ACTIONS(s)` returns the set of actions that can be executed in state `s`

### transition model

$$
RESULT(s: state, a: action): r
$$

`RESULT(s,a)` returns the state resulting from performing action `a` in state `s`

### state space

the set of all states reachable from the initial state by any sequence of actions

### goal test

way to determine whether a given is a goal state

### path cost

numerical cost associated with a given path

### solution

a sequence of actions that leads from the initial state to a goal state

### optimal solution

a solution that has the lowest path cost among all solutions

### node

a data structure that keeps track of

- a state
- a parent (node that generated this node)
- an action (action applied to parent to get this node)
- a path cost (from initial state to node)

### stack

first-in last-out data type

### queue

first-in first-out data type

### uninformed search

search strategy that uses no problem-specific knowledge

### informed search

search strategy that uses problem-specific knowledge to find solutions more efficiently



<h2 style="text-align: center">
Logic Terms
</h2>

---

### knowledge-based agents

agents that reason by operating on internal presentations of knowledge.

### sentence

an assertion about the world in a knowledge representation language.



<h2 style="text-align: center">
Propositional Logic
</h2>

---

Symbols:
$$
P  Q  R
$$


### model

assignment of a truth value to every proposition symbol (a possible world)

### knowledge base

a set of sentences known by a knowledge-based agent to be true

### entailment

$$
a ⊨ B
$$

in every model in which sentence **a** is true, sentence **b** is also true.

(a: alpha, b: beta).



### inference

the process of deriving new sentences from old ones.
$$
KB = (P ∧ ¬Q) –> R
$$

### Model checking algorithm

To determine if:
$$
KB ⊨ a
$$
Enumerates all possible models.

If in every model where **KB** is true, **a** is true, then **KB** entails **a**.

Otherwise, **KB** does not entail **a**.

### Modus Ponens (rule)

$$
a -> B
$$

$$
a
$$

$$
---
$$

$$
B
$$

### And elimination

$$
a ∧ B
$$

$$
---
$$

$$
a
$$

### Double negation elimination

$$
¬(¬a)
$$

$$
---
$$

$$
a
$$

### Implication elimination

$$
a -> B
$$

$$
---
$$

$$
¬a v B
$$

### Conditional elimination

$$
a <-> B
$$

$$
---
$$

$$
(a -> B) ∧ (B -> a)
$$

### De Morgan's law

$$
¬(a ∧ B)
$$

$$
---
$$

$$
(¬a) v (¬B)
$$

and also:
$$
¬(avB)
$$

$$
---
$$

$$
¬a ∧ ¬B
$$

### Distributive property

$$
(a ∧ (BvY))
$$

$$
---
$$

$$
(a ∧ B) v (a ∧ Y)
$$

### Resolution rule

$$
PvQ
$$

$$
¬P
$$

$$
---
$$

$$
Q
$$

also:
$$
PvQ
$$

$$
¬PvR
$$

$$
---
$$

$$
QvR
$$

---

also:
$$
P
$$

$$
¬P
$$

$$
---
$$

$$
()
$$

### Clause

A disjunction of literals.

e.g. `P v Q v R`

### conjunctive normal form

logical sentence that is a conjunction of clauses

e.g. `(A v B v C) ∧ (D v ¬E) ∧ (F v G)`

### Conversion to CNF

Eliminate biconditionals

​	turn **(a <-> B)** into **(a -> B) ^ (B -> a)**

Eliminate implications

​	turn **(a -> B)** into **¬a v B**

Move **¬** inwards using De Morgan's Laws

​	turn **¬(a ^ B)** into **¬a v ¬B**

Use distributive law to distribute **v** whenever possible.


$$
(P v Q) -> R
$$

$$
¬(PvQ) v R
$$

$$
(¬P ∧ ¬Q) v R
$$

$$
(¬P v R) ∧ (¬Q v R)
$$

### Inference by resolution

To determine if **KB ⊨ a**:

​	Convert **(KB ^ ¬a)** to CNF.

​	Keep checking to see if we can use resolution to produce a new clause:

​		if ever we produce the empty clause (false), we have a contradiction, and **KB ⊨ a**.

​		Otherwise, if we can't add new clauses, no entailment.

---

<h2 style="text-align: center">
Probability
</h2>

$$
P(w)
$$

where w = worlds.
$$
0 <= P(2) <= 1
$$

$$
Σ P(w) = 1
$$

### conditional probability

$$
P(a|b)
$$

$$
P(a|b) = P(a ∧ b) / P(b)
$$

$$
P(a ∧ b) = P(a)P(b|a)
$$



### random variable

a variable in probability theory with a domain of possible values it can take on.

### independence

$$
P(a ∧ b) = P(a)P(b)
$$



### Bayes' rule

$$
P(b|a) = (P(b)P(a|b))/P(a)
$$

### Bayesian network

data structure that represents the dependencies among random variables.

directed graph.

each node represents a random variable.

arrow from X to Y means X is a parent of Y.

each node X has probability distribution:
$$
P(X|Parents(X))
$$
