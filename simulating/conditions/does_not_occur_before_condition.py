from typing import Iterable

from pm4py import PetriNet

from simulating.conditions.condition import Condition


class DoesNotOccurBeforeCondition(Condition):
    def __init__(self, a: PetriNet.Transition, b: PetriNet.Transition):
        self.a = a
        self.b = b

    def check(self, trace: set[PetriNet.Transition | str]) -> bool:
        return self.a not in trace

    def still_relevant(self, trace: set[PetriNet.Transition | str]) -> bool:
        return self.b not in trace

    def get_dependent(self) -> Iterable[PetriNet.Transition | str]:
        return [self.b]
