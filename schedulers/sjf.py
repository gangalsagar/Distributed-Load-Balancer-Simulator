from typing import Any, Dict, List, Tuple

from task_manager import prepare_tasks


def sjf_schedule(
    tasks: List[Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    prepared = prepare_tasks(tasks)
    schedule_slices: List[Dict[str, Any]] = []
    task_metrics: Dict[str, Dict[str, Any]] = {}
    if not prepared:
        return (schedule_slices, task_metrics)
    unarrived = sorted(
        prepared, key=lambda t: (t["arrival_time"], t["burst_time"], str(t["task_id"]))
    )
    current_time = 0
    ready_queue: List[Dict[str, Any]] = []

    def admit_arrived():
        while unarrived and unarrived[0]["arrival_time"] <= current_time:
            ready_queue.append(unarrived.pop(0))

    admit_arrived()
    while ready_queue or unarrived:
        if not ready_queue:
            current_time = unarrived[0]["arrival_time"]
            admit_arrived()
        ready_queue.sort(
            key=lambda t: (t["burst_time"], t["arrival_time"], str(t["task_id"]))
        )
        current_task = ready_queue.pop(0)
        start_time = current_time
        duration = current_task["burst_time"]
        current_time += duration
        completion_time = current_time
        turnaround_time = completion_time - current_task["arrival_time"]
        waiting_time = turnaround_time - current_task["burst_time"]
        slice_record = {
            "task_id": current_task["task_id"],
            "start_time": start_time,
            "end_time": completion_time,
            "duration": duration,
            "remaining_time": 0,
            "completed": True,
        }
        schedule_slices.append(slice_record)
        task_metrics[current_task["task_id"]] = {
            "task_id": current_task["task_id"],
            "arrival_time": current_task["arrival_time"],
            "burst_time": current_task["burst_time"],
            "completion_time": completion_time,
            "turnaround_time": turnaround_time,
            "waiting_time": waiting_time,
        }
        admit_arrived()
    return (schedule_slices, task_metrics)
