from collections import defaultdict
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


def _plot_methods(
    methods: list[Method], n_variables: int, runs: int = 100
) -> DataFrame:
    timings = defaultdict(list)
    for variables in range(n_variables):
        print(variables)
        for method in methods:
            current_timing = []
            for _ in range(runs):
                formula = generate_3sat_formula(3 + variables)
                current_timing.append(time(method.function, formula, **method.kwargs))
            timings[method.name].append(np.mean(current_timing))

    df = DataFrame(
        {
            **{"Numar de variabile": map(lambda x: int(x + 3), range(n_variables))},
            **{name: timing for name, timing in timings.items()},
        }
    )
    viz = df.plot(x="Numar de variabile", title="3 SAT cu ratia 4.26/Clauza")
    viz.set_ylabel("Timp (secunde)")
    pyplot.show()


def plot_bf_vs_resolution(n_variables: int):
    _plot_methods(
        [
            Method(name="Brute force", function=brute_force, kwargs={}),
            Method(name="Rezolutie", function=resolution, kwargs={}),
        ],
        n_variables,
        10,
    )


def plot_dpll_heuristics(n_variables: int):
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
                name="DPLL euristica MOMsf cu k = 0",
                function=dpll,
                kwargs={"moms_heuristic": True},
            ),
        ],
        n_variables,
        100,
    )
