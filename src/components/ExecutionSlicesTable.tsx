import React, { useState } from 'react';
import { ScheduleSlice } from '../types';
import { ChevronDown, ChevronUp, Clock } from 'lucide-react';

interface ExecutionSlicesTableProps {
  slices: ScheduleSlice[];
}

export const ExecutionSlicesTable: React.FC<ExecutionSlicesTableProps> = ({ slices }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="bg-white border border-neutral-900 rounded p-4 mb-6">
      <button
        type="button"
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full flex items-center justify-between text-left cursor-pointer group"
      >
        <div className="flex items-center gap-2">
          <Clock className="w-4 h-4 text-blue-600" />
          <h3 className="text-xs font-semibold uppercase tracking-wider text-neutral-800">
            Chronological Execution Slices ({slices.length} slices)
          </h3>
        </div>
        <div className="flex items-center gap-1 text-xs text-neutral-500 group-hover:text-neutral-900">
          <span>{isExpanded ? 'Hide Trace' : 'Show Detailed Trace'}</span>
          {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </div>
      </button>

      {isExpanded && (
        <div className="mt-3 overflow-x-auto border border-neutral-200 rounded">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-neutral-100 text-neutral-700 uppercase tracking-wider border-b border-neutral-300">
              <tr>
                <th className="py-2 px-3">Slice #</th>
                <th className="py-2 px-3">Task ID</th>
                <th className="py-2 px-3">Start Time</th>
                <th className="py-2 px-3">End Time</th>
                <th className="py-2 px-3">Duration</th>
                <th className="py-2 px-3">Remaining</th>
                <th className="py-2 px-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-neutral-200">
              {slices.map((slice, idx) => (
                <tr key={idx} className="hover:bg-neutral-50">
                  <td className="py-2 px-3 text-neutral-500">{idx + 1}</td>
                  <td className="py-2 px-3 font-bold text-blue-600">{slice.task_id}</td>
                  <td className="py-2 px-3">{slice.start_time}</td>
                  <td className="py-2 px-3">{slice.end_time}</td>
                  <td className="py-2 px-3">{slice.duration}</td>
                  <td className="py-2 px-3">{slice.remaining_time}</td>
                  <td className="py-2 px-3">
                    <span
                      className={`inline-block px-1.5 py-0.5 rounded text-[10px] font-sans font-semibold ${
                        slice.completed
                          ? 'bg-emerald-100 text-emerald-800 border border-emerald-300'
                          : 'bg-amber-100 text-amber-800 border border-amber-300'
                      }`}
                    >
                      {slice.completed ? 'Completed' : 'Preempted'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
