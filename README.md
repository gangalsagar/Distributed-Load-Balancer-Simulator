<<<<<<< HEAD
# Distributed Load Balancer Simulator (Pure Python)
*Simulating CPU Task Scheduling and Multi-Node Cluster Load Balancing*

## 1. Overview
The **Distributed Load Balancer Simulator** is an interactive web and CLI simulation platform written **entirely in Python 3** using the standard library. It models and visualizes preemptive and non-preemptive task scheduling algorithms (Round Robin, FCFS, and SJF) as well as multi-node cluster load balancing.

Zero external pip dependencies are required — it runs directly on standard Python 3.10+.

---

## 2. Key Modules & Architecture
=======
# Distributed Load Balancer Simulator
*Simulating Task Scheduling Across Multiple Nodes*

## 1. Overview
The **Distributed Load Balancer Simulator** is an Operating Systems mini-project that models and visualizes distributed task scheduling and load balancing across multiple computing nodes.

In modern distributed environments, scheduling algorithms determine how computational tasks are dispatched to compute nodes to maximize throughput, minimize turnaround/waiting times, and achieve balanced resource utilization.

---

## 2. Current Implementation Status

| Component | Status | Details |
|---|---|---|
| **Project Structure & Environment** | Completed | Clean layout, `.venv` configured, dependencies documented in `requirements.txt` |
| **Task Management (`task_manager.py`)** | Completed | Task generation, strict type & domain validation, deep-copy preparation |
| **CLI Entry Point (`main.py`)** | Completed | Terminal summary table, execution slices, metrics, and roadmap |
| **Round Robin Scheduler (`schedulers/round_robin.py`)** | Completed | Preemptive single-node Round Robin with configurable quantum and FIFO queue |
| **FCFS Scheduler (`schedulers/fcfs.py`)** | Completed | Non-preemptive First-Come, First-Served CPU scheduling with deterministic tie-breaking |
| **SJF Scheduler (`schedulers/sjf.py`)** | Completed | Non-preemptive Shortest Job First CPU scheduling with deterministic tie-breaking |
| **Metrics Engine (`metrics.py`)** | Completed | Aggregates KPIs (Waiting time, Turnaround time, Makespan) and identifies idle intervals |
| **Streamlit Web Dashboard (`app.py`)** | Completed | Interactive UI, algorithm selector (RR, FCFS, SJF), dynamic task editor, KPI cards, Plotly Gantt chart with idle time, and metrics comparisons |
| **Automated Unit Tests (`tests/`)** | Completed | 100% passed (42 tests covering task manager, round robin, fcfs, sjf, and metrics) |
| **Node Simulator (`node_simulator.py`)** | Planned | Multi-node cluster simulation and task load balancing (future stage) |

---

## 3. Project Structure
>>>>>>> 4ab66d6ce60f640de08a69a5ff3c9989b6d222f1

```text
distributed-load-balancer-simulator/
│
<<<<<<< HEAD
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
=======
├── app.py                      # Interactive Streamlit Web Dashboard
├── main.py                     # CLI demonstration entry-point program
├── task_manager.py             # Task data structures, validation & preparation
├── metrics.py                  # Performance metrics aggregation & idle gap detection
├── node_simulator.py           # [Planned] Multi-node simulation engine
├── requirements.txt            # Project dependencies (streamlit, pandas, plotly)
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore rules
│
├── schedulers/                 # CPU Scheduling algorithm modules
│   ├── __init__.py
│   ├── round_robin.py          # Round Robin CPU scheduler (preemptive)
│   ├── fcfs.py                 # First-Come, First-Served CPU scheduler (non-preemptive)
│   └── sjf.py                  # Shortest Job First CPU scheduler (non-preemptive)
│
└── tests/                      # Automated unit test suite
    ├── __init__.py
    ├── test_task_manager.py    # Unit tests for task management
    ├── test_round_robin.py     # Unit tests for Round Robin scheduling
    ├── test_fcfs.py            # Unit tests for FCFS scheduling
    ├── test_sjf.py             # Unit tests for SJF scheduling
    └── test_metrics.py         # Unit tests for metrics engine
>>>>>>> 4ab66d6ce60f640de08a69a5ff3c9989b6d222f1
```

---

<<<<<<< HEAD
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
=======
## 4. Setup and Installation

### Prerequisites
- Python 3.10 or newer (Tested on Python 3.13)

### 1. Create Virtual Environment
```bash
python -m venv .venv
```

### 2. Activate Virtual Environment
- **Windows (PowerShell):**
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- **Windows (Command Prompt):**
  ```cmd
  .\.venv\Scripts\activate.bat
  ```
- **macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
*Dependencies:* `streamlit`, `pandas`, `plotly`.

---

## 5. Running the Application

### Option A: Interactive Streamlit Web Dashboard
To launch the graphical dashboard with interactive workload editing, Gantt chart, and KPI cards:
```bash
streamlit run app.py
```
Or using the virtual environment directly:
```bash
.\.venv\Scripts\streamlit.exe run app.py
```

### Option B: Command-Line Demonstration
To run the terminal-based workload generation and Round Robin demonstration:
```bash
python main.py
```
Or using the virtual environment directly:
```bash
.\.venv\Scripts\python.exe main.py
```

---

## 6. Running Tests

Run the test suite using Python's built-in `unittest` runner:
```bash
python -m unittest discover -s tests
```
Or using the virtual environment directly:
```bash
.\.venv\Scripts\python.exe -m unittest discover -s tests
```

---

## 7. Roadmap & Next Stages

1. **Stage 2: Additional CPU Schedulers (`schedulers/`)**
   - Implement FCFS with arrival ordering and deterministic tie-breaking.
   - Implement non-preemptive SJF selecting ready tasks with minimum burst time.
2. **Stage 3: Distributed Node Simulation (`node_simulator.py`)**
   - Simulate a cluster of $N$ worker nodes.
   - Load balancing policies (e.g., Round Robin node allocation, Least Loaded).
   - Event timeline recording (task dispatch, execution ticks, completion).
>>>>>>> 4ab66d6ce60f640de08a69a5ff3c9989b6d222f1
