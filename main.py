"""
Main Entry Point for Distributed Load Balancer Simulator.

Demonstrates initial project bootstrap, sample task generation,
validation, and summary statistics display.
"""

from typing import Any, Dict, List
from task_manager import generate_sample_tasks, prepare_tasks, validate_tasks


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


def main() -> None:
    """
    Run the entry point for the Distributed Load Balancer Simulator foundation.
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

    print("\n" + "-" * 70)
    print("[i] Architectural Notice / Planned Upcoming Modules:")
    print("    1. CPU Schedulers (schedulers/):")
    print("       - FCFS (First-Come, First-Served)")
    print("       - SJF (Shortest Job First - non-preemptive)")
    print("       - Round Robin (preemptive time-quantum scheduling)")
    print("    2. Node Simulator (node_simulator.py):")
    print("       - Multi-node cluster simulation and task load balancing")
    print("    3. Metrics Aggregator (metrics.py):")
    print("       - Waiting time, turnaround time, makespan, and node utilization")
    print("    4. Interactive Dashboard (Streamlit):")
    print("       - Web-based dynamic charts and Gantt scheduling visualizations")
    print("-" * 70 + "\n")


if __name__ == "__main__":
    main()
