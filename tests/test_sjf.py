<<<<<<< HEAD
=======
import copy
>>>>>>> 4ab66d6ce60f640de08a69a5ff3c9989b6d222f1
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
<<<<<<< HEAD
        self.assertEqual(metrics["T4"]["completion_time"], 7)
        self.assertEqual(metrics["T2"]["completion_time"], 10)
        self.assertEqual(metrics["T3"]["completion_time"], 18)
=======
        self.assertEqual(metrics["T1"]["turnaround_time"], 5)
        self.assertEqual(metrics["T1"]["waiting_time"], 0)
        self.assertEqual(metrics["T4"]["completion_time"], 7)
        self.assertEqual(metrics["T4"]["turnaround_time"], 4)
        self.assertEqual(metrics["T4"]["waiting_time"], 2)
        self.assertEqual(metrics["T2"]["completion_time"], 10)
        self.assertEqual(metrics["T2"]["turnaround_time"], 9)
        self.assertEqual(metrics["T2"]["waiting_time"], 6)
        self.assertEqual(metrics["T3"]["completion_time"], 18)
        self.assertEqual(metrics["T3"]["turnaround_time"], 16)
        self.assertEqual(metrics["T3"]["waiting_time"], 8)
>>>>>>> 4ab66d6ce60f640de08a69a5ff3c9989b6d222f1

    def test_shortest_available_selected_first(self):
        tasks = [
            {"task_id": "T_LONG", "arrival_time": 0, "burst_time": 10},
            {"task_id": "T_SHORT", "arrival_time": 0, "burst_time": 2},
            {"task_id": "T_MED", "arrival_time": 0, "burst_time": 6},
        ]
        slices, metrics = sjf_schedule(tasks)
        self.assertEqual([s["task_id"] for s in slices], ["T_SHORT", "T_MED", "T_LONG"])

<<<<<<< HEAD
    def test_equal_burst_times_deterministic_tie_breaker(self):
=======
    def test_unarrived_tasks_never_selected_early(self):
        tasks = [
            {"task_id": "T1", "arrival_time": 0, "burst_time": 5},
            {"task_id": "T_FAST", "arrival_time": 10, "burst_time": 1},
        ]
        slices, metrics = sjf_schedule(tasks)
        self.assertEqual(slices[0]["task_id"], "T1")
        self.assertEqual(slices[0]["start_time"], 0)
        self.assertEqual(slices[0]["end_time"], 5)
        self.assertEqual(slices[1]["task_id"], "T_FAST")
        self.assertEqual(slices[1]["start_time"], 10)
        self.assertEqual(slices[1]["end_time"], 11)

    def test_newly_arrived_shorter_task_waits_for_completion(self):
        tasks = [
            {"task_id": "T_RUNNING", "arrival_time": 0, "burst_time": 6},
            {"task_id": "T_SHORT", "arrival_time": 1, "burst_time": 1},
        ]
        slices, metrics = sjf_schedule(tasks)
        self.assertEqual(slices[0]["task_id"], "T_RUNNING")
        self.assertEqual(slices[0]["start_time"], 0)
        self.assertEqual(slices[0]["end_time"], 6)
        self.assertEqual(slices[1]["task_id"], "T_SHORT")
        self.assertEqual(slices[1]["start_time"], 6)
        self.assertEqual(slices[1]["end_time"], 7)

    def test_equal_burst_times_deterministic_tie_breaker(self):
        tasks_diff_arr = [
            {"task_id": "T_LATER", "arrival_time": 2, "burst_time": 4},
            {"task_id": "T_FIRST", "arrival_time": 0, "burst_time": 4},
        ]
        slices_a, _ = sjf_schedule(tasks_diff_arr)
        self.assertEqual([s["task_id"] for s in slices_a], ["T_FIRST", "T_LATER"])
>>>>>>> 4ab66d6ce60f640de08a69a5ff3c9989b6d222f1
        tasks_same_arr = [
            {"task_id": "Task_Z", "arrival_time": 0, "burst_time": 3},
            {"task_id": "Task_A", "arrival_time": 0, "burst_time": 3},
            {"task_id": "Task_M", "arrival_time": 0, "burst_time": 3},
        ]
        slices_b, _ = sjf_schedule(tasks_same_arr)
        self.assertEqual(
            [s["task_id"] for s in slices_b], ["Task_A", "Task_M", "Task_Z"]
        )

<<<<<<< HEAD
=======
    def test_cpu_idle_periods(self):
        tasks = [
            {"task_id": "T1", "arrival_time": 3, "burst_time": 2},
            {"task_id": "T2", "arrival_time": 8, "burst_time": 3},
        ]
        slices, metrics = sjf_schedule(tasks)
        self.assertEqual(len(slices), 2)
        self.assertEqual(slices[0]["start_time"], 3)
        self.assertEqual(slices[0]["end_time"], 5)
        self.assertEqual(slices[1]["start_time"], 8)
        self.assertEqual(slices[1]["end_time"], 11)

    def test_empty_input(self):
        slices, metrics = sjf_schedule([])
        self.assertEqual(slices, [])
        self.assertEqual(metrics, {})

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            sjf_schedule("not_a_list")
        with self.assertRaises(ValueError):
            sjf_schedule([{"task_id": "T1", "arrival_time": -2, "burst_time": 5}])
        with self.assertRaises(ValueError):
            sjf_schedule([{"task_id": "T1", "arrival_time": 0, "burst_time": 0}])

    def test_input_tasks_remain_unchanged(self):
        original = [
            {"task_id": "T1", "arrival_time": 2, "burst_time": 5},
            {"task_id": "T2", "arrival_time": 0, "burst_time": 2},
        ]
        snapshot = copy.deepcopy(original)
        sjf_schedule(original)
        self.assertEqual(original, snapshot)

>>>>>>> 4ab66d6ce60f640de08a69a5ff3c9989b6d222f1

if __name__ == "__main__":
    unittest.main()
