# mpi-sat

Acest repozitoriu gazduieste codul pentru articolul "<nume articol>".

Definirea datelor e identica cu cele din acest [blog](https://davefernig.com/2018/05/07/solving-sat-in-python/). Pentru implementarea metodei brute-force, generarea de formule si crearea graficelor a stat la baza acelasi blog, cu anumite modificari. Implementarea rezolutiei este bazata pe definitia rezolutiei din cartea *Logic for Computer Science: Foundations of Automatic Theorem Proving*[^1].

# Reprezentarea formulelor

Formulele sunt reprezentate astfel:
- Un literal este un tuplu format dintr-un string si un bool: `('a', False)` reprezinta literalul $\neg{a}$
- O clauza e un set de literali. Pentru simplitate, admitem ca intre toti literali are loc disjunctia: `{('a', False), ('b', True), ('c', False)}` reprezinta clauza $(\neg{a} \lor b \lor \neg{c})$
- O formula este o lista de seturi de literali. Pentru simplitate, admitem ca toate formulele sunt in CNF (momentan): `[{('a', True), ('a', False)}, {('b', True), ('c', False)}]` reprezinta clauza $((a \lor \neg{a}) \land (b \lor \neg{c}))$


[^1]: Logic for Computer Science: Foundations of Automatic Theorem Proving, Jean H. Gallier, 2003. definitia rezolutiei pe care am folosit-o poate fi gasita la capitolul 4.3.2