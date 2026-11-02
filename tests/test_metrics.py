import unittest

from metrics import (
    calculate_metrics_summary,
    identify_idle_intervals,
    run_algorithm_comparison,
)
from task_manager import generate_sample_tasks


class TestMetricsModule(unittest.TestCase):
    def test_calculate_metrics_summary(self):
        task_metrics = {
            "T1": {
                "waiting_time": 4,
                "turnaround_time": 9,
                "burst_time": 5,
                "completion_time": 9,
            },
            "T2": {
                "waiting_time": 2,
                "turnaround_time": 5,
                "burst_time": 3,
                "completion_time": 6,
            },
        }
        summary = calculate_metrics_summary(task_metrics)
        self.assertEqual(summary["total_tasks"], 2)
        self.assertEqual(summary["avg_waiting_time"], 3.0)
        self.assertEqual(summary["avg_turnaround_time"], 7.0)
        self.assertEqual(summary["makespan"], 9)
        self.assertEqual(summary["cpu_utilization"], 88.89)

    def test_identify_idle_intervals(self):
        slices = [
            {"task_id": "T1", "start_time": 3, "end_time": 5},
            {"task_id": "T2", "start_time": 8, "end_time": 10},
        ]
        idle = identify_idle_intervals(slices)
        self.assertEqual(len(idle), 2)
        self.assertEqual(idle[0]["start_time"], 0)
        self.assertEqual(idle[0]["end_time"], 3)
        self.assertEqual(idle[1]["start_time"], 5)
        self.assertEqual(idle[1]["end_time"], 8)

    def test_run_algorithm_comparison(self):
        tasks = generate_sample_tasks()
        comp = run_algorithm_comparison(tasks, time_quantum=2)
        self.assertIn("Round Robin (RR)", comp["algorithms"])
        self.assertIn("First Come, First Served (FCFS)", comp["algorithms"])
        self.assertIn("Shortest Job First (SJF)", comp["algorithms"])
        self.assertEqual(len(comp["comparison_rows"]), 3)


if __name__ == "__main__":
    unittest.main()
