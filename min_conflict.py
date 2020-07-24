from typing import Generic, Optional, List, Tuple, Dict
import random
from csp import CSP
from constraint import V, D
from state import State
import time

class MinConflict(Generic[V, D]):
    def __init__(self, csp: CSP[V, D], initial_state: State[V, D], max_steps: int) -> None:
        self.csp: CSP[V, D] = csp
        self.csp.current_state = initial_state
        self.max_steps: int = max_steps
        for variable in csp.variables:
            if variable not in initial_state.assignment:
                raise LookupError('Initial State should be full')

    def solve(self) -> Tuple[Optional[State[V, D]], List[Dict[str, object]], float]:
        start_time = time.time()
        csp = self.csp
        history: List[State[V, D]] = [csp.current_state]
        maxHistorySize = 15
        steps: List[Dict[str, object]] = []
        for i in range(self.max_steps):
            conflicted_variables = self.csp.conflicted()
            if not conflicted_variables:
                return csp.current_state, steps, time.time() - start_time
            choice: V = random.choice(conflicted_variables)
            _: int
            best_value: D
            possible_values = [(csp.conflict_value(choice, value), value) for value in csp.domains[choice]]

            col, best_value = min(possible_values, key=lambda x: (x[0], random.random))
            new_values = possible_values.copy()
            while new_values and history.count(csp.current_state.next_state(choice, best_value)) > 3:  # repeat too many time?
                new_values.remove((col, best_value))
                col, best_value = min(new_values, key=lambda x: (x[0], random.random))  # find a new best_value
            steps.append({"choice": {"x": choice+1, "y": best_value+1}, "conflicts": [{"position": {"x": choice+1, "y": i + 1}, "value": value[0]} for i, value in enumerate(possible_values)]})
            csp.current_state = csp.current_state.next_state(choice, best_value)
            if len(history) == maxHistorySize:  # enforce recent 10 histories
                history = history[1:] + [csp.current_state]
            else:
                history.append(csp.current_state)
        return None, steps, time.time() - start_time
