import itertools

from definitions import Formula


def brute_force(formula: Formula) -> bool:
    literals = {lit[0] for clause in formula for lit in clause}

    for seq in itertools.product([True, False], repeat=len(literals)):
        a = frozenset(zip(literals, seq))
        if all([bool(disj.intersection(a)) for disj in formula]):
            return True

    return False
