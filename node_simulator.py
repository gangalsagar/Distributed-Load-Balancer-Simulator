import copy
from typing import Any, Dict, List

from metrics import calculate_metrics_summary
from schedulers.fcfs import fcfs_schedule
from schedulers.round_robin import round_robin_schedule
from schedulers.sjf import sjf_schedule
from task_manager import validate_tasks


def simulate_cluster(
    tasks: List[Dict[str, Any]],
    node_count: int = 3,
    policy: str = "Least Loaded",
    local_algorithm: str = "FCFS",
    time_quantum: int = 2,
) -> Dict[str, Any]:
    """
    Simulates task distribution across N computing worker nodes using specified
    load balancing policy and per-node local CPU schedulers.
    """
    validate_tasks(tasks)
    if node_count < 1:
        raise ValueError(f"node_count must be at least 1, got {node_count}")

    node_tasks: List[List[Dict[str, Any]]] = [[] for _ in range(node_count)]
    node_workloads: List[int] = [0 for _ in range(node_count)]

    sorted_tasks = sorted(
        copy.deepcopy(tasks),
        key=lambda t: (t["arrival_time"], str(t["task_id"])),
    )

    for idx, task in enumerate(sorted_tasks):
        if policy == "Round Robin":
            target_node = idx % node_count
        elif policy == "Least Loaded":
            min_load = node_workloads[0]
            target_node = 0
            for n in range(1, node_count):
                if node_workloads[n] < min_load:
                    min_load = node_workloads[n]
                    target_node = n
        else:
            # Deterministic hash distribution
            hash_val = sum(ord(c) for c in str(task["task_id"]))
            target_node = hash_val % node_count

        task["assigned_node"] = f"Node {target_node + 1}"
        node_tasks[target_node].append(task)
        node_workloads[target_node] += task["burst_time"]

    nodes_results: List[Dict[str, Any]] = []
    all_metrics: Dict[str, Dict[str, Any]] = {}
    cluster_makespan = 0

    for i in range(node_count):
        ntasks = node_tasks[i]
        if local_algorithm == "RR":
            slices, metrics = round_robin_schedule(ntasks, time_quantum=time_quantum)
        elif local_algorithm == "SJF":
            slices, metrics = sjf_schedule(ntasks)
        else:
            slices, metrics = fcfs_schedule(ntasks)

        summary = calculate_metrics_summary(metrics, slices)
        nodes_results.append(
            {
                "node_id": f"Node {i + 1}",
                "tasks": ntasks,
                "slices": slices,
                "metrics": metrics,
                "summary": summary,
            }
        )
        if summary["makespan"] > cluster_makespan:
            cluster_makespan = summary["makespan"]
        all_metrics.update(metrics)

    metrics_list = list(all_metrics.values())
    total_tasks = len(metrics_list)
    avg_waiting = (
        round(sum(m["waiting_time"] for m in metrics_list) / total_tasks, 2)
        if total_tasks > 0
        else 0.0
    )
    avg_turnaround = (
        round(sum(m["turnaround_time"] for m in metrics_list) / total_tasks, 2)
        if total_tasks > 0
        else 0.0
    )
    active_nodes = [n for n in nodes_results if n["summary"]["total_tasks"] > 0]
    avg_cpu_util = (
        round(
            sum(n["summary"]["cpu_utilization"] for n in active_nodes)
            / len(active_nodes),
            2,
        )
        if active_nodes
        else 0.0
    )

    return {
        "nodes": nodes_results,
        "cluster_makespan": cluster_makespan,
        "total_tasks": total_tasks,
        "avg_waiting_time": avg_waiting,
        "avg_turnaround_time": avg_turnaround,
        "avg_cpu_utilization": avg_cpu_util,
    }
