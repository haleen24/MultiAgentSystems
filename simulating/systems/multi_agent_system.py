from itertools import chain
from random import choice
from typing import Tuple

from pm4py import Marking, PetriNet
from simulating.conditions.condition import Condition
from simulating.conditions.sync_condition import SyncCondition
from simulating.log.event_log import EventLog
from simulating.systems.deadlock_exception import DeadLockException
from simulating.systems.firing import play_from_places, play_from_transitions


class MultiAgentSystem:
    def __init__(self, nets: list[PetriNet], tokens: list[Marking], conditions: list[Condition]):
        self.nets = nets
        self.tokens = set(chain.from_iterable(i.keys() for i in tokens))
        self.trace = self.tokens.copy()
        self.conditions = conditions
        self.banned = set()
        self.logs = []
        self.sync_transitions = set(
            chain.from_iterable(i.get_dependent() for i in self.conditions if isinstance(i, SyncCondition)))
        for i in nets:
            for j in i.transitions:
                j.properties["net"] = i.name
            for j in i.places:
                j.properties["net"] = i.name

    def update_banned(self):
        self.banned = set(chain.from_iterable(
            i.get_dependent() for i in self.conditions if not i.check(self.trace)))

    def update_conditions(self):
        self.conditions = [i for i in self.conditions if i.still_relevant(self.trace)]
        self.sync_transitions -= set(i for i in self.sync_transitions if i in self.trace)

    def step(self,
             element: PetriNet.Transition | Tuple[set[PetriNet.Place], set[PetriNet.Transition]] | set[
                 PetriNet.Transition]):
        if isinstance(element, PetriNet.Transition):
            play_from_transitions(element, self.tokens)
            self.trace.update(i.target for i in element.out_arcs)

        elif isinstance(element, Tuple):
            places = element[0]
            transitions = element[1]
            play_from_places(places, transitions, self.tokens)
            self.trace.update(transitions)
            labels = ", ".join(i.label for i in transitions)
            nets = ", ".join(i.properties["net"] for i in transitions)
            self.logs.append(EventLog(labels, nets))
        self.update_conditions()
        self.update_banned()

    def simulate(self, max_depht: int = None):
        self.trace = set(self.tokens)
        if not self.tokens:
            raise Exception("empty start marking")
        max_depht = 2 * sum(len(i.places) + len(i.transitions) for i in self.nets) if max_depht is None else max_depht
        cur_depth = 0
        self.update_banned()
        while cur_depth < max_depht:
            active_elements = self.get_all_possible_elements()
            if not active_elements:
                break
            self.step(choice(active_elements))
            cur_depth += 1

        if any(len(i.out_arcs) != 0 for i in self.tokens):
            raise DeadLockException("deadlock", self.logs)
        return self.logs

    def get_all_possible_elements(self) -> list[
        PetriNet.Transition | Tuple[set[PetriNet.Place], set[PetriNet.Transition]]]:
        fire_from_transitions = [i for i in self.tokens if isinstance(i, PetriNet.Transition)]
        possible_transition = set(chain.from_iterable(
            [j.target for j in i.out_arcs if j.target not in self.sync_transitions and j.target not in self.banned] for
            i in self.tokens if
            isinstance(i, PetriNet.Place)))
        fire_from_places = []
        for i in possible_transition:
            s = set(j.source for j in i.in_arcs)
            if s.issubset(self.tokens):
                fire_from_places.append((s, {i}))
        for i in [j for j in self.conditions if isinstance(j, SyncCondition)]:
            if any(j in self.banned for j in i.get_dependent()):
                continue
            if i.check(self.tokens):
                fire_from_places.append(
                    (set(k.source for j in i.get_dependent() for k in j.in_arcs), i.get_dependent()))
        return fire_from_transitions + fire_from_places

    def get_trace(self):
        return self.trace

    def get_trace_in_labels(self):
        return [i.label for i in self.trace]

    def create_traces(self, n: int = 1, max_depth: int = None) -> list[list[EventLog]]:
        conditions = self.conditions
        tokens = self.tokens
        sync_transitions = self.sync_transitions
        result = []

        def restore_to_default():
            self.conditions = conditions.copy()
            self.tokens = tokens.copy()
            self.logs = []
            self.sync_transitions = sync_transitions.copy()

        for i in range(n):
            restore_to_default()
            try:
                trace = self.simulate(max_depth)
                result.append(trace)
            except DeadLockException as ex:
                return [ex.trace]
        restore_to_default()
        return result
