import { Task, ScheduleSlice, TaskMetric } from '../../types';
import { prepareTasks } from '../taskManager';

export function fcfsSchedule(
  tasks: Task[]
): { slices: ScheduleSlice[]; metrics: Record<string, TaskMetric> } {
  const prepared = prepareTasks(tasks);
  const scheduleSlices: ScheduleSlice[] = [];
  const taskMetrics: Record<string, TaskMetric> = {};

  if (!prepared.length) {
    return { slices: scheduleSlices, metrics: taskMetrics };
  }

  const unarrived = [...prepared].sort((a, b) => {
    if (a.arrival_time !== b.arrival_time) {
      return a.arrival_time - b.arrival_time;
    }
    return String(a.task_id).localeCompare(String(b.task_id));
  });

  let currentTime = 0;
  const readyQueue: Task[] = [];

  const admitArrived = () => {
    while (unarrived.length > 0 && unarrived[0].arrival_time <= currentTime) {
      readyQueue.push(unarrived.shift()!);
    }
    readyQueue.sort((a, b) => {
      if (a.arrival_time !== b.arrival_time) {
        return a.arrival_time - b.arrival_time;
      }
      return String(a.task_id).localeCompare(String(b.task_id));
    });
  };

  admitArrived();

  while (readyQueue.length > 0 || unarrived.length > 0) {
    if (readyQueue.length === 0) {
      currentTime = unarrived[0].arrival_time;
      admitArrived();
    }

    const currentTask = readyQueue.shift()!;
    const startTime = currentTime;
    const duration = currentTask.burst_time;
    currentTime += duration;
    const completionTime = currentTime;
    const turnaroundTime = completionTime - currentTask.arrival_time;
    const waitingTime = turnaroundTime - currentTask.burst_time;

    const sliceRecord: ScheduleSlice = {
      task_id: currentTask.task_id,
      start_time: startTime,
      end_time: completionTime,
      duration: duration,
      remaining_time: 0,
      completed: true,
    };
    scheduleSlices.push(sliceRecord);

    taskMetrics[currentTask.task_id] = {
      task_id: currentTask.task_id,
      arrival_time: currentTask.arrival_time,
      burst_time: currentTask.burst_time,
      completion_time: completionTime,
      turnaround_time: turnaroundTime,
      waiting_time: waitingTime,
    };

    admitArrived();
  }

  return { slices: scheduleSlices, metrics: taskMetrics };
}
