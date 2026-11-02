from collections import deque
from typing import Any, Dict, List, Tuple

from task_manager import prepare_tasks


def round_robin_schedule(
    tasks: List[Dict[str, Any]], time_quantum: int = 2
) -> Tuple[List[Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    if isinstance(time_quantum, bool) or not isinstance(time_quantum, int):
        raise TypeError(
            f"time_quantum must be an integer (booleans not accepted), got {type(time_quantum).__name__}."
        )
    if time_quantum <= 0:
        raise ValueError(
            f"time_quantum must be a positive integer (> 0), got {time_quantum}."
        )
    prepared = prepare_tasks(tasks)
    schedule_slices: List[Dict[str, Any]] = []
    task_metrics: Dict[str, Dict[str, Any]] = {}
    if not prepared:
        return (schedule_slices, task_metrics)
    for idx, task in enumerate(prepared):
        task["_order"] = idx
    unarrived = sorted(prepared, key=lambda t: (t["arrival_time"], t["_order"]))
    current_time = 0
    ready_queue: deque = deque()
    completed_count = 0
    total_tasks = len(prepared)

    def admit_arrived():
        while unarrived and unarrived[0]["arrival_time"] <= current_time:
            task = unarrived.pop(0)
            ready_queue.append(task)

    admit_arrived()
    while completed_count < total_tasks:
        if not ready_queue:
            current_time = unarrived[0]["arrival_time"]
            admit_arrived()
        current_task = ready_queue.popleft()
        start_time = current_time
        exec_duration = min(time_quantum, current_task["remaining_time"])
        current_time += exec_duration
        current_task["remaining_time"] -= exec_duration
        is_completed = current_task["remaining_time"] == 0
        slice_record = {
            "task_id": current_task["task_id"],
            "start_time": start_time,
            "end_time": current_time,
            "duration": exec_duration,
            "remaining_time": current_task["remaining_time"],
            "completed": is_completed,
        }
        schedule_slices.append(slice_record)
        admit_arrived()
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
    return (schedule_slices, task_metrics)
