import {
  Task,
  ScheduleSlice,
  TaskMetric,
  MetricsSummary,
  ComparisonResult,
  ComparisonRow,
  BestPerformers,
} from '../types';
import { roundRobinSchedule } from './schedulers/roundRobin';
import { fcfsSchedule } from './schedulers/fcfs';
import { sjfSchedule } from './schedulers/sjf';
import { validateTasks } from './taskManager';

export function calculateMetricsSummary(
  taskMetrics: Record<string, TaskMetric>,
  _scheduleSlices?: ScheduleSlice[]
): MetricsSummary {
  const metricValues = Object.values(taskMetrics);
  if (!metricValues.length) {
    return {
      total_tasks: 0,
      avg_waiting_time: 0.0,
      avg_turnaround_time: 0.0,
      makespan: 0,
      cpu_utilization: 0.0,
    };
  }

  const totalTasks = metricValues.length;
  const totalWaiting = metricValues.reduce((acc, m) => acc + m.waiting_time, 0);
  const totalTurnaround = metricValues.reduce((acc, m) => acc + m.turnaround_time, 0);
  const makespan = Math.max(...metricValues.map((m) => m.completion_time));
  const totalBusyTime = metricValues.reduce((acc, m) => acc + m.burst_time, 0);
  const cpuUtilization =
    makespan > 0 ? Number(((totalBusyTime / makespan) * 100).toFixed(2)) : 0.0;

  return {
    total_tasks: totalTasks,
    avg_waiting_time: Number((totalWaiting / totalTasks).toFixed(2)),
    avg_turnaround_time: Number((totalTurnaround / totalTasks).toFixed(2)),
    makespan: makespan,
    cpu_utilization: cpuUtilization,
  };
}

export function identifyIdleIntervals(scheduleSlices: ScheduleSlice[]): ScheduleSlice[] {
  const idleSlices: ScheduleSlice[] = [];
  if (!scheduleSlices || scheduleSlices.length === 0) {
    return idleSlices;
  }

  const firstStart = scheduleSlices[0].start_time;
  if (firstStart > 0) {
    idleSlices.push({
      task_id: 'Idle',
      start_time: 0,
      end_time: firstStart,
      duration: firstStart,
      remaining_time: 0,
      completed: true,
      is_idle: true,
    });
  }

  let prevEnd = scheduleSlices[0].end_time;
  for (let i = 1; i < scheduleSlices.length; i++) {
    const s = scheduleSlices[i];
    if (s.start_time > prevEnd) {
      idleSlices.push({
        task_id: 'Idle',
        start_time: prevEnd,
        end_time: s.start_time,
        duration: s.start_time - prevEnd,
        remaining_time: 0,
        completed: true,
        is_idle: true,
      });
    }
    if (s.end_time > prevEnd) {
      prevEnd = s.end_time;
    }
  }

  return idleSlices;
}

export function runAlgorithmComparison(
  tasks: Task[],
  timeQuantum: number = 2
): ComparisonResult {
  validateTasks(tasks);

  // Deep clone tasks for each run
  const cloneA = tasks.map((t) => ({ ...t }));
  const cloneB = tasks.map((t) => ({ ...t }));
  const cloneC = tasks.map((t) => ({ ...t }));

  const rrRes = roundRobinSchedule(cloneA, timeQuantum);
  const rrSummary = calculateMetricsSummary(rrRes.metrics, rrRes.slices);

  const fcfsRes = fcfsSchedule(cloneB);
  const fcfsSummary = calculateMetricsSummary(fcfsRes.metrics, fcfsRes.slices);

  const sjfRes = sjfSchedule(cloneC);
  const sjfSummary = calculateMetricsSummary(sjfRes.metrics, sjfRes.slices);

  const algorithmsData = {
    'Round Robin (RR)': {
      slices: rrRes.slices,
      metrics: rrRes.metrics,
      summary: rrSummary,
    },
    'First Come, First Served (FCFS)': {
      slices: fcfsRes.slices,
      metrics: fcfsRes.metrics,
      summary: fcfsSummary,
    },
    'Shortest Job First (SJF)': {
      slices: sjfRes.slices,
      metrics: sjfRes.metrics,
      summary: sjfSummary,
    },
  };

  const comparisonRows: ComparisonRow[] = [
    {
      Algorithm: 'Round Robin (RR)',
      'Avg Waiting Time': algorithmsData['Round Robin (RR)'].summary.avg_waiting_time,
      'Avg Turnaround Time': algorithmsData['Round Robin (RR)'].summary.avg_turnaround_time,
      Makespan: algorithmsData['Round Robin (RR)'].summary.makespan,
      'CPU Utilization (%)': algorithmsData['Round Robin (RR)'].summary.cpu_utilization,
    },
    {
      Algorithm: 'First Come, First Served (FCFS)',
      'Avg Waiting Time': algorithmsData['First Come, First Served (FCFS)'].summary.avg_waiting_time,
      'Avg Turnaround Time': algorithmsData['First Come, First Served (FCFS)'].summary.avg_turnaround_time,
      Makespan: algorithmsData['First Come, First Served (FCFS)'].summary.makespan,
      'CPU Utilization (%)': algorithmsData['First Come, First Served (FCFS)'].summary.cpu_utilization,
    },
    {
      Algorithm: 'Shortest Job First (SJF)',
      'Avg Waiting Time': algorithmsData['Shortest Job First (SJF)'].summary.avg_waiting_time,
      'Avg Turnaround Time': algorithmsData['Shortest Job First (SJF)'].summary.avg_turnaround_time,
      Makespan: algorithmsData['Shortest Job First (SJF)'].summary.makespan,
      'CPU Utilization (%)': algorithmsData['Shortest Job First (SJF)'].summary.cpu_utilization,
    },
  ];

  const bestPerformers: BestPerformers = {
    lowest_waiting: [],
    lowest_turnaround: [],
    shortest_makespan: [],
    highest_utilization: [],
  };

  if (comparisonRows.length > 0 && tasks.length > 0) {
    const minWait = Math.min(...comparisonRows.map((r) => r['Avg Waiting Time']));
    bestPerformers.lowest_waiting = comparisonRows
      .filter((r) => r['Avg Waiting Time'] === minWait)
      .map((r) => r.Algorithm);

    const minTat = Math.min(...comparisonRows.map((r) => r['Avg Turnaround Time']));
    bestPerformers.lowest_turnaround = comparisonRows
      .filter((r) => r['Avg Turnaround Time'] === minTat)
      .map((r) => r.Algorithm);

    const minMakespan = Math.min(...comparisonRows.map((r) => r.Makespan));
    bestPerformers.shortest_makespan = comparisonRows
      .filter((r) => r.Makespan === minMakespan)
      .map((r) => r.Algorithm);

    const maxUtil = Math.max(...comparisonRows.map((r) => r['CPU Utilization (%)']));
    bestPerformers.highest_utilization = comparisonRows
      .filter((r) => r['CPU Utilization (%)'] === maxUtil)
      .map((r) => r.Algorithm);
  }

  return {
    algorithms: algorithmsData,
    comparison_rows: comparisonRows,
    best_performers: bestPerformers,
  };
}
