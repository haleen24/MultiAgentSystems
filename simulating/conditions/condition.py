from typing import Iterable
from pm4py import PetriNet


class Condition:

    def check(self, trace: set[PetriNet.Transition | str]) -> bool:
        pass

    def still_relevant(self, trace: set[PetriNet.Transition | str]) -> bool:
        pass

    def get_dependent(self) -> Iterable[PetriNet.Transition | str]:
        pass
