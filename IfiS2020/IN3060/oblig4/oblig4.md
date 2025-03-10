
# Oblig 4  

#### markuhei - Markus Sverdvik Heiervang  
***

### 2.1

1: yes

2: yes, the derivation is  
fam:hasSister rdfs:subPropertyOf fam:hasSibling - P  
fam:hasSibling rdfs:subPropertyOf fam:isRelativeOf - P  
fam:hasSister rdfs:subPropertyOf fam:isRelativeOf - rdfsX, 5  

3: no  
4: yes, the derivation is:  
sim:lisa fam:hasParent [
  fam:hasBrother sim:Herb
] - P  
fam:hasBrother rdfs:range fam:Man rdfsX, 3  
5: yes, the derivation is:  
sim:Lisa fam:hasFather sim:Homer - P  
fam:hasFather rdfs:subPropertyOf fam:hasParent - P
fam:hasParent rdfs:subPropertyOf fam:isRelativeOf - P
sim:Lisa fam:isRelativeOf sim:Homer rdfsX, 5, 7
6: no  
7: yes, the derivation is:  
sim:Lisa fam:hasParent [ fam:hasSister sim:Patty ] - P  
fam:hasSister rdfs:range foaf:Person - P  
sim:Patty a foaf:Person rdfsX, 3  
