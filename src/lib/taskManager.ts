import { Task } from '../types';

export function generateSampleTasks(): Task[] {
  const sampleDefinitions = [
    { task_id: 'T1', arrival_time: 0, burst_time: 5 },
    { task_id: 'T2', arrival_time: 1, burst_time: 3 },
    { task_id: 'T3', arrival_time: 2, burst_time: 8 },
    { task_id: 'T4', arrival_time: 3, burst_time: 2 },
  ];

  return sampleDefinitions.map((item) => ({
    task_id: item.task_id,
    arrival_time: item.arrival_time,
    burst_time: item.burst_time,
    remaining_time: item.burst_time,
    status: 'Waiting',
    assigned_node: null,
  }));
}

export function validateTasks(tasks: Task[]): void {
  if (!Array.isArray(tasks)) {
    throw new TypeError(`Tasks collection must be an array, got ${typeof tasks}.`);
  }
  const seenIds = new Set<string>();

  for (let index = 0; index < tasks.length; index++) {
    const task = tasks[index];
    if (typeof task !== 'object' || task === null) {
      throw new TypeError(`Task at index ${index} must be an object, got ${typeof task}.`);
    }
    if (!('task_id' in task)) {
      throw new Error(`Task at index ${index} is missing required field 'task_id'.`);
    }
    const taskId = String(task.task_id);
    if (!taskId.trim()) {
      throw new Error(`Task at index ${index} 'task_id' cannot be empty or whitespace.`);
    }
    if (seenIds.has(taskId)) {
      throw new Error(`Duplicate task_id '${taskId}' detected at index ${index}.`);
    }
    seenIds.add(taskId);

    if (!('arrival_time' in task)) {
      throw new Error(`Task '${taskId}' at index ${index} is missing required field 'arrival_time'.`);
    }
    const arrivalTime = Number(task.arrival_time);
    if (isNaN(arrivalTime) || !Number.isInteger(arrivalTime)) {
      throw new TypeError(`Task '${taskId}' 'arrival_time' must be an integer, got ${task.arrival_time}.`);
    }
    if (arrivalTime < 0) {
      throw new Error(`Task '${taskId}' 'arrival_time' must be non-negative (>= 0), got ${arrivalTime}.`);
    }

    if (!('burst_time' in task)) {
      throw new Error(`Task '${taskId}' at index ${index} is missing required field 'burst_time'.`);
    }
    const burstTime = Number(task.burst_time);
    if (isNaN(burstTime) || !Number.isInteger(burstTime)) {
      throw new TypeError(`Task '${taskId}' 'burst_time' must be an integer, got ${task.burst_time}.`);
    }
    if (burstTime <= 0) {
      throw new Error(`Task '${taskId}' 'burst_time' must be a positive integer (> 0), got ${burstTime}.`);
    }
  }
}

export function prepareTasks(tasks: Task[]): Task[] {
  validateTasks(tasks);
  return tasks.map((item) => ({
    ...item,
    remaining_time: item.burst_time,
    status: 'Waiting',
    assigned_node: null,
  }));
}
