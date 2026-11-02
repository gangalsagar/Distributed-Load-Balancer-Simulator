import React, { useState } from 'react';
import { Task } from '../types';
import { generateSampleTasks } from '../lib/taskManager';
import { roundRobinSchedule } from '../lib/schedulers/roundRobin';
import { fcfsSchedule } from '../lib/schedulers/fcfs';
import { sjfSchedule } from '../lib/schedulers/sjf';
import { calculateMetricsSummary } from '../lib/metrics';
import { GanttChart } from './GanttChart';
import {
  ArrowRight,
  Play,
  Server,
  BarChart3,
  Check,
} from 'lucide-react';

interface LandingPageProps {
  onLaunchDashboard: (initialMode?: 'Individual' | 'Comparison' | 'Cluster', preset?: Task[]) => void;
}

export const LandingPage: React.FC<LandingPageProps> = ({ onLaunchDashboard }) => {
  const [interactiveAlgo, setInteractiveAlgo] = useState<'RR' | 'FCFS' | 'SJF'>('RR');
  const sampleTasks = generateSampleTasks();

  // Run preview algorithm calculation
  const previewResult = React.useMemo(() => {
    if (interactiveAlgo === 'RR') {
      const res = roundRobinSchedule(sampleTasks, 2);
      return { slices: res.slices, summary: calculateMetricsSummary(res.metrics, res.slices) };
    }
    if (interactiveAlgo === 'FCFS') {
      const res = fcfsSchedule(sampleTasks);
      return { slices: res.slices, summary: calculateMetricsSummary(res.metrics, res.slices) };
    }
    const res = sjfSchedule(sampleTasks);
    return { slices: res.slices, summary: calculateMetricsSummary(res.metrics, res.slices) };
  }, [interactiveAlgo]);

  const handleLaunchWithPreset = (presetName: string) => {
    let preset: Task[];
    switch (presetName) {
      case 'staggered':
        preset = [
          { task_id: 'T1', arrival_time: 0, burst_time: 4 },
          { task_id: 'T2', arrival_time: 3, burst_time: 2 },
          { task_id: 'T3', arrival_time: 7, burst_time: 5 },
          { task_id: 'T4', arrival_time: 14, burst_time: 3 },
        ];
        break;
      case 'high_variance':
        preset = [
          { task_id: 'T1', arrival_time: 0, burst_time: 12 },
          { task_id: 'T2', arrival_time: 1, burst_time: 1 },
          { task_id: 'T3', arrival_time: 2, burst_time: 14 },
          { task_id: 'T4', arrival_time: 3, burst_time: 2 },
        ];
        break;
      case 'idle_gaps':
        preset = [
          { task_id: 'T1', arrival_time: 3, burst_time: 3 },
          { task_id: 'T2', arrival_time: 9, burst_time: 4 },
          { task_id: 'T3', arrival_time: 17, burst_time: 2 },
        ];
        break;
      case 'sample':
      default:
        preset = generateSampleTasks();
        break;
    }
    onLaunchDashboard('Individual', preset);
  };

  return (
    <div className="min-h-screen bg-white text-neutral-900 font-sans flex flex-col">
      {/* Hero Section */}

      {/* 2. Hero Section */}
      <section id="overview" className="max-w-7xl mx-auto px-6 pt-12 md:pt-16 pb-14 w-full">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-center">
          <div className="lg:col-span-7 space-y-6">
            <div className="text-xs font-semibold uppercase tracking-wider text-blue-700 flex items-center gap-2">
              <span className="w-1.5 h-1.5 bg-blue-600 rounded-full" />
              <span>Operating Systems Task Scheduling & Cluster Load Balancing</span>
            </div>

            <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight text-neutral-900 leading-[1.15]" style={{ textWrap: 'balance' }}>
              Distributed CPU Scheduling
            </h1>

            <p className="text-sm md:text-base text-neutral-600 leading-relaxed max-w-2xl">
              An interactive simulation platform for exploring preemptive Round Robin, deterministic First-Come First-Served, and Shortest Job First scheduling alongside multi-node cluster load balancing.
            </p>

            <div className="flex flex-wrap items-center gap-3 pt-2">
              <button
                type="button"
                onClick={() => onLaunchDashboard('Individual')}
                className="flex items-center gap-2 px-5 py-2.5 text-xs font-bold text-white bg-blue-600 hover:bg-blue-700 rounded transition-colors cursor-pointer shadow-sm"
              >
                <Play className="w-3.5 h-3.5 fill-white" />
                <span>Launch Simulator Dashboard</span>
              </button>

              <button
                type="button"
                onClick={() => onLaunchDashboard('Comparison')}
                className="flex items-center gap-2 px-5 py-2.5 text-xs font-bold text-neutral-900 bg-white hover:bg-neutral-50 border border-neutral-900 rounded transition-colors cursor-pointer"
              >
                <BarChart3 className="w-3.5 h-3.5 text-neutral-700" />
                <span>Compare RR vs FCFS vs SJF</span>
              </button>

              <button
                type="button"
                onClick={() => onLaunchDashboard('Cluster')}
                className="flex items-center gap-2 px-5 py-2.5 text-xs font-bold text-neutral-900 bg-neutral-100 hover:bg-neutral-200 border border-neutral-300 rounded transition-colors cursor-pointer"
              >
                <Server className="w-3.5 h-3.5 text-neutral-700" />
                <span>Cluster Balancer (Stage 3)</span>
              </button>
            </div>

            {/* Quiet metadata stats (blank) */}
            <div className="pt-6"></div>
          </div>

          <div className="lg:col-span-5" aria-hidden="true">
          </div>
          </div>
        </div>
      </section>

      {/* 3. Interactive Live Mini-Preview Section */}
      <section id="interactive-preview" className="bg-neutral-50 border-y border-neutral-200 py-12">
        <div className="max-w-7xl mx-auto px-6 space-y-6">
          <div className="flex flex-wrap items-end justify-between gap-4">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-blue-700">Live Scheduling Engine</span>
              <h2 className="text-xl md:text-2xl font-bold text-neutral-900 mt-1">
                Interactive Timeline Preview
              </h2>
              <p className="text-xs text-neutral-600 mt-0.5">
                Switch algorithms below to observe instant timeline and waiting time variations on the standard 4-task workload.
              </p>
            </div>

            {/* Segmented controls for algorithm switcher */}
            <div className="flex items-center gap-1 bg-white p-1 border border-neutral-300 rounded text-xs">
              <button
                type="button"
                onClick={() => setInteractiveAlgo('RR')}
                className={`px-3 py-1.5 font-semibold rounded cursor-pointer transition-colors ${
                  interactiveAlgo === 'RR'
                    ? 'bg-blue-600 text-white'
                    : 'text-neutral-700 hover:text-neutral-900'
                }`}
              >
                Round Robin (q = 2)
              </button>
              <button
                type="button"
                onClick={() => setInteractiveAlgo('FCFS')}
                className={`px-3 py-1.5 font-semibold rounded cursor-pointer transition-colors ${
                  interactiveAlgo === 'FCFS'
                    ? 'bg-blue-600 text-white'
                    : 'text-neutral-700 hover:text-neutral-900'
                }`}
              >
                FCFS
              </button>
              <button
                type="button"
                onClick={() => setInteractiveAlgo('SJF')}
                className={`px-3 py-1.5 font-semibold rounded cursor-pointer transition-colors ${
                  interactiveAlgo === 'SJF'
                    ? 'bg-blue-600 text-white'
                    : 'text-neutral-700 hover:text-neutral-900'
                }`}
              >
                SJF (Non-Preemptive)
              </button>
            </div>
          </div>

          {/* Interactive Gantt */}
          <div className="bg-white border border-neutral-900 rounded p-4">
            <div className="flex flex-wrap items-center justify-between gap-4 mb-3 pb-2 border-b border-neutral-100">
              <div className="flex items-center gap-4 text-xs font-mono">
                <span>Makespan: <strong>{previewResult.summary.makespan}</strong> units</span>
                <span>Avg Waiting: <strong>{previewResult.summary.avg_waiting_time}</strong> units</span>
                <span>Avg Turnaround: <strong>{previewResult.summary.avg_turnaround_time}</strong> units</span>
                <span>CPU Util: <strong>{previewResult.summary.cpu_utilization}%</strong></span>
              </div>
              <button
                type="button"
                onClick={() => onLaunchDashboard('Individual')}
                className="text-xs font-bold text-blue-600 hover:text-blue-800 flex items-center gap-1 cursor-pointer"
              >
                <span>Edit Tasks in Full Workspace</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>

            <GanttChart
              slices={previewResult.slices}
              makespan={previewResult.summary.makespan}
              height={110}
            />
          </div>
        </div>
      </section>

      {/* 4. Core Algorithms Section */}
      <section id="algorithms" className="max-w-7xl mx-auto px-6 py-14 w-full space-y-8">
        <div>
          <span className="text-xs font-bold uppercase tracking-wider text-blue-700">Supported Schedulers</span>
          <h2 className="text-2xl font-bold text-neutral-900 mt-1">
            Scheduling Algorithms & Dispatch Heuristics
          </h2>
          <p className="text-xs text-neutral-600 mt-0.5">
            Deterministic implementations covering preemptive time-slicing and non-preemptive queue models.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Algorithm 1: Round Robin */}
          <div className="border border-neutral-900 rounded p-5 bg-white flex flex-col justify-between hover:border-blue-600 transition-colors">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono font-bold text-blue-600">01. PREEMPTIVE</span>
                <span className="text-[11px] font-semibold text-neutral-500">Quantum Sliced</span>
              </div>
              <h3 className="text-base font-bold text-neutral-900">
                Round Robin (RR)
              </h3>
              <p className="text-xs text-neutral-600 leading-relaxed">
                Allocates CPU time in discrete units ($q$). Tasks that do not complete within their time slice are preempted and re-inserted into the ready queue, ensuring fair CPU time sharing and starvation prevention.
              </p>
              <div className="pt-2 border-t border-neutral-100 text-[11px] text-neutral-500 space-y-1">
                <div>&bull; Configurable Time Quantum: $1 \le q \le 100$</div>
                <div>&bull; FIFO Ready Queue &amp; preemption logging</div>
              </div>
            </div>

            <button
              type="button"
              onClick={() => {
                onLaunchDashboard('Individual');
              }}
              className="mt-5 w-full py-2 px-3 text-xs font-semibold bg-white hover:bg-neutral-50 text-neutral-900 border border-neutral-900 rounded transition-colors cursor-pointer flex items-center justify-center gap-1.5"
            >
              <span>Simulate Round Robin</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          {/* Algorithm 2: FCFS */}
          <div className="border border-neutral-900 rounded p-5 bg-white flex flex-col justify-between hover:border-blue-600 transition-colors">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono font-bold text-blue-600">02. NON-PREEMPTIVE</span>
                <span className="text-[11px] font-semibold text-neutral-500">FIFO Queue</span>
              </div>
              <h3 className="text-base font-bold text-neutral-900">
                First-Come, First-Served (FCFS)
              </h3>
              <p className="text-xs text-neutral-600 leading-relaxed">
                Dispatches tasks in strict order of arrival time. Non-preemptive execution ensures each job runs to completion once allocated the CPU. Ties in arrival time are resolved deterministically by Task ID.
              </p>
              <div className="pt-2 border-t border-neutral-100 text-[11px] text-neutral-500 space-y-1">
                <div>&bull; Zero preemption overhead</div>
                <div>&bull; Convoy effect vulnerable with long burst jobs</div>
              </div>
            </div>

            <button
              type="button"
              onClick={() => {
                onLaunchDashboard('Individual');
              }}
              className="mt-5 w-full py-2 px-3 text-xs font-semibold bg-white hover:bg-neutral-50 text-neutral-900 border border-neutral-900 rounded transition-colors cursor-pointer flex items-center justify-center gap-1.5"
            >
              <span>Simulate FCFS</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          {/* Algorithm 3: SJF */}
          <div className="border border-neutral-900 rounded p-5 bg-white flex flex-col justify-between hover:border-blue-600 transition-colors">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono font-bold text-blue-600">03. OPTIMIZED</span>
                <span className="text-[11px] font-semibold text-neutral-500">Min Waiting Time</span>
              </div>
              <h3 className="text-base font-bold text-neutral-900">
                Shortest Job First (SJF)
              </h3>
              <p className="text-xs text-neutral-600 leading-relaxed">
                Selects the available arrived task with the shortest CPU burst time at each scheduling decision. Provides mathematically optimal minimum average waiting time among non-preemptive algorithms.
              </p>
              <div className="pt-2 border-t border-neutral-100 text-[11px] text-neutral-500 space-y-1">
                <div>&bull; Minimizes average waiting time</div>
                <div>&bull; Deterministic burst and arrival tie-breaker</div>
              </div>
            </div>

            <button
              type="button"
              onClick={() => {
                onLaunchDashboard('Individual');
              }}
              className="mt-5 w-full py-2 px-3 text-xs font-semibold bg-white hover:bg-neutral-50 text-neutral-900 border border-neutral-900 rounded transition-colors cursor-pointer flex items-center justify-center gap-1.5"
            >
              <span>Simulate SJF</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </section>

      {/* 5. Workload Presets Showcase (blank) */}
      <section id="presets" className="py-14"></section>

      {/* 6. Performance Metrics Section */}
      <section id="metrics" className="max-w-7xl mx-auto px-6 py-14 w-full space-y-8">
        <div>
          <span className="text-xs font-bold uppercase tracking-wider text-blue-700">Evaluation Metrics</span>
          <h2 className="text-2xl font-bold text-neutral-900 mt-1">
            Mathematical Metric Formulations
          </h2>
          <p className="text-xs text-neutral-600 mt-0.5">
            Key Performance Indicators aggregated across single-node executions and distributed clusters.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="border border-neutral-900 rounded p-4 bg-white">
            <div className="text-xs font-semibold text-neutral-500 uppercase tracking-wider">Turnaround Time (TAT)</div>
            <div className="text-lg font-mono font-bold text-neutral-900 mt-2">T_comp - T_arr</div>
            <p className="text-xs text-neutral-600 mt-2 leading-relaxed">
              Total elapsed time from task submission into the system until full execution completion.
            </p>
          </div>

          <div className="border border-neutral-900 rounded p-4 bg-white">
            <div className="text-xs font-semibold text-neutral-500 uppercase tracking-wider">Waiting Time (WT)</div>
            <div className="text-lg font-mono font-bold text-neutral-900 mt-2">T_tat - T_burst</div>
            <p className="text-xs text-neutral-600 mt-2 leading-relaxed">
              Total duration spent sitting in the ready queue waiting for CPU access.
            </p>
          </div>

          <div className="border border-neutral-900 rounded p-4 bg-white">
            <div className="text-xs font-semibold text-neutral-500 uppercase tracking-wider">Makespan</div>
            <div className="text-lg font-mono font-bold text-neutral-900 mt-2">max(T_completion)</div>
            <p className="text-xs text-neutral-600 mt-2 leading-relaxed">
              The total duration required to complete all configured tasks in the batch or cluster.
            </p>
          </div>

          <div className="border border-neutral-900 rounded p-4 bg-white">
            <div className="text-xs font-semibold text-neutral-500 uppercase tracking-wider">CPU Utilization</div>
            <div className="text-lg font-mono font-bold text-neutral-900 mt-2">(Total Burst / Makespan) &times; 100%</div>
            <p className="text-xs text-neutral-600 mt-2 leading-relaxed">
              Percentage of total execution duration during which the CPU was actively processing.
            </p>
          </div>
        </div>
      </section>

      {/* 7. Conversion CTA Banner */}
      <section className="bg-blue-600 text-white py-12 px-6">
        <div className="max-w-4xl mx-auto text-center space-y-4">
          <h2 className="text-2xl md:text-3xl font-bold tracking-tight">
            Ready to Simulate and Benchmark?
          </h2>
          <p className="text-xs md:text-sm text-blue-100 max-w-xl mx-auto">
            Open the interactive dashboard to customize workloads, tweak Round Robin quanta, inspect chronological slice traces, or run multi-node cluster simulations.
          </p>
          <div className="pt-2 flex justify-center gap-3">
            <button
              type="button"
              onClick={() => onLaunchDashboard('Individual')}
              className="px-6 py-3 bg-white text-blue-900 hover:bg-neutral-100 rounded text-xs font-bold transition-colors cursor-pointer shadow-md flex items-center gap-2"
            >
              <span>Open Simulator Dashboard</span>
              <ArrowRight className="w-4 h-4 text-blue-900" />
            </button>
          </div>
        </div>
      </section>

      {/* 8. Quiet Footer */}
      <footer className="bg-white border-t border-neutral-200 py-8 px-6 text-xs text-neutral-500">
        <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-4">
          <div>
            <div className="font-bold text-neutral-800">Distributed Load Balancer Simulator</div>
            <div className="text-[11px] mt-0.5">Operating Systems CPU Scheduling & Multi-Node Cluster Balancer</div>
          </div>
          <div className="flex items-center gap-6">
            <button
              type="button"
              onClick={() => onLaunchDashboard('Individual')}
              className="hover:text-neutral-900 transition-colors cursor-pointer"
            >
              Dashboard
            </button>
            <button
              type="button"
              onClick={() => onLaunchDashboard('Comparison')}
              className="hover:text-neutral-900 transition-colors cursor-pointer"
            >
              Comparison View
            </button>
            <button
              type="button"
              onClick={() => onLaunchDashboard('Cluster')}
              style={{ visibility: 'hidden', pointerEvents: 'none' }}
              tabIndex={-1}
              aria-hidden="true"
              className="cursor-default"
            >
              Cluster Balancer
            </button>
          </div>
        </div>
      </footer>
    </div>
  );
};
