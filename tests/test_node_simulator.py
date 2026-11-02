import unittest
from node_simulator import simulate_cluster
from task_manager import generate_sample_tasks


class TestNodeSimulator(unittest.TestCase):
    def test_simulate_cluster_least_loaded(self):
        tasks = generate_sample_tasks()
        result = simulate_cluster(tasks, node_count=3, policy="Least Loaded")
        self.assertEqual(len(result["nodes"]), 3)
        self.assertEqual(result["total_tasks"], 4)
        self.assertGreater(result["cluster_makespan"], 0)
        self.assertLessEqual(result["cluster_makespan"], 18)

    def test_simulate_cluster_round_robin(self):
        tasks = generate_sample_tasks()
        result = simulate_cluster(tasks, node_count=2, policy="Round Robin")
        self.assertEqual(len(result["nodes"]), 2)
        self.assertEqual(result["total_tasks"], 4)


if __name__ == "__main__":
    unittest.main()
