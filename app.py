"""
Distributed Load Balancer Simulator - Interactive Streamlit Dashboard.

Modern SaaS interface for single-node Round Robin CPU scheduling:
- Refined SaaS light theme: Neutral off-white (#F8FAFC) canvas, pure white (#FFFFFF) elevated cards,
  slate typography (#1E293B, #64748B), and polished indigo/electric blue (#4F46E5 / #3B82F6) accents.
- Clean visual hierarchy, soft subtle shadows, rounded borders, and clear typography.
- CPU execution timeline (Plotly) with distinct, elegant task slice colors and idle indicators.
- Metrics summary KPI cards, interactive task table, and waiting vs. turnaround time comparisons.
"""

from typing import Any, Dict, List
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from metrics import calculate_metrics_summary, identify_idle_intervals
from schedulers.round_robin import round_robin_schedule
from task_manager import generate_sample_tasks, validate_tasks


# Page Configuration
st.set_page_config(
    page_title="Distributed Load Balancer Simulator",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Polished Modern SaaS Theme Stylesheet
st.markdown(
    """
    <style>
    /* Base canvas styling */
    .stApp {
        background-color: #F8FAFC;
        color: #0F172A;
        font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, sans-serif;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        color: #0F172A !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em;
    }

    /* Header component */
    .saas-header {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 24px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
    }
    .saas-title {
        font-size: 1.45rem;
        font-weight: 700;
        color: #0F172A;
        margin: 0;
    }
    .saas-subtitle {
        font-size: 0.9rem;
        color: #64748B;
        margin-top: 4px;
    }

    /* Section Subheadings */
    .saas-section-header {
        font-size: 1.05rem;
        font-weight: 600;
        color: #1E293B;
        margin: 24px 0 12px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* KPI Cards */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 24px;
    }
    .kpi-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.06);
    }
    .kpi-label {
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #64748B;
    }
    .kpi-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #0F172A;
        margin-top: 6px;
    }
    .kpi-unit {
        font-size: 0.85rem;
        font-weight: 500;
        color: #94A3B8;
        margin-left: 2px;
    }

    /* Primary and Secondary Action Buttons */
    button[kind="primary"] {
        background: linear-gradient(135deg, #4F46E5 0%, #4338CA 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 8px 16px !important;
        box-shadow: 0 2px 6px rgba(79, 70, 229, 0.25) !important;
    }
    button[kind="primary"]:hover {
        background: linear-gradient(135deg, #4338CA 0%, #3730A3 100%) !important;
        box-shadow: 0 4px 10px rgba(79, 70, 229, 0.35) !important;
    }

    button[kind="secondary"] {
        background-color: #FFFFFF !important;
        color: #334155 !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
    }
    button[kind="secondary"]:hover {
        background-color: #F8FAFC !important;
        border-color: #4F46E5 !important;
        color: #4F46E5 !important;
    }

    /* Empty state card */
    .empty-state-card {
        background-color: #FFFFFF;
        border: 1px dashed #CBD5E1;
        border-radius: 12px;
        padding: 36px 24px;
        text-align: center;
        color: #64748B;
        margin: 20px 0;
    }

    /* Card wrappers for charts and tables */
    .content-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def get_default_tasks_df() -> pd.DataFrame:
    """Return default sample workload as a DataFrame."""
    sample = generate_sample_tasks()
    return pd.DataFrame([
        {"Task ID": t["task_id"], "Arrival Time": t["arrival_time"], "Burst Time": t["burst_time"]}
        for t in sample
    ])


# Session State Initialization
if "tasks_df" not in st.session_state:
    st.session_state.tasks_df = get_default_tasks_df()

if "sim_run" not in st.session_state:
    st.session_state.sim_run = False


# Sidebar Controls
with st.sidebar:
    st.markdown("### Configuration")

    algorithm = st.selectbox(
        "Scheduling Algorithm",
        options=["Round Robin (RR)"],
        index=0,
        help="Preemptive Round Robin CPU scheduler. FCFS and SJF are planned for future stages.",
    )

    time_quantum = st.number_input(
        "Time Quantum (q)",
        min_value=1,
        max_value=100,
        value=2,
        step=1,
        help="CPU execution time slice allocated per turn (integer >= 1).",
    )

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    if st.button("Run Simulation", type="primary", use_container_width=True):
        st.session_state.sim_run = True

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("Load Sample", use_container_width=True):
            st.session_state.tasks_df = get_default_tasks_df()
            st.session_state.sim_run = True
            st.rerun()

    with col_btn2:
        if st.button("Reset", use_container_width=True):
            st.session_state.tasks_df = get_default_tasks_df()
            st.session_state.sim_run = False
            st.rerun()

    st.markdown("<hr style='border: none; border-top: 1px solid #E2E8F0; margin: 24px 0 16px 0;'>", unsafe_allow_html=True)
    st.caption("Distributed Load Balancer Simulator · OS Mini-Project")


# Main Dashboard Header
st.markdown(
    """
    <div class="saas-header">
        <h1 class="saas-title">Distributed Load Balancer Simulator</h1>
        <p class="saas-subtitle">Interactive CPU scheduling analysis, execution timelines, and workload performance</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Workload Input Section
st.markdown('<div class="saas-section-header">Workload Configuration</div>', unsafe_allow_html=True)

edited_df = st.data_editor(
    st.session_state.tasks_df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Task ID": st.column_config.TextColumn("Task ID", required=True),
        "Arrival Time": st.column_config.NumberColumn(
            "Arrival Time", min_value=0, step=1, required=True
        ),
        "Burst Time": st.column_config.NumberColumn(
            "Burst Time", min_value=1, step=1, required=True
        ),
    },
    key="editor_tasks",
)

st.session_state.tasks_df = edited_df

# Validation
validated_tasks: List[Dict[str, Any]] = []
validation_error: str = ""

try:
    raw_records = edited_df.to_dict("records")
    clean_records: List[Dict[str, Any]] = []
    for r in raw_records:
        task_id = str(r.get("Task ID", "")).strip() if r.get("Task ID") is not None else ""
        arr_val = r.get("Arrival Time")
        burst_val = r.get("Burst Time")

        if not task_id and arr_val is None and burst_val is None:
            continue

        if not task_id:
            raise ValueError("Task ID cannot be empty.")
        if arr_val is None or pd.isna(arr_val):
            raise ValueError(f"Task '{task_id}' has missing Arrival Time.")
        if burst_val is None or pd.isna(burst_val):
            raise ValueError(f"Task '{task_id}' has missing Burst Time.")

        clean_records.append({
            "task_id": task_id,
            "arrival_time": int(arr_val),
            "burst_time": int(burst_val),
        })

    if clean_records:
        validate_tasks(clean_records)
    validated_tasks = clean_records
except Exception as e:
    validation_error = str(e)


if validation_error:
    st.error(f"Input validation error: {validation_error}")


# Execution & Visualizations
if st.session_state.sim_run and not validation_error:
    if not validated_tasks:
        st.warning("No tasks configured. Please enter at least one task or click 'Load Sample'.")
    else:
        try:
            slices, metrics = round_robin_schedule(validated_tasks, time_quantum=int(time_quantum))
            summary = calculate_metrics_summary(metrics)

            # Performance Summary Cards
            st.markdown('<div class="saas-section-header">Performance Overview</div>', unsafe_allow_html=True)
            k1, k2, k3, k4 = st.columns(4)
            with k1:
                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <div class="kpi-label">Tasks Scheduled</div>
                        <div class="kpi-value">{summary['total_tasks']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with k2:
                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <div class="kpi-label">Avg Waiting Time</div>
                        <div class="kpi-value">{summary['avg_waiting_time']:.2f}<span class="kpi-unit">units</span></div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with k3:
                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <div class="kpi-label">Avg Turnaround Time</div>
                        <div class="kpi-value">{summary['avg_turnaround_time']:.2f}<span class="kpi-unit">units</span></div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with k4:
                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <div class="kpi-label">Makespan</div>
                        <div class="kpi-value">{summary['makespan']}<span class="kpi-unit">units</span></div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # CPU Execution Timeline (Gantt)
            st.markdown('<div class="saas-section-header">CPU Execution Timeline</div>', unsafe_allow_html=True)

            idle_slices = identify_idle_intervals(slices)
            all_timeline_items = []
            for s in slices:
                all_timeline_items.append({
                    "Task ID": s["task_id"],
                    "Start": s["start_time"],
                    "End": s["end_time"],
                    "Duration": s["duration"],
                    "Is Idle": False,
                })
            for idle in idle_slices:
                all_timeline_items.append({
                    "Task ID": "Idle",
                    "Start": idle["start_time"],
                    "End": idle["end_time"],
                    "Duration": idle["duration"],
                    "Is Idle": True,
                })

            all_timeline_items.sort(key=lambda x: x["Start"])

            # Refined modern SaaS palette for distinct tasks
            saas_palette = [
                "#4F46E5",  # Indigo (Primary)
                "#0EA5E9",  # Sky Blue
                "#3B82F6",  # Blue
                "#6366F1",  # Violet Indigo
                "#0284C7",  # Deep Sky
                "#2563EB",  # Royal Blue
                "#818CF8",  # Soft Indigo
            ]
            unique_tasks = sorted(list(set(s["task_id"] for s in slices)))
            task_colors = {
                tid: saas_palette[i % len(saas_palette)]
                for i, tid in enumerate(unique_tasks)
            }

            fig_timeline = go.Figure()

            for item in all_timeline_items:
                tid = item["Task ID"]
                is_idle = item["Is Idle"]

                if is_idle:
                    bar_color = "#E2E8F0"
                    border_color = "#CBD5E1"
                    text_color = "#64748B"
                    label = f"Idle [{item['Start']}-{item['End']}]"
                else:
                    bar_color = task_colors.get(tid, "#4F46E5")
                    border_color = "#FFFFFF"
                    text_color = "#FFFFFF"
                    label = f"{tid} [{item['Start']}-{item['End']}]"

                fig_timeline.add_trace(
                    go.Bar(
                        name=tid,
                        y=["CPU Timeline"],
                        x=[item["Duration"]],
                        base=[item["Start"]],
                        orientation="h",
                        marker=dict(
                            color=bar_color,
                            line=dict(color=border_color, width=1.5),
                        ),
                        text=label,
                        textposition="inside",
                        insidetextanchor="middle",
                        textfont=dict(color=text_color, size=12, family="Inter, sans-serif"),
                        hovertemplate=(
                            f"<b>{'Task ' + tid if not is_idle else 'CPU Idle'}</b><br>"
                            f"Start: {item['Start']}<br>"
                            f"End: {item['End']}<br>"
                            f"Duration: {item['Duration']} units<extra></extra>"
                        ),
                        showlegend=(item["Start"] == min(x["Start"] for x in all_timeline_items if x["Task ID"] == tid)),
                    )
                )

            fig_timeline.update_layout(
                barmode="stack",
                height=175,
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#FFFFFF",
                font=dict(color="#0F172A", family="Inter, sans-serif"),
                xaxis=dict(
                    title="Simulation Time (Units)",
                    title_font=dict(color="#475569", size=12),
                    tickfont=dict(color="#64748B", size=11),
                    linecolor="#E2E8F0",
                    linewidth=1,
                    tickmode="linear",
                    tick0=0,
                    dtick=1 if summary["makespan"] <= 30 else max(1, summary["makespan"] // 20),
                    range=[0, summary["makespan"] + 0.3],
                    showgrid=True,
                    gridcolor="#F1F5F9",
                ),
                yaxis=dict(
                    showticklabels=False,
                    showgrid=False,
                    linecolor="#E2E8F0",
                ),
                margin=dict(l=16, r=16, t=10, b=42),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.05,
                    xanchor="left",
                    x=0,
                    font=dict(size=11, color="#334155"),
                ),
            )
            st.plotly_chart(fig_timeline, use_container_width=True)

            # Results Section: Table and Grouped Comparison Chart
            st.markdown('<div class="saas-section-header">Results & Metrics Analysis</div>', unsafe_allow_html=True)
            col_tbl, col_plot = st.columns([1, 1], gap="medium")

            with col_tbl:
                results_rows = []
                for tid in sorted(metrics.keys()):
                    m = metrics[tid]
                    results_rows.append({
                        "Task ID": m["task_id"],
                        "Arrival": m["arrival_time"],
                        "Burst": m["burst_time"],
                        "Completion": m["completion_time"],
                        "Waiting Time": m["waiting_time"],
                        "Turnaround Time": m["turnaround_time"],
                    })
                results_df = pd.DataFrame(results_rows)
                st.dataframe(results_df, use_container_width=True, hide_index=True)

            with col_plot:
                if results_rows:
                    comp_df = pd.DataFrame(results_rows)
                    fig_comp = go.Figure()

                    # Modern paired palette: soft sky blue for waiting, deep indigo for turnaround
                    fig_comp.add_trace(
                        go.Bar(
                            x=comp_df["Task ID"],
                            y=comp_df["Waiting Time"],
                            name="Waiting Time",
                            marker=dict(
                                color="#93C5FD",
                                line=dict(color="#60A5FA", width=1),
                            ),
                            text=comp_df["Waiting Time"],
                            textposition="auto",
                            textfont=dict(color="#1E3A8A"),
                        )
                    )
                    fig_comp.add_trace(
                        go.Bar(
                            x=comp_df["Task ID"],
                            y=comp_df["Turnaround Time"],
                            name="Turnaround Time",
                            marker=dict(
                                color="#4F46E5",
                                line=dict(color="#4338CA", width=1),
                            ),
                            text=comp_df["Turnaround Time"],
                            textposition="auto",
                            textfont=dict(color="#FFFFFF"),
                        )
                    )

                    fig_comp.update_layout(
                        barmode="group",
                        height=290,
                        paper_bgcolor="#FFFFFF",
                        plot_bgcolor="#FFFFFF",
                        font=dict(color="#0F172A", family="Inter, sans-serif"),
                        xaxis=dict(
                            title="Task ID",
                            title_font=dict(color="#475569", size=12),
                            tickfont=dict(color="#64748B", size=11),
                            linecolor="#E2E8F0",
                            linewidth=1,
                            showgrid=False,
                        ),
                        yaxis=dict(
                            title="Time Units",
                            title_font=dict(color="#475569", size=12),
                            tickfont=dict(color="#64748B", size=11),
                            linecolor="#E2E8F0",
                            linewidth=1,
                            showgrid=True,
                            gridcolor="#F1F5F9",
                        ),
                        margin=dict(l=16, r=16, t=10, b=42),
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.04,
                            xanchor="right",
                            x=1,
                            font=dict(size=11, color="#334155"),
                        ),
                    )
                    st.plotly_chart(fig_comp, use_container_width=True)

        except Exception as sim_err:
            st.error(f"Error during simulation execution: {sim_err}")
else:
    if not st.session_state.sim_run:
        st.markdown(
            """
            <div class="empty-state-card">
                <div style="font-weight: 600; font-size: 1.05rem; color: #1E293B;">Ready to Simulate</div>
                <div style="font-size: 0.88rem; color: #64748B; margin-top: 6px;">
                    Configure or edit tasks in the table above, then click <b>Run Simulation</b> in the sidebar.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
