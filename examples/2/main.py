from examples.export import export
from simulating.conditions.occurs_before_condition import OccursBeforeCondition
from simulating.log.export import export_csv
from simulating.systems.multi_agent_system import MultiAgentSystem

if __name__ == "__main__":
    # importing petri nets and markings from 'nets' directory
    nets, markings, transitions = export()

    # create conditions
    conditions = [
        OccursBeforeCondition(transitions['t1'], transitions['t2']),
        OccursBeforeCondition(transitions['t2'], transitions['t3']),
        OccursBeforeCondition(transitions['t3'], transitions['t4']),
        OccursBeforeCondition(transitions['t4'], transitions['t5'])
    ]

    # create multi-agent-system object
    multi_agent_system = MultiAgentSystem(nets, markings, conditions)

    # create traces and export them in csv
    export_csv("example", multi_agent_system.create_traces(3))
