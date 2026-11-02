#!/usr/bin/env python3
"""
Distributed Load Balancer Simulator - Web Application
Pure Python web server running on port 3000 using standard library http.server.
Requires zero external pip dependencies.
"""

import json
import os
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from metrics import calculate_metrics_summary, identify_idle_intervals, run_algorithm_comparison
from node_simulator import simulate_cluster
from schedulers.fcfs import fcfs_schedule
from schedulers.round_robin import round_robin_schedule
from schedulers.sjf import sjf_schedule
from task_manager import generate_sample_tasks, validate_tasks

HOST = "localhost"
PORT = 3000

HTML_PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Distributed Load Balancer Simulator</title>
  <meta name="description" content="Interactive CPU task scheduling and load balancing simulator in Python supporting Round Robin, FCFS, and SJF with Gantt charts and performance metrics." />
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body {
      background-color: #ffffff;
      color: #111111;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    .best-badge {
      background-color: #EFF6FF;
      color: #1D4ED8;
      border: 1px solid #2563EB;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 0.75rem;
      font-weight: 600;
    }
  </style>
</head>
<body class="min-h-screen flex flex-col antialiased">

  <!-- Constant Top Navigation Bar for Whole Website -->
  <header class="sticky top-0 z-50 bg-white/95 backdrop-blur-sm border-b border-neutral-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 h-14 flex items-center justify-between gap-6">
      <div class="flex items-center gap-2 shrink-0">
        <button onclick="navigateTo('landing')" class="flex items-center gap-2 text-sm sm:text-base font-bold tracking-tight text-neutral-900 hover:text-blue-600 transition-colors text-left cursor-pointer">
          <span class="w-2 h-2 rounded-full bg-blue-600"></span>
          <span>Distributed Load Balancer Simulator</span>
        </button>
      </div>

      <nav class="hidden md:flex items-center gap-1 lg:gap-2 text-xs font-semibold">
        <button id="nav-btn-landing" onclick="navigateTo('landing')" class="px-3 py-1.5 rounded transition-colors whitespace-nowrap bg-neutral-100 text-neutral-900 font-bold cursor-pointer">
          Overview
        </button>
        <button id="nav-btn-single" onclick="navigateTo('dashboard', 'Individual Simulation')" class="px-3 py-1.5 rounded transition-colors whitespace-nowrap text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50 cursor-pointer">
          Simulation
        </button>
        <button id="nav-btn-comp" onclick="navigateTo('dashboard', 'Algorithm Comparison')" class="px-3 py-1.5 rounded transition-colors whitespace-nowrap text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50 cursor-pointer">
          Algorithm Comparison
        </button>
        <button id="nav-btn-cluster" onclick="navigateTo('dashboard', 'Multi-Node Cluster (Stage 3)')" style="visibility: hidden; pointer-events: none;" class="px-3 py-1.5 rounded transition-colors whitespace-nowrap text-neutral-600 cursor-default" tabindex="-1" aria-hidden="true">
          Cluster Balancer
        </button>
      </nav>

      <div class="flex items-center gap-2 shrink-0">
        <button id="top-action-btn" onclick="navigateTo('dashboard', 'Individual Simulation')" class="px-3.5 py-1.5 text-xs font-bold text-white bg-blue-600 hover:bg-blue-700 rounded transition-colors shadow-sm cursor-pointer">
          Launch Simulator &rarr;
        </button>
      </div>
    </div>
  </header>

  <!-- VIEW 1: LANDING PAGE -->
  <main id="view-landing" class="flex-1">
    <!-- Hero Section -->
    <section class="max-w-7xl mx-auto px-6 pt-12 md:pt-16 pb-14 w-full">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-center">
        <div class="lg:col-span-7 space-y-6">
          <div class="text-xs font-semibold uppercase tracking-wider text-blue-700 flex items-center gap-2">
            <span class="w-1.5 h-1.5 bg-blue-600 rounded-full"></span>
            <span>Operating Systems Task Scheduling &amp; Cluster Load Balancing</span>
          </div>

          <h1 class="text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight text-neutral-900 leading-[1.15]">
            Distributed CPU Scheduling
          </h1>

          <p class="text-sm md:text-base text-neutral-600 leading-relaxed max-w-2xl">
            A pure Python simulation platform for exploring preemptive Round Robin, deterministic First-Come First-Served, and Shortest Job First scheduling alongside multi-node cluster load balancing.
          </p>

          <div class="flex flex-wrap items-center gap-3 pt-2">
            <button onclick="navigateTo('dashboard', 'Individual Simulation')" class="px-5 py-2.5 text-xs font-bold text-white bg-blue-600 hover:bg-blue-700 rounded transition-colors cursor-pointer shadow-sm">
              &#9654; Launch Simulator Dashboard
            </button>
            <button onclick="navigateTo('dashboard', 'Algorithm Comparison')" class="px-5 py-2.5 text-xs font-bold text-neutral-900 bg-white hover:bg-neutral-50 border border-neutral-900 rounded transition-colors cursor-pointer">
              Compare RR vs FCFS vs SJF
            </button>
            <button onclick="navigateTo('dashboard', 'Multi-Node Cluster (Stage 3)')" class="px-5 py-2.5 text-xs font-bold text-neutral-900 bg-neutral-100 hover:bg-neutral-200 border border-neutral-300 rounded transition-colors cursor-pointer">
              Cluster Balancer (Stage 3)
            </button>
          </div>

          <div class="pt-6"></div>
        </div>

        <div class="lg:col-span-5" aria-hidden="true">
        </div>
      </div>
    </section>

    <!-- Algorithms Section -->
    <section class="max-w-7xl mx-auto px-6 py-14 border-t border-neutral-200 space-y-8">
      <div>
        <span className="text-xs font-bold uppercase tracking-wider text-blue-700">Supported Schedulers</span>
        <h2 class="text-2xl font-bold text-neutral-900 mt-1">CPU Scheduling Algorithms</h2>
        <p class="text-xs text-neutral-600">Deterministic implementations modeling preemptive time-slicing and queue heuristics.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="border border-neutral-900 rounded p-5 bg-white flex flex-col justify-between">
          <div class="space-y-3">
            <span class="text-xs font-mono font-bold text-blue-600">01. PREEMPTIVE</span>
            <h3 class="text-base font-bold text-neutral-900">Round Robin (RR)</h3>
            <p class="text-xs text-neutral-600 leading-relaxed">
              Allocates CPU time in discrete time quanta ($q$). Tasks not finished return to the circular FIFO ready queue, preventing CPU starvation and ensuring fairness.
            </p>
          </div>
          <button onclick="loadAlgoAndGo('Round Robin (RR)')" class="mt-5 w-full py-2 px-3 text-xs font-semibold bg-white hover:bg-neutral-50 text-neutral-900 border border-neutral-900 rounded cursor-pointer">
            Simulate Round Robin &rarr;
          </button>
        </div>

        <div class="border border-neutral-900 rounded p-5 bg-white flex flex-col justify-between">
          <div class="space-y-3">
            <span class="text-xs font-mono font-bold text-blue-600">02. NON-PREEMPTIVE</span>
            <h3 class="text-base font-bold text-neutral-900">First-Come, First-Served (FCFS)</h3>
            <p class="text-xs text-neutral-600 leading-relaxed">
              Dispatches jobs in arrival time order. Once execution begins, the task runs to full completion without preemption. Ties resolved deterministically by Task ID.
            </p>
          </div>
          <button onclick="loadAlgoAndGo('First Come, First Served (FCFS)')" class="mt-5 w-full py-2 px-3 text-xs font-semibold bg-white hover:bg-neutral-50 text-neutral-900 border border-neutral-900 rounded cursor-pointer">
            Simulate FCFS &rarr;
          </button>
        </div>

        <div class="border border-neutral-900 rounded p-5 bg-white flex flex-col justify-between">
          <div class="space-y-3">
            <span class="text-xs font-mono font-bold text-blue-600">03. OPTIMIZED</span>
            <h3 class="text-base font-bold text-neutral-900">Shortest Job First (SJF)</h3>
            <p class="text-xs text-neutral-600 leading-relaxed">
              At each decision point, selects the arrived task with minimal burst time. Proven to achieve minimum average waiting time among non-preemptive schedulers.
            </p>
          </div>
          <button onclick="loadAlgoAndGo('Shortest Job First (SJF — Non-Preemptive)')" class="mt-5 w-full py-2 px-3 text-xs font-semibold bg-white hover:bg-neutral-50 text-neutral-900 border border-neutral-900 rounded cursor-pointer">
            Simulate SJF &rarr;
          </button>
        </div>
      </div>
    </section>

    <!-- Presets Section (blank) -->
    <section class="py-14"></section>
  </main>

  <!-- VIEW 2: DASHBOARD WORKSPACE -->
  <main id="view-dashboard" class="flex-1 hidden flex flex-col md:flex-row">
    <!-- Sidebar -->
    <aside class="w-full md:w-80 bg-neutral-50 border-r border-neutral-300 p-5 flex flex-col justify-between shrink-0 font-sans">
      <div class="space-y-6">
        <div>
          <div class="flex items-center justify-between mb-3">
            <h2 class="text-xs font-bold uppercase tracking-wider text-neutral-900">Navigation</h2>
            <button onclick="navigateTo('landing')" class="text-[11px] font-semibold text-blue-600 hover:text-blue-800 cursor-pointer">
              Landing Page &rarr;
            </button>
          </div>
          <div class="space-y-1.5 text-xs">
            <button id="side-btn-single" onclick="setDashboardMode('Individual Simulation')" class="w-full px-3 py-2 rounded text-left font-semibold border bg-blue-600 text-white border-blue-600 cursor-pointer">
              Individual Simulation
            </button>
            <button id="side-btn-comp" onclick="setDashboardMode('Algorithm Comparison')" class="w-full px-3 py-2 rounded text-left font-semibold border bg-white text-neutral-800 border-neutral-300 hover:border-neutral-900 cursor-pointer">
              Algorithm Comparison
            </button>
            <button id="side-btn-cluster" onclick="setDashboardMode('Multi-Node Cluster (Stage 3)')" class="w-full px-3 py-2 rounded text-left font-semibold border bg-white text-neutral-800 border-neutral-300 hover:border-neutral-900 cursor-pointer">
              Multi-Node Cluster (Stage 3)
            </button>
          </div>
        </div>

        <hr class="border-neutral-200" />

        <!-- Controls -->
        <div>
          <h2 class="text-xs font-bold uppercase tracking-wider text-neutral-900 mb-3">Controls</h2>
          <div id="controls-single" class="space-y-4 text-xs">
            <div>
              <label class="block font-semibold text-neutral-700 mb-1">Scheduling Algorithm</label>
              <select id="select-algo" onchange="onAlgoChange()" class="w-full px-3 py-2 bg-white border border-neutral-900 rounded font-medium cursor-pointer">
                <option value="Round Robin (RR)">Round Robin (RR)</option>
                <option value="First Come, First Served (FCFS)">First Come, First Served (FCFS)</option>
                <option value="Shortest Job First (SJF — Non-Preemptive)">Shortest Job First (SJF — Non-Preemptive)</option>
              </select>
            </div>
            <div id="rr-quantum-block">
              <label class="block font-semibold text-neutral-700 mb-1">Time Quantum (q)</label>
              <input id="input-quantum" type="number" min="1" max="100" value="2" class="w-full px-3 py-2 bg-white border border-neutral-900 rounded font-mono" />
            </div>
          </div>

          <div id="controls-comp" class="space-y-4 text-xs hidden">
            <div>
              <label class="block font-semibold text-neutral-700 mb-1">Round Robin Quantum (q)</label>
              <input id="input-comp-quantum" type="number" min="1" max="100" value="2" class="w-full px-3 py-2 bg-white border border-neutral-900 rounded font-mono" />
            </div>
          </div>

          <div id="controls-cluster" class="space-y-4 text-xs hidden">
            <div>
              <label class="block font-semibold text-neutral-700 mb-1">Cluster Size (Nodes)</label>
              <select id="select-cluster-nodes" class="w-full px-3 py-2 bg-white border border-neutral-900 rounded font-medium">
                <option value="2">2 Nodes</option>
                <option value="3" selected>3 Nodes</option>
                <option value="4">4 Nodes</option>
                <option value="5">5 Nodes</option>
              </select>
            </div>
            <div>
              <label class="block font-semibold text-neutral-700 mb-1">Balancing Policy</label>
              <select id="select-cluster-policy" class="w-full px-3 py-2 bg-white border border-neutral-900 rounded font-medium">
                <option value="Least Loaded" selected>Least Loaded (Min Workload)</option>
                <option value="Round Robin">Round Robin Allocation</option>
                <option value="Random">Hash/Random Distribution</option>
              </select>
            </div>
          </div>

          <div class="mt-5 space-y-2">
            <button onclick="executeCurrentSimulation()" class="w-full py-2.5 px-4 bg-blue-600 hover:bg-blue-700 text-white rounded text-xs font-bold shadow-sm cursor-pointer">
              &#9654; Run Simulation
            </button>
            <div class="grid grid-cols-2 gap-2 text-xs">
              <button onclick="loadSampleTasks()" class="py-2 px-3 bg-white hover:bg-neutral-100 text-neutral-900 border border-neutral-900 rounded font-semibold cursor-pointer">
                Load Sample
              </button>
              <button onclick="resetTasks()" class="py-2 px-3 bg-white hover:bg-neutral-100 text-neutral-900 border border-neutral-900 rounded font-semibold cursor-pointer">
                Reset
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="pt-6 border-t border-neutral-200 text-center text-[11px] text-neutral-500">
        Pure Python OS Scheduling Simulator
      </div>
    </aside>

    <!-- Workspace Main Content -->
    <div class="flex-1 p-6 md:p-8 max-w-7xl overflow-y-auto space-y-6">
      <header class="border-b border-neutral-900 pb-3 flex flex-wrap items-center justify-between gap-2">
        <div>
          <h1 class="text-2xl font-bold text-neutral-900 tracking-tight">Distributed Load Balancer Simulator</h1>
          <p id="dash-subtitle" class="text-xs text-neutral-600 mt-1">Single-node CPU scheduling and performance analysis</p>
        </div>
        <button onclick="navigateTo('landing')" class="px-3 py-1.5 bg-white hover:bg-neutral-100 text-neutral-800 border border-neutral-300 rounded text-xs font-semibold cursor-pointer">
          Home / Landing Page
        </button>
      </header>

      <!-- Algorithm info banner -->
      <div id="algo-info-banner" class="bg-blue-50 border border-blue-200 rounded p-3 text-xs text-blue-900"></div>

      <!-- Workload Configuration Editor -->
      <div class="bg-white border border-neutral-900 rounded p-4">
        <div class="flex flex-wrap items-center justify-between gap-3 mb-3">
          <div>
            <h2 class="text-sm font-semibold uppercase tracking-wider text-neutral-800">Workload Configuration</h2>
            <p class="text-xs text-neutral-500">Configure arrival times and burst requirements</p>
          </div>
          <div class="flex items-center gap-2">
            <button onclick="addNewTaskRow()" class="px-3 py-1 bg-white hover:bg-neutral-50 border border-neutral-900 rounded text-xs font-semibold cursor-pointer">
              + Add Task
            </button>
          </div>
        </div>
        <div class="overflow-x-auto border border-neutral-300 rounded">
          <table class="w-full text-left text-xs">
            <thead class="bg-neutral-100 border-b border-neutral-300 text-neutral-700 font-semibold uppercase">
              <tr>
                <th class="py-2.5 px-3 w-16">#</th>
                <th class="py-2.5 px-3">Task ID</th>
                <th class="py-2.5 px-3">Arrival Time (&ge; 0)</th>
                <th class="py-2.5 px-3">Burst Time (&gt; 0)</th>
                <th class="py-2.5 px-3 text-right w-20">Action</th>
              </tr>
            </thead>
            <tbody id="task-table-body" class="divide-y divide-neutral-200 font-mono"></tbody>
          </table>
        </div>
      </div>

      <!-- Workspace Results Area -->
      <div id="results-container"></div>
    </div>
  </main>

  <footer class="bg-white border-t border-neutral-200 py-6 px-6 text-xs text-neutral-500">
    <div class="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-4">
      <div>
        <div class="font-bold text-neutral-800">Distributed Load Balancer Simulator</div>
        <div class="text-[11px]">100% Python Engine · Port 3000</div>
      </div>
      <div class="flex items-center gap-6">
        <button onclick="navigateTo('landing')" class="hover:text-neutral-900 cursor-pointer">Overview</button>
        <button onclick="navigateTo('dashboard', 'Individual Simulation')" class="hover:text-neutral-900 cursor-pointer">Simulation</button>
        <button onclick="navigateTo('dashboard', 'Algorithm Comparison')" class="hover:text-neutral-900 cursor-pointer">Comparison</button>
        <button onclick="navigateTo('dashboard', 'Multi-Node Cluster (Stage 3)')" style="visibility: hidden; pointer-events: none;" class="cursor-default" tabindex="-1" aria-hidden="true">Cluster Balancer</button>
      </div>
    </div>
  </footer>

  <!-- Application Logic (Interacting directly with Python endpoints) -->
  <script>
    let currentTasks = [
      { task_id: 'T1', arrival_time: 0, burst_time: 5 },
      { task_id: 'T2', arrival_time: 1, burst_time: 3 },
      { task_id: 'T3', arrival_time: 2, burst_time: 8 },
      { task_id: 'T4', arrival_time: 3, burst_time: 2 }
    ];
    let currentMode = 'Individual Simulation';

    function renderTaskTable() {
      const tbody = document.getElementById('task-table-body');
      tbody.innerHTML = '';
      currentTasks.forEach((t, i) => {
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-neutral-50';
        tr.innerHTML = `
          <td class="py-2 px-3 text-neutral-400 font-mono">${i + 1}</td>
          <td class="py-2 px-3">
            <input type="text" value="${t.task_id}" onchange="updateTask(${i}, 'task_id', this.value)" class="w-full px-2 py-1 border border-neutral-300 rounded font-bold font-mono text-xs focus:outline-none" />
          </td>
          <td class="py-2 px-3">
            <input type="number" min="0" value="${t.arrival_time}" onchange="updateTask(${i}, 'arrival_time', this.value)" class="w-full px-2 py-1 border border-neutral-300 rounded font-mono text-xs focus:outline-none" />
          </td>
          <td class="py-2 px-3">
            <input type="number" min="1" value="${t.burst_time}" onchange="updateTask(${i}, 'burst_time', this.value)" class="w-full px-2 py-1 border border-neutral-300 rounded font-mono text-xs focus:outline-none" />
          </td>
          <td class="py-2 px-3 text-right">
            <button onclick="removeTask(${i})" class="text-neutral-400 hover:text-red-600 cursor-pointer font-sans text-sm">&times;</button>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    function updateTask(index, field, value) {
      if (field === 'task_id') {
        currentTasks[index].task_id = value;
      } else {
        currentTasks[index][field] = Math.max(0, parseInt(value, 10) || 0);
      }
    }

    function addNewTaskRow() {
      currentTasks.push({
        task_id: 'T' + (currentTasks.length + 1),
        arrival_time: currentTasks.length > 0 ? Math.max(...currentTasks.map(t => t.arrival_time)) + 1 : 0,
        burst_time: 3
      });
      renderTaskTable();
    }

    function removeTask(index) {
      if (currentTasks.length > 1) {
        currentTasks.splice(index, 1);
        renderTaskTable();
      }
    }

    function loadSampleTasks() {
      currentTasks = [
        { task_id: 'T1', arrival_time: 0, burst_time: 5 },
        { task_id: 'T2', arrival_time: 1, burst_time: 3 },
        { task_id: 'T3', arrival_time: 2, burst_time: 8 },
        { task_id: 'T4', arrival_time: 3, burst_time: 2 }
      ];
      renderTaskTable();
      executeCurrentSimulation();
    }

    function resetTasks() {
      loadSampleTasks();
    }

    function navigateTo(view, mode) {
      if (view === 'landing') {
        document.getElementById('view-landing').classList.remove('hidden');
        document.getElementById('view-dashboard').classList.add('hidden');
        document.getElementById('nav-btn-landing').className = 'px-3 py-1.5 rounded transition-colors whitespace-nowrap bg-neutral-100 text-neutral-900 font-bold cursor-pointer';
        document.getElementById('nav-btn-single').className = 'px-3 py-1.5 rounded transition-colors whitespace-nowrap text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50 cursor-pointer';
        document.getElementById('nav-btn-comp').className = 'px-3 py-1.5 rounded transition-colors whitespace-nowrap text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50 cursor-pointer';
        document.getElementById('nav-btn-cluster').className = 'px-3 py-1.5 rounded transition-colors whitespace-nowrap text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50 cursor-pointer';
        window.scrollTo({ top: 0, behavior: 'smooth' });
      } else {
        document.getElementById('view-landing').classList.add('hidden');
        document.getElementById('view-dashboard').classList.remove('hidden');
        renderTaskTable();
        if (mode) setDashboardMode(mode);
        else executeCurrentSimulation();
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    }

    function loadAlgoAndGo(algo) {
      document.getElementById('select-algo').value = algo;
      onAlgoChange();
      navigateTo('dashboard', 'Individual Simulation');
    }

    function loadPresetAndGo(preset) {
      if (preset === 'staggered') {
        currentTasks = [
          { task_id: 'T1', arrival_time: 0, burst_time: 4 },
          { task_id: 'T2', arrival_time: 3, burst_time: 2 },
          { task_id: 'T3', arrival_time: 7, burst_time: 5 },
          { task_id: 'T4', arrival_time: 14, burst_time: 3 }
        ];
      } else if (preset === 'high_variance') {
        currentTasks = [
          { task_id: 'T1', arrival_time: 0, burst_time: 12 },
          { task_id: 'T2', arrival_time: 1, burst_time: 1 },
          { task_id: 'T3', arrival_time: 2, burst_time: 14 },
          { task_id: 'T4', arrival_time: 3, burst_time: 2 }
        ];
      } else if (preset === 'idle_gaps') {
        currentTasks = [
          { task_id: 'T1', arrival_time: 3, burst_time: 3 },
          { task_id: 'T2', arrival_time: 9, burst_time: 4 },
          { task_id: 'T3', arrival_time: 17, burst_time: 2 }
        ];
      } else {
        loadSampleTasks();
      }
      renderTaskTable();
      navigateTo('dashboard', 'Individual Simulation');
    }

    function onAlgoChange() {
      const algo = document.getElementById('select-algo').value;
      const rrBlock = document.getElementById('rr-quantum-block');
      if (algo === 'Round Robin (RR)') {
        rrBlock.classList.remove('hidden');
      } else {
        rrBlock.classList.add('hidden');
      }
      executeCurrentSimulation();
    }

    function setDashboardMode(mode) {
      currentMode = mode;
      document.getElementById('controls-single').classList.add('hidden');
      document.getElementById('controls-comp').classList.add('hidden');
      document.getElementById('controls-cluster').classList.add('hidden');

      document.getElementById('side-btn-single').className = 'w-full px-3 py-2 rounded text-left font-semibold border bg-white text-neutral-800 border-neutral-300 hover:border-neutral-900 cursor-pointer';
      document.getElementById('side-btn-comp').className = 'w-full px-3 py-2 rounded text-left font-semibold border bg-white text-neutral-800 border-neutral-300 hover:border-neutral-900 cursor-pointer';
      document.getElementById('side-btn-cluster').className = 'w-full px-3 py-2 rounded text-left font-semibold border bg-white text-neutral-800 border-neutral-300 hover:border-neutral-900 cursor-pointer';

      const banner = document.getElementById('algo-info-banner');

      if (mode === 'Individual Simulation') {
        document.getElementById('controls-single').classList.remove('hidden');
        document.getElementById('side-btn-single').className = 'w-full px-3 py-2 rounded text-left font-semibold border bg-blue-600 text-white border-blue-600 cursor-pointer';
        document.getElementById('dash-subtitle').innerText = 'Single-node CPU scheduling and performance analysis';
        banner.innerHTML = '<strong>Simulation:</strong> Run Round Robin, FCFS, or SJF and inspect execution slices, idle periods, and waiting times.';
      } else if (mode === 'Algorithm Comparison') {
        document.getElementById('controls-comp').classList.remove('hidden');
        document.getElementById('side-btn-comp').className = 'w-full px-3 py-2 rounded text-left font-semibold border bg-blue-600 text-white border-blue-600 cursor-pointer';
        document.getElementById('dash-subtitle').innerText = 'Multi-algorithm side-by-side performance benchmarking';
        banner.innerHTML = '<strong>Algorithm Comparison:</strong> Evaluates Round Robin, FCFS, and SJF against the exact same workload to determine optimal scheduling.';
      } else {
        document.getElementById('controls-cluster').classList.remove('hidden');
        document.getElementById('side-btn-cluster').className = 'w-full px-3 py-2 rounded text-left font-semibold border bg-blue-600 text-white border-blue-600 cursor-pointer';
        document.getElementById('dash-subtitle').innerText = 'Multi-node cluster load balancing simulation';
        banner.innerHTML = '<strong>Cluster Balancer:</strong> Dispatches tasks across N compute worker nodes using Least Loaded or Round Robin policies.';
      }
      executeCurrentSimulation();
    }

    async function executeCurrentSimulation() {
      const container = document.getElementById('results-container');
      container.innerHTML = '<div class="text-neutral-500 text-xs py-4">Running simulation in Python...</div>';

      try {
        if (currentMode === 'Individual Simulation') {
          const algo = document.getElementById('select-algo').value;
          const q = parseInt(document.getElementById('input-quantum').value, 10) || 2;
          const res = await fetch('/api/simulate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ tasks: currentTasks, algorithm: algo, time_quantum: q })
          });
          const data = await res.json();
          renderSingleResults(data, algo);
        } else if (currentMode === 'Algorithm Comparison') {
          const q = parseInt(document.getElementById('input-comp-quantum').value, 10) || 2;
          const res = await fetch('/api/compare', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ tasks: currentTasks, time_quantum: q })
          });
          const data = await res.json();
          renderComparisonResults(data);
        } else {
          const nodes = parseInt(document.getElementById('select-cluster-nodes').value, 10) || 3;
          const policy = document.getElementById('select-cluster-policy').value;
          const res = await fetch('/api/cluster', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ tasks: currentTasks, node_count: nodes, policy: policy })
          });
          const data = await res.json();
          renderClusterResults(data);
        }
      } catch (err) {
        container.innerHTML = `<div class="p-3 bg-red-50 border border-red-500 text-red-700 text-xs rounded">Error running simulation: ${err.message}</div>`;
      }
    }

    function renderGanttSvg(slices, makespan, idleIntervals) {
      const allSlices = [
        ...slices.map(s => ({ ...s, is_idle: false })),
        ...(idleIntervals || []).map(s => ({ ...s, is_idle: true }))
      ].sort((a, b) => a.start_time - b.start_time);

      const maxTime = Math.max(makespan, 1);
      const width = 800;
      const height = 110;
      const padLeft = 40;
      const padRight = 20;
      const barY = 25;
      const barH = 40;
      const usableW = width - padLeft - padRight;

      const colors = ['#2563EB', '#1D4ED8', '#3B82F6', '#60A5FA', '#1E40AF', '#93C5FD'];
      const uniqueTasks = Array.from(new Set(slices.map(s => s.task_id)));
      const colorMap = {};
      uniqueTasks.forEach((t, i) => colorMap[t] = colors[i % colors.length]);

      let svg = `<svg viewBox="0 0 ${width} ${height}" class="w-full h-auto select-none font-sans">`;
      // baseline
      svg += `<line x1="${padLeft}" y1="${barY + barH}" x2="${width - padRight}" y2="${barY + barH}" stroke="#111111" stroke-width="1.5" />`;
      svg += `<line x1="${padLeft}" y1="${barY}" x2="${padLeft}" y2="${barY + barH + 6}" stroke="#111111" stroke-width="1.5" />`;

      // ticks
      const step = makespan <= 25 ? 1 : Math.max(1, Math.floor(makespan / 15));
      for (let t = 0; t <= Math.ceil(makespan); t += step) {
        const x = padLeft + (t / maxTime) * usableW;
        svg += `<line x1="${x}" y1="${barY}" x2="${x}" y2="${barY + barH + 6}" stroke="#E5E7EB" stroke-width="1" />`;
        svg += `<text x="${x}" y="${barY + barH + 18}" text-anchor="middle" font-size="10" font-family="monospace" fill="#555">${t}</text>`;
      }

      // slices
      allSlices.forEach(s => {
        const x = padLeft + (s.start_time / maxTime) * usableW;
        const w = Math.max((s.duration / maxTime) * usableW, 2);
        const fill = s.is_idle ? '#FFFFFF' : (colorMap[s.task_id] || '#2563EB');
        const textFill = s.is_idle ? '#111111' : '#FFFFFF';
        const label = s.is_idle ? `Idle [${s.start_time}-${s.end_time}]` : `${s.task_id} [${s.start_time}-${s.end_time}]`;
        svg += `<rect x="${x}" y="${barY}" width="${w}" height="${barH}" fill="${fill}" stroke="#111111" stroke-width="1.5" />`;
        if (w > 25) {
          svg += `<text x="${x + w / 2}" y="${barY + barH / 2 + 4}" text-anchor="middle" fill="${textFill}" font-size="11" font-weight="600">${w > 55 ? label : s.task_id}</text>`;
        }
      });
      svg += `</svg>`;
      return svg;
    }

    function renderSingleResults(data, algo) {
      const summary = data.summary;
      const slices = data.slices;
      const metrics = data.metrics;
      const idle = data.idle_intervals;

      const container = document.getElementById('results-container');
      container.innerHTML = `
        <div class="space-y-6">
          <div>
            <h2 class="text-sm font-semibold uppercase tracking-wider text-neutral-800 pb-1 mb-3 border-b border-neutral-200">Performance Summary</h2>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div class="border border-neutral-900 rounded p-4 bg-white">
                <div class="text-[11px] uppercase tracking-wider text-neutral-500 font-semibold">Tasks Scheduled</div>
                <div class="text-2xl font-bold text-neutral-900 mt-1">${summary.total_tasks}</div>
              </div>
              <div class="border border-neutral-900 rounded p-4 bg-white">
                <div class="text-[11px] uppercase tracking-wider text-neutral-500 font-semibold">Average Waiting Time</div>
                <div class="text-2xl font-bold text-neutral-900 mt-1">${summary.avg_waiting_time.toFixed(2)} <span class="text-xs font-normal text-neutral-500">units</span></div>
              </div>
              <div class="border border-neutral-900 rounded p-4 bg-white">
                <div class="text-[11px] uppercase tracking-wider text-neutral-500 font-semibold">Average Turnaround Time</div>
                <div class="text-2xl font-bold text-neutral-900 mt-1">${summary.avg_turnaround_time.toFixed(2)} <span class="text-xs font-normal text-neutral-500">units</span></div>
              </div>
              <div class="border border-neutral-900 rounded p-4 bg-white">
                <div class="text-[11px] uppercase tracking-wider text-neutral-500 font-semibold">Makespan</div>
                <div class="text-2xl font-bold text-neutral-900 mt-1">${summary.makespan} <span class="text-xs font-normal text-neutral-500">units</span></div>
              </div>
            </div>
          </div>

          <div>
            <h2 class="text-sm font-semibold uppercase tracking-wider text-neutral-800 pb-1 mb-3 border-b border-neutral-200">CPU Execution Timeline (Gantt Chart)</h2>
            <div class="border border-neutral-900 rounded p-4 bg-white">
              ${renderGanttSvg(slices, summary.makespan, idle)}
            </div>
          </div>

          <div>
            <h2 class="text-sm font-semibold uppercase tracking-wider text-neutral-800 pb-1 mb-3 border-b border-neutral-200">Task Performance Metrics</h2>
            <div class="overflow-x-auto border border-neutral-900 rounded bg-white font-mono text-xs">
              <table class="w-full text-left">
                <thead class="bg-neutral-100 border-b border-neutral-900 font-bold font-sans">
                  <tr>
                    <th class="py-2.5 px-3">Task ID</th>
                    <th class="py-2.5 px-3">Arrival</th>
                    <th class="py-2.5 px-3">Burst</th>
                    <th class="py-2.5 px-3">Completion</th>
                    <th class="py-2.5 px-3">Waiting Time</th>
                    <th class="py-2.5 px-3">Turnaround</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-neutral-200">
                  ${Object.values(metrics).map(m => `
                    <tr class="hover:bg-neutral-50">
                      <td class="py-2.5 px-3 font-bold text-blue-600">${m.task_id}</td>
                      <td class="py-2.5 px-3">${m.arrival_time}</td>
                      <td class="py-2.5 px-3">${m.burst_time}</td>
                      <td class="py-2.5 px-3">${m.completion_time}</td>
                      <td class="py-2.5 px-3 font-bold">${m.waiting_time}</td>
                      <td class="py-2.5 px-3">${m.turnaround_time}</td>
                    </tr>
                  `).join('')}
                </tbody>
              </table>
            </div>
          </div>

          <div>
            <h2 class="text-sm font-semibold uppercase tracking-wider text-neutral-800 pb-1 mb-3 border-b border-neutral-200">Chronological Execution Slices (${slices.length} slices)</h2>
            <div class="overflow-x-auto border border-neutral-200 rounded font-mono text-xs">
              <table class="w-full text-left">
                <thead class="bg-neutral-100 border-b border-neutral-300 font-sans">
                  <tr>
                    <th class="py-2 px-3">Slice #</th>
                    <th class="py-2 px-3">Task ID</th>
                    <th class="py-2 px-3">Start</th>
                    <th class="py-2 px-3">End</th>
                    <th class="py-2 px-3">Duration</th>
                    <th class="py-2 px-3">Remaining</th>
                    <th class="py-2 px-3">Status</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-neutral-200">
                  ${slices.map((s, idx) => `
                    <tr class="hover:bg-neutral-50">
                      <td class="py-2 px-3 text-neutral-500">${idx + 1}</td>
                      <td class="py-2 px-3 font-bold text-blue-600">${s.task_id}</td>
                      <td class="py-2 px-3">${s.start_time}</td>
                      <td class="py-2 px-3">${s.end_time}</td>
                      <td class="py-2 px-3">${s.duration}</td>
                      <td class="py-2 px-3">${s.remaining_time}</td>
                      <td class="py-2 px-3 font-sans font-semibold">${s.completed ? '<span class="text-emerald-700">Completed</span>' : '<span class="text-amber-700">Preempted</span>'}</td>
                    </tr>
                  `).join('')}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      `;
    }

    function renderComparisonResults(data) {
      const rows = data.comparison_rows;
      const best = data.best_performers;
      const algos = data.algorithms;

      const container = document.getElementById('results-container');
      container.innerHTML = `
        <div class="space-y-6">
          <div>
            <h2 class="text-sm font-semibold uppercase tracking-wider text-neutral-800 pb-1 mb-3 border-b border-neutral-200">Comparative Performance Overview</h2>
            <div class="overflow-x-auto border border-neutral-900 rounded font-mono text-xs">
              <table class="w-full text-left">
                <thead class="bg-neutral-100 border-b border-neutral-900 font-bold font-sans">
                  <tr>
                    <th class="py-2.5 px-4">Algorithm</th>
                    <th class="py-2.5 px-4">Avg Waiting Time</th>
                    <th class="py-2.5 px-4">Avg Turnaround Time</th>
                    <th class="py-2.5 px-4">Makespan</th>
                    <th class="py-2.5 px-4">CPU Utilization (%)</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-neutral-200">
                  ${rows.map(r => `
                    <tr class="hover:bg-neutral-50">
                      <td class="py-2.5 px-4 font-bold font-sans text-neutral-900">${r.Algorithm}</td>
                      <td class="py-2.5 px-4">${r['Avg Waiting Time'].toFixed(2)} units</td>
                      <td class="py-2.5 px-4">${r['Avg Turnaround Time'].toFixed(2)} units</td>
                      <td class="py-2.5 px-4">${r.Makespan} units</td>
                      <td class="py-2.5 px-4">${r['CPU Utilization (%)'].toFixed(2)}%</td>
                    </tr>
                  `).join('')}
                </tbody>
              </table>
            </div>
          </div>

          <div>
            <h2 class="text-sm font-semibold uppercase tracking-wider text-neutral-800 pb-1 mb-3 border-b border-neutral-200">Automated Summary</h2>
            <div class="bg-neutral-50 border border-neutral-900 rounded p-4 text-xs space-y-2">
              <div><b>Lowest Waiting Time:</b> <span class="best-badge">${best.lowest_waiting.join(', ')}</span></div>
              <div><b>Lowest Turnaround Time:</b> <span class="best-badge">${best.lowest_turnaround.join(', ')}</span></div>
              <div><b>Shortest Makespan:</b> <span class="best-badge">${best.shortest_makespan.join(', ')}</span></div>
              <div><b>Highest CPU Utilization:</b> <span class="best-badge">${best.highest_utilization.join(', ')}</span></div>
            </div>
          </div>

          <div>
            <h2 class="text-sm font-semibold uppercase tracking-wider text-neutral-800 pb-1 mb-3 border-b border-neutral-200">Gantt Comparison</h2>
            <div class="space-y-4">
              <div class="border border-neutral-900 rounded p-4 bg-white">
                <div class="text-xs font-bold mb-2">Round Robin (RR)</div>
                ${renderGanttSvg(algos['Round Robin (RR)'].slices, algos['Round Robin (RR)'].summary.makespan, [])}
              </div>
              <div class="border border-neutral-900 rounded p-4 bg-white">
                <div class="text-xs font-bold mb-2">First-Come, First-Served (FCFS)</div>
                ${renderGanttSvg(algos['First Come, First Served (FCFS)'].slices, algos['First Come, First Served (FCFS)'].summary.makespan, [])}
              </div>
              <div class="border border-neutral-900 rounded p-4 bg-white">
                <div class="text-xs font-bold mb-2">Shortest Job First (SJF)</div>
                ${renderGanttSvg(algos['Shortest Job First (SJF)'].slices, algos['Shortest Job First (SJF)'].summary.makespan, [])}
              </div>
            </div>
          </div>
        </div>
      `;
    }

    function renderClusterResults(data) {
      const container = document.getElementById('results-container');
      container.innerHTML = `
        <div class="space-y-6">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-left">
            <div class="border border-neutral-900 rounded p-4 bg-white">
              <div class="text-[11px] uppercase tracking-wider text-neutral-500 font-semibold">Total Dispatched</div>
              <div class="text-2xl font-bold text-neutral-900 mt-1">${data.total_tasks} tasks</div>
            </div>
            <div class="border border-neutral-900 rounded p-4 bg-white">
              <div class="text-[11px] uppercase tracking-wider text-neutral-500 font-semibold">Cluster Makespan</div>
              <div class="text-2xl font-bold text-neutral-900 mt-1">${data.cluster_makespan} units</div>
            </div>
            <div class="border border-neutral-900 rounded p-4 bg-white">
              <div class="text-[11px] uppercase tracking-wider text-neutral-500 font-semibold">Avg Waiting Time</div>
              <div class="text-2xl font-bold text-neutral-900 mt-1">${data.avg_waiting_time.toFixed(2)} units</div>
            </div>
            <div class="border border-neutral-900 rounded p-4 bg-white">
              <div class="text-[11px] uppercase tracking-wider text-neutral-500 font-semibold">Avg Node CPU Util</div>
              <div class="text-2xl font-bold text-neutral-900 mt-1">${data.avg_cpu_utilization.toFixed(1)}%</div>
            </div>
          </div>

          <div class="space-y-4">
            <h3 class="text-sm font-semibold uppercase tracking-wider text-neutral-800 pb-1 border-b border-neutral-200">Per-Node Execution Timelines</h3>
            ${data.nodes.map(n => `
              <div class="border border-neutral-900 rounded p-4 bg-white">
                <div class="flex justify-between items-center mb-2 text-xs">
                  <div class="font-bold text-neutral-900">${n.node_id} (${n.tasks.length} tasks: ${n.tasks.map(t => t.task_id).join(', ') || 'None'})</div>
                  <div class="font-mono">Duration: <b>${n.summary.makespan}</b> | Util: <b>${n.summary.cpu_utilization}%</b></div>
                </div>
                ${n.slices.length > 0 ? renderGanttSvg(n.slices, Math.max(n.summary.makespan, data.cluster_makespan), []) : '<div class="text-neutral-400 text-xs py-2">Node idle</div>'}
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }

    // Initialize on page load
    renderTaskTable();
  </script>
</body>
</html>
"""


class SimulatorRequestHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        parsed = urlparse(self.path)
        if parsed.path in ("/", "/index.html"):
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
        else:
            self.send_error(HTTPStatus.NOT_FOUND, "Page not found")

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path in ("/", "/index.html"):
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        else:
            self.send_error(HTTPStatus.NOT_FOUND, "Page not found")

    def do_POST(self):
        parsed = urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)

        try:
            payload = json.loads(post_data.decode("utf-8")) if post_data else {}
        except json.JSONDecodeError:
            self.send_error(HTTPStatus.BAD_REQUEST, "Invalid JSON payload")
            return

        if parsed.path == "/api/simulate":
            tasks = payload.get("tasks", [])
            algo = payload.get("algorithm", "Round Robin (RR)")
            q = int(payload.get("time_quantum", 2))

            try:
                validate_tasks(tasks)
                if algo == "Round Robin (RR)":
                    slices, metrics = round_robin_schedule(tasks, time_quantum=q)
                elif algo == "First Come, First Served (FCFS)":
                    slices, metrics = fcfs_schedule(tasks)
                else:
                    slices, metrics = sjf_schedule(tasks)

                summary = calculate_metrics_summary(metrics, slices)
                idle = identify_idle_intervals(slices)

                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(
                    json.dumps(
                        {
                            "slices": slices,
                            "metrics": metrics,
                            "summary": summary,
                            "idle_intervals": idle,
                        }
                    ).encode("utf-8")
                )
            except Exception as e:
                self.send_response(HTTPStatus.BAD_REQUEST)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif parsed.path == "/api/compare":
            tasks = payload.get("tasks", [])
            q = int(payload.get("time_quantum", 2))
            try:
                comp = run_algorithm_comparison(tasks, time_quantum=q)
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(comp).encode("utf-8"))
            except Exception as e:
                self.send_response(HTTPStatus.BAD_REQUEST)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif parsed.path == "/api/cluster":
            tasks = payload.get("tasks", [])
            node_count = int(payload.get("node_count", 3))
            policy = payload.get("policy", "Least Loaded")
            try:
                cluster_res = simulate_cluster(
                    tasks, node_count=node_count, policy=policy
                )
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(cluster_res).encode("utf-8"))
            except Exception as e:
                self.send_response(HTTPStatus.BAD_REQUEST)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        else:
            self.send_error(HTTPStatus.NOT_FOUND, "API endpoint not found")

    def log_message(self, format, *args):
        # Quiet standard logging to avoid log noise
        return


def run_server():
    server_address = (HOST, PORT)
    httpd = ThreadingHTTPServer(server_address, SimulatorRequestHandler)
    print(f"[*] Distributed Load Balancer Simulator running on http://{HOST}:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Stopping server...")
        httpd.server_close()


if __name__ == "__main__":
    run_server()
