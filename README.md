<<<<<<< HEAD
# Distributed Load Balancer Simulator
*Simulating Task Scheduling Across Multiple Nodes*

## 1. Overview
The **Distributed Load Balancer Simulator** is an Operating Systems mini-project that models and visualizes distributed task scheduling and load balancing across multiple computing nodes.

In modern distributed environments, scheduling algorithms determine how computational tasks are dispatched to compute nodes to maximize throughput, minimize turnaround/waiting times, and achieve balanced resource utilization.

---

## 2. Current Implementation Status

| Component | Status | Details |
|---|---|---|
| **Project Structure & Environment** | Completed | Clean layout, `.venv` configured, dependencies documented |
| **Task Management (`task_manager.py`)** | Completed | Task generation, strict type & domain validation, deep-copy preparation |
| **CLI Entry Point (`main.py`)** | Completed | Formatted summary table, total burst time, architecture roadmap |
| **Automated Unit Tests (`tests/`)** | Completed | 100% passed using Python standard `unittest` |
| **Schedulers (`schedulers/`)** | Planned | Placeholders with design documentation for FCFS, SJF, and Round Robin |
| **Node Simulator (`node_simulator.py`)** | Planned | Placeholder with design documentation for multi-node simulation |
| **Metrics Engine (`metrics.py`)** | Planned | Placeholder with design documentation for performance evaluation |
| **Streamlit Web Dashboard** | Planned | Planned interactive UI and Gantt timeline charts |

---

## 3. Project Structure

```text
distributed-load-balancer-simulator/
│
├── main.py                     # CLI entry-point program
├── task_manager.py             # Task data structures, validation & preparation
├── node_simulator.py           # [Planned] Multi-node simulation engine
├── metrics.py                  # [Planned] Performance metrics calculation
├── requirements.txt            # Project dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore rules
│
├── schedulers/                 # CPU Scheduling algorithm modules
│   ├── __init__.py
│   ├── fcfs.py                 # [Planned] First-Come, First-Served
│   ├── sjf.py                  # [Planned] Shortest Job First (non-preemptive)
│   └── round_robin.py          # [Planned] Round Robin (preemptive)
│
└── tests/                      # Automated unit test suite
    ├── __init__.py
    └── test_task_manager.py    # Unit tests for task management
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

Execute the entry-point script:
```bash
python main.py
# Or using the virtual environment directly:
.\.venv\Scripts\python.exe main.py
```

### Expected Output
- Project title and header.
- Formatted table of generated sample tasks (T1 to T4).
- Total tasks: `4`.
- Total CPU burst time: `18` units.
- Confirmation of successful generation and validation.
- Outline of planned upcoming modules.

---

## 6. Running Tests

Run the test suite using Python's built-in `unittest` runner:
```bash
python -m unittest discover -s tests
# Or using the virtual environment directly:
.\.venv\Scripts\python.exe -m unittest discover -s tests
```

---

## 7. Roadmap & Next Stages

1. **Stage 2: Scheduling Algorithms (`schedulers/`)**
   - Implement FCFS with arrival ordering and deterministic tie-breaking.
   - Implement non-preemptive SJF selecting ready tasks with minimum burst time.
   - Implement preemptive Round Robin with configurable time quantum ($q$) and requeueing.
2. **Stage 3: Distributed Node Simulation (`node_simulator.py`)**
   - Simulate a cluster of $N$ worker nodes.
   - Load balancing policies (e.g., Round Robin node allocation, Least Loaded).
   - Event timeline recording (task dispatch, execution ticks, completion).
3. **Stage 4: Metrics Engine (`metrics.py`)**
   - Compute waiting time, turnaround time, makespan, and node utilization percentage.
4. **Stage 5: Interactive Web Dashboard (`dashboard.py` / Streamlit)**
   - Dynamic Gantt charts using Plotly.
   - Interactive algorithm comparison and parameter tuning.
=======
# Distributed-Load-Balancer-Simulator
 Simulating Task Scheduling Across Multiple Nodes
>>>>>>> 88ca63d3d3712410b2a3ba5f640ddc18b6563213
