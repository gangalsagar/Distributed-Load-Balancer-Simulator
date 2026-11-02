<<<<<<< HEAD
=======
import copy
>>>>>>> 4ab66d6ce60f640de08a69a5ff3c9989b6d222f1
import unittest

from metrics import (
    calculate_metrics_summary,
    identify_idle_intervals,
    run_algorithm_comparison,
)
from task_manager import generate_sample_tasks


class TestMetricsModule(unittest.TestCase):
<<<<<<< HEAD
    def test_calculate_metrics_summary(self):
=======
    def test_calculate_metrics_summary_empty(self):
        summary = calculate_metrics_summary({})
        self.assertEqual(summary["total_tasks"], 0)
        self.assertEqual(summary["avg_waiting_time"], 0.0)
        self.assertEqual(summary["avg_turnaround_time"], 0.0)
        self.assertEqual(summary["makespan"], 0)
        self.assertEqual(summary["cpu_utilization"], 0.0)

    def test_calculate_metrics_summary_normal(self):
>>>>>>> 4ab66d6ce60f640de08a69a5ff3c9989b6d222f1
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

<<<<<<< HEAD
    def test_identify_idle_intervals(self):
=======
    def test_identify_idle_intervals_none(self):
        slices = [
            {"task_id": "T1", "start_time": 0, "end_time": 2},
            {"task_id": "T2", "start_time": 2, "end_time": 5},
        ]
        idle = identify_idle_intervals(slices)
        self.assertEqual(idle, [])

    def test_identify_idle_intervals_with_initial_and_middle_gaps(self):
>>>>>>> 4ab66d6ce60f640de08a69a5ff3c9989b6d222f1
        slices = [
            {"task_id": "T1", "start_time": 3, "end_time": 5},
            {"task_id": "T2", "start_time": 8, "end_time": 10},
        ]
        idle = identify_idle_intervals(slices)
        self.assertEqual(len(idle), 2)
<<<<<<< HEAD
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
=======
        self.assertEqual(idle[0]["task_id"], "Idle")
        self.assertEqual(idle[0]["start_time"], 0)
        self.assertEqual(idle[0]["end_time"], 3)
        self.assertEqual(idle[1]["task_id"], "Idle")
        self.assertEqual(idle[1]["start_time"], 5)
        self.assertEqual(idle[1]["end_time"], 8)


class TestAlgorithmComparison(unittest.TestCase):
    def test_comparison_identical_workload_immutability(self):
        tasks = generate_sample_tasks()
        snapshot = copy.deepcopy(tasks)
        comp = run_algorithm_comparison(tasks, time_quantum=2)
        self.assertEqual(tasks, snapshot)
        algos = comp["algorithms"]
        self.assertIn("Round Robin (RR)", algos)
        self.assertIn("First Come, First Served (FCFS)", algos)
        self.assertIn("Shortest Job First (SJF)", algos)
        rows = comp["comparison_rows"]
        self.assertEqual(len(rows), 3)
        sjf_row = next(
            (r for r in rows if r["Algorithm"] == "Shortest Job First (SJF)")
        )
        self.assertEqual(sjf_row["Avg Waiting Time"], 4.0)
        self.assertEqual(sjf_row["Avg Turnaround Time"], 8.5)
        self.assertEqual(sjf_row["Makespan"], 18)
        self.assertEqual(
            comp["best_performers"]["lowest_waiting"], ["Shortest Job First (SJF)"]
        )
        self.assertEqual(
            comp["best_performers"]["lowest_turnaround"], ["Shortest Job First (SJF)"]
        )
        self.assertEqual(len(comp["best_performers"]["shortest_makespan"]), 3)

    def test_comparison_handles_ties_fairly(self):
        tasks = [
            {"task_id": "T1", "arrival_time": 0, "burst_time": 2},
            {"task_id": "T2", "arrival_time": 0, "burst_time": 2},
        ]
        comp = run_algorithm_comparison(tasks, time_quantum=2)
        best_wait = comp["best_performers"]["lowest_waiting"]
        self.assertEqual(len(best_wait), 3)

    def test_comparison_empty_workload(self):
        comp = run_algorithm_comparison([])
        self.assertEqual(len(comp["comparison_rows"]), 3)
        for r in comp["comparison_rows"]:
            self.assertEqual(r["Makespan"], 0)
            self.assertEqual(r["Avg Waiting Time"], 0.0)
>>>>>>> 4ab66d6ce60f640de08a69a5ff3c9989b6d222f1


if __name__ == "__main__":
    unittest.main()
