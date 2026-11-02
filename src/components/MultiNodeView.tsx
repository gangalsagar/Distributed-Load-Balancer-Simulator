import React, { useState } from 'react';
import { Task } from '../types';
import {
  simulateCluster,
  LoadBalancingPolicy,
} from '../lib/schedulers/nodeSimulator';
import { GanttChart } from './GanttChart';
import { Server, Cpu, Layers } from 'lucide-react';

interface MultiNodeViewProps {
  tasks: Task[];
  timeQuantum: number;
}

export const MultiNodeView: React.FC<MultiNodeViewProps> = ({ tasks, timeQuantum }) => {
  const [nodeCount, setNodeCount] = useState<number>(3);
  const [policy, setPolicy] = useState<LoadBalancingPolicy>('Least Loaded');
  const [localAlgorithm, setLocalAlgorithm] = useState<'FCFS' | 'RR' | 'SJF'>('FCFS');

  const clusterResult = simulateCluster(
    tasks,
    nodeCount,
    policy,
    localAlgorithm,
    timeQuantum
  );

  return (
    <div className="space-y-6">
      {/* Configuration Controls Bar */}
      <div className="bg-white border border-neutral-900 rounded p-4">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider text-neutral-800">
              Cluster Balancer Configuration
            </h3>
            <p className="text-xs text-neutral-500">
              Dispatch workload across a pool of independent worker nodes
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-4 text-xs">
            <div className="flex items-center gap-2">
              <label htmlFor="node-count-select" className="font-semibold text-neutral-700">Cluster Size:</label>
              <select
                id="node-count-select"
                aria-label="Cluster Size"
                value={nodeCount}
                onChange={(e) => setNodeCount(Number(e.target.value))}
                className="px-2 py-1 border border-neutral-300 rounded font-medium focus:border-blue-600 focus:outline-none"
              >
                <option value={2}>2 Compute Nodes</option>
                <option value={3}>3 Compute Nodes</option>
                <option value={4}>4 Compute Nodes</option>
                <option value={5}>5 Compute Nodes</option>
              </select>
            </div>

            <div className="flex items-center gap-2">
              <label htmlFor="policy-select" className="font-semibold text-neutral-700">Balancing Policy:</label>
              <select
                id="policy-select"
                aria-label="Balancing Policy"
                value={policy}
                onChange={(e) => setPolicy(e.target.value as LoadBalancingPolicy)}
                className="px-2 py-1 border border-neutral-300 rounded font-medium focus:border-blue-600 focus:outline-none"
              >
                <option value="Least Loaded">Least Loaded (Shortest Workload)</option>
                <option value="Round Robin">Round Robin Allocation</option>
                <option value="Random">Hash/Random Distribution</option>
              </select>
            </div>

            <div className="flex items-center gap-2">
              <label htmlFor="local-scheduler-select" className="font-semibold text-neutral-700">Node Scheduler:</label>
              <select
                id="local-scheduler-select"
                aria-label="Node Scheduler"
                value={localAlgorithm}
                onChange={(e) => setLocalAlgorithm(e.target.value as 'FCFS' | 'RR' | 'SJF')}
                className="px-2 py-1 border border-neutral-300 rounded font-medium focus:border-blue-600 focus:outline-none"
              >
                <option value="FCFS">FCFS (Non-preemptive)</option>
                <option value="RR">Round Robin (q = {timeQuantum})</option>
                <option value="SJF">Shortest Job First</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Cluster KPI summary */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="border border-neutral-900 rounded p-4 bg-white text-left">
          <div className="text-[11px] uppercase tracking-wider text-neutral-500 font-semibold flex items-center gap-1.5">
            <Layers className="w-3.5 h-3.5 text-blue-600" /> Total Dispatched
          </div>
          <div className="text-2xl font-bold text-neutral-900 mt-1">
            {clusterResult.totalTasks} <span className="text-sm font-normal text-neutral-500">tasks</span>
          </div>
        </div>

        <div className="border border-neutral-900 rounded p-4 bg-white text-left">
          <div className="text-[11px] uppercase tracking-wider text-neutral-500 font-semibold flex items-center gap-1.5">
            <Server className="w-3.5 h-3.5 text-blue-600" /> Cluster Makespan
          </div>
          <div className="text-2xl font-bold text-neutral-900 mt-1">
            {clusterResult.clusterMakespan} <span className="text-sm font-normal text-neutral-500">units</span>
          </div>
        </div>

        <div className="border border-neutral-900 rounded p-4 bg-white text-left">
          <div className="text-[11px] uppercase tracking-wider text-neutral-500 font-semibold flex items-center gap-1.5">
            <Cpu className="w-3.5 h-3.5 text-blue-600" /> Avg Cluster Waiting
          </div>
          <div className="text-2xl font-bold text-neutral-900 mt-1">
            {clusterResult.avgWaitingTime.toFixed(2)} <span className="text-sm font-normal text-neutral-500">units</span>
          </div>
        </div>

        <div className="border border-neutral-900 rounded p-4 bg-white text-left">
          <div className="text-[11px] uppercase tracking-wider text-neutral-500 font-semibold flex items-center gap-1.5">
            <Cpu className="w-3.5 h-3.5 text-blue-600" /> Avg Node CPU Util
          </div>
          <div className="text-2xl font-bold text-neutral-900 mt-1">
            {clusterResult.avgCpuUtilization.toFixed(1)}%
          </div>
        </div>
      </div>

      {/* Per Node Timelines */}
      <div className="space-y-4">
        <h3 className="text-sm font-semibold uppercase tracking-wider text-neutral-800 pb-1 border-b border-neutral-200">
          Node Execution Timelines & Load Distribution
        </h3>

        {clusterResult.nodes.map((node) => (
          <div key={node.nodeId} className="border border-neutral-900 rounded p-4 bg-white">
            <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
              <div className="flex items-center gap-2">
                <span className="font-bold text-sm text-neutral-900 flex items-center gap-1.5">
                  <Server className="w-4 h-4 text-blue-600" />
                  {node.nodeId}
                </span>
                <span className="text-xs text-neutral-500">
                  ({node.tasks.length} tasks assigned: {node.tasks.map((t) => t.task_id).join(', ') || 'None'})
                </span>
              </div>
              <div className="flex items-center gap-4 text-xs font-mono">
                <span>Duration: <strong>{node.summary.makespan}</strong> units</span>
                <span>CPU Util: <strong>{node.summary.cpu_utilization}%</strong></span>
                <span>Avg Wait: <strong>{node.summary.avg_waiting_time}</strong></span>
              </div>
            </div>

            {node.slices.length > 0 ? (
              <GanttChart
                slices={node.slices}
                makespan={Math.max(node.summary.makespan, clusterResult.clusterMakespan)}
                height={100}
              />
            ) : (
              <div className="border border-dashed border-neutral-300 rounded p-6 text-center text-xs text-neutral-500">
                Node idle — no tasks routed to this node.
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
