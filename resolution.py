from definitions import Clause, Formula
import itertools


def _resolve(a: Clause, b: Clause) -> Formula:
    resolvents = set()
    for var, neg in a:
        complementary = (var, not neg)
        if complementary in b:
            new_clause = frozenset((a - {(var, neg)}) | (b - {complementary}))
            resolvents.add(new_clause)
    return resolvents


def resolution(
    formula: Formula,
) -> bool:
    if any(len(clause) == 0 for clause in formula):
        return False

    clauses = set(formula)
    new = set()

    while True:
        pairs = list(itertools.combinations(clauses, 2))
        for ca, cb in pairs:
            resolvents = _resolve(ca, cb)
            for resolvent in resolvents:
                if not resolvent:
                    return False

            new |= resolvents

        if new <= clauses:
            return True

        clauses |= new
