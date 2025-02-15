This library allows you to simulate multi-agent-system using pm4py representation of Petri nets

### About conditions:

There are several types of conditions in package simulating/conditions.
condition.py - contains a definition of abstract class. This class contains following methods:

1. check(self, trace: dict[PetriNet.Transition | str, int]) -> bool. Used for checking conditions by traveled path
2. still_relevant(self, trace: dict[PetriNet.Transition | str, int]) -> bool. Used for checking the conditions for
   relevance
3. get_dependent(self) -> Iterable[PetriNet.Transition | str]. Used to get dependent part of condition. See

Let a and b are transitions in some Petri net, then
the library provides following types of condition:

1. a occurs before b (a < b). In case of cyclic interactions after the first 'a' there can be any number of 'b'
2. a occurs before b with cyclic interaction. Provides following opportunity for transitions: for each 'b' in trace
   should be
   own 'a'. For example, the trace a -> ... -> a -> ... -> b -> ... -> b also satisfies the condition
3. a does not occur before b (a !< b)
4. a set of transitions must be triggered synchronously. This condition also can be used with cycled interactions. By
   default, after first trigger of all synchronized transition, the condition become irrelevant. If cycled mod enabled,
   the condition is always relevant

### How to use library for simulating multi-agent-systems:

1. Import/create Petri nets and initial markings by using pm4py
2. Create iterable object of conditions
3. Create MultiAgentSystems object (pass him Petri nets, marking, time of start logging (optional) and duration of
   transition's trigger (optional))
4. Create traces trough method create_traces. You can pass number of traces (by default = 1) and maximal depth (by
   default = 2 * sum of number of elements in all nets). This method return list of event logs (
   simulating/log/event_log.py)
5. You can export in csv the list from previous step by using method export_csv from simulating/log/export.py

###### In case of deadlock at least in one of simulated traces the create_traces method returns only trace that reached the deadlock. See example in ~/examples/1/