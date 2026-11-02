import copy
import unittest

from schedulers.fcfs import fcfs_schedule
from task_manager import generate_sample_tasks


class TestFCFSScheduler(unittest.TestCase):
    def test_sample_workload(self):
        tasks = generate_sample_tasks()
        slices, metrics = fcfs_schedule(tasks)
        self.assertEqual(len(slices), 4)
        expected_slices = [
            ("T1", 0, 5, 5, 0, True),
            ("T2", 5, 8, 3, 0, True),
            ("T3", 8, 16, 8, 0, True),
            ("T4", 16, 18, 2, 0, True),
        ]
        for s, expected in zip(slices, expected_slices):
            self.assertEqual(s["task_id"], expected[0])
            self.assertEqual(s["start_time"], expected[1])
            self.assertEqual(s["end_time"], expected[2])
            self.assertEqual(s["duration"], expected[3])
            self.assertEqual(s["remaining_time"], expected[4])
            self.assertEqual(s["completed"], expected[5])
        self.assertEqual(metrics["T1"]["completion_time"], 5)
        self.assertEqual(metrics["T1"]["turnaround_time"], 5)
        self.assertEqual(metrics["T1"]["waiting_time"], 0)
        self.assertEqual(metrics["T2"]["completion_time"], 8)
        self.assertEqual(metrics["T2"]["turnaround_time"], 7)
        self.assertEqual(metrics["T2"]["waiting_time"], 4)
        self.assertEqual(metrics["T3"]["completion_time"], 16)
        self.assertEqual(metrics["T3"]["turnaround_time"], 14)
        self.assertEqual(metrics["T3"]["waiting_time"], 6)
        self.assertEqual(metrics["T4"]["completion_time"], 18)
        self.assertEqual(metrics["T4"]["turnaround_time"], 15)
        self.assertEqual(metrics["T4"]["waiting_time"], 13)

    def test_tasks_supplied_out_of_arrival_order(self):
        tasks = [
            {"task_id": "T3", "arrival_time": 4, "burst_time": 2},
            {"task_id": "T1", "arrival_time": 0, "burst_time": 3},
            {"task_id": "T2", "arrival_time": 2, "burst_time": 4},
        ]
        slices, metrics = fcfs_schedule(tasks)
        self.assertEqual([s["task_id"] for s in slices], ["T1", "T2", "T3"])
        self.assertEqual(slices[0]["start_time"], 0)
        self.assertEqual(slices[0]["end_time"], 3)
        self.assertEqual(slices[1]["start_time"], 3)
        self.assertEqual(slices[1]["end_time"], 7)
        self.assertEqual(slices[2]["start_time"], 7)
        self.assertEqual(slices[2]["end_time"], 9)

    def test_equal_arrival_times_tie_breaker(self):
        tasks = [
            {"task_id": "Task_C", "arrival_time": 0, "burst_time": 2},
            {"task_id": "Task_A", "arrival_time": 0, "burst_time": 3},
            {"task_id": "Task_B", "arrival_time": 0, "burst_time": 1},
        ]
        slices, metrics = fcfs_schedule(tasks)
        order = [s["task_id"] for s in slices]
        self.assertEqual(order, ["Task_A", "Task_B", "Task_C"])

    def test_cpu_idle_before_first_task_and_gaps(self):
        tasks = [
            {"task_id": "T1", "arrival_time": 5, "burst_time": 3},
            {"task_id": "T2", "arrival_time": 12, "burst_time": 4},
        ]
        slices, metrics = fcfs_schedule(tasks)
        self.assertEqual(len(slices), 2)
        self.assertEqual(slices[0]["task_id"], "T1")
        self.assertEqual(slices[0]["start_time"], 5)
        self.assertEqual(slices[0]["end_time"], 8)
        self.assertEqual(metrics["T1"]["waiting_time"], 0)
        self.assertEqual(metrics["T1"]["turnaround_time"], 3)
        self.assertEqual(slices[1]["task_id"], "T2")
        self.assertEqual(slices[1]["start_time"], 12)
        self.assertEqual(slices[1]["end_time"], 16)
        self.assertEqual(metrics["T2"]["waiting_time"], 0)
        self.assertEqual(metrics["T2"]["turnaround_time"], 4)

    def test_empty_task_list(self):
        slices, metrics = fcfs_schedule([])
        self.assertEqual(slices, [])
        self.assertEqual(metrics, {})

    def test_invalid_task_input(self):
        with self.assertRaises(TypeError):
            fcfs_schedule("not_a_list")
        with self.assertRaises(TypeError):
            fcfs_schedule(
                [{"task_id": "T1", "arrival_time": "invalid", "burst_time": 5}]
            )
        with self.assertRaises(ValueError):
            fcfs_schedule([{"task_id": "T1", "arrival_time": -1, "burst_time": 5}])
        with self.assertRaises(ValueError):
            fcfs_schedule([{"task_id": "T1", "arrival_time": 0, "burst_time": 0}])

    def test_input_tasks_remain_unchanged(self):
        original_tasks = [
            {"task_id": "T1", "arrival_time": 2, "burst_time": 4},
            {"task_id": "T2", "arrival_time": 0, "burst_time": 3},
        ]
        snapshot = copy.deepcopy(original_tasks)
        slices, metrics = fcfs_schedule(original_tasks)
        self.assertEqual(original_tasks, snapshot)

    def test_every_task_executes_once_and_completes(self):
        tasks = [
            {"task_id": "T1", "arrival_time": 0, "burst_time": 5},
            {"task_id": "T2", "arrival_time": 1, "burst_time": 4},
            {"task_id": "T3", "arrival_time": 2, "burst_time": 3},
        ]
        slices, metrics = fcfs_schedule(tasks)
        self.assertEqual(len(slices), 3)
        self.assertEqual(len(metrics), 3)
        for s in slices:
            self.assertTrue(s["completed"])
            self.assertEqual(s["remaining_time"], 0)


if __name__ == "__main__":
    unittest.main()
