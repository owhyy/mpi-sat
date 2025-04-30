# mpi-sat

Acest repozitoriu gazduieste codul pentru articolul "<nume articol>".

Codul e bazat in mare parte pe acest [blog](https://davefernig.com/2018/05/07/solving-sat-in-python/), cu aditia metodelor DP si a rezolutie.

Pentru a reprezenta clauzele folosesc urmatoarea reprezentare:
- Un literal este un tuplu format dintr-un string si un bool: `('a', False)` reprezinta literalul $\neg{a}$
- O clauza e un set de literali. Pentru simplitate, admitem ca intre toti literali are loc disjunctia: `{('a', False), ('b', True), ('c', False)}` reprezinta clauza $(\neg{a} \lor b \lor \neg{c})$
- O formula este o lista de seturi de literali. Pentru simplitate, admitem ca toate formulele sunt in CNF (momentan): `[{('a', True), ('a', False)}, {('b', True), ('c', False)}]` reprezinta clauza $((a \lor \neg{a}) \land (b \lor \neg{c}))$
