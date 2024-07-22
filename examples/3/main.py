from examples.export import export
from simulating.conditions.sync_condition import SyncCondition
from simulating.log.export import export_csv
from simulating.systems.multi_agent_system import MultiAgentSystem

if __name__ == "__main__":
    # importing petri nets and markings from 'nets' directory
    nets, markings, transitions = export()

    # create conditions
    conditions = [
        SyncCondition([transitions['t1'], transitions['t2'], transitions['t3']]),
        SyncCondition([transitions['t4'], transitions['t5']])
    ]

    # create multi-agent-system object
    multi_agent_system = MultiAgentSystem(nets, markings, conditions)

    # create traces and export them in csv
    export_csv("example", multi_agent_system.create_traces())
