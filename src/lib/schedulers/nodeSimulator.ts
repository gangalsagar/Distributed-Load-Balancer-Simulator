import { Task, ScheduleSlice, TaskMetric } from '../../types';
import { fcfsSchedule } from './fcfs';
import { roundRobinSchedule } from './roundRobin';
import { sjfSchedule } from './sjf';
import { calculateMetricsSummary } from '../metrics';

export type LoadBalancingPolicy = 'Round Robin' | 'Least Loaded' | 'Random';

export interface NodeSimulationResult {
  nodeId: string;
  tasks: Task[];
  slices: ScheduleSlice[];
  metrics: Record<string, TaskMetric>;
  summary: ReturnType<typeof calculateMetricsSummary>;
}

export interface ClusterSimulationResult {
  nodes: NodeSimulationResult[];
  clusterMakespan: number;
  totalTasks: number;
  avgWaitingTime: number;
  avgTurnaroundTime: number;
  avgCpuUtilization: number;
}

export function simulateCluster(
  tasks: Task[],
  nodeCount: number = 3,
  policy: LoadBalancingPolicy = 'Round Robin',
  localAlgorithm: 'FCFS' | 'RR' | 'SJF' = 'FCFS',
  timeQuantum: number = 2
): ClusterSimulationResult {
  const nodeTasks: Task[][] = Array.from({ length: nodeCount }, () => []);
  const nodeWorkloads: number[] = Array.from({ length: nodeCount }, () => 0);

  // Sort tasks by arrival time to dispatch deterministically
  const sortedTasks = [...tasks].sort((a, b) => {
    if (a.arrival_time !== b.arrival_time) return a.arrival_time - b.arrival_time;
    return String(a.task_id).localeCompare(String(b.task_id));
  });

  sortedTasks.forEach((task, idx) => {
    let targetNodeIdx = 0;
    if (policy === 'Round Robin') {
      targetNodeIdx = idx % nodeCount;
    } else if (policy === 'Least Loaded') {
      // Find node with minimum accumulated workload
      let minLoad = nodeWorkloads[0];
      targetNodeIdx = 0;
      for (let n = 1; n < nodeCount; n++) {
        if (nodeWorkloads[n] < minLoad) {
          minLoad = nodeWorkloads[n];
          targetNodeIdx = n;
        }
      }
    } else {
      // Random deterministic-like based on hash of task_id
      const hash = task.task_id.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
      targetNodeIdx = hash % nodeCount;
    }

    const assignedTask: Task = {
      ...task,
      assigned_node: `Node ${targetNodeIdx + 1}`,
    };
    nodeTasks[targetNodeIdx].push(assignedTask);
    nodeWorkloads[targetNodeIdx] += task.burst_time;
  });

  const nodeResults: NodeSimulationResult[] = [];
  let allMetrics: Record<string, TaskMetric> = {};
  let clusterMakespan = 0;

  for (let i = 0; i < nodeCount; i++) {
    const nTasks = nodeTasks[i];
    let runResult: { slices: ScheduleSlice[]; metrics: Record<string, TaskMetric> };

    if (localAlgorithm === 'RR') {
      runResult = roundRobinSchedule(nTasks, timeQuantum);
    } else if (localAlgorithm === 'SJF') {
      runResult = sjfSchedule(nTasks);
    } else {
      runResult = fcfsSchedule(nTasks);
    }

    const summary = calculateMetricsSummary(runResult.metrics, runResult.slices);
    nodeResults.push({
      nodeId: `Node ${i + 1}`,
      tasks: nTasks,
      slices: runResult.slices,
      metrics: runResult.metrics,
      summary,
    });

    if (summary.makespan > clusterMakespan) {
      clusterMakespan = summary.makespan;
    }
    allMetrics = { ...allMetrics, ...runResult.metrics };
  }

  const allMetricsList = Object.values(allMetrics);
  const totalTasks = allMetricsList.length;
  const avgWait = totalTasks > 0
    ? Number((allMetricsList.reduce((acc, m) => acc + m.waiting_time, 0) / totalTasks).toFixed(2))
    : 0;
  const avgTat = totalTasks > 0
    ? Number((allMetricsList.reduce((acc, m) => acc + m.turnaround_time, 0) / totalTasks).toFixed(2))
    : 0;
  const activeNodesWithWork = nodeResults.filter((n) => n.summary.total_tasks > 0);
  const avgUtil = activeNodesWithWork.length > 0
    ? Number((activeNodesWithWork.reduce((acc, n) => acc + n.summary.cpu_utilization, 0) / activeNodesWithWork.length).toFixed(2))
    : 0;

  return {
    nodes: nodeResults,
    clusterMakespan,
    totalTasks,
    avgWaitingTime: avgWait,
    avgTurnaroundTime: avgTat,
    avgCpuUtilization: avgUtil,
  };
}
