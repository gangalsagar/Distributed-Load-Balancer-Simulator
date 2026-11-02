import copy
from typing import Any, Dict, List, Optional


def generate_sample_tasks() -> List[Dict[str, Any]]:
    sample_definitions = [
        {"task_id": "T1", "arrival_time": 0, "burst_time": 5},
        {"task_id": "T2", "arrival_time": 1, "burst_time": 3},
        {"task_id": "T3", "arrival_time": 2, "burst_time": 8},
        {"task_id": "T4", "arrival_time": 3, "burst_time": 2},
    ]
    tasks: List[Dict[str, Any]] = []
    for item in sample_definitions:
        task = {
            "task_id": item["task_id"],
            "arrival_time": item["arrival_time"],
            "burst_time": item["burst_time"],
            "remaining_time": item["burst_time"],
            "status": "Waiting",
            "assigned_node": None,
        }
        tasks.append(task)
    return tasks


def validate_tasks(tasks: Any) -> None:
    if not isinstance(tasks, list):
        raise TypeError(f"Tasks collection must be a list, got {type(tasks).__name__}.")
    seen_ids = set()
    for index, task in enumerate(tasks):
        if not isinstance(task, dict):
            raise TypeError(
                f"Task at index {index} must be a dictionary, got {type(task).__name__}."
            )
        if "task_id" not in task:
            raise ValueError(
                f"Task at index {index} is missing required field 'task_id'."
            )
        task_id = task["task_id"]
        if not isinstance(task_id, str):
            raise TypeError(
                f"Task at index {index} 'task_id' must be a string, got {type(task_id).__name__}."
            )
        if not task_id.strip():
            raise ValueError(
                f"Task at index {index} 'task_id' cannot be empty or whitespace."
            )
        if task_id in seen_ids:
            raise ValueError(
                f"Duplicate task_id '{task_id}' detected at index {index}."
            )
        seen_ids.add(task_id)
        if "arrival_time" not in task:
            raise ValueError(
                f"Task '{task_id}' at index {index} is missing required field 'arrival_time'."
            )
        arrival_time = task["arrival_time"]
        if isinstance(arrival_time, bool) or not isinstance(arrival_time, int):
            raise TypeError(
                f"Task '{task_id}' 'arrival_time' must be an integer (booleans not accepted), got {type(arrival_time).__name__}."
            )
        if arrival_time < 0:
            raise ValueError(
                f"Task '{task_id}' 'arrival_time' must be non-negative (>= 0), got {arrival_time}."
            )
        if "burst_time" not in task:
            raise ValueError(
                f"Task '{task_id}' at index {index} is missing required field 'burst_time'."
            )
        burst_time = task["burst_time"]
        if isinstance(burst_time, bool) or not isinstance(burst_time, int):
            raise TypeError(
                f"Task '{task_id}' 'burst_time' must be an integer (booleans not accepted), got {type(burst_time).__name__}."
            )
        if burst_time <= 0:
            raise ValueError(
                f"Task '{task_id}' 'burst_time' must be a positive integer (> 0), got {burst_time}."
            )
        if "remaining_time" in task:
            rem = task["remaining_time"]
            if isinstance(rem, bool) or not isinstance(rem, int):
                raise TypeError(
                    f"Task '{task_id}' 'remaining_time' must be an integer, got {type(rem).__name__}."
                )
            if rem < 0:
                raise ValueError(
                    f"Task '{task_id}' 'remaining_time' cannot be negative, got {rem}."
                )
        if "status" in task and (not isinstance(task["status"], str)):
            raise TypeError(
                f"Task '{task_id}' 'status' must be a string, got {type(task['status']).__name__}."
            )
        if "assigned_node" in task and task["assigned_node"] is not None:
            if not isinstance(task["assigned_node"], str):
                raise TypeError(
                    f"Task '{task_id}' 'assigned_node' must be a string or None, got {type(task['assigned_node']).__name__}."
                )


def prepare_tasks(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    validate_tasks(tasks)
    prepared: List[Dict[str, Any]] = []
    for item in tasks:
        task_copy = copy.deepcopy(item)
        task_copy["remaining_time"] = task_copy["burst_time"]
        task_copy["status"] = "Waiting"
        task_copy["assigned_node"] = None
        prepared.append(task_copy)
    return prepared
