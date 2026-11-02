import React, { useState, useMemo } from 'react';
import {
  Task,
  AppMode,
  SchedulingAlgorithm,
  ScheduleSlice,
  TaskMetric,
} from './types';
import { generateSampleTasks, validateTasks } from './lib/taskManager';
import { roundRobinSchedule } from './lib/schedulers/roundRobin';
import { fcfsSchedule } from './lib/schedulers/fcfs';
import { sjfSchedule } from './lib/schedulers/sjf';
import {
  calculateMetricsSummary,
  runAlgorithmComparison,
} from './lib/metrics';
import { Sidebar } from './components/Sidebar';
import { TaskEditor } from './components/TaskEditor';
import { GanttChart } from './components/GanttChart';
import {
  TaskComparisonChart,
  AlgorithmMetricBar,
} from './components/MetricCharts';
import { ExecutionSlicesTable } from './components/ExecutionSlicesTable';
import { MultiNodeView } from './components/MultiNodeView';
import { LandingPage } from './components/LandingPage';
import { Navbar } from './components/Navbar';
import {
  Info,
  Award,
  Play,
  AlertCircle,
  Home,
} from 'lucide-react';

export const App: React.FC = () => {
  const [currentView, setCurrentView] = useState<'landing' | 'dashboard'>('landing');
  const [tasks, setTasks] = useState<Task[]>(generateSampleTasks());
  const [appMode, setAppMode] = useState<AppMode>('Individual Simulation');
  const [algorithm, setAlgorithm] = useState<SchedulingAlgorithm>('Round Robin (RR)');
  const [timeQuantum, setTimeQuantum] = useState<number>(2);
  const [simRun, setSimRun] = useState<boolean>(true);
  const [comparisonTab, setComparisonTab] = useState<'RR' | 'FCFS' | 'SJF'>('RR');

  // Validate tasks in real-time
  const validationError = useMemo(() => {
    try {
      if (!tasks.length) {
        return 'No tasks configured. Please add at least one task.';
      }
      validateTasks(tasks);
      return '';
    } catch (err: unknown) {
      if (err instanceof Error) {
        return err.message;
      }
      return String(err);
    }
  }, [tasks]);

  // Execute single algorithm simulation
  const singleSimResult = useMemo(() => {
    if (!simRun || validationError || !tasks.length) return null;
    try {
      let slices: ScheduleSlice[] = [];
      let metrics: Record<string, TaskMetric> = {};

      if (algorithm === 'Round Robin (RR)') {
        const res = roundRobinSchedule(tasks, timeQuantum);
        slices = res.slices;
        metrics = res.metrics;
      } else if (algorithm === 'First Come, First Served (FCFS)') {
        const res = fcfsSchedule(tasks);
        slices = res.slices;
        metrics = res.metrics;
      } else {
        const res = sjfSchedule(tasks);
        slices = res.slices;
        metrics = res.metrics;
      }

      const summary = calculateMetricsSummary(metrics, slices);
      return { slices, metrics, summary };
    } catch {
      return null;
    }
  }, [simRun, validationError, tasks, algorithm, timeQuantum]);

  // Execute comparison simulation
  const comparisonResult = useMemo(() => {
    if (!simRun || validationError || !tasks.length || appMode !== 'Algorithm Comparison') {
      return null;
    }
    try {
      return runAlgorithmComparison(tasks, timeQuantum);
    } catch {
      return null;
    }
  }, [simRun, validationError, tasks, timeQuantum, appMode]);

  const handleRun = () => {
    setSimRun(true);
  };

  const handleLoadSample = () => {
    setTasks(generateSampleTasks());
    setSimRun(true);
  };

  const handleReset = () => {
    setTasks(generateSampleTasks());
    setSimRun(false);
  };

  const handleLaunchDashboard = (
    mode?: 'Individual' | 'Comparison' | 'Cluster',
    preset?: Task[]
  ) => {
    if (preset && preset.length > 0) {
      setTasks(preset);
    }
    if (mode === 'Comparison') {
      setAppMode('Algorithm Comparison');
    } else if (mode === 'Cluster') {
      setAppMode('Multi-Node Cluster (Stage 3)');
    } else if (mode === 'Individual') {
      setAppMode('Individual Simulation');
    }
    setSimRun(true);
    setCurrentView('dashboard');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const getAlgorithmExplanation = () => {
    if (appMode === 'Algorithm Comparison') {
      return (
        <div className="bg-blue-50 border border-blue-200 rounded p-3 mb-6 flex items-start gap-2.5 text-xs text-blue-900">
          <Info className="w-4 h-4 text-blue-600 shrink-0 mt-0.5" />
          <div>
            <strong>Algorithm Comparison:</strong> Executes Round Robin, FCFS, and SJF against the{' '}
            <strong>exact same workload</strong> and compares their metrics, Gantt timelines, and CPU
            utilization fairly side-by-side.
          </div>
        </div>
      );
    }
    if (appMode === 'Multi-Node Cluster (Stage 3)') {
      return (
        <div className="bg-blue-50 border border-blue-200 rounded p-3 mb-6 flex items-start gap-2.5 text-xs text-blue-900">
          <Info className="w-4 h-4 text-blue-600 shrink-0 mt-0.5" />
          <div>
            <strong>Distributed Multi-Node Cluster:</strong> Models a cluster of independent compute nodes.
            Tasks are dynamically dispatched according to load balancing policies (e.g. Least Loaded, Round Robin)
            to minimize cluster makespan and balance computing resources.
          </div>
        </div>
      );
    }
    if (algorithm === 'First Come, First Served (FCFS)') {
      return (
        <div className="bg-blue-50 border border-blue-200 rounded p-3 mb-6 flex items-start gap-2.5 text-xs text-blue-900">
          <Info className="w-4 h-4 text-blue-600 shrink-0 mt-0.5" />
          <div>
            <strong>FCFS:</strong> Executes tasks in arrival order. It is non-preemptive, so a task runs
            until completion once execution begins.
          </div>
        </div>
      );
    }
    if (algorithm === 'Shortest Job First (SJF — Non-Preemptive)') {
      return (
        <div className="bg-blue-50 border border-blue-200 rounded p-3 mb-6 flex items-start gap-2.5 text-xs text-blue-900">
          <Info className="w-4 h-4 text-blue-600 shrink-0 mt-0.5" />
          <div>
            <strong>SJF (Non-Preemptive):</strong> At each scheduling decision, selects the available arrived
            task with the smallest burst time. Once execution begins, the task runs to completion without preemption.
          </div>
        </div>
      );
    }
    return (
      <div className="bg-blue-50 border border-blue-200 rounded p-3 mb-6 flex items-start gap-2.5 text-xs text-blue-900">
        <Info className="w-4 h-4 text-blue-600 shrink-0 mt-0.5" />
        <div>
          <strong>Round Robin:</strong> Gives tasks CPU time in turns using a configurable time quantum (q = {timeQuantum}).
          Tasks that are not finished return to the ready queue.
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-white text-neutral-900 flex flex-col font-sans">
      {/* Constant Navigation Bar for Whole Website */}
      <Navbar
        currentView={currentView}
        appMode={appMode}
        onNavigateHome={() => {
          setCurrentView('landing');
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }}
        onNavigateMode={(mode) => {
          setAppMode(mode);
          setSimRun(true);
          setCurrentView('dashboard');
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }}
      />

      {currentView === 'landing' ? (
        <LandingPage onLaunchDashboard={handleLaunchDashboard} />
      ) : (
        <div className="flex-1 flex flex-col md:flex-row">
          {/* Sidebar Controls */}
          <Sidebar
            appMode={appMode}
            setAppMode={setAppMode}
            algorithm={algorithm}
            setAlgorithm={setAlgorithm}
            timeQuantum={timeQuantum}
            setTimeQuantum={setTimeQuantum}
            onRun={handleRun}
            onLoadSample={handleLoadSample}
            onReset={handleReset}
            onBackToLanding={() => setCurrentView('landing')}
          />

          {/* Main Content Area */}
          <main className="flex-1 p-6 md:p-8 max-w-7xl overflow-y-auto">
        {/* Header */}
        <header className="border-b border-neutral-900 pb-3 mb-6">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <div>
              <h1 className="text-2xl font-bold text-neutral-900 tracking-tight">
                Distributed Load Balancer Simulator
              </h1>
              <p className="text-xs text-neutral-600 mt-1">
                {appMode === 'Multi-Node Cluster (Stage 3)'
                  ? 'Multi-node cluster simulation and load balancing policies'
                  : 'Single-node CPU scheduling and performance analysis'}
              </p>
            </div>
            <div className="flex items-center gap-3">
              <button
                type="button"
                onClick={() => setCurrentView('landing')}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-white hover:bg-neutral-100 text-neutral-800 border border-neutral-300 rounded text-xs font-semibold cursor-pointer transition-colors"
              >
                <Home className="w-3.5 h-3.5 text-blue-600" />
                <span>Landing Page</span>
              </button>
              <span className="inline-flex items-center gap-1.5 px-2.5 py-1 bg-neutral-100 border border-neutral-300 rounded text-xs font-medium text-neutral-700">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                Simulation Workspace
              </span>
            </div>
          </div>
        </header>

        {/* Algorithm Explanation Banner */}
        {getAlgorithmExplanation()}

        {/* Workload Configuration Table */}
        <TaskEditor
          tasks={tasks}
          onChange={(newTasks) => {
            setTasks(newTasks);
            if (!simRun) setSimRun(true);
          }}
          validationError={validationError}
        />

        {/* State: Not Run or Valid Error */}
        {!simRun ? (
          <div className="border border-dashed border-neutral-400 rounded p-8 text-center bg-neutral-50 my-6">
            <Play className="w-8 h-8 text-neutral-400 mx-auto mb-2" />
            <h3 className="font-semibold text-sm text-neutral-900">Ready to Simulate</h3>
            <p className="text-xs text-neutral-600 mt-1">
              Configure the task workload above and click{' '}
              <strong>
                {appMode === 'Individual Simulation'
                  ? 'Run Simulation'
                  : appMode === 'Algorithm Comparison'
                  ? 'Run Comparison'
                  : 'Run Cluster Balancer'}
              </strong>{' '}
              in the sidebar to execute.
            </p>
          </div>
        ) : validationError ? (
          <div className="border border-red-300 bg-red-50 text-red-700 p-4 rounded text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>Please resolve workload validation errors to run the simulation.</span>
          </div>
        ) : appMode === 'Multi-Node Cluster (Stage 3)' ? (
          /* Multi-Node Cluster View */
          <MultiNodeView tasks={tasks} timeQuantum={timeQuantum} />
        ) : appMode === 'Algorithm Comparison' && comparisonResult ? (
          /* Algorithm Comparison Mode */
          <div className="space-y-6">
            {/* Comparative Performance Overview Table */}
            <div>
              <h2 className="text-sm font-semibold uppercase tracking-wider text-neutral-800 pb-1 mb-3 border-b border-neutral-200">
                Comparative Performance Overview
              </h2>
              <div className="overflow-x-auto border border-neutral-900 rounded">
                <table className="w-full text-left text-xs">
                  <thead className="bg-neutral-100 border-b border-neutral-900 font-bold text-neutral-800">
                    <tr>
                      <th className="py-2.5 px-4">Algorithm</th>
                      <th className="py-2.5 px-4">Avg Waiting Time</th>
                      <th className="py-2.5 px-4">Avg Turnaround Time</th>
                      <th className="py-2.5 px-4">Makespan</th>
                      <th className="py-2.5 px-4">CPU Utilization (%)</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-neutral-200 font-mono">
                    {comparisonResult.comparison_rows.map((row) => (
                      <tr key={row.Algorithm} className="hover:bg-neutral-50">
                        <td className="py-2.5 px-4 font-sans font-bold text-neutral-900">
                          {row.Algorithm}
                        </td>
                        <td className="py-2.5 px-4">
                          {row['Avg Waiting Time'].toFixed(2)} units
                        </td>
                        <td className="py-2.5 px-4">
                          {row['Avg Turnaround Time'].toFixed(2)} units
                        </td>
                        <td className="py-2.5 px-4">{row.Makespan} units</td>
                        <td className="py-2.5 px-4">
                          {row['CPU Utilization (%)'].toFixed(2)}%
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Automated Performance Summary */}
            <div>
              <h2 className="text-sm font-semibold uppercase tracking-wider text-neutral-800 pb-1 mb-3 border-b border-neutral-200">
                Automated Performance Summary
              </h2>
              <div className="bg-neutral-50 border border-neutral-900 rounded p-4 text-xs">
                <ul className="space-y-2 text-neutral-800">
                  <li className="flex items-center gap-2 flex-wrap">
                    <span className="font-bold">Lowest Average Waiting Time:</span>
                    <span className="bg-blue-50 text-blue-700 border border-blue-600 px-2 py-0.5 rounded font-semibold text-[11px] flex items-center gap-1">
                      <Award className="w-3 h-3 text-blue-600" />
                      {comparisonResult.best_performers.lowest_waiting.join(', ')}
                      {comparisonResult.best_performers.lowest_waiting.length > 1 && ' (Tied)'}
                    </span>
                    <span className="text-neutral-500 font-mono">
                      (
                      {Math.min(
                        ...comparisonResult.comparison_rows.map((r) => r['Avg Waiting Time'])
                      ).toFixed(2)}{' '}
                      units)
                    </span>
                  </li>

                  <li className="flex items-center gap-2 flex-wrap">
                    <span className="font-bold">Lowest Average Turnaround Time:</span>
                    <span className="bg-blue-50 text-blue-700 border border-blue-600 px-2 py-0.5 rounded font-semibold text-[11px] flex items-center gap-1">
                      <Award className="w-3 h-3 text-blue-600" />
                      {comparisonResult.best_performers.lowest_turnaround.join(', ')}
                      {comparisonResult.best_performers.lowest_turnaround.length > 1 && ' (Tied)'}
                    </span>
                    <span className="text-neutral-500 font-mono">
                      (
                      {Math.min(
                        ...comparisonResult.comparison_rows.map(
                          (r) => r['Avg Turnaround Time']
                        )
                      ).toFixed(2)}{' '}
                      units)
                    </span>
                  </li>

                  <li className="flex items-center gap-2 flex-wrap">
                    <span className="font-bold">Shortest Makespan:</span>
                    <span className="bg-blue-50 text-blue-700 border border-blue-600 px-2 py-0.5 rounded font-semibold text-[11px] flex items-center gap-1">
                      <Award className="w-3 h-3 text-blue-600" />
                      {comparisonResult.best_performers.shortest_makespan.join(', ')}
                      {comparisonResult.best_performers.shortest_makespan.length > 1 && ' (Tied)'}
                    </span>
                    <span className="text-neutral-500 font-mono">
                      (
                      {Math.min(
                        ...comparisonResult.comparison_rows.map((r) => r.Makespan)
                      )}{' '}
                      units)
                    </span>
                  </li>

                  <li className="flex items-center gap-2 flex-wrap">
                    <span className="font-bold">Highest CPU Utilization:</span>
                    <span className="bg-blue-50 text-blue-700 border border-blue-600 px-2 py-0.5 rounded font-semibold text-[11px] flex items-center gap-1">
                      <Award className="w-3 h-3 text-blue-600" />
                      {comparisonResult.best_performers.highest_utilization.join(', ')}
                      {comparisonResult.best_performers.highest_utilization.length > 1 &&
                        ' (Tied)'}
                    </span>
                    <span className="text-neutral-500 font-mono">
                      (
                      {Math.max(
                        ...comparisonResult.comparison_rows.map(
                          (r) => r['CPU Utilization (%)']
                        )
                      ).toFixed(2)}
                      %)
                    </span>
                  </li>
                </ul>

                <p className="mt-3 pt-3 border-t border-neutral-200 text-[11px] text-neutral-500 italic">
                  Note: Scheduling performance is heavily workload-dependent and influenced by the
                  Round Robin quantum (q = {timeQuantum}). Shortest Job First typically minimizes
                  average waiting time when burst variances are high, while Round Robin provides fair
                  CPU sharing.
                </p>
              </div>
            </div>

            {/* Comparative Metric Charts */}
            <div>
              <h2 className="text-sm font-semibold uppercase tracking-wider text-neutral-800 pb-1 mb-3 border-b border-neutral-200">
                Comparative Metric Charts
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <AlgorithmMetricBar
                  title="Avg Waiting Time (Lower is Better)"
                  rows={comparisonResult.comparison_rows}
                  dataKey="Avg Waiting Time"
                  color="#2563EB"
                />
                <AlgorithmMetricBar
                  title="Avg Turnaround Time (Lower is Better)"
                  rows={comparisonResult.comparison_rows}
                  dataKey="Avg Turnaround Time"
                  color="#3B82F6"
                />
                <AlgorithmMetricBar
                  title="Makespan / Total Duration"
                  rows={comparisonResult.comparison_rows}
                  dataKey="Makespan"
                  color="#1D4ED8"
                />
                <AlgorithmMetricBar
                  title="CPU Utilization (%)"
                  rows={comparisonResult.comparison_rows}
                  dataKey="CPU Utilization (%)"
                  color="#60A5FA"
                  isPercent
                />
              </div>
            </div>

            {/* Execution Timelines (Gantt Comparison) Tabs */}
            <div>
              <h2 className="text-sm font-semibold uppercase tracking-wider text-neutral-800 pb-1 mb-3 border-b border-neutral-200">
                Execution Timelines (Gantt Comparison)
              </h2>
              <div className="flex items-center gap-2 mb-3">
                <button
                  type="button"
                  onClick={() => setComparisonTab('RR')}
                  className={`px-3 py-1.5 text-xs font-semibold rounded cursor-pointer transition-colors border ${
                    comparisonTab === 'RR'
                      ? 'bg-blue-600 text-white border-blue-600'
                      : 'bg-white text-neutral-700 border-neutral-300 hover:border-neutral-900'
                  }`}
                >
                  Round Robin (RR)
                </button>
                <button
                  type="button"
                  onClick={() => setComparisonTab('FCFS')}
                  className={`px-3 py-1.5 text-xs font-semibold rounded cursor-pointer transition-colors border ${
                    comparisonTab === 'FCFS'
                      ? 'bg-blue-600 text-white border-blue-600'
                      : 'bg-white text-neutral-700 border-neutral-300 hover:border-neutral-900'
                  }`}
                >
                  First Come, First Served (FCFS)
                </button>
                <button
                  type="button"
                  onClick={() => setComparisonTab('SJF')}
                  className={`px-3 py-1.5 text-xs font-semibold rounded cursor-pointer transition-colors border ${
                    comparisonTab === 'SJF'
                      ? 'bg-blue-600 text-white border-blue-600'
                      : 'bg-white text-neutral-700 border-neutral-300 hover:border-neutral-900'
                  }`}
                >
                  Shortest Job First (SJF)
                </button>
              </div>

              {comparisonTab === 'RR' && (
                <GanttChart
                  slices={comparisonResult.algorithms['Round Robin (RR)'].slices}
                  makespan={Math.max(
                    ...comparisonResult.comparison_rows.map((r) => r.Makespan)
                  )}
                />
              )}
              {comparisonTab === 'FCFS' && (
                <GanttChart
                  slices={
                    comparisonResult.algorithms['First Come, First Served (FCFS)'].slices
                  }
                  makespan={Math.max(
                    ...comparisonResult.comparison_rows.map((r) => r.Makespan)
                  )}
                />
              )}
              {comparisonTab === 'SJF' && (
                <GanttChart
                  slices={comparisonResult.algorithms['Shortest Job First (SJF)'].slices}
                  makespan={Math.max(
                    ...comparisonResult.comparison_rows.map((r) => r.Makespan)
                  )}
                />
              )}
            </div>
          </div>
        ) : singleSimResult ? (
          /* Individual Simulation Mode */
          <div className="space-y-6">
            {/* KPI Performance Summary */}
            <div>
              <h2 className="text-sm font-semibold uppercase tracking-wider text-neutral-800 pb-1 mb-3 border-b border-neutral-200">
                Performance Summary
              </h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="border border-neutral-900 rounded p-4 bg-white text-left">
                  <div className="text-[11px] uppercase tracking-wider text-neutral-500 font-semibold">
                    Tasks Scheduled
                  </div>
                  <div className="text-2xl font-bold text-neutral-900 mt-1">
                    {singleSimResult.summary.total_tasks}
                  </div>
                </div>

                <div className="border border-neutral-900 rounded p-4 bg-white text-left">
                  <div className="text-[11px] uppercase tracking-wider text-neutral-500 font-semibold">
                    Average Waiting Time
                  </div>
                  <div className="text-2xl font-bold text-neutral-900 mt-1">
                    {singleSimResult.summary.avg_waiting_time.toFixed(2)}{' '}
                    <span className="text-xs font-normal text-neutral-500">units</span>
                  </div>
                </div>

                <div className="border border-neutral-900 rounded p-4 bg-white text-left">
                  <div className="text-[11px] uppercase tracking-wider text-neutral-500 font-semibold">
                    Average Turnaround Time
                  </div>
                  <div className="text-2xl font-bold text-neutral-900 mt-1">
                    {singleSimResult.summary.avg_turnaround_time.toFixed(2)}{' '}
                    <span className="text-xs font-normal text-neutral-500">units</span>
                  </div>
                </div>

                <div className="border border-neutral-900 rounded p-4 bg-white text-left">
                  <div className="text-[11px] uppercase tracking-wider text-neutral-500 font-semibold">
                    Makespan
                  </div>
                  <div className="text-2xl font-bold text-neutral-900 mt-1">
                    {singleSimResult.summary.makespan}{' '}
                    <span className="text-xs font-normal text-neutral-500">units</span>
                  </div>
                </div>
              </div>
            </div>

            {/* CPU Execution Timeline (Gantt Chart) */}
            <div>
              <h2 className="text-sm font-semibold uppercase tracking-wider text-neutral-800 pb-1 mb-3 border-b border-neutral-200">
                CPU Execution Timeline
              </h2>
              <GanttChart
                slices={singleSimResult.slices}
                makespan={singleSimResult.summary.makespan}
              />
            </div>

            {/* Task Results & Comparison */}
            <div>
              <h2 className="text-sm font-semibold uppercase tracking-wider text-neutral-800 pb-1 mb-3 border-b border-neutral-200">
                Task Results & Comparison
              </h2>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
                {/* Results Table */}
                <div className="overflow-x-auto border border-neutral-900 rounded bg-white">
                  <table className="w-full text-left text-xs">
                    <thead className="bg-neutral-100 border-b border-neutral-900 font-bold text-neutral-800">
                      <tr>
                        <th className="py-2.5 px-3">Task ID</th>
                        <th className="py-2.5 px-3">Arrival</th>
                        <th className="py-2.5 px-3">Burst</th>
                        <th className="py-2.5 px-3">Completion</th>
                        <th className="py-2.5 px-3">Waiting Time</th>
                        <th className="py-2.5 px-3">Turnaround</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-neutral-200 font-mono">
                      {Object.values(singleSimResult.metrics)
                        .sort((a, b) =>
                          String(a.task_id).localeCompare(String(b.task_id))
                        )
                        .map((m) => (
                          <tr key={m.task_id} className="hover:bg-neutral-50">
                            <td className="py-2.5 px-3 font-sans font-bold text-blue-600">
                              {m.task_id}
                            </td>
                            <td className="py-2.5 px-3">{m.arrival_time}</td>
                            <td className="py-2.5 px-3">{m.burst_time}</td>
                            <td className="py-2.5 px-3">{m.completion_time}</td>
                            <td className="py-2.5 px-3">{m.waiting_time}</td>
                            <td className="py-2.5 px-3">{m.turnaround_time}</td>
                          </tr>
                        ))}
                    </tbody>
                  </table>
                </div>

                {/* Grouped Bar Chart */}
                <div>
                  <TaskComparisonChart metrics={singleSimResult.metrics} />
                </div>
              </div>
            </div>

            {/* Detailed Execution Slices Trace */}
            <ExecutionSlicesTable slices={singleSimResult.slices} />
          </div>
        ) : null}
      </main>
        </div>
      )}
    </div>
  );
};
