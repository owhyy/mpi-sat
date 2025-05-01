import itertools

from resolution import optimised_resolution, resolution

from definitions import Formula
from utils import generate_random_formula, print_cnf, time


def brute_force(formula: Formula) -> bool:
    literals = {lit[0] for clause in formula for lit in clause}

    for seq in itertools.product([True, False], repeat=len(literals)):
        a = frozenset(zip(literals, seq))
        if all([bool(disj.intersection(a)) for disj in formula]):
            return True

    return False


if __name__ == "__main__":
    formula = generate_random_formula(1000, 100, 20)
    # print_cnf(formula)
    # print(time(brute_force, formula))
    print(time(optimised_resolution, formula))
    # print(time(resolution, formula))

