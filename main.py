"""
Main Entry Point for Distributed Load Balancer Simulator.

Demonstrates initial project bootstrap, sample task generation,
validation, summary statistics display, and Round Robin scheduling execution.
"""

from typing import Any, Dict, List
from task_manager import generate_sample_tasks, prepare_tasks
from schedulers.round_robin import round_robin_schedule


def display_task_table(tasks: List[Dict[str, Any]]) -> None:
    """
    Format and display task details in a clean terminal table.

    Args:
        tasks (List[Dict[str, Any]]): List of task dictionaries.
    """
    header = f"{'Task ID':<10} | {'Arrival':<10} | {'Burst':<10} | {'Remaining':<10} | {'Status':<12} | {'Assigned Node':<15}"
    separator = "-" * len(header)
    print(separator)
    print(header)
    print(separator)
    for task in tasks:
        node_str = str(task.get("assigned_node")) if task.get("assigned_node") is not None else "None (Unassigned)"
        row = (
            f"{task['task_id']:<10} | "
            f"{task['arrival_time']:<10} | "
            f"{task['burst_time']:<10} | "
            f"{task['remaining_time']:<10} | "
            f"{task['status']:<12} | "
            f"{node_str:<15}"
        )
        print(row)
    print(separator)


def display_schedule_slices(slices: List[Dict[str, Any]]) -> None:
    """
    Format and display Round Robin execution slices.

    Args:
        slices (List[Dict[str, Any]]): Chronological execution slices.
    """
    header = f"{'Slice #':<8} | {'Task ID':<10} | {'Start':<8} | {'End':<8} | {'Duration':<10} | {'Remaining':<11} | {'Status':<12}"
    separator = "-" * len(header)
    print(separator)
    print(header)
    print(separator)
    for idx, s in enumerate(slices, 1):
        status_str = "Completed" if s["completed"] else "Preempted"
        row = (
            f"{idx:<8} | "
            f"{s['task_id']:<10} | "
            f"{s['start_time']:<8} | "
            f"{s['end_time']:<8} | "
            f"{s['duration']:<10} | "
            f"{s['remaining_time']:<11} | "
            f"{status_str:<12}"
        )
        print(row)
    print(separator)


def display_task_metrics_table(metrics: Dict[str, Dict[str, Any]]) -> None:
    """
    Format and display per-task metrics and calculate averages.

    Args:
        metrics (Dict[str, Dict[str, Any]]): Metrics per task.
    """
    header = f"{'Task ID':<10} | {'Arrival':<10} | {'Burst':<10} | {'Completion':<12} | {'Turnaround':<12} | {'Waiting':<10}"
    separator = "-" * len(header)
    print(separator)
    print(header)
    print(separator)

    total_waiting = 0
    total_turnaround = 0
    for task_id in sorted(metrics.keys()):
        m = metrics[task_id]
        total_waiting += m["waiting_time"]
        total_turnaround += m["turnaround_time"]
        row = (
            f"{m['task_id']:<10} | "
            f"{m['arrival_time']:<10} | "
            f"{m['burst_time']:<10} | "
            f"{m['completion_time']:<12} | "
            f"{m['turnaround_time']:<12} | "
            f"{m['waiting_time']:<10}"
        )
        print(row)
    print(separator)

    count = len(metrics)
    if count > 0:
        avg_wait = total_waiting / count
        avg_tat = total_turnaround / count
        print(f"Average Waiting Time    : {avg_wait:.2f} time units")
        print(f"Average Turnaround Time : {avg_tat:.2f} time units")


def main() -> None:
    """
    Run the entry point for the Distributed Load Balancer Simulator.
    """
    banner_title = "DISTRIBUTED LOAD BALANCER SIMULATOR"
    subtitle = "Simulating Task Scheduling Across Multiple Computing Nodes"
    border = "=" * 70

    print(f"\n{border}")
    print(f"{banner_title:^70}")
    print(f"{subtitle:^70}")
    print(f"{border}\n")

    print("[*] Generating sample simulation workload...")
    raw_tasks = generate_sample_tasks()

    print("[*] Validating and preparing tasks for simulation...")
    tasks = prepare_tasks(raw_tasks)

    # Compute high-level task metrics
    total_tasks = len(tasks)
    total_burst_time = sum(task["burst_time"] for task in tasks)

    print("\n[+] Configured Simulation Tasks:")
    display_task_table(tasks)

    print("\n[+] Workload Summary:")
    print(f"    - Total Number of Tasks : {total_tasks}")
    print(f"    - Total CPU Burst Time  : {total_burst_time} units")

    print("\n[+] Status: Task generation and validation SUCCEEDED!")

    # Execute Round Robin Scheduling Demonstration
    time_quantum = 2
    print(f"\n{'=' * 70}")
    print(f"[*] Running Round Robin CPU Scheduling (Time Quantum = {time_quantum})...")
    print(f"{'=' * 70}")

    slices, metrics = round_robin_schedule(raw_tasks, time_quantum=time_quantum)

    print("\n[+] Execution Slices (Chronological Order):")
    display_schedule_slices(slices)

    print("\n[+] Task Performance Metrics:")
    display_task_metrics_table(metrics)

    print("\n" + "-" * 70)
    print("[i] Architectural Notice / Planned Upcoming Modules:")
    print("    1. Additional CPU Schedulers (schedulers/):")
    print("       - FCFS (First-Come, First-Served)")
    print("       - SJF (Shortest Job First - non-preemptive)")
    print("    2. Node Simulator (node_simulator.py):")
    print("       - Multi-node cluster simulation and task load balancing")
    print("    3. Metrics Aggregator (metrics.py):")
    print("       - Centralized metrics aggregation across nodes and algorithms")
    print("    4. Interactive Dashboard (Streamlit):")
    print("       - Web-based dynamic charts and Gantt scheduling visualizations")
    print("-" * 70 + "\n")


if __name__ == "__main__":
    main()
