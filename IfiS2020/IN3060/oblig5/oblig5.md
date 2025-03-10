
# Oblig 5
### Markus Sverdvik Heiervang - markuhei
***
## 1 Model Semantics

### 1.1

1. $\mathcal{I}_1 \models \Gamma_1$  

$\mathcal{I}_1:$

$$ \Delta^{\mathcal{I}_1} = \{T, J, B\} $$
$$ Tweety^{\mathcal{I}_1} = T $$
$$ JollyJumper^{\mathcal{I}_1} = J $$
$$ Bruce^{\mathcal{I}_1} = B = \beta(b) $$  

$$ Animal^{\mathcal{I}_1} = \Delta^{\mathcal{I}_1} $$
$$ Food^{\mathcal{I}_1} = \{B\} $$
$$ Bird^{\mathcal{I}_1} = \{T\} $$
$$ Penguin^{\mathcal{I}_1} = Bird^{\mathcal{I}_1}$$
$$ Fish^{\mathcal{I}_1} = Food^{\mathcal{I}_1} $$
$$ Horse^{\mathcal{I}_1} = \{J, B\} $$
$$ Vegetable^{\mathcal{I}_1} = \emptyset $$

$$ eats^{\mathcal{I}_1} = \{\langle J, B \rangle\} $$
$$ likes^{\mathcal{I}_1} = \{\langle J, T \rangle\} $$
$$ hasNickname^{\mathcal{I}_1} = \{\langle J, "JJ" \rangle, \langle B, "Alonso" \rangle\} $$
$$ favoriteFood^{\mathcal{I}_1} = eats^{\mathcal{I}_1} $$


2. $\mathcal{I}_2 \nvDash \Gamma_1$  
$\mathcal{I}_2:$

$$ \Delta^{\mathcal{I}_2} = \{T, J, B\} $$
$$ Tweety^{\mathcal{I}_2} = T $$
$$ JollyJumper^{\mathcal{I}_2} = J $$
$$ Bruce^{\mathcal{I}_2} = B = \beta(b) $$  

$$ Animal^{\mathcal{I}_2} = \emptyset $$
$$ Food^{\mathcal{I}_2} = \{B\} $$
$$ Bird^{\mathcal{I}_2} = \{T\} $$
$$ Penguin^{\mathcal{I}_2} = Bird^{\mathcal{I}_2}$$
$$ Fish^{\mathcal{I}_2} = Food^{\mathcal{I}_2} $$
$$ Horse^{\mathcal{I}_2} = \{J, B\} $$
$$ Vegetable^{\mathcal{I}_2} = \Delta^{\mathcal{I}_2} $$

$$ eats^{\mathcal{I}_2} = \{\langle J, B \rangle\} $$
$$ likes^{\mathcal{I}_2} = \{\langle J, T \rangle\} $$
$$ hasNickname^{\mathcal{I}_2} = \Delta^{\mathcal{I}_2} \times \Delta^{\mathcal{I}_2}$$
$$ favoriteFood^{\mathcal{I}_2} = eats^{\mathcal{I}_2} $$


### 1.2

1. $\Gamma_1$ entails that :Tweety is an animal  

  > 1. :Tweety rdf:type :Penguin - P
  > 2. :Penguin rdfs:subclassOf :Bird - P
  > 3. :Bird rdfs:subclassOf :Animal - P
  > 4. :Penguin rdfs:subclassOf :Animal rdfs11, 2, 3
  > 5. :Tweety rdf:type :Animal rdfs9, 1

  > in short:  

$$\frac{Penguin(Tweety) \;\;\;\; Penguin \sqsubseteq Animal}{Animal(Tweety)}rdfs9$$

2. $\Gamma_1$ does not entail that :Tweety likes :JollyJumper because:
$$\mathcal{I}_1 \models \Gamma_1$$
$$\mathcal{I}_1 \nvDash likes(Tweety, JollyJumper)$$

3. $\Gamma_1$ entails that food is the range of favoriteFood because:  

  if property $a \sqsubseteq b$, $a^\mathcal{I} \subseteq b^\mathcal{I}$
  for any interpretation $\mathcal{I}$  

  That means that every element of $favoriteFood^\mathcal{I}$ exist in $eats^\mathcal{I}$ for any
  interpretation $\mathcal{I}$ where $\mathcal{I} \models \Gamma_1$

  $\forall x \forall y(\langle x, y \rangle \in eats^\mathcal{I} \rightarrow y \in Food^\mathcal{I}) \;\; \because \;\; rg(eats, Food)$  
  $\forall x \forall y(\langle x, y \rangle \in favoriteFood^\mathcal{I} \rightarrow y \in Food^\mathcal{I}) \;\; \because \;\; favoriteFood^\mathcal{I} \subseteq eats^\mathcal{I}$  
  for any interpretation $\mathcal{I}$ where $\mathcal{I} \models \Gamma_1$

So in short:  
$$\frac{rg(eats, Food) \;\;\;\; favoriteFood \sqsubseteq
   eats}{rg(favoriteFood, Food)}$$

4. $\Gamma_1$ does not entail that :Bruce has some favourite food because:
$$\mathcal{I}_1 \models \Gamma_1$$
$$\forall x(\mathcal{I}_1 \nvDash favoriteFood(Bruce, x))$$

5. $\Gamma_1$ does not entail that :Bruce is a vegetable because:
$$\mathcal{I}_1 \models \Gamma_1$$
$$\mathcal{I}_1 \nvDash Vegetable(Bruce)$$

6. $\Gamma_1$ entails that :Bruce is a horse:  

> 1. :Bruce :hasNickname "Alonso" - P  
> 2. :hasNickname rdfs:domain :Horse - P  
> 3. :Bruce rdfs:type :Horse rdfs2, 1, 2  

$$\frac{dom(hasNickname, Horse) \;\;\;\; hasNickname(Bruce, "Alonso")}{Horse(Bruce)}rdfs2$$  


7. $\Gamma^1$ entails that bruce is a fish because it is explicitly stated in the graph:
$$Fish(Bruce) \in \Gamma^1$$
Trivially, statement entails itself  

## 2 Semantic web and reasoning

1. When asking question to a knowledge base, we typically have two ways of interpreting the truth value of the question. With closed world assumption, we assume that all information about the world is contained in the knowledge base, or that the knowledge base is it's own little closed world. With CWA, if something doesn't exist in the knowledge base, it is assumed to not exist in general. With open world assumption, we assume the knowledge base to contain some knowledge about the world. Hence, we can ask general questions concerning the real world, preferring a lack of an answer to an incorrect one. OWA is used in the semantic web as new information can be added or changed in the future, and we do not make any assumption based on lack of information.

2. The Unique Name Assumption is the assumption that the mapping from names to items is injective. In other words, no two names can refer to the same thing. The Non Unique Name Assumption is the assumption that the names might refer to the same things. In the semantic web, we use NUNA because Anyone can say Anything about Anything

3. "Forward rule chaining" and "backwards rule chaining" are methods of reasoning used with an inference engine. The difference between them is simply the direction in which they traverse a chain of implications/entailment rules. With forward chaining we start with our statements, and traverse until a "goal" is reached. That goal being whatever we are trying to find out. With backwards chaining, we start by this goal and traverse backwards, towards the statements we initially have.

4. The way we have defined interpretations of rdfs graphs to model rdfs graphs correspond with the rdfs entailment rules.

5. An rdfs graph can entail more than what is expressed in the rdfs rules. Example being Food is the range of favoriteFood in $\Gamma_1$ from task 1
