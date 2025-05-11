from collections import defaultdict
from ctypes import ArgumentError
from dataclasses import dataclass
from typing import Any, Callable
from matplotlib import pyplot
import numpy as np
from brute_force import brute_force
from dp import dp
from dpll import dpll
from resolution import resolution
from utils import generate_3sat_formula, time
from pandas import DataFrame


@dataclass
class Method:
    name: str
    function: Callable[[Any], bool]
    kwargs: dict[str, Any]


def _plot_methods(methods: list[Method], n_variables: int = 4, runs: int = 100) -> None:
    if n_variables < 4:
        raise ArgumentError("At least 3 variables are required")

    timings = defaultdict(list)
    for variables in range(3, n_variables + 1):
        for method in methods:
            current_timing = []
            for _ in range(runs):
                formula = generate_3sat_formula(variables)
                current_timing.append(time(method.function, formula, **method.kwargs))
            timings[method.name].append(np.mean(current_timing))
        print(variables)

    df = DataFrame(
        {
            **{"Numar de variabile": range(3, n_variables + 1)},
            **{name: timing for name, timing in timings.items()},
        }
    )
    viz = df.plot(
        x="Numar de variabile", title="3-SAT cu ratia de clauza per variabila = 4.26"
    )
    viz.set_ylabel("Timp (secunde)")
    pyplot.show()


def resolution_plots() -> None:
    _plot_methods(
        [
            Method(name="Brute force", function=brute_force, kwargs={}),
            Method(name="Rezolutie", function=resolution, kwargs={}),
        ],
        6,
        1,
    )


def dp_plots() -> None:
    _plot_methods(
        [
            Method(name="Brute force", function=brute_force, kwargs={}),
            Method(name="Rezolutie", function=resolution, kwargs={}),
            Method(name="DP", function=dp, kwargs={}),
        ],
        6,
        1,
    )
    _plot_methods(
        [
            Method(name="Brute force", function=brute_force, kwargs={}),
            Method(name="DP", function=dp, kwargs={}),
        ],
        13,
        10,
    )

    _plot_methods(
        [
            Method(name="DP", function=dp, kwargs={}),
            Method(
                name="Eliminarea clauzelor subsumate",
                function=dp,
                kwargs={"remove_subsumed_clauses": True},
            ),
            Method(
                name="Euristica min-occurence",
                function=dp,
                kwargs={"min_occurence_variable_heuristic": True},
            ),
        ],
        13,
        10,
    )

    _plot_methods(
        [
            Method(name="Brute force", function=brute_force, kwargs={}),
            Method(name="DP", function=dp, kwargs={}),
            Method(
                name="DP cu optimizari",
                function=dp,
                kwargs={
                    "min_occurence_variable_heuristic": True,
                    "remove_subsumed_clauses": True,
                },
            ),
        ],
        13,
        10,
    )

    _plot_methods(
        [
            Method(name="Brute force", function=brute_force, kwargs={}),
            Method(
                name="DP cu optimizari",
                function=dp,
                kwargs={
                    "min_occurence_variable_heuristic": True,
                    "remove_subsumed_clauses": True,
                },
            ),
        ],
        20,
        1,
    )


def dpll_plots() -> None:
    _plot_methods(
        [
            Method(name="DPLL", function=dpll, kwargs={}),
            Method(
                name="DP cu optimizari",
                function=dp,
                kwargs={
                    "min_occurence_variable_heuristic": True,
                    "remove_subsumed_clauses": True,
                },
            ),
        ],
        22,
        10,
    )

    _plot_methods(
        [
            Method(name="DPLL", function=dpll, kwargs={}),
            Method(
                name="DPLL euristica MOM", function=dpll, kwargs={"mom_heuristic": True}
            ),
            Method(
                name="DPLL euristica JW2", function=dpll, kwargs={"jw_heuristic": True}
            ),
            Method(
                name="DPLL euristica MOMsf",
                function=dpll,
                kwargs={"moms_heuristic": True},
            ),
        ],
        60,
        10,
    )
