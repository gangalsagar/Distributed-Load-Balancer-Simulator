<<<<<<< HEAD
import copy
=======
>>>>>>> 4ab66d6ce60f640de08a69a5ff3c9989b6d222f1
from typing import Any, Dict, List


def calculate_metrics_summary(
    task_metrics: Dict[str, Dict[str, Any]],
    schedule_slices: List[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    if not task_metrics:
        return {
            "total_tasks": 0,
            "avg_waiting_time": 0.0,
            "avg_turnaround_time": 0.0,
            "makespan": 0,
            "cpu_utilization": 0.0,
        }
    total_tasks = len(task_metrics)
    total_waiting = sum((m["waiting_time"] for m in task_metrics.values()))
    total_turnaround = sum((m["turnaround_time"] for m in task_metrics.values()))
    makespan = max((m["completion_time"] for m in task_metrics.values()))
    total_busy_time = sum((m["burst_time"] for m in task_metrics.values()))
    cpu_utilization = (
        round(total_busy_time / makespan * 100, 2) if makespan > 0 else 0.0
    )
    return {
        "total_tasks": total_tasks,
        "avg_waiting_time": round(total_waiting / total_tasks, 2),
        "avg_turnaround_time": round(total_turnaround / total_tasks, 2),
        "makespan": makespan,
        "cpu_utilization": cpu_utilization,
    }


def identify_idle_intervals(
    schedule_slices: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    idle_slices: List[Dict[str, Any]] = []
    if not schedule_slices:
        return idle_slices
    first_start = schedule_slices[0]["start_time"]
    if first_start > 0:
        idle_slices.append(
            {
                "task_id": "Idle",
                "start_time": 0,
                "end_time": first_start,
                "duration": first_start,
                "is_idle": True,
            }
        )
    prev_end = schedule_slices[0]["end_time"]
    for s in schedule_slices[1:]:
        if s["start_time"] > prev_end:
            idle_slices.append(
                {
                    "task_id": "Idle",
                    "start_time": prev_end,
                    "end_time": s["start_time"],
                    "duration": s["start_time"] - prev_end,
                    "is_idle": True,
                }
            )
        if s["end_time"] > prev_end:
            prev_end = s["end_time"]
    return idle_slices


def run_algorithm_comparison(
    tasks: List[Dict[str, Any]], time_quantum: int = 2
) -> Dict[str, Any]:
<<<<<<< HEAD
=======
    import copy

>>>>>>> 4ab66d6ce60f640de08a69a5ff3c9989b6d222f1
    from schedulers.fcfs import fcfs_schedule
    from schedulers.round_robin import round_robin_schedule
    from schedulers.sjf import sjf_schedule
    from task_manager import validate_tasks

    validate_tasks(tasks)
    rr_slices, rr_metrics = round_robin_schedule(
        copy.deepcopy(tasks), time_quantum=time_quantum
    )
    rr_summary = calculate_metrics_summary(rr_metrics, rr_slices)
    fcfs_slices, fcfs_metrics = fcfs_schedule(copy.deepcopy(tasks))
    fcfs_summary = calculate_metrics_summary(fcfs_metrics, fcfs_slices)
    sjf_slices, sjf_metrics = sjf_schedule(copy.deepcopy(tasks))
    sjf_summary = calculate_metrics_summary(sjf_metrics, sjf_slices)
    algorithms_data = {
        "Round Robin (RR)": {
            "slices": rr_slices,
            "metrics": rr_metrics,
            "summary": rr_summary,
<<<<<<< HEAD
            "idle_intervals": identify_idle_intervals(rr_slices),
=======
>>>>>>> 4ab66d6ce60f640de08a69a5ff3c9989b6d222f1
        },
        "First Come, First Served (FCFS)": {
            "slices": fcfs_slices,
            "metrics": fcfs_metrics,
            "summary": fcfs_summary,
<<<<<<< HEAD
            "idle_intervals": identify_idle_intervals(fcfs_slices),
=======
>>>>>>> 4ab66d6ce60f640de08a69a5ff3c9989b6d222f1
        },
        "Shortest Job First (SJF)": {
            "slices": sjf_slices,
            "metrics": sjf_metrics,
            "summary": sjf_summary,
<<<<<<< HEAD
            "idle_intervals": identify_idle_intervals(sjf_slices),
=======
>>>>>>> 4ab66d6ce60f640de08a69a5ff3c9989b6d222f1
        },
    }
    comparison_rows = [
        {
            "Algorithm": name,
            "Avg Waiting Time": data["summary"]["avg_waiting_time"],
            "Avg Turnaround Time": data["summary"]["avg_turnaround_time"],
            "Makespan": data["summary"]["makespan"],
            "CPU Utilization (%)": data["summary"]["cpu_utilization"],
        }
        for name, data in algorithms_data.items()
    ]
    best_performers: Dict[str, List[str]] = {
        "lowest_waiting": [],
        "lowest_turnaround": [],
        "shortest_makespan": [],
        "highest_utilization": [],
    }
    if comparison_rows and tasks:
        min_wait = min((r["Avg Waiting Time"] for r in comparison_rows))
        best_performers["lowest_waiting"] = [
            r["Algorithm"] for r in comparison_rows if r["Avg Waiting Time"] == min_wait
        ]
        min_tat = min((r["Avg Turnaround Time"] for r in comparison_rows))
        best_performers["lowest_turnaround"] = [
            r["Algorithm"]
            for r in comparison_rows
            if r["Avg Turnaround Time"] == min_tat
        ]
        min_makespan = min((r["Makespan"] for r in comparison_rows))
        best_performers["shortest_makespan"] = [
            r["Algorithm"] for r in comparison_rows if r["Makespan"] == min_makespan
        ]
        max_util = max((r["CPU Utilization (%)"] for r in comparison_rows))
        best_performers["highest_utilization"] = [
            r["Algorithm"]
            for r in comparison_rows
            if r["CPU Utilization (%)"] == max_util
        ]
    return {
        "algorithms": algorithms_data,
        "comparison_rows": comparison_rows,
        "best_performers": best_performers,
    }
