"""
Metrics Module for Distributed Load Balancer Simulator.

Calculates and aggregates performance metrics from scheduler execution results:
- Waiting Time: Total duration a task waits in ready queues prior to and during CPU execution.
- Turnaround Time: Total elapsed time from task arrival to final completion.
- Makespan: Total time required to complete execution of the entire task workload.
- Averages: Average waiting time and turnaround time across all tasks.
"""

from typing import Any, Dict, List


def calculate_metrics_summary(task_metrics: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate summary metrics from task metrics dictionary returned by a scheduler.

    Args:
        task_metrics (Dict[str, Dict[str, Any]]): Dictionary keyed by task_id with
            arrival_time, burst_time, completion_time, turnaround_time, and waiting_time.

    Returns:
        Dict[str, Any]: Summary metrics containing:
            - total_tasks (int): Number of scheduled tasks.
            - avg_waiting_time (float): Average waiting time.
            - avg_turnaround_time (float): Average turnaround time.
            - makespan (int): Maximum completion time (or 0 if empty).
    """
    if not task_metrics:
        return {
            "total_tasks": 0,
            "avg_waiting_time": 0.0,
            "avg_turnaround_time": 0.0,
            "makespan": 0,
        }

    total_tasks = len(task_metrics)
    total_waiting = sum(m["waiting_time"] for m in task_metrics.values())
    total_turnaround = sum(m["turnaround_time"] for m in task_metrics.values())
    makespan = max(m["completion_time"] for m in task_metrics.values())

    return {
        "total_tasks": total_tasks,
        "avg_waiting_time": round(total_waiting / total_tasks, 2),
        "avg_turnaround_time": round(total_turnaround / total_tasks, 2),
        "makespan": makespan,
    }


def identify_idle_intervals(schedule_slices: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Detect idle intervals (gaps) in a sequence of execution slices.

    Args:
        schedule_slices (List[Dict[str, Any]]): Chronological execution slices
            containing 'start_time' and 'end_time'.

    Returns:
        List[Dict[str, Any]]: List of idle interval slices with:
            - task_id (str): "Idle"
            - start_time (int): Start of idle period
            - end_time (int): End of idle period
            - duration (int): Length of idle period
            - is_idle (bool): True
    """
    idle_slices: List[Dict[str, Any]] = []
    if not schedule_slices:
        return idle_slices

    # Slices are sorted chronologically
    first_start = schedule_slices[0]["start_time"]
    if first_start > 0:
        idle_slices.append({
            "task_id": "Idle",
            "start_time": 0,
            "end_time": first_start,
            "duration": first_start,
            "is_idle": True,
        })

    prev_end = schedule_slices[0]["end_time"]
    for s in schedule_slices[1:]:
        if s["start_time"] > prev_end:
            idle_slices.append({
                "task_id": "Idle",
                "start_time": prev_end,
                "end_time": s["start_time"],
                "duration": s["start_time"] - prev_end,
                "is_idle": True,
            })
        if s["end_time"] > prev_end:
            prev_end = s["end_time"]

    return idle_slices
