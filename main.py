import itertools

from resolution import optimised_resolution, resolution

from definitions import Formula
from utils import generate_random_formula, print_cnf, time
import numpy as np
from pandas import DataFrame
from matplotlib import pyplot
import seaborn as sns

sns.set_theme()


def brute_force(formula: Formula) -> bool:
    literals = {lit[0] for clause in formula for lit in clause}

    for seq in itertools.product([True, False], repeat=len(literals)):
        a = frozenset(zip(literals, seq))
        if all([bool(disj.intersection(a)) for disj in formula]):
            return True

    return False


def test_1():
    n_literals = 10
    bf_timings, r_timings, or_timings = [], [], []
    c_bf_timings, c_r_timings, c_or_timings = [], [], []

    for clauses in range(n_literals):
        c_bf_timings, c_r_timings, c_or_timings = [], [], []
        print(clauses)
        for _ in range(100):
            formula = generate_random_formula(
                clauses=clauses + 1, max_literals_per_clause=5, distinct_literals=5
            )
            # print_cnf(formula)
            c_bf_timings.append(time(brute_force, formula))
            c_r_timings.append(time(resolution, formula))
            c_or_timings.append(time(optimised_resolution, formula))

        bf_timings.append(np.mean(c_bf_timings))
        r_timings.append(np.mean(c_r_timings))
        or_timings.append(np.mean(c_or_timings))

    df = DataFrame(
        {
            "Numar de literali": range(n_literals),
            "Brute force": bf_timings,
            "Resolution": r_timings,
            "Optimized resolution": or_timings,
        }
    )

    viz = df.plot(x="Numar de literali", title="maxim 5 literali/clauza")
    viz.set_ylabel("Timp (Secunde)")
    # sns.relplot(data=df, x="Numar de literali")
    pyplot.show()


if __name__ == "__main__":
    test_1()
