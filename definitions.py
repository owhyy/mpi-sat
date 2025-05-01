from typing import FrozenSet, Set, Tuple

Literal = Tuple[str, bool]
Clause = FrozenSet[Literal]
Formula = Set[Clause]
