<<<<<<< HEAD
import sys
from typing import Any, Dict, List

from metrics import calculate_metrics_summary
from node_simulator import simulate_cluster
from schedulers.fcfs import fcfs_schedule
from schedulers.round_robin import round_robin_schedule
from schedulers.sjf import sjf_schedule
=======
from typing import Any, Dict, List

from schedulers.round_robin import round_robin_schedule
>>>>>>> 4ab66d6ce60f640de08a69a5ff3c9989b6d222f1
from task_manager import generate_sample_tasks, prepare_tasks


def display_task_table(tasks: List[Dict[str, Any]]) -> None:
    header = f"{'Task ID':<10} | {'Arrival':<10} | {'Burst':<10} | {'Remaining':<10} | {'Status':<12} | {'Assigned Node':<15}"
    separator = "-" * len(header)
    print(separator)
    print(header)
    print(separator)
    for task in tasks:
        node_str = (
            str(task.get("assigned_node"))
            if task.get("assigned_node") is not None
            else "None (Unassigned)"
        )
        row = f"{task['task_id']:<10} | {task['arrival_time']:<10} | {task['burst_time']:<10} | {task['remaining_time']:<10} | {task['status']:<12} | {node_str:<15}"
        print(row)
    print(separator)


def display_schedule_slices(slices: List[Dict[str, Any]]) -> None:
    header = f"{'Slice #':<8} | {'Task ID':<10} | {'Start':<8} | {'End':<8} | {'Duration':<10} | {'Remaining':<11} | {'Status':<12}"
    separator = "-" * len(header)
    print(separator)
    print(header)
    print(separator)
    for idx, s in enumerate(slices, 1):
        status_str = "Completed" if s["completed"] else "Preempted"
        row = f"{idx:<8} | {s['task_id']:<10} | {s['start_time']:<8} | {s['end_time']:<8} | {s['duration']:<10} | {s['remaining_time']:<11} | {status_str:<12}"
        print(row)
    print(separator)


def display_task_metrics_table(metrics: Dict[str, Dict[str, Any]]) -> None:
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
        row = f"{m['task_id']:<10} | {m['arrival_time']:<10} | {m['burst_time']:<10} | {m['completion_time']:<12} | {m['turnaround_time']:<12} | {m['waiting_time']:<10}"
        print(row)
    print(separator)
    count = len(metrics)
    if count > 0:
        avg_wait = total_waiting / count
        avg_tat = total_turnaround / count
        print(f"Average Waiting Time    : {avg_wait:.2f} time units")
        print(f"Average Turnaround Time : {avg_tat:.2f} time units")


def main() -> None:
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
    total_tasks = len(tasks)
    total_burst_time = sum((task["burst_time"] for task in tasks))
    print("\n[+] Configured Simulation Tasks:")
    display_task_table(tasks)
    print("\n[+] Workload Summary:")
    print(f"    - Total Number of Tasks : {total_tasks}")
    print(f"    - Total CPU Burst Time  : {total_burst_time} units")
    print("\n[+] Status: Task generation and validation SUCCEEDED!")
<<<<<<< HEAD

=======
>>>>>>> 4ab66d6ce60f640de08a69a5ff3c9989b6d222f1
    time_quantum = 2
    print(f"\n{'=' * 70}")
    print(f"[*] Running Round Robin CPU Scheduling (Time Quantum = {time_quantum})...")
    print(f"{'=' * 70}")
    slices, metrics = round_robin_schedule(raw_tasks, time_quantum=time_quantum)
    print("\n[+] Execution Slices (Chronological Order):")
    display_schedule_slices(slices)
    print("\n[+] Task Performance Metrics:")
    display_task_metrics_table(metrics)
<<<<<<< HEAD

    print(f"\n{'=' * 70}")
    print("[*] Running Stage 3 Multi-Node Cluster Load Balancer...")
    print(f"{'=' * 70}")
    cluster_res = simulate_cluster(raw_tasks, node_count=3, policy="Least Loaded")
    print(f"    - Number of Nodes       : {len(cluster_res['nodes'])}")
    print(f"    - Balancing Policy      : Least Loaded")
    print(f"    - Cluster Makespan      : {cluster_res['cluster_makespan']} units")
    print(f"    - Average Waiting Time  : {cluster_res['avg_waiting_time']:.2f} units")
    print(f"    - Average Node CPU Util : {cluster_res['avg_cpu_utilization']:.2f}%")
    for n in cluster_res["nodes"]:
        assigned = [t["task_id"] for t in n["tasks"]]
        print(f"      * {n['node_id']}: Tasks={assigned}, Duration={n['summary']['makespan']} units, CPU Util={n['summary']['cpu_utilization']}%")

    print("\n" + "-" * 70)
    print("[i] Complete Python Simulation Suite is Operational.")
=======
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
>>>>>>> 4ab66d6ce60f640de08a69a5ff3c9989b6d222f1
    print("-" * 70 + "\n")


if __name__ == "__main__":
    main()
