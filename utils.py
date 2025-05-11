from timeit import default_timer
from definitions import Clause, Formula
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


def generate_3sat_clause(distinct_literals: int) -> Clause:
    variables = random.sample(range(distinct_literals), 3)
    return frozenset((f"x{var}", random.choice([True, False])) for var in variables)


def generate_3sat_formula(num_variables: int) -> Formula:
    # 4.26 for phase transition    
    # see https://en.wikipedia.org/wiki/Boolean_satisfiability_problem#3-satisfiability
    num_clauses = int(4.26 * num_variables) 
    return set(generate_3sat_clause(num_variables) for _ in range(num_clauses))
