from typing import Iterable

from simulating.conditions.condition import Condition
from pm4py import PetriNet


class OccursBeforeCondition(Condition):
    def __init__(self, a: PetriNet.Transition | str, b: PetriNet.Transition | str):
        self.a = a
        self.b = b

    def check(self, trace: dict[PetriNet.Transition | str, int]) -> bool:
        return self.a in trace

    def still_relevant(self, trace: dict[PetriNet.Transition | str, int]) -> bool:
        return self.b not in trace

    def get_dependent(self) -> Iterable[PetriNet.Transition | str]:
        return [self.b]
