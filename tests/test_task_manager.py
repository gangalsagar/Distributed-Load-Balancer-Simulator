"""
Unit Tests for Task Management Module.

Tests task generation, validation rules (types, constraints, edge cases),
immutability of original structures during preparation, and empty workloads.
"""

import unittest
from task_manager import generate_sample_tasks, validate_tasks, prepare_tasks


class TestTaskManager(unittest.TestCase):
    def test_generate_sample_tasks_structure(self):
        """Verify sample task generation yields 4 tasks with all required fields."""
        tasks = generate_sample_tasks()
        self.assertIsInstance(tasks, list)
        self.assertEqual(len(tasks), 4)

        expected_ids = ["T1", "T2", "T3", "T4"]
        expected_bursts = [5, 3, 8, 2]
        expected_arrivals = [0, 1, 2, 3]

        for i, task in enumerate(tasks):
            self.assertEqual(task["task_id"], expected_ids[i])
            self.assertEqual(task["arrival_time"], expected_arrivals[i])
            self.assertEqual(task["burst_time"], expected_bursts[i])
            self.assertEqual(task["remaining_time"], expected_bursts[i])
            self.assertEqual(task["status"], "Waiting")
            self.assertIsNone(task["assigned_node"])

    def test_total_tasks_and_burst_time(self):
        """Verify standard sample workload metrics: 4 tasks and 18 total burst time."""
        tasks = generate_sample_tasks()
        total_tasks = len(tasks)
        total_burst = sum(t["burst_time"] for t in tasks)
        self.assertEqual(total_tasks, 4)
        self.assertEqual(total_burst, 18)

    def test_validate_tasks_valid_input(self):
        """Verify that properly formatted tasks pass validation without exceptions."""
        tasks = generate_sample_tasks()
        # Should not raise any error
        validate_tasks(tasks)

    def test_validate_tasks_empty_list(self):
        """Verify empty list is accepted as a valid empty workload."""
        validate_tasks([])
        prepared = prepare_tasks([])
        self.assertEqual(prepared, [])

    def test_validate_tasks_not_a_list(self):
        """Verify non-list container raises TypeError."""
        with self.assertRaises(TypeError):
            validate_tasks("not a list")
        with self.assertRaises(TypeError):
            validate_tasks({"task_id": "T1", "arrival_time": 0, "burst_time": 5})

    def test_validate_tasks_element_not_a_dict(self):
        """Verify non-dict items in list raise TypeError."""
        with self.assertRaises(TypeError):
            validate_tasks(["not_a_dict"])

    def test_validate_tasks_missing_fields(self):
        """Verify missing required fields raise ValueError."""
        # Missing task_id
        with self.assertRaises(ValueError):
            validate_tasks([{"arrival_time": 0, "burst_time": 5}])
        # Missing arrival_time
        with self.assertRaises(ValueError):
            validate_tasks([{"task_id": "T1", "burst_time": 5}])
        # Missing burst_time
        with self.assertRaises(ValueError):
            validate_tasks([{"task_id": "T1", "arrival_time": 0}])

    def test_validate_tasks_empty_or_duplicate_task_id(self):
        """Verify empty task_id or duplicate task_id raises ValueError."""
        # Empty string
        with self.assertRaises(ValueError):
            validate_tasks([{"task_id": "", "arrival_time": 0, "burst_time": 5}])
        # Whitespace
        with self.assertRaises(ValueError):
            validate_tasks([{"task_id": "   ", "arrival_time": 0, "burst_time": 5}])
        # Duplicate ID
        tasks = [
            {"task_id": "T1", "arrival_time": 0, "burst_time": 5},
            {"task_id": "T1", "arrival_time": 1, "burst_time": 3},
        ]
        with self.assertRaises(ValueError):
            validate_tasks(tasks)

    def test_validate_tasks_invalid_arrival_time(self):
        """Verify negative arrival_time or invalid types raise appropriate errors."""
        # Negative arrival_time
        with self.assertRaises(ValueError):
            validate_tasks([{"task_id": "T1", "arrival_time": -1, "burst_time": 5}])
        # Float arrival_time
        with self.assertRaises(TypeError):
            validate_tasks([{"task_id": "T1", "arrival_time": 1.5, "burst_time": 5}])
        # String arrival_time
        with self.assertRaises(TypeError):
            validate_tasks([{"task_id": "T1", "arrival_time": "0", "burst_time": 5}])

    def test_validate_tasks_invalid_burst_time(self):
        """Verify zero, negative, or invalid types for burst_time raise errors."""
        # Zero burst_time
        with self.assertRaises(ValueError):
            validate_tasks([{"task_id": "T1", "arrival_time": 0, "burst_time": 0}])
        # Negative burst_time
        with self.assertRaises(ValueError):
            validate_tasks([{"task_id": "T1", "arrival_time": 0, "burst_time": -4}])
        # Float burst_time
        with self.assertRaises(TypeError):
            validate_tasks([{"task_id": "T1", "arrival_time": 0, "burst_time": 2.5}])

    def test_validate_tasks_boolean_rejection(self):
        """Verify Python booleans (which are int subclasses) are strictly rejected."""
        # Boolean arrival_time
        with self.assertRaises(TypeError):
            validate_tasks([{"task_id": "T1", "arrival_time": True, "burst_time": 5}])
        with self.assertRaises(TypeError):
            validate_tasks([{"task_id": "T1", "arrival_time": False, "burst_time": 5}])
        # Boolean burst_time
        with self.assertRaises(TypeError):
            validate_tasks([{"task_id": "T1", "arrival_time": 0, "burst_time": True}])

    def test_prepare_tasks_does_not_mutate_original(self):
        """Verify prepare_tasks creates an independent working copy without altering input."""
        original = [
            {"task_id": "T1", "arrival_time": 0, "burst_time": 5},
            {"task_id": "T2", "arrival_time": 1, "burst_time": 3},
        ]
        prepared = prepare_tasks(original)

        # Mutate prepared copy
        prepared[0]["status"] = "Running"
        prepared[0]["remaining_time"] = 2
        prepared[0]["assigned_node"] = "Node-1"

        # Check original is untouched
        self.assertNotIn("status", original[0])
        self.assertNotIn("remaining_time", original[0])
        self.assertNotIn("assigned_node", original[0])

        # Verify prepared task has correct updated fields
        self.assertEqual(prepared[0]["status"], "Running")
        self.assertEqual(prepared[0]["remaining_time"], 2)
        self.assertEqual(prepared[0]["assigned_node"], "Node-1")

        # Second prepared task has default initializations
        self.assertEqual(prepared[1]["status"], "Waiting")
        self.assertEqual(prepared[1]["remaining_time"], 3)
        self.assertIsNone(prepared[1]["assigned_node"])


if __name__ == "__main__":
    unittest.main()
