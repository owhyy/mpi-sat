from timeit import default_timer
from definitions import Clause, Formula, Literal
import string
import random


def time(f, *args, **kwargs):
    s = default_timer()
    f(*args, **kwargs)
    e = default_timer()
    return e - s


def clause_to_str(clause: Clause) -> str:
    return " ∨ ".join(f"¬{var}" if is_negated else var for var, is_negated in clause)


def print_cnf(formula: Formula) -> None:
    cnf_str = " ∧\n".join(f"({clause_to_str(clause)})" for clause in formula)
    print(cnf_str if cnf_str else "Empty formula")


def generate_literal(max_char: int) -> Literal:
    return (
        random.choice(string.ascii_lowercase[:max_char]),
        random.choice([True, False]),
    )


def generate_random_clause(max_literals: int, distinct_literals: int) -> Clause:
    literals_to_generate = random.randint(1, max_literals)
    return frozenset(
        generate_literal(distinct_literals) for _ in range(literals_to_generate)
    )


def generate_random_formula(
        clauses: int, max_literals_per_clause: int, distinct_literals: int = 10
) -> Formula:
    return set(
        generate_random_clause(max_literals_per_clause, distinct_literals)
        for _ in range(clauses)
    )

