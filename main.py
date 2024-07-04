# from simulating.conditions.sync_condition import SyncCondition
from simulating.conditions.occurs_before_condition import OccursBeforeCondition
from simulating.conditions.sync_condition import SyncCondition
from simulating.systems.multi_agent_system import MultiAgentSystem
# from simulating.conditions.occurs_before_condition import OccursBeforeCondition
from simulating.log.export import export_csv
from pm4py import Marking, read_pnml, view_petri_net
from pm4py import PetriNet
from pm4py.objects.petri_net.utils.petri_utils import add_place
from pm4py.objects.petri_net.utils.petri_utils import add_transition
from pm4py.objects.petri_net.utils.petri_utils import add_arc_from_to


def find_by_id(id):
    return find_by_label(str(id))


def find_by_label(label):
    return [i for i in net.transitions if i.label == label][0]


net, init, end = read_pnml("test/IP-1_composition_mined.pnml")
# j = 0
# for i in net.transitions:
#     i.label = str(j)
#     j += 1
# view_petri_net(net, init)

net.name = "net 1"
net2 = PetriNet()
p = [add_place(net2) for i in range(4)]
t = [add_transition(net2, label=f"-{i}") for i in range(1, 4)]
add_arc_from_to(p[0], t[0], net2)
add_arc_from_to(t[0], p[1], net2)
add_arc_from_to(p[1], t[1], net2)
add_arc_from_to(t[1], p[2], net2)
add_arc_from_to(p[2], t[2], net2)
add_arc_from_to(t[2], p[3], net2)
m = Marking()
m[p[0]] = 1

conditions = [
    # SyncCondition([find_by_id(11), find_by_id(34)]),
    # OccursBeforeCondition(t[1], find_by_id(34)),
    # OccursBeforeCondition(find_by_id(26), t[1]),
    # DoesNotOccurBeforeCondition(t[2], find_by_id(32))
    # DoesNotOccurBeforeCondition(find_by_id(24), find_by_id(10))
    SyncCondition([find_by_id(11), find_by_id(34), t[0]]),
    SyncCondition([find_by_id(10), find_by_id(24), find_by_id(38), find_by_id(19), t[2]]),
    OccursBeforeCondition(t[0], find_by_id(32))
]
net2.name = "net 2"
# view_petri_net(net2, m)
agent = MultiAgentSystem([net, net2], [init, m], conditions)

export_csv("tmp", agent.create_traces(5000))
