from typing import Generic, List, Tuple, Dict
from constraint import V, D, Constraint
from state import State


class CSP(Generic[V, D]):
    def __init__(self, variables: List[V], domains: Dict[V, List[D]]) -> None:
        self.variables: List[V] = variables
        self.domains: Dict[V, List[D]] = domains
        self.constraints: Dict[V, List[Constraint[V, D]]] = {}
        self.current_state: State[V, D] = State[V, D]({})
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError('Each variable must have a domain associated with it')

    def add_constraint(self, constraint: Constraint[V, D]) -> None:
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError('Invalid Constraint: some variable not in CSP')
            else:
                self.constraints[variable].append(constraint)

    def consistent(self, variable: V, value: D):  # used for other algorithms. maybe?
        state: State[V, D] = self.current_state.next_state(variable, value)
        for constraint in self.constraints[variable]:
            if not constraint.is_satisfied(state.assignment):
                return False
        return True

    def conflicted(self) -> List[V]:
        conflicted_variables: List[V] = []
        for variable in self.variables:
            for constraint in self.constraints[variable]:
                local_conflicted_variables = constraint.get_conflicted(self.current_state.assignment)
                conflicted_variables.extend(local_conflicted_variables)
        return list(set(conflicted_variables))

    def conflict_value(self, variable: V, value: D) -> int:
        state = self.current_state.next_state(variable, value)
        # conflicted_variables: List[V] = []
        count = 0
        for constraint in self.constraints[variable]:
            if not constraint.is_satisfied(state.assignment):
                count = count + 1
        return count
