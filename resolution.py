from definitions import Clause, Formula
import itertools


def _resolve(a: Clause, b: Clause) -> Formula:
    resolvents = set()
    for var, neg in a:
        complementary = (var, not neg)
        if complementary in b:
            resolvents.add(frozenset((a - {(var, neg)}) | (b - {complementary})))
    return resolvents


def resolution(formula: Formula) -> bool:
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


def _remove_redundant_literals(clauses: Formula) -> Formula:
    new_clauses = set()
    for clause in clauses:
        simplified = set()
        seen = set()
        for var, neg in clause:
            if (var, not neg) not in seen:
                simplified.add((var, neg))
                seen.add((var, neg))
        new_clauses.add(frozenset(simplified))
    return new_clauses


def _optimized_resolve(a: Clause, b: Clause):
    resolvents = set()
    for var, neg in a:
        complementary = (var, not neg)
        if complementary in b:
            new_clause = frozenset((a - {(var, neg)}) | (b - {complementary}))
            # Ignore clauses that include tautologies -- they are always true
            if any(
                (var, True) in new_clause and (var, False) in new_clause
                for var, _ in new_clause
            ):
                continue

            resolvents.add(new_clause)
    return resolvents


def optimised_resolution(formula: Formula) -> bool:
    if any(len(clause) == 0 for clause in formula):
        return False

    clauses = _remove_redundant_literals(formula)
    ordered_clauses = list(sorted(clauses, key=len))
    new = set()

    while True:
        pairs = list(itertools.combinations(ordered_clauses, 2))
        for ca, cb in pairs:
            resolvents = _optimized_resolve(ca, cb)
            for resolvent in resolvents:
                if not resolvent:
                    return False

                if resolvent in [clauses, new]:
                    continue

            new |= resolvents

        if new <= clauses:
            return True

        clauses |= new
