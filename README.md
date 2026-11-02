# Distributed Load Balancer & CPU Scheduling Simulator

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests: 20 Passed](https://img.shields.io/badge/tests-20%20passed-brightgreen.svg)]()

An interactive simulation platform designed to model, analyze, and visualize classic Operating System CPU scheduling algorithms and multi-node cluster load balancing.

---

## 📋 System Prerequisites

Before running this project, ensure you have the following installed on your machine:

1. **Python 3.10 or higher**
   - Download: [python.org/downloads](https://www.python.org/downloads/)
   - *Windows Note:* Ensure you check the box **"Add Python to PATH"** during installation.
2. **Git** (for cloning and version control)
   - Download: [git-scm.com](https://git-scm.com/)
3. **A Modern Web Browser** (Chrome, Edge, Firefox, Brave, Safari) to view the interactive UI.

---

## ⚙️ Environment Setup & Installation

### Step 1: Clone the Repository
```bash
git clone <your-repository-url>
cd "OS Miniproject"
```

### Step 2: (Recommended) Create and Activate a Virtual Environment

Creating an isolated virtual environment keeps your project clean and organized:

- **Windows (Command Prompt / PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  ```

- **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### Step 3: Dependencies
This project is built **100% using Python's standard library** (`http.server`, `json`, `threading`, `collections`, etc.). 
No third-party `pip` packages are strictly required. If you want to ensure your environment is verified:
```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run

### 1. Launch the Interactive Web Dashboard
Run the following command from the root directory:

```bash
python app.py
```

Then open your browser and go to:
👉 **[http://localhost:3000](http://localhost:3000)**

*(Windows users can also double-click `run.bat` or run `.\run.bat`)*

---

### 2. Run the CLI Simulation
To run terminal-based workload generation and view scheduling slices in the console:

```bash
python main.py
```

---

### 3. Run the Automated Unit Tests
To verify all scheduler algorithms, metrics engines, and cluster simulators:

```bash
python -m unittest discover -s tests
```

---

## ✨ Features

- **Interactive Simulation**:
  - Add, edit, or remove custom tasks on the fly (Task ID, Arrival Time, Burst Time).
  - Switch between scheduling algorithms (**Round Robin**, **FCFS**, and **SJF**).
  - Dynamically configure Round Robin time quantum.
  - Interactive SVG Gantt Chart with CPU idle gap visualization.
  - Complete metrics breakdown (Turnaround Time, Waiting Time, Makespan, CPU Utilization).

- **Algorithm Comparison**:
  - Benchmark Round Robin, First-Come First-Served, and Shortest Job First simultaneously against identical workloads.
  - Side-by-side performance comparison table and metrics breakdown highlighting top-performing policies.

- **Multi-Node Cluster Simulation**:
  - Model distributed workload distribution across $N$ worker nodes.
  - Supports load balancing policies including **Least Loaded** and **Round Robin**.
  - Visualizes per-node task assignments and overall cluster makespan.

---

## 🧠 Implemented Algorithms

| Algorithm | Paradigm | Description |
| :--- | :--- | :--- |
| **Round Robin (RR)** | Preemptive | Tasks are allocated CPU in fixed time slices (quantum) with cyclic queue rotation. |
| **First Come, First Served (FCFS)** | Non-preemptive | Tasks execute in the exact order of their arrival with deterministic tie-breaking. |
| **Shortest Job First (SJF)** | Non-preemptive | Selects the task with the smallest burst time among all currently arrived tasks. |

---

## 📁 Repository Structure

```text
.
├── app.py                      # Standalone HTTP server & web dashboard (Port 3000)
├── main.py                     # CLI demonstration and terminal visualizer
├── task_manager.py             # Task data structures, validation & preparation
├── metrics.py                  # Performance calculation engine & idle gap detection
├── node_simulator.py           # Multi-node cluster load balancing logic
├── run.bat                     # Windows one-click execution shortcut
├── requirements.txt            # Project specification
├── README.md                   # Project documentation
│
├── schedulers/                 # CPU Scheduling core modules
│   ├── __init__.py
│   ├── round_robin.py          # Round Robin algorithm implementation
│   ├── fcfs.py                 # First-Come, First-Served algorithm implementation
│   └── sjf.py                  # Shortest Job First algorithm implementation
│
└── tests/                      # Automated test suite (20 unit tests)
    ├── __init__.py
    ├── test_task_manager.py    # Tests for task validation & schema
    ├── test_round_robin.py     # Tests for Round Robin scheduler
    ├── test_fcfs.py            # Tests for FCFS scheduler
    ├── test_sjf.py             # Tests for SJF scheduler
    ├── test_metrics.py         # Tests for KPI calculations
    └── test_node_simulator.py  # Tests for multi-node load balancing
```
