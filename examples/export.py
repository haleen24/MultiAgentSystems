import pm4py.objects.petri_net.utils.petri_utils
from simulating.conditions.does_not_occur_before_condition import DoesNotOccurBeforeCondition
from simulating.log.export import export_csv
from simulating.systems.multi_agent_system import MultiAgentSystem


def export():
    # importing petri nets and markings from 'nets' directory
    nets, markings, _ = zip(*[pm4py.read_pnml(f"../nets/net{i}.pnml") for i in range(1, 6)])
    transitions = dict((j.label, j) for i in nets for j in i.transitions)

    return nets, markings, transitions
