export interface Task {
  task_id: string;
  arrival_time: number;
  burst_time: number;
  remaining_time?: number;
  status?: string;
  assigned_node?: string | null;
  _order?: number;
}

export interface ScheduleSlice {
  task_id: string;
  start_time: number;
  end_time: number;
  duration: number;
  remaining_time: number;
  completed: boolean;
  is_idle?: boolean;
}

export interface TaskMetric {
  task_id: string;
  arrival_time: number;
  burst_time: number;
  completion_time: number;
  turnaround_time: number;
  waiting_time: number;
}

export interface MetricsSummary {
  total_tasks: number;
  avg_waiting_time: number;
  avg_turnaround_time: number;
  makespan: number;
  cpu_utilization: number;
}

export interface AlgorithmRun {
  slices: ScheduleSlice[];
  metrics: Record<string, TaskMetric>;
  summary: MetricsSummary;
}

export interface ComparisonRow {
  Algorithm: string;
  'Avg Waiting Time': number;
  'Avg Turnaround Time': number;
  Makespan: number;
  'CPU Utilization (%)': number;
}

export interface BestPerformers {
  lowest_waiting: string[];
  lowest_turnaround: string[];
  shortest_makespan: string[];
  highest_utilization: string[];
}

export interface ComparisonResult {
  algorithms: {
    'Round Robin (RR)': AlgorithmRun;
    'First Come, First Served (FCFS)': AlgorithmRun;
    'Shortest Job First (SJF)': AlgorithmRun;
  };
  comparison_rows: ComparisonRow[];
  best_performers: BestPerformers;
}

export type SchedulingAlgorithm =
  | 'Round Robin (RR)'
  | 'First Come, First Served (FCFS)'
  | 'Shortest Job First (SJF — Non-Preemptive)';

export type AppMode = 'Individual Simulation' | 'Algorithm Comparison' | 'Multi-Node Cluster (Stage 3)';
