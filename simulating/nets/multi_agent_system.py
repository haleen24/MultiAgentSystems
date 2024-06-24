from pm4py import PetriNet
from pm4py import Marking
from random import choice

from simulating.condition import Condition
from itertools import chain


class MultiAgentSystem:
    def __init__(self, nets: list[PetriNet], tokens: list[Marking], conditions: list[Condition]):
        self.nets = nets
        self.tokens = [set(i.keys()) for i in tokens]
        self.trace = []
        self.conditions = conditions

    def step(self, places: set[PetriNet.Place], banned: set[PetriNet.transitions]) -> bool:
        flag = False
        new_places = places.copy()
        for i in places:
            allowed_transitions = [j.target for j in i.out_arcs if
                                   j.target not in banned and set(k.source for k in j.target.in_arcs).issubset(
                                       new_places)]
            if not allowed_transitions:
                continue

            cur_trans = choice(allowed_transitions)

            self.trace.append(cur_trans)

            new_places.remove(i)

            new_places.update(set(k.target for k in cur_trans.out_arcs))

            flag = True
        places.clear()
        places.update(new_places)
        return flag

    def foreach_step(self) -> bool:
        banned = set(chain.from_iterable(i.get_dependent() for i in self.conditions if not i.check(self.trace)))
        flag = 0
        for i in self.tokens:
            flag += self.step(i, banned)
        self.conditions = [i for i in self.conditions if i.still_relevant(self.trace)]
        return flag != 0

    def simulate(self):
        self.trace = []
        if not self.tokens:
            raise Exception("empty start marking")
        if len(self.tokens) != len(self.nets):
            raise Exception("tokens dont match nets")
        while self.foreach_step():
            continue
        return self.trace

    def get_trace(self):
        return self.trace

    def get_trace_in_labels(self):
        return [i.label for i in self.trace]
