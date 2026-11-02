# Distributed Load Balancer Simulator (Pure Python)
*Simulating CPU Task Scheduling and Multi-Node Cluster Load Balancing*

## 1. Overview
The **Distributed Load Balancer Simulator** is an interactive web and CLI simulation platform written **entirely in Python 3** using the standard library. It models and visualizes preemptive and non-preemptive task scheduling algorithms (Round Robin, FCFS, and SJF) as well as multi-node cluster load balancing.

Zero external pip dependencies are required — it runs directly on standard Python 3.10+.

---

## 2. Key Modules & Architecture

```text
distributed-load-balancer-simulator/
│
├── app.py                      # Pure Python web server (port 3000) & interactive dashboard
├── main.py                     # Pure Python CLI demonstration & terminal visualization
├── task_manager.py             # Task schema, type validation, sample generation
├── metrics.py                  # KPI calculations, idle gap detection, comparison engine
├── node_simulator.py           # Stage 3 multi-node cluster load balancing simulator
├── requirements.txt            # Project specification (pure Python standard library)
├── README.md                   # Project documentation
│
├── schedulers/                 # CPU Scheduling algorithm modules
│   ├── __init__.py
│   ├── round_robin.py          # Preemptive Round Robin with configurable quantum
│   ├── fcfs.py                 # Non-preemptive First-Come, First-Served scheduler
│   └── sjf.py                  # Non-preemptive Shortest Job First scheduler
│
└── tests/                      # Automated unit test suite (20 unit tests)
    ├── __init__.py
    ├── test_task_manager.py    # Unit tests for task validation and preparation
    ├── test_round_robin.py     # Unit tests for Round Robin scheduling
    ├── test_fcfs.py            # Unit tests for FCFS scheduling
    ├── test_sjf.py             # Unit tests for SJF scheduling
    ├── test_metrics.py         # Unit tests for metrics engine
    └── test_node_simulator.py  # Unit tests for multi-node cluster simulation
```

---

## 3. Running the Project

### A. Run the Interactive Web Application
Launch the standalone HTTP web dashboard (listening on `0.0.0.0:3000`):
```bash
python3 app.py
```
Open your browser to `http://localhost:3000` to interact with:
- **Persistent Top Navigation Bar**: Constant across the whole website.
- **Landing Page ("Distributed CPU Scheduling")**: Overview, algorithm breakdown, curated presets, and live interactive preview.
- **Simulation**: Interactive task editor, configurable algorithms, KPI summary cards, SVG Gantt timeline with CPU idle gap visualization, metrics table, and chronological slice trace.
- **Algorithm Comparison**: Side-by-side benchmarking of Round Robin, FCFS, and SJF against identical workloads.
- **Cluster Balancer (Stage 3)**: Dispatches tasks across $N$ worker nodes using Least Loaded or Round Robin policies with per-node Gantt timelines.

### B. Run the CLI Demonstration
To run the terminal workload generator and scheduling demonstration:
```bash
python3 main.py
```

### C. Run the Automated Test Suite
Run the 20 unit tests covering every scheduler, metrics calculation, and cluster balancer:
```bash
python3 -m unittest discover -s tests
```
All tests execute in milliseconds using Python's built-in `unittest` runner.
