import pm4py.objects.petri_net.utils.petri_utils
from pm4py import Marking

from examples.export import export
from simulating.conditions.does_not_occur_before_condition import DoesNotOccurBeforeCondition
from simulating.log.export import export_csv
from simulating.systems.multi_agent_system import MultiAgentSystem

if __name__ == "__main__":
    # importing petri nets and markings from 'nets' directory
    nets, markings, transitions = export()

    # create conditions
    conditions = [
        DoesNotOccurBeforeCondition(transitions['t1'], transitions['t2']),
        DoesNotOccurBeforeCondition(transitions['t1'], transitions['t5']),
    ]

    # create multi-agent-system object
    multi_agent_system = MultiAgentSystem(nets, markings, conditions)

    # create traces and export them in csv
    export_csv("example", multi_agent_system.create_traces(5000))
