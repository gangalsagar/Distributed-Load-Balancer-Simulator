"""
Shortest Job First (SJF) CPU Scheduling Algorithm (Non-preemptive).

[PLANNED COMPONENT - FUTURE STAGE]
Design & Implementation Plan:
- Non-preemptive scheduling policy.
- At any scheduling decision point, selects the task with the minimum burst_time
  among tasks that have arrived and are in ready state.
- Deterministic tie-breaking: when burst times are equal, break ties using arrival_time,
  followed by lexicographical task_id.
- Once CPU is allocated to a task, it runs to completion without interruption.

Note: Algorithm implementation will be completed in a later project stage.
"""
