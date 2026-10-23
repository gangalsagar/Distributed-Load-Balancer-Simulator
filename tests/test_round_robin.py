"""
Unit Tests for Round Robin CPU Scheduling Algorithm.

Validates:
- All tasks arriving at time 0.
- Tasks arriving at different times.
- Tasks arriving while another task is executing.
- Burst times shorter than, equal to, and longer than quantum.
- CPU idle time before first task arrives or between task gaps.
- Empty task input handling.
- Input validation (invalid tasks, invalid or boolean time quantum).
- Non-mutation of original caller's task list.
- Exact one-time completion per task.
- Non-violation of causality (no task executes before arrival).
- Correct completion, waiting, and turnaround times on standard workloads.
"""

import unittest
from schedulers.round_robin import round_robin_schedule
from task_manager import generate_sample_tasks


class TestRoundRobinScheduler(unittest.TestCase):
    def test_sample_workload_default_quantum(self):
        """
        Verify the standard sample workload with quantum = 2:
        T1: arrival 0, burst 5
        T2: arrival 1, burst 3
        T3: arrival 2, burst 8
        T4: arrival 3, burst 2

        Timeline trace:
        - t=0: queue=[T1]. T1 runs [0, 2], rem=3. Arrivals at/before 2: T2 (arr 1), T3 (arr 2).
          T1 requeued -> queue=[T2, T3, T1].
        - t=2: T2 runs [2, 4], rem=1. Arrivals at/before 4: T4 (arr 3).
          T2 requeued -> queue=[T3, T1, T4, T2].
        - t=4: T3 runs [4, 6], rem=6.
          T3 requeued -> queue=[T1, T4, T2, T3].
        - t=6: T1 runs [6, 8], rem=1.
          T1 requeued -> queue=[T4, T2, T3, T1].
        - t=8: T4 runs [8, 10], rem=0 -> Completes at 10.
          queue=[T2, T3, T1].
        - t=10: T2 runs [10, 11], rem=0 -> Completes at 11.
          queue=[T3, T1].
        - t=11: T3 runs [11, 13], rem=4.
          T3 requeued -> queue=[T1, T3].
        - t=13: T1 runs [13, 14], rem=0 -> Completes at 14.
          queue=[T3].
        - t=14: T3 runs [14, 16], rem=2.
          queue=[T3].
        - t=16: T3 runs [16, 18], rem=0 -> Completes at 18.
        """
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

        # Completion times
        self.assertEqual(metrics["T4"]["completion_time"], 10)
        self.assertEqual(metrics["T2"]["completion_time"], 11)
        self.assertEqual(metrics["T1"]["completion_time"], 14)
        self.assertEqual(metrics["T3"]["completion_time"], 18)

        # Turnaround times (completion - arrival):
        # T4: 10 - 3 = 7
        # T2: 11 - 1 = 10
        # T1: 14 - 0 = 14
        # T3: 18 - 2 = 16
        self.assertEqual(metrics["T4"]["turnaround_time"], 7)
        self.assertEqual(metrics["T2"]["turnaround_time"], 10)
        self.assertEqual(metrics["T1"]["turnaround_time"], 14)
        self.assertEqual(metrics["T3"]["turnaround_time"], 16)

        # Waiting times (turnaround - burst):
        # T4: 7 - 2 = 5
        # T2: 10 - 3 = 7
        # T1: 14 - 5 = 9
        # T3: 16 - 8 = 8
        self.assertEqual(metrics["T4"]["waiting_time"], 5)
        self.assertEqual(metrics["T2"]["waiting_time"], 7)
        self.assertEqual(metrics["T1"]["waiting_time"], 9)
        self.assertEqual(metrics["T3"]["waiting_time"], 8)

        # Averages
        avg_wait = sum(m["waiting_time"] for m in metrics.values()) / len(metrics)
        avg_tat = sum(m["turnaround_time"] for m in metrics.values()) / len(metrics)
        self.assertAlmostEqual(avg_wait, 7.25)
        self.assertAlmostEqual(avg_tat, 11.75)

    def test_all_tasks_arrive_at_zero(self):
        """Test scheduling when all tasks arrive simultaneously at time 0."""
        tasks = [
            {"task_id": "T1", "arrival_time": 0, "burst_time": 4},
            {"task_id": "T2", "arrival_time": 0, "burst_time": 3},
            {"task_id": "T3", "arrival_time": 0, "burst_time": 1},
        ]
        slices, metrics = round_robin_schedule(tasks, time_quantum=2)

        # Slices with q=2:
        # [0, 2]: T1 (rem 2)
        # [2, 4]: T2 (rem 1)
        # [4, 5]: T3 (rem 0, completes at 5)
        # [5, 7]: T1 (rem 0, completes at 7)
        # [7, 8]: T2 (rem 0, completes at 8)
        self.assertEqual(metrics["T3"]["completion_time"], 5)
        self.assertEqual(metrics["T1"]["completion_time"], 7)
        self.assertEqual(metrics["T2"]["completion_time"], 8)

        # Turnaround: T3=5, T1=7, T2=8
        # Waiting: T3=5-1=4, T1=7-4=3, T2=8-3=5
        self.assertEqual(metrics["T3"]["waiting_time"], 4)
        self.assertEqual(metrics["T1"]["waiting_time"], 3)
        self.assertEqual(metrics["T2"]["waiting_time"], 5)

    def test_tasks_arriving_at_different_times_and_during_execution(self):
        """Test task arriving in the middle of another task's slice."""
        tasks = [
            {"task_id": "A", "arrival_time": 0, "burst_time": 4},
            {"task_id": "B", "arrival_time": 1, "burst_time": 2},
        ]
        # q=3: A runs [0, 3], B arrived at 1. Then A requeued (rem 1). B runs [3, 5], finishes. A runs [5, 6].
        slices, metrics = round_robin_schedule(tasks, time_quantum=3)
        self.assertEqual(len(slices), 3)
        self.assertEqual(slices[0]["task_id"], "A")
        self.assertEqual(slices[1]["task_id"], "B")
        self.assertEqual(slices[2]["task_id"], "A")
        self.assertEqual(metrics["B"]["completion_time"], 5)
        self.assertEqual(metrics["A"]["completion_time"], 6)

    def test_burst_times_shorter_equal_longer_than_quantum(self):
        """Test mixture of burst times: shorter (< q), equal (== q), and longer (> q)."""
        tasks = [
            {"task_id": "SHORT", "arrival_time": 0, "burst_time": 1},   # < 3
            {"task_id": "EQUAL", "arrival_time": 0, "burst_time": 3},   # == 3
            {"task_id": "LONG", "arrival_time": 0, "burst_time": 7},    # > 3
        ]
        slices, metrics = round_robin_schedule(tasks, time_quantum=3)
        # Preserving input list order at t=0:
        # [0, 1]: SHORT (completes at 1)
        # [1, 4]: EQUAL (completes at 4)
        # [4, 7]: LONG (rem 4)
        # [7, 10]: LONG (rem 1)
        # [10, 11]: LONG (completes at 11)
        self.assertEqual(metrics["SHORT"]["completion_time"], 1)
        self.assertEqual(metrics["EQUAL"]["completion_time"], 4)
        self.assertEqual(metrics["LONG"]["completion_time"], 11)

    def test_cpu_idle_before_first_task_and_gaps(self):
        """Test simulation when CPU is initially idle or between tasks."""
        tasks = [
            {"task_id": "T1", "arrival_time": 5, "burst_time": 2},
            {"task_id": "T2", "arrival_time": 10, "burst_time": 3},
        ]
        slices, metrics = round_robin_schedule(tasks, time_quantum=2)
        # T1 runs [5, 7]
        # CPU idle [7, 10]
        # T2 runs [10, 12], [12, 13]
        self.assertEqual(slices[0]["start_time"], 5)
        self.assertEqual(slices[0]["end_time"], 7)
        self.assertEqual(metrics["T1"]["completion_time"], 7)
        self.assertEqual(slices[1]["start_time"], 10)
        self.assertEqual(metrics["T2"]["completion_time"], 13)

    def test_empty_task_list(self):
        """Test that empty input returns empty slices and empty metrics."""
        slices, metrics = round_robin_schedule([])
        self.assertEqual(slices, [])
        self.assertEqual(metrics, {})

    def test_invalid_tasks_and_quantum(self):
        """Test rejection of invalid task inputs and invalid quantum parameters."""
        # Non-integer quantum
        with self.assertRaises(TypeError):
            round_robin_schedule([], time_quantum=2.5)
        # Boolean quantum
        with self.assertRaises(TypeError):
            round_robin_schedule([], time_quantum=True)
        # Non-positive quantum
        with self.assertRaises(ValueError):
            round_robin_schedule([], time_quantum=0)
        with self.assertRaises(ValueError):
            round_robin_schedule([], time_quantum=-2)

        # Invalid tasks
        with self.assertRaises(TypeError):
            round_robin_schedule("not_a_list")
        with self.assertRaises(ValueError):
            round_robin_schedule([{"task_id": "T1", "arrival_time": -1, "burst_time": 2}])

    def test_input_tasks_remain_unchanged(self):
        """Test that the caller's original task dictionaries are never modified."""
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
        """Verify no task runs prior to arrival and each completes exactly once."""
        tasks = [
            {"task_id": "T1", "arrival_time": 4, "burst_time": 6},
            {"task_id": "T2", "arrival_time": 6, "burst_time": 2},
        ]
        slices, metrics = round_robin_schedule(tasks, time_quantum=2)

        completed_events = {}
        for s in slices:
            # Task must have arrived before or at start_time
            arrival = metrics[s["task_id"]]["arrival_time"]
            self.assertGreaterEqual(s["start_time"], arrival)

            if s["completed"]:
                completed_events[s["task_id"]] = completed_events.get(s["task_id"], 0) + 1

        # Every task must complete exactly once
        for task in tasks:
            tid = task["task_id"]
            self.assertEqual(completed_events.get(tid), 1)


if __name__ == "__main__":
    unittest.main()
