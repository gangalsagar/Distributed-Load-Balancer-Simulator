import unittest
from task_manager import generate_sample_tasks, prepare_tasks, validate_tasks


class TestTaskManager(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
