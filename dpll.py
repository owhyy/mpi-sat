from definitions import Formula, Literal
from collections import defaultdict


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


def _failed_literal_detection(
    formula: Formula, assignment: dict[str, bool]
) -> list[Literal]:
    literals = set(
        (var, sign)
        for clause in formula
        for var, sign in clause
        if var not in assignment
    )
    failed_literals = []
    for var, sign in literals:
        test_assignment = assignment.copy()
        test_assignment[var] = sign
        simplified = _simplify_formula(formula, test_assignment)
        if any(not clause for clause in simplified):
            failed_literals.append((var, not sign))
    return failed_literals


def _shortest_clause_literal(formula: Formula, assignment: dict[str, bool]) -> Literal:
    shortest = min(
        (
            clause
            for clause in formula
            if any(var not in assignment for var, _ in clause)
        ),
        key=len,
    )
    for lit in shortest:
        if lit[0] not in assignment:
            return lit
    return next(var for clause in formula for var in clause if var[0] not in assignment)


def _remove_subsumed_clauses(formula: Formula) -> Formula:
    result = set(formula)
    for c1 in formula:
        for c2 in formula:
            if c1 != c2 and c1 <= c2:
                result.discard(c2)
    return result


def dpll(
    formula: Formula,
    remove_subsumed_clauses: bool = False,
    failed_literal_detection: bool = False,
    shortest_clause_heuristic: bool = False,
) -> bool:
    def _dpll(
        formula: Formula,
        assignment: dict[str, bool],
        remove_subsumed_clauses: bool,
        failed_literal_detection: bool,
        shortest_clause_heuristic: bool,
    ) -> bool:
        if remove_subsumed_clauses:
            formula = _remove_subsumed_clauses(formula)
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
            return _dpll(
                formula,
                new_assignment,
                remove_subsumed_clauses,
                failed_literal_detection,
                shortest_clause_heuristic,
            )

        if failed_literal_detection and (
            failed_literals := _failed_literal_detection(formula, assignment)
        ):
            new_assignment.update(failed_literals)
            return _dpll(
                formula,
                new_assignment,
                remove_subsumed_clauses,
                failed_literal_detection,
                shortest_clause_heuristic,
            )

        var, sign = (
            _shortest_clause_literal(formula, assignment)
            if shortest_clause_heuristic
            else (
                next(var for c in formula for var, _ in c if var not in assignment),
                True,
            )
        )
        return _dpll(
            formula,
            {**new_assignment, var: sign},
            remove_subsumed_clauses,
            failed_literal_detection,
            shortest_clause_heuristic,
        ) or _dpll(
            formula,
            {**new_assignment, var: not sign},
            remove_subsumed_clauses,
            failed_literal_detection,
            shortest_clause_heuristic,
        )

    return _dpll(
        formula,
        {},
        remove_subsumed_clauses,
        failed_literal_detection,
        shortest_clause_heuristic,
    )
