import React from 'react';
import { Task } from '../types';
import { Plus, Trash2, RotateCcw, Sparkles } from 'lucide-react';
import { generateSampleTasks } from '../lib/taskManager';

interface TaskEditorProps {
  tasks: Task[];
  onChange: (tasks: Task[]) => void;
  validationError: string;
}

export const TaskEditor: React.FC<TaskEditorProps> = ({
  tasks,
  onChange,
  validationError,
}) => {
  const handleTaskChange = (
    index: number,
    field: 'task_id' | 'arrival_time' | 'burst_time',
    value: string
  ) => {
    const updated = [...tasks];
    if (field === 'task_id') {
      updated[index] = { ...updated[index], task_id: value };
    } else {
      const num = parseInt(value, 10);
      updated[index] = {
        ...updated[index],
        [field]: isNaN(num) ? 0 : num,
      };
    }
    onChange(updated);
  };

  const handleAddTask = () => {
    const nextIdNum = tasks.length + 1;
    const newTask: Task = {
      task_id: `T${nextIdNum}`,
      arrival_time: tasks.length > 0 ? Math.max(...tasks.map((t) => t.arrival_time)) + 1 : 0,
      burst_time: 3,
      status: 'Waiting',
      assigned_node: null,
    };
    onChange([...tasks, newTask]);
  };

  const handleRemoveTask = (index: number) => {
    const updated = tasks.filter((_, i) => i !== index);
    onChange(updated);
  };

  const handleLoadPreset = (presetName: string) => {
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
      case 'simultaneous':
        preset = [
          { task_id: 'T1', arrival_time: 0, burst_time: 4 },
          { task_id: 'T2', arrival_time: 0, burst_time: 3 },
          { task_id: 'T3', arrival_time: 0, burst_time: 1 },
          { task_id: 'T4', arrival_time: 0, burst_time: 6 },
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
    onChange(preset);
  };

  return (
    <div className="bg-white border border-neutral-900 rounded p-4 mb-6">
      <div className="flex flex-wrap items-center justify-between gap-3 mb-3">
        <div>
          <h2 className="text-sm font-semibold uppercase tracking-wider text-neutral-800">
            Workload Configuration
          </h2>
          <p className="text-xs text-neutral-500">
            Define task arrival times and CPU burst requirements
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <div className="flex items-center gap-1.5 text-xs text-neutral-600 bg-neutral-100 px-2 py-1 rounded border border-neutral-300">
            <Sparkles className="w-3.5 h-3.5 text-blue-600" />
            <span>Preset:</span>
            <select
              className="bg-transparent border-none text-xs font-medium text-neutral-800 focus:outline-none cursor-pointer"
              onChange={(e) => handleLoadPreset(e.target.value)}
              defaultValue="sample"
            >
              <option value="sample">Default Sample (4 tasks)</option>
              <option value="staggered">Staggered Arrivals</option>
              <option value="high_variance">High Burst Variance</option>
              <option value="simultaneous">Simultaneous Arrival (Ties)</option>
              <option value="idle_gaps">Idle Gaps Workload</option>
            </select>
          </div>

          <button
            type="button"
            onClick={handleAddTask}
            className="flex items-center gap-1 px-3 py-1 bg-white hover:bg-neutral-50 text-neutral-900 border border-neutral-900 rounded text-xs font-semibold cursor-pointer transition-colors"
          >
            <Plus className="w-3.5 h-3.5" />
            Add Task
          </button>

          <button
            type="button"
            onClick={() => handleLoadPreset('sample')}
            className="flex items-center gap-1 px-2.5 py-1 text-neutral-600 hover:text-neutral-900 hover:bg-neutral-100 rounded text-xs transition-colors cursor-pointer"
            title="Reset to default sample"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            Reset
          </button>
        </div>
      </div>

      {validationError && (
        <div className="mb-3 px-3 py-2 bg-red-50 border border-red-500 text-red-700 text-xs rounded">
          <strong>Validation Error:</strong> {validationError}
        </div>
      )}

      <div className="overflow-x-auto border border-neutral-300 rounded">
        <table className="w-full text-left text-xs">
          <thead className="bg-neutral-100 border-b border-neutral-300 text-neutral-700 font-semibold uppercase tracking-wider">
            <tr>
              <th className="py-2.5 px-3 w-16">#</th>
              <th className="py-2.5 px-3">Task ID</th>
              <th className="py-2.5 px-3">Arrival Time (≥ 0)</th>
              <th className="py-2.5 px-3">Burst Time (&gt; 0)</th>
              <th className="py-2.5 px-3 text-right w-20">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-neutral-200">
            {tasks.map((task, idx) => (
              <tr key={idx} className="hover:bg-neutral-50 transition-colors">
                <td className="py-2 px-3 text-neutral-400 font-mono">{idx + 1}</td>
                <td className="py-2 px-3">
                  <input
                    type="text"
                    value={task.task_id}
                    onChange={(e) => handleTaskChange(idx, 'task_id', e.target.value)}
                    className="w-full px-2 py-1 border border-neutral-300 rounded focus:border-blue-600 focus:outline-none font-medium font-mono text-xs"
                    placeholder="e.g. T1"
                  />
                </td>
                <td className="py-2 px-3">
                  <input
                    type="number"
                    min="0"
                    step="1"
                    value={task.arrival_time}
                    onChange={(e) => handleTaskChange(idx, 'arrival_time', e.target.value)}
                    className="w-full px-2 py-1 border border-neutral-300 rounded focus:border-blue-600 focus:outline-none font-mono text-xs"
                  />
                </td>
                <td className="py-2 px-3">
                  <input
                    type="number"
                    min="1"
                    step="1"
                    value={task.burst_time}
                    onChange={(e) => handleTaskChange(idx, 'burst_time', e.target.value)}
                    className="w-full px-2 py-1 border border-neutral-300 rounded focus:border-blue-600 focus:outline-none font-mono text-xs"
                  />
                </td>
                <td className="py-2 px-3 text-right">
                  <button
                    type="button"
                    onClick={() => handleRemoveTask(idx)}
                    disabled={tasks.length <= 1}
                    className="text-neutral-400 hover:text-red-600 disabled:opacity-30 disabled:hover:text-neutral-400 p-1 cursor-pointer transition-colors"
                    title={tasks.length <= 1 ? 'Minimum 1 task required' : 'Delete task'}
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="flex justify-between items-center text-[11px] text-neutral-500 mt-2 px-1">
        <span>Total configured: {tasks.length} task(s)</span>
        <span>Total workload: {tasks.reduce((sum, t) => sum + (Number(t.burst_time) || 0), 0)} CPU units</span>
      </div>
    </div>
  );
};
