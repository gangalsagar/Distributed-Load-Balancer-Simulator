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
| **Metrics Engine (`metrics.py`)** | Completed | Aggregates KPIs (Waiting time, Turnaround time, Makespan) and identifies idle intervals |
| **Streamlit Web Dashboard (`app.py`)** | Completed | Interactive UI, dynamic task editor, KPI cards, Plotly Gantt chart with idle time, and metrics comparisons |
| **Automated Unit Tests (`tests/`)** | Completed | 100% passed (25 tests covering task manager, round robin, and metrics) |
| **Node Simulator (`node_simulator.py`)** | Planned | Multi-node cluster simulation and task load balancing (future stage) |
| **Additional Schedulers (`schedulers/`)** | Planned | Placeholders for FCFS and SJF (future stage) |

---

## 3. Project Structure

```text
distributed-load-balancer-simulator/
│
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
│   ├── fcfs.py                 # [Planned] First-Come, First-Served
│   └── sjf.py                  # [Planned] Shortest Job First (non-preemptive)
│
└── tests/                      # Automated unit test suite
    ├── __init__.py
    ├── test_task_manager.py    # Unit tests for task management
    ├── test_round_robin.py     # Unit tests for Round Robin scheduling
    └── test_metrics.py         # Unit tests for metrics engine
```

---

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
