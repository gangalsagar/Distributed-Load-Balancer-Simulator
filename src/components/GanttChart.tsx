import React, { useState } from 'react';
import { ScheduleSlice } from '../types';
import { identifyIdleIntervals } from '../lib/metrics';

interface GanttChartProps {
  slices: ScheduleSlice[];
  makespan: number;
  height?: number;
}

export const GanttChart: React.FC<GanttChartProps> = ({ slices, makespan, height = 130 }) => {
  const [hoveredSlice, setHoveredSlice] = useState<ScheduleSlice | null>(null);
  const [mousePos, setMousePos] = useState<{ x: number; y: number }>({ x: 0, y: 0 });

  const idleSlices = identifyIdleIntervals(slices);
  const allItems = [
    ...slices.map((s) => ({ ...s, is_idle: false })),
    ...idleSlices.map((s) => ({ ...s, is_idle: true })),
  ].sort((a, b) => a.start_time - b.start_time);

  const uniqueTasks = Array.from(new Set(slices.map((s) => s.task_id))).sort();
  const blueShades = [
    '#2563EB', // blue-600
    '#1D4ED8', // blue-700
    '#3B82F6', // blue-500
    '#60A5FA', // blue-400
    '#1E40AF', // blue-800
    '#93C5FD', // blue-300
    '#0284C7', // sky-600
    '#4F46E5', // indigo-600
  ];

  const colorMap = new Map<string, string>();
  uniqueTasks.forEach((tid, idx) => {
    colorMap.set(tid, blueShades[idx % blueShades.length]);
  });

  const totalDuration = Math.max(makespan, 1);
  const maxTime = totalDuration + (makespan > 0 ? 0.2 : 1);

  // Generate tick steps
  const tickStep = makespan <= 25 ? 1 : Math.max(1, Math.floor(makespan / 15));
  const ticks: number[] = [];
  for (let t = 0; t <= Math.ceil(makespan); t += tickStep) {
    ticks.push(t);
  }
  if (!ticks.includes(makespan) && makespan > 0) {
    ticks.push(makespan);
  }

  const paddingLeft = 45;
  const paddingRight = 20;
  const paddingTop = 32;
  const barHeight = 44;

  return (
    <div className="w-full bg-white border border-neutral-900 rounded p-4 relative font-sans">
      {/* Legend */}
      <div className="flex flex-wrap items-center gap-3 text-xs mb-3 font-medium">
        <span className="text-neutral-500">Legend:</span>
        {uniqueTasks.map((tid) => (
          <div key={tid} className="flex items-center gap-1.5">
            <span
              className="inline-block w-3.5 h-3.5 border border-neutral-900"
              style={{ backgroundColor: colorMap.get(tid) }}
            />
            <span className="text-neutral-900">{tid}</span>
          </div>
        ))}
        {idleSlices.length > 0 && (
          <div className="flex items-center gap-1.5">
            <span className="inline-block w-3.5 h-3.5 border border-neutral-900 bg-white" />
            <span className="text-neutral-700">Idle (Unassigned CPU)</span>
          </div>
        )}
      </div>

      {/* SVG Timeline */}
      <div className="w-full overflow-x-auto">
        <div style={{ minWidth: '600px' }}>
          <svg
            viewBox={`0 0 1000 ${height}`}
            className="w-full h-auto select-none"
            style={{ minHeight: `${height}px` }}
            onMouseMove={(e) => {
              const rect = e.currentTarget.getBoundingClientRect();
              setMousePos({ x: e.clientX - rect.left, y: e.clientY - rect.top });
            }}
            onMouseLeave={() => setHoveredSlice(null)}
          >
            {/* Background Grid & Axis Line */}
            <line
              x1={paddingLeft}
              y1={paddingTop + barHeight}
              x2={1000 - paddingRight}
              y2={paddingTop + barHeight}
              stroke="#111111"
              strokeWidth="1.5"
            />
            <line
              x1={paddingLeft}
              y1={paddingTop}
              x2={paddingLeft}
              y2={paddingTop + barHeight + 8}
              stroke="#111111"
              strokeWidth="1.5"
            />

            {/* Y label */}
            <text
              x={paddingLeft - 10}
              y={paddingTop + barHeight / 2 + 4}
              textAnchor="end"
              className="text-[11px] font-semibold fill-neutral-800"
            >
              CPU
            </text>

            {/* Ticks and Vertical Grid Lines */}
            {ticks.map((t) => {
              const xPos =
                paddingLeft +
                (t / maxTime) * (1000 - paddingLeft - paddingRight);
              return (
                <g key={t}>
                  <line
                    x1={xPos}
                    y1={paddingTop}
                    x2={xPos}
                    y2={paddingTop + barHeight + 6}
                    stroke="#E5E7EB"
                    strokeWidth="1"
                    strokeDasharray={t % 5 === 0 ? undefined : '2,2'}
                  />
                  <line
                    x1={xPos}
                    y1={paddingTop + barHeight}
                    x2={xPos}
                    y2={paddingTop + barHeight + 6}
                    stroke="#111111"
                    strokeWidth="1"
                  />
                  <text
                    x={xPos}
                    y={paddingTop + barHeight + 18}
                    textAnchor="middle"
                    className="text-[10px] fill-neutral-700 font-mono"
                  >
                    {t}
                  </text>
                </g>
              );
            })}

            {/* Axis Title */}
            <text
              x={paddingLeft + (1000 - paddingLeft - paddingRight) / 2}
              y={height - 2}
              textAnchor="middle"
              className="text-[11px] fill-neutral-800 font-semibold"
            >
              Simulation Time (Units)
            </text>

            {/* Timeline Blocks */}
            {allItems.map((item, idx) => {
              const startX =
                paddingLeft +
                (item.start_time / maxTime) * (1000 - paddingLeft - paddingRight);
              const width =
                (item.duration / maxTime) * (1000 - paddingLeft - paddingRight);
              const isIdle = item.is_idle;
              const bgColor = isIdle ? '#FFFFFF' : colorMap.get(item.task_id) || '#2563EB';
              const textColor = isIdle ? '#111111' : '#FFFFFF';
              const label = isIdle
                ? `Idle [${item.start_time}-${item.end_time}]`
                : `${item.task_id} [${item.start_time}-${item.end_time}]`;

              return (
                <g
                  key={`${item.task_id}-${item.start_time}-${idx}`}
                  className="cursor-pointer transition-opacity hover:opacity-90"
                  onMouseEnter={() => setHoveredSlice(item)}
                >
                  <rect
                    x={startX}
                    y={paddingTop}
                    width={Math.max(width, 2)}
                    height={barHeight}
                    fill={bgColor}
                    stroke="#111111"
                    strokeWidth="1.5"
                  />
                  {width > 28 && (
                    <text
                      x={startX + width / 2}
                      y={paddingTop + barHeight / 2 + 4}
                      textAnchor="middle"
                      fill={textColor}
                      className="text-[11px] font-medium pointer-events-none select-none font-sans"
                    >
                      {width > 55 ? label : item.task_id}
                    </text>
                  )}
                </g>
              );
            })}
          </svg>
        </div>
      </div>

      {/* Hover Tooltip */}
      {hoveredSlice && (
        <div
          className="absolute z-20 pointer-events-none bg-neutral-900 text-white text-xs px-3 py-2 rounded shadow-lg border border-neutral-700"
          style={{
            left: `${Math.min(Math.max(mousePos.x + 10, 10), 500)}px`,
            top: `${Math.max(mousePos.y - 65, 10)}px`,
          }}
        >
          <div className="font-bold text-blue-300">
            {hoveredSlice.is_idle ? 'CPU Idle' : `Task ${hoveredSlice.task_id}`}
          </div>
          <div>Start Time: {hoveredSlice.start_time}</div>
          <div>End Time: {hoveredSlice.end_time}</div>
          <div>Duration: {hoveredSlice.duration} units</div>
          {!hoveredSlice.is_idle && (
            <div>Remaining after slice: {hoveredSlice.remaining_time} units</div>
          )}
        </div>
      )}
    </div>
  );
};
