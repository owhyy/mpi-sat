from definitions import Formula, Literal
from collections import defaultdict, Counter


def _simplify_formula(formula: Formula, assignment: dict[str, bool]) -> Formula:
    new_formula = set()
    for clause in formula:
        if any(assignment.get(var) == sign for var, sign in clause):
            continue
        new_formula.add(
            frozenset((var, sign) for var, sign in clause if var not in assignment)
        )
    return new_formula


def _find_unit_clause_literals(formula: Formula) -> list[Literal]:
    return [next(iter(clause)) for clause in formula if len(clause) == 1]


def _find_pure_literals(formula: Formula, assignment: dict[str, bool]) -> list[Literal]:
    polarity = defaultdict(set)
    for clause in formula:
        for var, sign in clause:
            if var in assignment:
                continue
            polarity[var].add(sign)
    return [(v, signs.pop()) for v, signs in polarity.items() if len(signs) == 1]


def _mom_heuristic_literal(formula: Formula, assignment: dict[str, bool]) -> Literal:
    min_size = min(
        len(clause)
        for clause in formula
        if any(var not in assignment for var, _ in clause)
    )
    literal_count = defaultdict(int)

    for clause in formula:
        if len(clause) != min_size:
            continue
        for var, sign in clause:
            if var not in assignment:
                literal_count[(var, sign)] += 1

    if not literal_count:
        return next(
            (var, True)
            for clause in formula
            for var, _ in clause
            if var not in assignment
        )

    return max(literal_count.items(), key=lambda x: x[1])[0]


def _jw2_heuristic(formula: Formula, assignment: dict[str, bool]) -> Literal:
    scores = Counter()
    for clause in formula:
        if any(var in assignment for var, _ in clause):
            continue
        for var, sign in clause:
            if var not in assignment:
                scores[(var, sign)] += 2 ** (-len(clause))

    symbols = {var for var, _ in scores}
    best_var = max(symbols, key=lambda v: scores[(v, True)] + scores[(v, False)])
    sign = True if scores[(best_var, True)] >= scores[(best_var, False)] else False
    return best_var, sign


def _momsf_heuristic(
    formula: Formula, assignment: dict[str, bool], k: int = 0
) -> Literal:
    min_size = min(
        len(clause)
        for clause in formula
        if any(var not in assignment for var, _ in clause)
    )
    scores = Counter()

    for clause in formula:
        if len(clause) != min_size:
            continue
        for var, sign in clause:
            if var not in assignment:
                scores[(var, sign)] += 2 ** (-len(clause))

    best_var = max(
        scores,
        key=lambda l: scores[l]
        + scores[(l[0], not l[1])] * 2**k
        + scores[l] * scores[(l[0], not l[1])],
    )
    sign = True if scores[best_var] >= scores[(best_var[0], not best_var[1])] else False
    return best_var[0], sign


def dpll(
    formula: Formula,
    mom_heuristic: bool = False,
    jw_heuristic: bool = False,
    moms_heuristic: bool = False,
    k: int = 0,
) -> bool:
    def _dpll(
        formula: Formula,
        assignment: dict[str, bool],
    ) -> bool:
        formula = _simplify_formula(formula, assignment)

        if not formula:
            return True
        if any(not clause for clause in formula):
            return False

        new_assignment = assignment.copy()
        literals = _find_unit_clause_literals(formula) or _find_pure_literals(
            formula, assignment
        )
        if literals:
            new_assignment.update(literals)
            return _dpll(formula, new_assignment)

        if moms_heuristic:
            var, sign = _momsf_heuristic(formula, assignment, k)
        elif jw_heuristic:
            var, sign = _jw2_heuristic(formula, assignment)
        elif mom_heuristic:
            var, sign = _mom_heuristic_literal(formula, assignment)
        else:
            var = next(var for c in formula for var, _ in c if var not in assignment)
            sign = True

        return _dpll(formula, {**new_assignment, var: sign}) or _dpll(
            formula, {**new_assignment, var: not sign}
        )

    return _dpll(formula, {})
