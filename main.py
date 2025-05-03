import itertools

from resolution import optimised_resolution, resolution
from dp import dp

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


def dp_optimization_tests():
    n_literals = 200
    dp_timings, rt_timings, rsc_timings, rpl_timings, movh_timings = [], [], [], [], []
    c_dp_timings, c_rt_timings, c_rsc_timings, c_rpl_timings, c_movh_timings = [], [], [], [], []  # fmt: skip

    for clauses in range(n_literals):
        c_dp_timings, c_rt_timings, c_rsc_timings, c_rpl_timings, c_movh_timings = [], [], [], [], []  # fmt: skip
        print(clauses)
        for _ in range(100):
            formula = generate_random_formula(
                clauses=clauses + 1, max_literals_per_clause=10, distinct_literals=10
            )
            c_dp_timings.append(time(dp, formula))
            c_rt_timings.append(time(dp, formula, remove_tautologies=True))
            c_rsc_timings.append(time(dp, formula, remove_subsumed_clauses=True))
            c_rpl_timings.append(time(dp, formula, remove_pure_literals=True))
            c_movh_timings.append(
                time(dp, formula, min_occurence_variable_heuristic=True)
            )

        dp_timings.append(np.mean(c_dp_timings))
        rt_timings.append(np.mean(c_rt_timings))
        rsc_timings.append(np.mean(c_rsc_timings))
        rpl_timings.append(np.mean(c_rpl_timings))
        movh_timings.append(np.mean(c_rpl_timings))

    df = DataFrame(
        {
            "Numar de literali": range(n_literals),
            "DP Neoptimizat": dp_timings,
            "Eliminarea tautologiilor": rt_timings,
            "Eliminarea cauzelor subsumate": rsc_timings,
            "Eliminarea literalilor puri": rpl_timings,
            "Euristica min-occurence": movh_timings,
        }
    )

    viz = df.plot(x="Numar de literali", title="maxim 5 literali/clauza")
    viz.set_ylabel("Timp (Secunde)")
    pyplot.show()


def test_1():
    n_literals = 50
    bf_timings, or_timings, dp_timings = [], [], []
    c_bf_timings, c_or_timings, dp_timings = [], [], []

    for clauses in range(n_literals):
        c_bf_timings, c_or_timings, c_dp_timings = [], [], []
        print(clauses)
        for _ in range(100):
            formula = generate_random_formula(
                clauses=clauses + 1, max_literals_per_clause=15, distinct_literals=10
            )
            # print_cnf(formula)
            c_bf_timings.append(time(brute_force, formula))
            c_or_timings.append(time(optimised_resolution, formula))
            c_dp_timings.append(time(dp, formula))

        bf_timings.append(np.mean(c_bf_timings))
        or_timings.append(np.mean(c_or_timings))
        dp_timings.append(np.mean(c_dp_timings))

    df = DataFrame(
        {
            "Numar de literali": range(n_literals),
            "Brute force": bf_timings,
            "DP timings": dp_timings,
            "Optimized DP timings": dp_timings,
            "Optimized resolution": or_timings,
        }
    )

    viz = df.plot(x="Numar de literali", title="maxim 5 literali/clauza")
    viz.set_ylabel("Timp (Secunde)")
    pyplot.show()


if __name__ == "__main__":
    dp_optimization_tests()
