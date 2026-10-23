"""
Unit Tests for Metrics Module.
"""

import unittest
from metrics import calculate_metrics_summary, identify_idle_intervals


class TestMetricsModule(unittest.TestCase):
    def test_calculate_metrics_summary_empty(self):
        summary = calculate_metrics_summary({})
        self.assertEqual(summary["total_tasks"], 0)
        self.assertEqual(summary["avg_waiting_time"], 0.0)
        self.assertEqual(summary["avg_turnaround_time"], 0.0)
        self.assertEqual(summary["makespan"], 0)

    def test_calculate_metrics_summary_normal(self):
        task_metrics = {
            "T1": {"waiting_time": 4, "turnaround_time": 9, "completion_time": 9},
            "T2": {"waiting_time": 2, "turnaround_time": 5, "completion_time": 6},
        }
        summary = calculate_metrics_summary(task_metrics)
        self.assertEqual(summary["total_tasks"], 2)
        self.assertEqual(summary["avg_waiting_time"], 3.0)
        self.assertEqual(summary["avg_turnaround_time"], 7.0)
        self.assertEqual(summary["makespan"], 9)

    def test_identify_idle_intervals_none(self):
        slices = [
            {"task_id": "T1", "start_time": 0, "end_time": 2},
            {"task_id": "T2", "start_time": 2, "end_time": 5},
        ]
        idle = identify_idle_intervals(slices)
        self.assertEqual(idle, [])

    def test_identify_idle_intervals_with_initial_and_middle_gaps(self):
        slices = [
            {"task_id": "T1", "start_time": 3, "end_time": 5},
            {"task_id": "T2", "start_time": 8, "end_time": 10},
        ]
        idle = identify_idle_intervals(slices)
        self.assertEqual(len(idle), 2)
        self.assertEqual(idle[0]["task_id"], "Idle")
        self.assertEqual(idle[0]["start_time"], 0)
        self.assertEqual(idle[0]["end_time"], 3)
        self.assertEqual(idle[1]["task_id"], "Idle")
        self.assertEqual(idle[1]["start_time"], 5)
        self.assertEqual(idle[1]["end_time"], 8)


if __name__ == "__main__":
    unittest.main()
