import { Task, ScheduleSlice, TaskMetric } from '../../types';
import { prepareTasks } from '../taskManager';

export function roundRobinSchedule(
  tasks: Task[],
  timeQuantum: number = 2
): { slices: ScheduleSlice[]; metrics: Record<string, TaskMetric> } {
  if (typeof timeQuantum !== 'number' || isNaN(timeQuantum) || !Number.isInteger(timeQuantum)) {
    throw new TypeError(`time_quantum must be an integer, got ${timeQuantum}.`);
  }
  if (timeQuantum <= 0) {
    throw new Error(`time_quantum must be a positive integer (> 0), got ${timeQuantum}.`);
  }

  const prepared = prepareTasks(tasks);
  const scheduleSlices: ScheduleSlice[] = [];
  const taskMetrics: Record<string, TaskMetric> = {};

  if (!prepared.length) {
    return { slices: scheduleSlices, metrics: taskMetrics };
  }

  prepared.forEach((task, idx) => {
    task._order = idx;
  });

  const unarrived = [...prepared].sort((a, b) => {
    if (a.arrival_time !== b.arrival_time) {
      return a.arrival_time - b.arrival_time;
    }
    return (a._order ?? 0) - (b._order ?? 0);
  });

  let currentTime = 0;
  const readyQueue: Task[] = [];
  let completedCount = 0;
  const totalTasks = prepared.length;

  const admitArrived = () => {
    while (unarrived.length > 0 && unarrived[0].arrival_time <= currentTime) {
      readyQueue.push(unarrived.shift()!);
    }
  };

  admitArrived();

  while (completedCount < totalTasks) {
    if (readyQueue.length === 0) {
      if (unarrived.length > 0) {
        currentTime = unarrived[0].arrival_time;
        admitArrived();
      } else {
        break;
      }
    }

    const currentTask = readyQueue.shift()!;
    const startTime = currentTime;
    const remaining = currentTask.remaining_time ?? currentTask.burst_time;
    const execDuration = Math.min(timeQuantum, remaining);

    currentTime += execDuration;
    currentTask.remaining_time = remaining - execDuration;
    const isCompleted = currentTask.remaining_time === 0;

    const sliceRecord: ScheduleSlice = {
      task_id: currentTask.task_id,
      start_time: startTime,
      end_time: currentTime,
      duration: execDuration,
      remaining_time: currentTask.remaining_time,
      completed: isCompleted,
    };
    scheduleSlices.push(sliceRecord);

    admitArrived();

    if (isCompleted) {
      completedCount++;
      const completionTime = currentTime;
      const turnaroundTime = completionTime - currentTask.arrival_time;
      const waitingTime = turnaroundTime - currentTask.burst_time;

      taskMetrics[currentTask.task_id] = {
        task_id: currentTask.task_id,
        arrival_time: currentTask.arrival_time,
        burst_time: currentTask.burst_time,
        completion_time: completionTime,
        turnaround_time: turnaroundTime,
        waiting_time: waitingTime,
      };
    } else {
      readyQueue.push(currentTask);
    }
  }

  return { slices: scheduleSlices, metrics: taskMetrics };
}
