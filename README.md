# mpi-sat

Acest repozitoriu gazduieste codul pentru articolul "<nume articol>".

Definirea datelor e identica cu cele din acest [blog](https://davefernig.com/2018/05/07/solving-sat-in-python/). Pentru implementarea metodei brute-force, generarea de formule si crearea graficelor a stat la baza acelasi blog, cu anumite modificari. Implementarea rezolutiei este bazata pe definitia rezolutiei din cartea *Logic for Computer Science: Foundations of Automatic Theorem Proving*[^1].

## Reprezentarea formulelor

Formulele sunt reprezentate astfel:
- Un literal este un tuplu format dintr-un string si un bool: `('a', False)` reprezinta literalul $\neg{a}$
- O clauza e un set de literali. Pentru simplitate, admitem ca intre toti literali are loc disjunctia: `{('a', False), ('b', True), ('c', False)}` reprezinta clauza $(\neg{a} \lor b \lor \neg{c})$
- O formula este o lista de seturi de literali. Pentru simplitate, admitem ca toate formulele sunt in CNF (momentan): `[{('a', True), ('a', False)}, {('b', True), ('c', False)}]` reprezinta clauza $((a \lor \neg{a}) \land (b \lor \neg{c}))$


## Pasii de rulare

Proiectul a fost testat pe linux, dar procesul de rulare este analogic pe restul sistemelor de operare.

1. Verificarea versiunii si asigurarea ca e >= decat 3.10
`$ python3 --version`
`Python 3.13.3`

Daca versiunea Python e **mai mica** decat 3.10, trebuie instalata o versiune mai noua. Aceasta se poate face aici: https://www.python.org/downloads/

2. Crearea unui virtual environement si activarea acestuia
`$ cd mpi-sat`
`$ python3 -m venv venv`
`$ source venv/bin/activate`

3. Instalarea dependetelor
`$ pip install -r requirements.txt`

4. Rularea codului
`python3 main.py`

Daca totul a mers bine, testele ar trebui sa ruleze, si graficele ar trebui sa se deschida. Outputul din linia de comanda va indica testul curent care se ruleaza. In dependenta de performanta calculatorului, acest lucru poate dura cateva secunde.

[^1]: Logic for Computer Science: Foundations of Automatic Theorem Proving, Jean H. Gallier, 2003. Definitia rezolutiei pe care am folosit-o poate fi gasita la capitolul 4.3.2
