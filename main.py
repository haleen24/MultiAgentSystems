from simulating.nets.multi_agent_system import MultiAgentSystem
from simulating.occurs_before_condition import OccursBeforeCondition
from pm4py.read import read_pnml
from pm4py import view_petri_net, Marking
from pm4py import PetriNet
from pm4py.objects.petri_net.utils.petri_utils import add_place
from pm4py.objects.petri_net.utils.petri_utils import add_transition
from pm4py.objects.petri_net.utils.petri_utils import add_arc_from_to

# net, init, end = read_pnml("test/result_1-2.pnml")
# view_petri_net(net, init)
#
# agent = MultiAgentSystem([net], [init], [])
#
# print(agent.simulate())

# places = [PetriNet.Place(str(i)) for i in range(100)]
# transitions = [PetriNet.Transition(str(i), str(i)) for i in range(200)]

net1 = PetriNet()
net2 = PetriNet()

places1 = [add_place(net1) for i in range(6)]
transitions1 = [add_transition(net1, str(i), str(i)) for i in range(4)]

add_arc_from_to(places1[0], transitions1[0], net1)
add_arc_from_to(places1[0], transitions1[1], net1)
add_arc_from_to(transitions1[0], places1[1], net1)
add_arc_from_to(transitions1[1], places1[2], net1)
add_arc_from_to(places1[1], transitions1[2], net1)
add_arc_from_to(places1[2], transitions1[3], net1)
add_arc_from_to(transitions1[2], places1[3], net1)
add_arc_from_to(transitions1[3], places1[4], net1)
add_arc_from_to(places1[5], transitions1[1], net1)

places2 = [add_place(net2) for i in range(3)]
transitions2 = [add_transition(net2, str(i), str(i) + '\'') for i in range(2)]
add_arc_from_to(places2[0], transitions2[0], net2)
add_arc_from_to(transitions2[0], places2[1], net2)
add_arc_from_to(places2[1], transitions2[1], net2)
add_arc_from_to(transitions2[1], places2[2], net2)

conditions = [
    # OccursBeforeCondition(transitions1[1], transitions2[0]),
    # OccursBeforeCondition(transitions2[0], transitions1[0]),
    # OccursBeforeCondition(transitions2[0], transitions1[1])
    OccursBeforeCondition(transitions2[1], transitions1[0])
]
tokens = [
    Marking(),
    Marking()
]
tokens[0][places1[0]] = 1
tokens[1][places2[0]] = 1
tokens[0][places1[5]] = 1
view_petri_net(net1, tokens[0])
view_petri_net(net2, tokens[1])

sys = MultiAgentSystem([net1, net2], tokens, conditions)
sys.simulate()
print(sys.get_trace_in_labels())
