from itertools import chain
from typing import Iterable

from pm4py import PetriNet

from simulating.conditions.condition import Condition


class SyncCondition(Condition):

    def __init__(self, transitions: Iterable[PetriNet.Transition]):
        self.transitions = set(transitions)
        self.prepositions = set(chain.from_iterable([j.source for j in i.in_arcs] for i in transitions))

    def check(self, trace: set[PetriNet.Transition | str] = None) -> bool:
        return self.prepositions.issubset(trace)

    def still_relevant(self, trace: set[PetriNet.Transition | str]) -> bool:
        return any(i not in trace for i in self.transitions)

    def get_dependent(self) -> Iterable[PetriNet.Transition | str]:
        return self.transitions
