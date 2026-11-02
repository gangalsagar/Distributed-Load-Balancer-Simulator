import React from 'react';
import { TaskMetric, ComparisonRow } from '../types';

interface TaskComparisonChartProps {
  metrics: Record<string, TaskMetric>;
}

export const TaskComparisonChart: React.FC<TaskComparisonChartProps> = ({ metrics }) => {
  const taskList = Object.values(metrics).sort((a, b) =>
    String(a.task_id).localeCompare(String(b.task_id))
  );

  if (!taskList.length) return null;

  const maxVal = Math.max(
    ...taskList.map((t) => Math.max(t.waiting_time, t.turnaround_time, 1))
  );
  const chartHeight = 220;
  const chartWidth = 500;
  const paddingLeft = 40;
  const paddingBottom = 40;
  const paddingTop = 20;
  const paddingRight = 20;

  const availableWidth = chartWidth - paddingLeft - paddingRight;
  const availableHeight = chartHeight - paddingTop - paddingBottom;
  const groupWidth = availableWidth / taskList.length;
  const barWidth = Math.min(groupWidth * 0.35, 32);

  return (
    <div className="w-full bg-white border border-neutral-900 rounded p-4 font-sans">
      <div className="flex items-center justify-between mb-3 text-xs">
        <span className="font-semibold text-neutral-800">Task Performance Comparison</span>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-1.5">
            <span className="inline-block w-3.5 h-3.5 bg-white border border-neutral-900" />
            <span className="text-neutral-700">Waiting Time</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="inline-block w-3.5 h-3.5 bg-blue-600 border border-neutral-900" />
            <span className="text-neutral-700">Turnaround Time</span>
          </div>
        </div>
      </div>

      <div className="w-full overflow-x-auto">
        <svg viewBox={`0 0 ${chartWidth} ${chartHeight}`} className="w-full h-auto">
          {/* Y-axis ticks */}
          {[0, Math.round(maxVal / 2), maxVal].map((val) => {
            const yPos =
              paddingTop + availableHeight - (val / (maxVal || 1)) * availableHeight;
            return (
              <g key={val}>
                <line
                  x1={paddingLeft}
                  y1={yPos}
                  x2={chartWidth - paddingRight}
                  y2={yPos}
                  stroke="#F3F4F6"
                  strokeWidth="1"
                />
                <text
                  x={paddingLeft - 8}
                  y={yPos + 4}
                  textAnchor="end"
                  className="text-[10px] fill-neutral-600 font-mono"
                >
                  {val}
                </text>
              </g>
            );
          })}

          {/* Axes */}
          <line
            x1={paddingLeft}
            y1={paddingTop + availableHeight}
            x2={chartWidth - paddingRight}
            y2={paddingTop + availableHeight}
            stroke="#111111"
            strokeWidth="1.5"
          />
          <line
            x1={paddingLeft}
            y1={paddingTop}
            x2={paddingLeft}
            y2={paddingTop + availableHeight}
            stroke="#111111"
            strokeWidth="1.5"
          />

          {/* Bars */}
          {taskList.map((task, idx) => {
            const centerX = paddingLeft + idx * groupWidth + groupWidth / 2;
            const waitHeight = (task.waiting_time / (maxVal || 1)) * availableHeight;
            const tatHeight = (task.turnaround_time / (maxVal || 1)) * availableHeight;

            const waitX = centerX - barWidth - 2;
            const tatX = centerX + 2;

            const waitY = paddingTop + availableHeight - waitHeight;
            const tatY = paddingTop + availableHeight - tatHeight;

            return (
              <g key={task.task_id}>
                {/* Waiting Time Bar */}
                <rect
                  x={waitX}
                  y={waitY}
                  width={barWidth}
                  height={Math.max(waitHeight, 2)}
                  fill="#FFFFFF"
                  stroke="#111111"
                  strokeWidth="1.5"
                />
                <text
                  x={waitX + barWidth / 2}
                  y={waitY - 4}
                  textAnchor="middle"
                  className="text-[10px] fill-neutral-900 font-mono font-bold"
                >
                  {task.waiting_time}
                </text>

                {/* Turnaround Time Bar */}
                <rect
                  x={tatX}
                  y={tatY}
                  width={barWidth}
                  height={Math.max(tatHeight, 2)}
                  fill="#2563EB"
                  stroke="#111111"
                  strokeWidth="1.5"
                />
                <text
                  x={tatX + barWidth / 2}
                  y={tatY - 4}
                  textAnchor="middle"
                  className="text-[10px] fill-blue-700 font-mono font-bold"
                >
                  {task.turnaround_time}
                </text>

                {/* X axis Task label */}
                <text
                  x={centerX}
                  y={paddingTop + availableHeight + 18}
                  textAnchor="middle"
                  className="text-[11px] fill-neutral-900 font-medium"
                >
                  {task.task_id}
                </text>
              </g>
            );
          })}
        </svg>
      </div>
    </div>
  );
};

interface AlgorithmMetricBarProps {
  title: string;
  rows: ComparisonRow[];
  dataKey: keyof ComparisonRow;
  color: string;
  isPercent?: boolean;
}

export const AlgorithmMetricBar: React.FC<AlgorithmMetricBarProps> = ({
  title,
  rows,
  dataKey,
  color,
  isPercent = false,
}) => {
  const values = rows.map((r) => Number(r[dataKey]));
  const maxVal = Math.max(...values, isPercent ? 100 : 1);

  const chartHeight = 180;
  const chartWidth = 340;
  const paddingLeft = 45;
  const paddingBottom = 40;
  const paddingTop = 25;
  const paddingRight = 15;

  const availableWidth = chartWidth - paddingLeft - paddingRight;
  const availableHeight = chartHeight - paddingTop - paddingBottom;
  const colWidth = availableWidth / rows.length;
  const barWidth = Math.min(colWidth * 0.55, 48);

  const shortNames: Record<string, string> = {
    'Round Robin (RR)': 'RR',
    'First Come, First Served (FCFS)': 'FCFS',
    'Shortest Job First (SJF)': 'SJF',
  };

  return (
    <div className="bg-white border border-neutral-900 rounded p-4 font-sans">
      <div className="text-xs font-semibold text-neutral-800 mb-2 truncate">
        {title}
      </div>
      <svg viewBox={`0 0 ${chartWidth} ${chartHeight}`} className="w-full h-auto">
        {/* Horizontal gridlines */}
        {[0, Math.round(maxVal / 2), maxVal].map((val) => {
          const yPos =
            paddingTop + availableHeight - (val / (maxVal || 1)) * availableHeight;
          return (
            <g key={val}>
              <line
                x1={paddingLeft}
                y1={yPos}
                x2={chartWidth - paddingRight}
                y2={yPos}
                stroke="#F3F4F6"
                strokeWidth="1"
              />
              <text
                x={paddingLeft - 6}
                y={yPos + 3}
                textAnchor="end"
                className="text-[9px] fill-neutral-600 font-mono"
              >
                {val}
                {isPercent ? '%' : ''}
              </text>
            </g>
          );
        })}

        {/* Axes */}
        <line
          x1={paddingLeft}
          y1={paddingTop + availableHeight}
          x2={chartWidth - paddingRight}
          y2={paddingTop + availableHeight}
          stroke="#111111"
          strokeWidth="1.5"
        />
        <line
          x1={paddingLeft}
          y1={paddingTop}
          x2={paddingLeft}
          y2={paddingTop + availableHeight}
          stroke="#111111"
          strokeWidth="1.5"
        />

        {rows.map((row, idx) => {
          const val = Number(row[dataKey]);
          const barHeight = (val / (maxVal || 1)) * availableHeight;
          const centerX = paddingLeft + idx * colWidth + colWidth / 2;
          const barX = centerX - barWidth / 2;
          const barY = paddingTop + availableHeight - barHeight;

          return (
            <g key={row.Algorithm}>
              <rect
                x={barX}
                y={barY}
                width={barWidth}
                height={Math.max(barHeight, 2)}
                fill={color}
                stroke="#111111"
                strokeWidth="1.5"
              />
              <text
                x={centerX}
                y={barY - 4}
                textAnchor="middle"
                className="text-[10px] font-mono font-bold fill-neutral-900"
              >
                {isPercent ? `${val.toFixed(1)}%` : Number.isInteger(val) ? val : val.toFixed(2)}
              </text>
              <text
                x={centerX}
                y={paddingTop + availableHeight + 16}
                textAnchor="middle"
                className="text-[11px] font-semibold fill-neutral-800"
              >
                {shortNames[row.Algorithm] || row.Algorithm}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
};
