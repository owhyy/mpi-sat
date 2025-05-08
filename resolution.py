from definitions import Clause, Formula
import itertools


def _resolve(a: Clause, b: Clause, ignore_tautologies: bool = False) -> Formula:
    resolvents = set()
    for var, neg in a:
        complementary = (var, not neg)
        if complementary in b:
            new_clause = frozenset((a - {(var, neg)}) | (b - {complementary}))
            # Ignore clauses that include tautologies -- they are always true
            if ignore_tautologies and any(
                (var, True) in new_clause and (var, False) in new_clause
                for var, _ in new_clause
            ):
                continue

            resolvents.add(new_clause)
    return resolvents


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


def resolution(
    formula: Formula,
    remove_redundant_literals: bool = False,    
    sort_clauses_by_len: bool = False,
    ignore_tautologies: bool = False,
    ignore_resolvent: bool = False,    
) -> bool:
    if any(len(clause) == 0 for clause in formula):
        return False

    clauses = set(formula)
    new = set()

    if remove_redundant_literals:
        clauses = _remove_redundant_literals(formula)

    ordered_clauses = list(clauses)
    if sort_clauses_by_len:
        ordered_clauses = list(sorted(clauses, key=len))

    while True:
        pairs = list(itertools.combinations(ordered_clauses, 2))
        for ca, cb in pairs:
            resolvents = _resolve(ca, cb, ignore_tautologies)
            for resolvent in resolvents:
                if not resolvent:
                    return False

                if ignore_resolvent and resolvent in [clauses, new]:
                    continue

            new |= resolvents

        if new <= clauses:
            return True

        clauses |= new
