# mpi-sat

Acest repozitoriu gazduieste codul sursa pentru articolul *O comparatie a performantei metodelor clasice de determinare a satisfiabilitatii*.

Definirea datelor e asemanatoare cu cele din acest [blog](https://davefernig.com/2018/05/07/solving-sat-in-python/). Pentru implementarea metodei brute-force, generarea de formule si crearea graficelor a stat la baza acelasi blog, cu anumite modificari originale. Implementarea rezolutiei este bazata pe definitia rezolutiei din cartea *Logic for Computer Science: Foundations of Automatic Theorem Proving*[^1]. Optimizarile pentru DPLL au fost inspirate din notebook-ul `improving_sat_algorithms`[^2] corespunzatoare cartii *Artificial Intelligence: A Modern Approach* a lui Peter Norvig[^3].

## Reprezentarea formulelor

Formulele sunt reprezentate astfel:
- Un literal este un tuplu format dintr-un string cu structura 'x<numar>' si un bool: `('x12', False)` reprezinta literalul $\neg{x12}$
- O clauza e un set de literali. Pentru simplitate, admitem ca intre toti literali are loc disjunctia: `{('x1', False), ('x2', True), ('x3', False)}` reprezinta clauza $(\neg{x1} \lor x2 \lor \neg{x3})$
- O formula este o lista de seturi de literali. Pentru simplitate, admitem ca toate formulele sunt in CNF (momentan): `[{('x1', True), ('x1', False)}, {('x2', True), ('x3', False)}]` reprezinta clauza $((x1 \lor \neg{x1}) \land (x2 \lor \neg{x3}))$


## Pasii de rulare

Proiectul a fost testat pe Linux, dar procesul de rulare este analogic pe restul sistemelor de operare. Pasii de mai jos sunt prezentati pentru Linux.

1. Verificarea versiunii si asigurarea ca e >= ca 3.10
```sh
$ python3 --version
Python 3.13.3
```

Daca versiunea Python e **mai mica** decat 3.10, trebuie instalata o versiune mai noua. Aceasta se poate face aici: https://www.python.org/downloads/

2. Crearea unui virtual environement si activarea acestuia
```sh
$ cd mpi-sat
$ python3 -m venv venv
$ source venv/bin/activate
```

3. Instalarea dependetelor
```sh
$ pip install -r requirements.txt
```

4. Rularea codului
```sh
$ python3 main.py
```

Daca totul a mers bine, testele ar trebui sa ruleze, si graficele ar trebui sa se deschida. Outputul din linia de comanda va indica testul curent care se ruleaza. In dependenta de performanta calculatorului, acest lucru poate dura cateva secunde.

Graficele din articol au fost facute pe un calculator cu Intel i5-4300M @ 3.300GHz si 8GB RAM. Este posibil ca pe alte specificatii, valorile timpulului din grafice sa difere, dar tendintele graficului ar trebui sa fie aproximativ aceleasi.


[^1]: Logic for Computer Science: Foundations of Automatic Theorem Proving, Jean H. Gallier, 2003. Definitia rezolutiei pe care am folosit-o poate fi gasita la capitolul 4.3.2
[^2]: https://github.com/aimacode/aima-python/blob/master/improving_sat_algorithms.ipynb
[^3]: https://aima.cs.berkeley.edu/
