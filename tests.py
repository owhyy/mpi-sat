from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Callable
from matplotlib import pyplot
import numpy as np
from brute_force import brute_force
from dp import dp
from dpll import dpll
from resolution import resolution
from utils import generate_random_formula, time
from pandas import DataFrame


@dataclass
class Method:
    name: str
    function: Callable[[Any], bool]
    kwargs: dict[str, Any]


def _clause_based_test_df(
    n_clauses: int,
    max_literals_per_clause: int,
    distinct_literals: int,
    methods: list[Method],
) -> DataFrame:
    timings = defaultdict(list)
    for clauses in range(n_clauses):
        print(clauses)
        for method in methods:
            current_timing = []
            for _ in range(100):
                formula = generate_random_formula(
                    clauses=clauses + 1,
                    max_literals_per_clause=max_literals_per_clause,
                    distinct_literals=distinct_literals,
                )
                current_timing.append(time(method.function, formula, **method.kwargs))
            timings[method.name].append(np.mean(current_timing))

    return DataFrame(
        {
            **{"Numar de clauze": range(n_clauses)},
            **{name: timing for name, timing in timings.items()},
        }
    )


def plot_general_method_comparison():
    methods = [
        # Method(name="Brute force", function=brute_force, kwargs={}),
        # Method(name="Rezolutie neoptimizata", function=resolution, kwargs={}),
        Method(
            name="Rezolutie optimizata",
            function=resolution,
            kwargs={
                "remove_redundant_literals": True,
                "sort_clauses_by_len": True,
                "ignore_tautologies": True,
                "ignore_resolvent": True,
            },
        ),
        Method(name="DP neoptimizat", function=dp, kwargs={}),
        Method(
            name="DP optimizat",
            function=dp,
            kwargs={
                "remove_tautologies": True,
                "remove_subsumed_clauses": True,
                "remove_pure_literals": True,
                "min_occurence_variable_heuristic": True,
            },
        ),
        Method(
            name="DPLL",
            function=dpll,
            kwargs={},
        ),
        Method(
            name="DPLL Optimizat",
            function=dpll,
            kwargs={
                "remove_subsumed_clauses": True,
                "failed_literal_detection": False,
                "shortest_clause_heuristic": True,
            },
        ),
    ]
    df1 = _clause_based_test_df(
        n_clauses=100,
        max_literals_per_clause=100,
        distinct_literals=30,
        methods=methods,
    )
    viz = df1.plot(x="Numar de clauze", title="maxim 10 literali/clauza")
    viz.set_ylabel("Timp (secunde)")
    pyplot.show()


def plot_resolution_optimizations():
    methods = [
        Method(name="Rezolutie neoptimizata", function=resolution, kwargs={}),
        Method(
            name="Eliminarea literalilor redundanti",
            function=resolution,
            kwargs={"remove_redundant_literals": True},
        ),
        Method(
            name="Euristica min-length",
            function=resolution,
            kwargs={"sort_clauses_by_len": True},
        ),
        Method(
            name="Ignorarea tautologiilor",
            function=resolution,
            kwargs={"ignore_tautologies": True},
        ),
        Method(
            name="Ignorarea resolventului",
            function=resolution,
            kwargs={"ignore_resolvent": True},
        ),
    ]
    df1 = _clause_based_test_df(
        n_clauses=1000,
        max_literals_per_clause=10,
        distinct_literals=10,
        methods=methods,
    )
    viz = df1.plot(x="Numar de clauze", title="maxim 10 literali/clauza")
    viz.set_ylabel("Timp (secunde)")
    pyplot.show()

    df2 = _clause_based_test_df(
        n_clauses=100,
        max_literals_per_clause=100,
        distinct_literals=100,
        methods=methods,
    )
    viz = df2.plot(x="Numar de clauze", title="maxim 100 literali/clauza")
    viz.set_ylabel("Timp (secunde)")
    pyplot.show()

    df3 = _clause_based_test_df(
        n_clauses=100,
        max_literals_per_clause=1000,
        distinct_literals=1000,
        methods=methods,
    )
    viz = df3.plot(x="Numar de clauze", title="maxim 1000 literali/clauza")
    viz.set_ylabel("Timp (secunde)")
    pyplot.show()


def plot_dp_optimizations():
    methods = [
        Method(name="DP neoptimizat", function=dp, kwargs={}),
        Method(
            name="Eliminarea tautologiilor",
            function=dp,
            kwargs={"remove_tautologies": True},
        ),
        Method(
            name="Eliminarea clauzelor subsumate",
            function=dp,
            kwargs={"remove_subsumed_clauses": True},
        ),
        Method(
            name="Eliminarea literalilor puri",
            function=dp,
            kwargs={"remove_pure_literals": True},
        ),
        Method(
            name="Euristica min-occurence",
            function=dp,
            kwargs={"min_occurence_variable_heuristic": True},
        ),
    ]
    df1 = _clause_based_test_df(
        n_clauses=100, max_literals_per_clause=10, distinct_literals=10, methods=methods
    )
    viz = df1.plot(x="Numar de clauze", title="maxim 10 literali/clauza")
    viz.set_ylabel("Timp (secunde)")
    pyplot.show()

    df2 = _clause_based_test_df(
        n_clauses=100,
        max_literals_per_clause=100,
        distinct_literals=20,
        methods=methods,
    )
    viz = df2.plot(x="Numar de clauze", title="maxim 100 literali/clauza")
    viz.set_ylabel("Timp (secunde)")
    pyplot.show()

    df3 = _clause_based_test_df(
        n_clauses=100,
        max_literals_per_clause=1000,
        distinct_literals=20,
        methods=methods,
    )
    viz = df3.plot(x="Numar de clauze", title="maxim 1000 literali/clauza")
    viz.set_ylabel("Timp (secunde)")
    pyplot.show()


def plot_dpll_optimizations():
    methods = [
        Method(name="DPLL neoptimizat", function=dpll, kwargs={}),
        Method(
            name="Eliminarea clauzelor subsumate",
            function=dpll,
            kwargs={"remove_subsumed_clauses": True},
        ),
        Method(
            name="Detectarea literalilor esuati",
            function=dpll,
            kwargs={"failed_literal_detection": True},
        ),
        Method(
            name="Euristica shortest-clause",
            function=dpll,
            kwargs={"shortest_clause_heuristic": True},
        ),
    ]
    df1 = _clause_based_test_df(
        n_clauses=100, max_literals_per_clause=10, distinct_literals=10, methods=methods
    )
    viz = df1.plot(x="Numar de clauze", title="maxim 10 literali/clauza")
    viz.set_ylabel("Timp (secunde)")
    pyplot.show()

    df2 = _clause_based_test_df(
        n_clauses=100,
        max_literals_per_clause=100,
        distinct_literals=20,
        methods=methods,
    )
    viz = df2.plot(x="Numar de clauze", title="maxim 100 literali/clauza")
    viz.set_ylabel("Timp (secunde)")
    pyplot.show()

    df3 = _clause_based_test_df(
        n_clauses=100,
        max_literals_per_clause=1000,
        distinct_literals=20,
        methods=methods,
    )
    viz = df3.plot(x="Numar de clauze", title="maxim 1000 literali/clauza")
    viz.set_ylabel("Timp (secunde)")
    pyplot.show()
