from typing import Iterable

from simulating.condition import Condition
from pm4py import PetriNet


class OccursBeforeCondition(Condition):
    def __init__(self, a: PetriNet.Transition | str, b: PetriNet.Transition | str):
        self.a = a
        self.b = b

    def check(self, trace: list[PetriNet.Transition | str]) -> bool:
        return self.a in trace

    def still_relevant(self, trace: list[PetriNet.Transition | str]) -> bool:
        return self.b in trace

    def get_dependent(self) -> Iterable[PetriNet.Transition | str]:
        return [self.b]
