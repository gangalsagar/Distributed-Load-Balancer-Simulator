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

<<<<<<< HEAD
=======
    def test_tasks_arriving_at_different_times_and_during_execution(self):
        tasks = [
            {"task_id": "A", "arrival_time": 0, "burst_time": 4},
            {"task_id": "B", "arrival_time": 1, "burst_time": 2},
        ]
        slices, metrics = round_robin_schedule(tasks, time_quantum=3)
        self.assertEqual(len(slices), 3)
        self.assertEqual(slices[0]["task_id"], "A")
        self.assertEqual(slices[1]["task_id"], "B")
        self.assertEqual(slices[2]["task_id"], "A")
        self.assertEqual(metrics["B"]["completion_time"], 5)
        self.assertEqual(metrics["A"]["completion_time"], 6)

    def test_burst_times_shorter_equal_longer_than_quantum(self):
        tasks = [
            {"task_id": "SHORT", "arrival_time": 0, "burst_time": 1},
            {"task_id": "EQUAL", "arrival_time": 0, "burst_time": 3},
            {"task_id": "LONG", "arrival_time": 0, "burst_time": 7},
        ]
        slices, metrics = round_robin_schedule(tasks, time_quantum=3)
        self.assertEqual(metrics["SHORT"]["completion_time"], 1)
        self.assertEqual(metrics["EQUAL"]["completion_time"], 4)
        self.assertEqual(metrics["LONG"]["completion_time"], 11)

    def test_cpu_idle_before_first_task_and_gaps(self):
        tasks = [
            {"task_id": "T1", "arrival_time": 5, "burst_time": 2},
            {"task_id": "T2", "arrival_time": 10, "burst_time": 3},
        ]
        slices, metrics = round_robin_schedule(tasks, time_quantum=2)
        self.assertEqual(slices[0]["start_time"], 5)
        self.assertEqual(slices[0]["end_time"], 7)
        self.assertEqual(metrics["T1"]["completion_time"], 7)
        self.assertEqual(slices[1]["start_time"], 10)
        self.assertEqual(metrics["T2"]["completion_time"], 13)

>>>>>>> 4ab66d6ce60f640de08a69a5ff3c9989b6d222f1
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
<<<<<<< HEAD
=======
        with self.assertRaises(ValueError):
            round_robin_schedule([], time_quantum=-2)
        with self.assertRaises(TypeError):
            round_robin_schedule("not_a_list")
        with self.assertRaises(ValueError):
            round_robin_schedule(
                [{"task_id": "T1", "arrival_time": -1, "burst_time": 2}]
            )

    def test_input_tasks_remain_unchanged(self):
        original = [
            {"task_id": "T1", "arrival_time": 0, "burst_time": 5},
            {"task_id": "T2", "arrival_time": 1, "burst_time": 3},
        ]
        original_copy = [dict(t) for t in original]
        round_robin_schedule(original, time_quantum=2)
        self.assertEqual(original, original_copy)
        self.assertNotIn("remaining_time", original[0])
        self.assertNotIn("status", original[0])
        self.assertNotIn("_order", original[0])

    def test_causality_and_single_completion(self):
        tasks = [
            {"task_id": "T1", "arrival_time": 4, "burst_time": 6},
            {"task_id": "T2", "arrival_time": 6, "burst_time": 2},
        ]
        slices, metrics = round_robin_schedule(tasks, time_quantum=2)
        completed_events = {}
        for s in slices:
            arrival = metrics[s["task_id"]]["arrival_time"]
            self.assertGreaterEqual(s["start_time"], arrival)
            if s["completed"]:
                completed_events[s["task_id"]] = (
                    completed_events.get(s["task_id"], 0) + 1
                )
        for task in tasks:
            tid = task["task_id"]
            self.assertEqual(completed_events.get(tid), 1)
>>>>>>> 4ab66d6ce60f640de08a69a5ff3c9989b6d222f1


if __name__ == "__main__":
    unittest.main()
