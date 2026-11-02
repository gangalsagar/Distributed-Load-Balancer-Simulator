import React from 'react';
import { AppMode, SchedulingAlgorithm } from '../types';
import { Play, RotateCcw, FileText, Layers, GitCompare, Server, Home } from 'lucide-react';

interface SidebarProps {
  appMode: AppMode;
  setAppMode: (mode: AppMode) => void;
  algorithm: SchedulingAlgorithm;
  setAlgorithm: (algo: SchedulingAlgorithm) => void;
  timeQuantum: number;
  setTimeQuantum: (q: number) => void;
  onRun: () => void;
  onLoadSample: () => void;
  onReset: () => void;
  onBackToLanding: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  appMode,
  setAppMode,
  algorithm,
  setAlgorithm,
  timeQuantum,
  setTimeQuantum,
  onRun,
  onLoadSample,
  onReset,
  onBackToLanding,
}) => {
  return (
    <aside className="w-full md:w-80 bg-neutral-50 border-r border-neutral-300 p-5 flex flex-col justify-between shrink-0 font-sans">
      <div className="space-y-6">
        {/* Navigation Section */}
        <div>
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-xs font-bold uppercase tracking-wider text-neutral-900">
              Navigation
            </h2>
            <button
              type="button"
              onClick={onBackToLanding}
              className="text-[11px] font-semibold text-blue-600 hover:text-blue-800 flex items-center gap-1 cursor-pointer"
              title="Return to Landing Page"
            >
              <Home className="w-3.5 h-3.5" />
              <span>Landing Page</span>
            </button>
          </div>
          <div className="space-y-1.5">
            <button
              type="button"
              onClick={() => setAppMode('Individual Simulation')}
              className={`w-full flex items-center gap-2.5 px-3 py-2 rounded text-xs font-semibold text-left transition-colors cursor-pointer border ${
                appMode === 'Individual Simulation'
                  ? 'bg-blue-600 text-white border-blue-600'
                  : 'bg-white text-neutral-800 border-neutral-300 hover:border-neutral-900'
              }`}
            >
              <Layers className="w-4 h-4 shrink-0" />
              <span>Individual Simulation</span>
            </button>

            <button
              type="button"
              onClick={() => setAppMode('Algorithm Comparison')}
              className={`w-full flex items-center gap-2.5 px-3 py-2 rounded text-xs font-semibold text-left transition-colors cursor-pointer border ${
                appMode === 'Algorithm Comparison'
                  ? 'bg-blue-600 text-white border-blue-600'
                  : 'bg-white text-neutral-800 border-neutral-300 hover:border-neutral-900'
              }`}
            >
              <GitCompare className="w-4 h-4 shrink-0" />
              <span>Algorithm Comparison</span>
            </button>

            <button
              type="button"
              onClick={() => setAppMode('Multi-Node Cluster (Stage 3)')}
              className={`w-full flex items-center gap-2.5 px-3 py-2 rounded text-xs font-semibold text-left transition-colors cursor-pointer border ${
                appMode === 'Multi-Node Cluster (Stage 3)'
                  ? 'bg-blue-600 text-white border-blue-600'
                  : 'bg-white text-neutral-800 border-neutral-300 hover:border-neutral-900'
              }`}
            >
              <Server className="w-4 h-4 shrink-0" />
              <span>Multi-Node Cluster (Stage 3)</span>
            </button>
          </div>
        </div>

        <hr className="border-neutral-200" />

        {/* Controls Section */}
        <div>
          <h2 className="text-xs font-bold uppercase tracking-wider text-neutral-900 mb-3">
            Controls
          </h2>

          {appMode === 'Individual Simulation' ? (
            <div className="space-y-4">
              <div>
                <label htmlFor="algorithm-select" className="block text-xs font-semibold text-neutral-700 mb-1">
                  Scheduling Algorithm
                </label>
                <select
                  id="algorithm-select"
                  aria-label="Scheduling Algorithm"
                  value={algorithm}
                  onChange={(e) => setAlgorithm(e.target.value as SchedulingAlgorithm)}
                  className="w-full px-3 py-2 bg-white border border-neutral-900 rounded text-xs font-medium focus:outline-none focus:ring-1 focus:ring-blue-600 cursor-pointer"
                >
                  <option value="Round Robin (RR)">Round Robin (RR)</option>
                  <option value="First Come, First Served (FCFS)">
                    First Come, First Served (FCFS)
                  </option>
                  <option value="Shortest Job First (SJF — Non-Preemptive)">
                    Shortest Job First (SJF — Non-Preemptive)
                  </option>
                </select>
                <p className="text-[11px] text-neutral-500 mt-1">
                  {algorithm.includes('Round Robin')
                    ? 'Preemptive time-sliced CPU allocation.'
                    : 'Non-preemptive queue-based allocation.'}
                </p>
              </div>

              {algorithm === 'Round Robin (RR)' && (
                <div>
                  <label htmlFor="rr-quantum-input" className="block text-xs font-semibold text-neutral-700 mb-1">
                    Time Quantum (q)
                  </label>
                  <input
                    id="rr-quantum-input"
                    aria-label="Time Quantum (q)"
                    type="number"
                    min="1"
                    max="100"
                    value={timeQuantum}
                    onChange={(e) => setTimeQuantum(Math.max(1, parseInt(e.target.value, 10) || 1))}
                    className="w-full px-3 py-2 bg-white border border-neutral-900 rounded text-xs font-mono font-medium focus:outline-none focus:ring-1 focus:ring-blue-600"
                  />
                  <p className="text-[11px] text-neutral-500 mt-1">
                    Positive integer time slice per execution slice.
                  </p>
                </div>
              )}
            </div>
          ) : (
            <div className="space-y-4">
              <div>
                <label htmlFor="comp-quantum-input" className="block text-xs font-semibold text-neutral-700 mb-1">
                  Round Robin Quantum (q)
                </label>
                <input
                  id="comp-quantum-input"
                  aria-label="Round Robin Quantum (q)"
                  type="number"
                  min="1"
                  max="100"
                  value={timeQuantum}
                  onChange={(e) => setTimeQuantum(Math.max(1, parseInt(e.target.value, 10) || 1))}
                  className="w-full px-3 py-2 bg-white border border-neutral-900 rounded text-xs font-mono font-medium focus:outline-none focus:ring-1 focus:ring-blue-600"
                />
                <p className="text-[11px] text-neutral-500 mt-1">
                  Time quantum applied to Round Robin during side-by-side comparison.
                </p>
              </div>
            </div>
          )}

          {/* Action buttons */}
          <div className="mt-5 space-y-2">
            <button
              type="button"
              onClick={onRun}
              className="w-full flex items-center justify-center gap-2 py-2.5 px-4 bg-blue-600 hover:bg-blue-700 text-white border border-blue-600 rounded text-xs font-bold cursor-pointer transition-colors shadow-sm"
            >
              <Play className="w-3.5 h-3.5 fill-white" />
              {appMode === 'Individual Simulation'
                ? 'Run Simulation'
                : appMode === 'Algorithm Comparison'
                ? 'Run Comparison'
                : 'Run Cluster Balancer'}
            </button>

            <div className="grid grid-cols-2 gap-2">
              <button
                type="button"
                onClick={onLoadSample}
                className="flex items-center justify-center gap-1.5 py-2 px-3 bg-white hover:bg-neutral-100 text-neutral-900 border border-neutral-900 rounded text-xs font-semibold cursor-pointer transition-colors"
              >
                <FileText className="w-3.5 h-3.5" />
                Load Sample
              </button>

              <button
                type="button"
                onClick={onReset}
                className="flex items-center justify-center gap-1.5 py-2 px-3 bg-white hover:bg-neutral-100 text-neutral-900 border border-neutral-900 rounded text-xs font-semibold cursor-pointer transition-colors"
              >
                <RotateCcw className="w-3.5 h-3.5" />
                Reset
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="pt-6 border-t border-neutral-200 text-center">
        <p className="text-[11px] text-neutral-500">
          OS Mini-Project · CPU Scheduling Simulator
        </p>
        <p className="text-[10px] text-neutral-400 mt-0.5">
          Deterministic single-node & distributed multi-node
        </p>
      </div>
    </aside>
  );
};
