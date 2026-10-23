"""
Round Robin (RR) CPU Scheduling Algorithm (Preemptive).

Simulates single-node Round Robin CPU scheduling with a configurable time quantum.
Maintains a FIFO ready queue, handles arbitrary arrival times, idle periods,
preemptions, deterministic tie-breaking (by arrival_time, then original list order),
and produces detailed execution slices along with task completion summaries.
"""

from collections import deque
from typing import Any, Dict, List, Tuple
from task_manager import prepare_tasks


def round_robin_schedule(
    tasks: List[Dict[str, Any]],
    time_quantum: int = 2
) -> Tuple[List[Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    """
    Execute Round Robin CPU scheduling on a set of tasks.

    Args:
        tasks (List[Dict[str, Any]]): List of task dictionaries. Each task must contain
            'task_id', 'arrival_time', and 'burst_time'.
        time_quantum (int): Positive integer time slice allocation (default: 2).

    Returns:
        Tuple[List[Dict[str, Any]], Dict[str, Dict[str, Any]]]:
            1. schedule_slices: Chronological execution slices, each dictionary containing:
                - task_id (str): Task identifier executed.
                - start_time (int): Start time of slice.
                - end_time (int): End time of slice.
                - duration (int): Duration of CPU execution in this slice.
                - remaining_time (int): Remaining burst time of task after this slice.
                - completed (bool): True if task finished in this slice, False otherwise.
            2. task_metrics: Dictionary keyed by task_id containing:
                - task_id (str)
                - arrival_time (int)
                - burst_time (int)
                - completion_time (int)
                - turnaround_time (int): completion_time - arrival_time
                - waiting_time (int): turnaround_time - burst_time

    Raises:
        TypeError: If time_quantum is not an integer or is a boolean.
        ValueError: If time_quantum <= 0.
        TypeError / ValueError: If tasks fail validation via task_manager.
    """
    # Validate time_quantum strictly
    if isinstance(time_quantum, bool) or not isinstance(time_quantum, int):
        raise TypeError(
            f"time_quantum must be an integer (booleans not accepted), got {type(time_quantum).__name__}."
        )
    if time_quantum <= 0:
        raise ValueError(f"time_quantum must be a positive integer (> 0), got {time_quantum}.")

    # Validate and deep-copy tasks to guarantee caller's list is untouched
    prepared = prepare_tasks(tasks)

    schedule_slices: List[Dict[str, Any]] = []
    task_metrics: Dict[str, Dict[str, Any]] = {}

    if not prepared:
        return schedule_slices, task_metrics

    # Attach original index to preserve stable arrival order among simultaneous arrivals
    for idx, task in enumerate(prepared):
        task["_order"] = idx

    # Sort unarrived tasks by arrival_time, then original list order
    unarrived = sorted(prepared, key=lambda t: (t["arrival_time"], t["_order"]))

    current_time = 0
    ready_queue: deque = deque()
    completed_count = 0
    total_tasks = len(prepared)

    # Function to check and admit newly arrived tasks into ready_queue
    def admit_arrived():
        while unarrived and unarrived[0]["arrival_time"] <= current_time:
            task = unarrived.pop(0)
            ready_queue.append(task)

    # Initial admission at time 0
    admit_arrived()

    while completed_count < total_tasks:
        if not ready_queue:
            # CPU is idle, advance time to next task arrival
            current_time = unarrived[0]["arrival_time"]
            admit_arrived()

        current_task = ready_queue.popleft()
        start_time = current_time
        exec_duration = min(time_quantum, current_task["remaining_time"])
        current_time += exec_duration
        current_task["remaining_time"] -= exec_duration
        is_completed = current_task["remaining_time"] == 0

        # Create record for this execution slice
        slice_record = {
            "task_id": current_task["task_id"],
            "start_time": start_time,
            "end_time": current_time,
            "duration": exec_duration,
            "remaining_time": current_task["remaining_time"],
            "completed": is_completed,
        }
        schedule_slices.append(slice_record)

        # In standard OS Round Robin:
        # 1. Admit tasks that arrived during [start_time, current_time]
        admit_arrived()

        # 2. Requeue or finish current task
        if is_completed:
            completed_count += 1
            completion_time = current_time
            turnaround_time = completion_time - current_task["arrival_time"]
            waiting_time = turnaround_time - current_task["burst_time"]

            task_metrics[current_task["task_id"]] = {
                "task_id": current_task["task_id"],
                "arrival_time": current_task["arrival_time"],
                "burst_time": current_task["burst_time"],
                "completion_time": completion_time,
                "turnaround_time": turnaround_time,
                "waiting_time": waiting_time,
            }
        else:
            ready_queue.append(current_task)

    return schedule_slices, task_metrics
