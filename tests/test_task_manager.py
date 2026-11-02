import unittest
<<<<<<< HEAD
=======

>>>>>>> 4ab66d6ce60f640de08a69a5ff3c9989b6d222f1
from task_manager import generate_sample_tasks, prepare_tasks, validate_tasks


class TestTaskManager(unittest.TestCase):
<<<<<<< HEAD
    def test_generate_sample_tasks(self):
        tasks = generate_sample_tasks()
        self.assertEqual(len(tasks), 4)
        task_ids = [t["task_id"] for t in tasks]
        self.assertEqual(task_ids, ["T1", "T2", "T3", "T4"])
        for t in tasks:
            self.assertEqual(t["status"], "Waiting")
            self.assertEqual(t["remaining_time"], t["burst_time"])
            self.assertIsNone(t["assigned_node"])

    def test_validate_tasks_valid(self):
        sample = generate_sample_tasks()
        validate_tasks(sample)

    def test_validate_tasks_type_errors(self):
        with self.assertRaises(TypeError):
            validate_tasks("not a list")
        with self.assertRaises(TypeError):
            validate_tasks([123])
        with self.assertRaises(TypeError):
            validate_tasks([{"task_id": 1, "arrival_time": 0, "burst_time": 5}])
        with self.assertRaises(TypeError):
            validate_tasks([{"task_id": "T1", "arrival_time": True, "burst_time": 5}])
        with self.assertRaises(TypeError):
            validate_tasks([{"task_id": "T1", "arrival_time": 0, "burst_time": False}])

    def test_validate_tasks_value_errors(self):
        with self.assertRaises(ValueError):
            validate_tasks([{"task_id": "", "arrival_time": 0, "burst_time": 5}])
        with self.assertRaises(ValueError):
            validate_tasks([
                {"task_id": "T1", "arrival_time": 0, "burst_time": 5},
                {"task_id": "T1", "arrival_time": 1, "burst_time": 3},
            ])
        with self.assertRaises(ValueError):
            validate_tasks([{"task_id": "T1", "arrival_time": -1, "burst_time": 5}])
        with self.assertRaises(ValueError):
            validate_tasks([{"task_id": "T1", "arrival_time": 0, "burst_time": 0}])

    def test_prepare_tasks(self):
        raw = [
            {"task_id": "A", "arrival_time": 0, "burst_time": 5},
            {"task_id": "B", "arrival_time": 2, "burst_time": 4},
        ]
        prepared = prepare_tasks(raw)
        self.assertEqual(len(prepared), 2)
        self.assertEqual(prepared[0]["remaining_time"], 5)
        self.assertEqual(prepared[1]["remaining_time"], 4)
        # Verify deep copy
        prepared[0]["remaining_time"] = 0
        self.assertEqual(raw[0]["burst_time"], 5)
=======
    def test_generate_sample_tasks_structure(self):
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
        tasks = generate_sample_tasks()
        total_tasks = len(tasks)
        total_burst = sum((t["burst_time"] for t in tasks))
        self.assertEqual(total_tasks, 4)
        self.assertEqual(total_burst, 18)

    def test_validate_tasks_valid_input(self):
        tasks = generate_sample_tasks()
        validate_tasks(tasks)

    def test_validate_tasks_empty_list(self):
        validate_tasks([])
        prepared = prepare_tasks([])
        self.assertEqual(prepared, [])

    def test_validate_tasks_not_a_list(self):
        with self.assertRaises(TypeError):
            validate_tasks("not a list")
        with self.assertRaises(TypeError):
            validate_tasks({"task_id": "T1", "arrival_time": 0, "burst_time": 5})

    def test_validate_tasks_element_not_a_dict(self):
        with self.assertRaises(TypeError):
            validate_tasks(["not_a_dict"])

    def test_validate_tasks_missing_fields(self):
        with self.assertRaises(ValueError):
            validate_tasks([{"arrival_time": 0, "burst_time": 5}])
        with self.assertRaises(ValueError):
            validate_tasks([{"task_id": "T1", "burst_time": 5}])
        with self.assertRaises(ValueError):
            validate_tasks([{"task_id": "T1", "arrival_time": 0}])

    def test_validate_tasks_empty_or_duplicate_task_id(self):
        with self.assertRaises(ValueError):
            validate_tasks([{"task_id": "", "arrival_time": 0, "burst_time": 5}])
        with self.assertRaises(ValueError):
            validate_tasks([{"task_id": "   ", "arrival_time": 0, "burst_time": 5}])
        tasks = [
            {"task_id": "T1", "arrival_time": 0, "burst_time": 5},
            {"task_id": "T1", "arrival_time": 1, "burst_time": 3},
        ]
        with self.assertRaises(ValueError):
            validate_tasks(tasks)

    def test_validate_tasks_invalid_arrival_time(self):
        with self.assertRaises(ValueError):
            validate_tasks([{"task_id": "T1", "arrival_time": -1, "burst_time": 5}])
        with self.assertRaises(TypeError):
            validate_tasks([{"task_id": "T1", "arrival_time": 1.5, "burst_time": 5}])
        with self.assertRaises(TypeError):
            validate_tasks([{"task_id": "T1", "arrival_time": "0", "burst_time": 5}])

    def test_validate_tasks_invalid_burst_time(self):
        with self.assertRaises(ValueError):
            validate_tasks([{"task_id": "T1", "arrival_time": 0, "burst_time": 0}])
        with self.assertRaises(ValueError):
            validate_tasks([{"task_id": "T1", "arrival_time": 0, "burst_time": -4}])
        with self.assertRaises(TypeError):
            validate_tasks([{"task_id": "T1", "arrival_time": 0, "burst_time": 2.5}])

    def test_validate_tasks_boolean_rejection(self):
        with self.assertRaises(TypeError):
            validate_tasks([{"task_id": "T1", "arrival_time": True, "burst_time": 5}])
        with self.assertRaises(TypeError):
            validate_tasks([{"task_id": "T1", "arrival_time": False, "burst_time": 5}])
        with self.assertRaises(TypeError):
            validate_tasks([{"task_id": "T1", "arrival_time": 0, "burst_time": True}])

    def test_prepare_tasks_does_not_mutate_original(self):
        original = [
            {"task_id": "T1", "arrival_time": 0, "burst_time": 5},
            {"task_id": "T2", "arrival_time": 1, "burst_time": 3},
        ]
        prepared = prepare_tasks(original)
        prepared[0]["status"] = "Running"
        prepared[0]["remaining_time"] = 2
        prepared[0]["assigned_node"] = "Node-1"
        self.assertNotIn("status", original[0])
        self.assertNotIn("remaining_time", original[0])
        self.assertNotIn("assigned_node", original[0])
        self.assertEqual(prepared[0]["status"], "Running")
        self.assertEqual(prepared[0]["remaining_time"], 2)
        self.assertEqual(prepared[0]["assigned_node"], "Node-1")
        self.assertEqual(prepared[1]["status"], "Waiting")
        self.assertEqual(prepared[1]["remaining_time"], 3)
        self.assertIsNone(prepared[1]["assigned_node"])
>>>>>>> 4ab66d6ce60f640de08a69a5ff3c9989b6d222f1


if __name__ == "__main__":
    unittest.main()
