from typing import Generic, TypeVar, Dict, List
from abc import ABC, abstractmethod

V = TypeVar('V')
D = TypeVar('D')


class Constraint(Generic[V, D], ABC):
    def __init__(self, variables: List[V]) -> None:
        self.variables = variables

    @abstractmethod
    def is_satisfied(self, assignment: Dict[V, D]) -> bool:
        pass

    @abstractmethod
    def get_conflicted(self, assignment: Dict[V, D]) -> List[V]:
        pass
