import unittest

from schedulers.round_robin import round_robin_schedule
from task_manager import generate_sample_tasks


class TestRoundRobinScheduler(unittest.TestCase):
    def test_sample_workload_default_quantum(self):
        tasks = generate_sample_tasks()
        slices, metrics = round_robin_schedule(tasks, time_quantum=2)
        self.assertEqual(len(slices), 10)
        expected_slices = [
            ("T1", 0, 2, 2, 3, False),
            ("T2", 2, 4, 2, 1, False),
            ("T3", 4, 6, 2, 6, False),
            ("T1", 6, 8, 2, 1, False),
            ("T4", 8, 10, 2, 0, True),
            ("T2", 10, 11, 1, 0, True),
            ("T3", 11, 13, 2, 4, False),
            ("T1", 13, 14, 1, 0, True),
            ("T3", 14, 16, 2, 2, False),
            ("T3", 16, 18, 2, 0, True),
        ]
        for s, exp in zip(slices, expected_slices):
            self.assertEqual(s["task_id"], exp[0])
            self.assertEqual(s["start_time"], exp[1])
            self.assertEqual(s["end_time"], exp[2])
            self.assertEqual(s["duration"], exp[3])
            self.assertEqual(s["remaining_time"], exp[4])
            self.assertEqual(s["completed"], exp[5])
        self.assertEqual(metrics["T4"]["completion_time"], 10)
        self.assertEqual(metrics["T2"]["completion_time"], 11)
        self.assertEqual(metrics["T1"]["completion_time"], 14)
        self.assertEqual(metrics["T3"]["completion_time"], 18)
        self.assertEqual(metrics["T4"]["turnaround_time"], 7)
        self.assertEqual(metrics["T2"]["turnaround_time"], 10)
        self.assertEqual(metrics["T1"]["turnaround_time"], 14)
        self.assertEqual(metrics["T3"]["turnaround_time"], 16)
        self.assertEqual(metrics["T4"]["waiting_time"], 5)
        self.assertEqual(metrics["T2"]["waiting_time"], 7)
        self.assertEqual(metrics["T1"]["waiting_time"], 9)
        self.assertEqual(metrics["T3"]["waiting_time"], 8)
        avg_wait = sum((m["waiting_time"] for m in metrics.values())) / len(metrics)
        avg_tat = sum((m["turnaround_time"] for m in metrics.values())) / len(metrics)
        self.assertAlmostEqual(avg_wait, 7.25)
        self.assertAlmostEqual(avg_tat, 11.75)

    def test_all_tasks_arrive_at_zero(self):
        tasks = [
            {"task_id": "T1", "arrival_time": 0, "burst_time": 4},
            {"task_id": "T2", "arrival_time": 0, "burst_time": 3},
            {"task_id": "T3", "arrival_time": 0, "burst_time": 1},
        ]
        slices, metrics = round_robin_schedule(tasks, time_quantum=2)
        self.assertEqual(metrics["T3"]["completion_time"], 5)
        self.assertEqual(metrics["T1"]["completion_time"], 7)
        self.assertEqual(metrics["T2"]["completion_time"], 8)
        self.assertEqual(metrics["T3"]["waiting_time"], 4)
        self.assertEqual(metrics["T1"]["waiting_time"], 3)
        self.assertEqual(metrics["T2"]["waiting_time"], 5)

    def test_empty_task_list(self):
        slices, metrics = round_robin_schedule([])
        self.assertEqual(slices, [])
        self.assertEqual(metrics, {})

    def test_invalid_tasks_and_quantum(self):
        with self.assertRaises(TypeError):
            round_robin_schedule([], time_quantum=2.5)
        with self.assertRaises(TypeError):
            round_robin_schedule([], time_quantum=True)
        with self.assertRaises(ValueError):
            round_robin_schedule([], time_quantum=0)


if __name__ == "__main__":
    unittest.main()
