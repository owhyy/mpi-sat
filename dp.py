from collections import Counter, defaultdict
from definitions import Clause, Formula


def _resolve_var(a: Clause, b: Clause, var: str) -> Clause | None:
    if (var, True) in a and (var, False) in b:
        new_clause = (a - {(var, True)}) | (b - {(var, False)})
    elif (var, False) in a and (var, True) in b:
        new_clause = (a - {(var, False)}) | (b - {(var, True)})
    else:
        return None

    if any((var, not neg) in new_clause for var, neg in new_clause):
        return None

    return frozenset(new_clause)


def is_tautology(clause: Clause) -> bool:
    return any((var, True) in clause and (var, False) in clause for var, _ in clause)


def _remove_subsumed_clauses(formula: Formula) -> Formula:
    result = set(formula)
    for c1 in formula:
        for c2 in formula:
            if c1 < c2:
                result.discard(c2)
    return result


def _remove_pure_literals(formula: Formula) -> Formula:
    polarity = defaultdict(set)
    for clause in formula:
        for var, neg in clause:
            polarity[var].add(neg)

    pure_vars = {v for v, signs in polarity.items() if len(signs) == 1}
    return {
        clause for clause in formula if all(var not in pure_vars for var, _ in clause)
    }


def dp(
    formula: Formula,
    remove_tautologies: bool = False,
    remove_subsumed_clauses: bool = False,
    remove_pure_literals: bool = False,
    min_occurence_variable_heuristic: bool = False,
) -> bool:
    if remove_tautologies:
        formula = {clause for clause in formula if not is_tautology(clause)}
    if remove_subsumed_clauses:
        formula = _remove_subsumed_clauses(formula)

    # this does not seem to do anything
    if remove_pure_literals:
        formula = _remove_pure_literals(formula)

    if frozenset() in formula:
        return False
    if not formula:
        return True

    if min_occurence_variable_heuristic:
        count = Counter(var for clause in formula for var, _ in clause)
        var = min(count, key=count.get)
    else:
        var = next(iter(set(lit[0] for clause in formula for lit in clause)))

    pos_clauses = {c for c in formula if (var, True) in c}
    neg_clauses = {c for c in formula if (var, False) in c}

    resolvents = set()
    for a in pos_clauses:
        for b in neg_clauses:
            res = _resolve_var(a, b, var)
            if res is not None:
                resolvents.add(res)

    new_formula = (formula - pos_clauses - neg_clauses) | resolvents
    return dp(
        new_formula, remove_tautologies, remove_subsumed_clauses, remove_pure_literals
    )
