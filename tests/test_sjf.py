import unittest

from schedulers.sjf import sjf_schedule
from task_manager import generate_sample_tasks


class TestSJFScheduler(unittest.TestCase):
    def test_sample_workload(self):
        tasks = generate_sample_tasks()
        slices, metrics = sjf_schedule(tasks)
        self.assertEqual(len(slices), 4)
        expected_order = ["T1", "T4", "T2", "T3"]
        self.assertEqual([s["task_id"] for s in slices], expected_order)
        self.assertEqual(slices[0]["start_time"], 0)
        self.assertEqual(slices[0]["end_time"], 5)
        self.assertEqual(slices[1]["start_time"], 5)
        self.assertEqual(slices[1]["end_time"], 7)
        self.assertEqual(slices[2]["start_time"], 7)
        self.assertEqual(slices[2]["end_time"], 10)
        self.assertEqual(slices[3]["start_time"], 10)
        self.assertEqual(slices[3]["end_time"], 18)
        self.assertEqual(metrics["T1"]["completion_time"], 5)
        self.assertEqual(metrics["T4"]["completion_time"], 7)
        self.assertEqual(metrics["T2"]["completion_time"], 10)
        self.assertEqual(metrics["T3"]["completion_time"], 18)

    def test_shortest_available_selected_first(self):
        tasks = [
            {"task_id": "T_LONG", "arrival_time": 0, "burst_time": 10},
            {"task_id": "T_SHORT", "arrival_time": 0, "burst_time": 2},
            {"task_id": "T_MED", "arrival_time": 0, "burst_time": 6},
        ]
        slices, metrics = sjf_schedule(tasks)
        self.assertEqual([s["task_id"] for s in slices], ["T_SHORT", "T_MED", "T_LONG"])

    def test_equal_burst_times_deterministic_tie_breaker(self):
        tasks_same_arr = [
            {"task_id": "Task_Z", "arrival_time": 0, "burst_time": 3},
            {"task_id": "Task_A", "arrival_time": 0, "burst_time": 3},
            {"task_id": "Task_M", "arrival_time": 0, "burst_time": 3},
        ]
        slices_b, _ = sjf_schedule(tasks_same_arr)
        self.assertEqual(
            [s["task_id"] for s in slices_b], ["Task_A", "Task_M", "Task_Z"]
        )


if __name__ == "__main__":
    unittest.main()
