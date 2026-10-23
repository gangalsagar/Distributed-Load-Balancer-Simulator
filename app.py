"""
Distributed Load Balancer Simulator - Interactive Streamlit Dashboard.

Horizon-Inspired UI/UX:
- Clean, airy aesthetic with Plus Jakarta Sans typography.
- Glassmorphic translucent cards (bg-white/40, border-white/60, backdrop-blur-xl).
- Coral/peach vibrant accent (#FF5E3A), soft sky (#38BDF8), lavender (#C084FC), and lime highlights.
- Rounded pill badges, floating headers, and luminous multi-color gradients.
- Interactive CPU Gantt timeline and grouped metrics charts styled with matching vibrant pastels.
"""

from typing import Any, Dict, List
import pandas as pd
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

# Custom Horizon / Stitch Styling
st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">

    <style>
    /* Global Base */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(56, 189, 248, 0.08) 0%, transparent 40%),
                    radial-gradient(circle at 90% 10%, rgba(192, 132, 252, 0.12) 0%, transparent 50%),
                    radial-gradient(circle at 50% 80%, rgba(255, 94, 58, 0.06) 0%, transparent 60%),
                    #FAFAF9;
        color: #111111;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        color: #000000 !important;
        letter-spacing: -0.03em !important;
    }

    /* Floating Navigation / Header Card */
    .horizon-nav {
        background: rgba(255, 255, 255, 0.65);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.8);
        border-radius: 9999px;
        padding: 12px 28px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.04);
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 24px;
    }
    .horizon-logo {
        font-weight: 800;
        font-size: 1.25rem;
        color: #FF5E3A;
        display: flex;
        align-items: center;
        gap: 8px;
        text-decoration: none;
    }
    .horizon-badge {
        background: #D6ED7A;
        color: #3F4C00;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        padding: 4px 10px;
        border-radius: 9999px;
    }

    /* Glass Cards */
    .horizon-card {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(255, 255, 255, 0.85);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.03);
        margin-bottom: 20px;
    }

    /* KPI Cards */
    .kpi-horizon-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.9);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    .kpi-horizon-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 32px rgba(255, 94, 58, 0.08);
    }
    .kpi-pill {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 3px 8px;
        border-radius: 9999px;
        display: inline-block;
        margin-bottom: 8px;
    }
    .kpi-val {
        font-size: 2rem;
        font-weight: 800;
        color: #000000;
        line-height: 1.1;
        letter-spacing: -0.04em;
    }

    /* Section Subtitle */
    .section-eyebrow {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #555555;
        margin-bottom: 4px;
    }
    .section-headline {
        font-size: 1.25rem;
        font-weight: 700;
        color: #000000;
        margin-bottom: 16px;
        letter-spacing: -0.02em;
    }

    /* Buttons */
    button[kind="primary"] {
        background: #FF5E3A !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 9999px !important;
        font-weight: 700 !important;
        padding: 10px 24px !important;
        font-size: 0.95rem !important;
        box-shadow: 0 4px 16px rgba(255, 94, 58, 0.35) !important;
        transition: all 0.2s ease !important;
    }
    button[kind="primary"]:hover {
        background: #F44923 !important;
        box-shadow: 0 6px 20px rgba(255, 94, 58, 0.5) !important;
        transform: scale(0.98);
    }

    button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(12px) !important;
        color: #000000 !important;
        border-radius: 9999px !important;
        font-weight: 600 !important;
    }
    button[kind="secondary"]:hover {
        background: rgba(255, 255, 255, 0.9) !important;
        border-color: #FF5E3A !important;
        color: #FF5E3A !important;
    }

    /* Empty state */
    .horizon-empty {
        background: rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(20px);
        border: 1px dashed rgba(255, 94, 58, 0.3);
        border-radius: 16px;
        padding: 40px 24px;
        text-align: center;
        margin-top: 16px;
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


# Sidebar Controls (Airy Glassmorphism)
with st.sidebar:
    st.markdown(
        """
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
            <span style="color:#FF5E3A; font-weight:800; font-size:1.15rem;">Load Balancer</span>
            <span class="horizon-badge">Simulator</span>
        </div>
        <p style="font-size:0.85rem; color:#555555; margin-bottom:20px;">
            Distributed CPU Scheduling & Load Balancer Simulator
        </p>
        """,
        unsafe_allow_html=True,
    )

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
        help="Positive integer time slice allocated per execution slice.",
    )

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    if st.button("Run Simulation", type="primary", use_container_width=True):
        st.session_state.sim_run = True

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button("Load Sample", use_container_width=True):
            st.session_state.tasks_df = get_default_tasks_df()
            st.session_state.sim_run = True
            st.rerun()

    with col_b2:
        if st.button("Reset", use_container_width=True):
            st.session_state.tasks_df = get_default_tasks_df()
            st.session_state.sim_run = False
            st.rerun()


# Floating Header Bar
st.markdown(
    """
    <div class="horizon-nav">
        <div class="horizon-logo">
            <span>Distributed Load Balancer Simulator</span>
        </div>
        <div style="display:flex; align-items:center; gap:16px;">
            <span style="font-size:0.85rem; color:#555555; font-weight:500;">Round Robin Preemptive Engine</span>
            <span class="horizon-badge">Active</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Overview Banner
st.markdown(
    """
    <div style="margin-bottom: 24px;">
        <h1 style="font-size: 2.2rem; font-weight: 800; line-height: 1.15; margin: 0 0 6px 0;">
            Distributed Load Balancer Simulator
        </h1>
        <p style="font-size: 1rem; color: #555555; margin: 0;">
            An airy, interactive CPU scheduling environment designed for clear visualization and performance analysis.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# Workload Configuration Section
st.markdown(
    """
    <div class="section-eyebrow">01 / Task Setup</div>
    <div class="section-headline">Workload Configuration</div>
    """,
    unsafe_allow_html=True,
)

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


# Simulation Execution & Results Display
if st.session_state.sim_run and not validation_error:
    if not validated_tasks:
        st.warning("No tasks configured. Please enter at least one task or click 'Load Sample'.")
    else:
        try:
            slices, metrics = round_robin_schedule(validated_tasks, time_quantum=int(time_quantum))
            summary = calculate_metrics_summary(metrics)

            # Performance Metrics Cards (Horizon Style)
            st.markdown(
                """
                <div style="margin-top: 24px;">
                    <div class="section-eyebrow">02 / Performance</div>
                    <div class="section-headline">Summary Metrics</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            k1, k2, k3, k4 = st.columns(4)
            with k1:
                st.markdown(
                    f"""
                    <div class="kpi-horizon-card">
                        <span class="kpi-pill" style="background: rgba(56, 189, 248, 0.2); color: #0284C7;">Workload</span>
                        <div class="kpi-val">{summary['total_tasks']}</div>
                        <div style="font-size: 0.8rem; color: #555555; margin-top: 4px;">Tasks Scheduled</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with k2:
                st.markdown(
                    f"""
                    <div class="kpi-horizon-card">
                        <span class="kpi-pill" style="background: rgba(255, 94, 58, 0.18); color: #C2410C;">Latency</span>
                        <div class="kpi-val">{summary['avg_waiting_time']:.2f} <span style="font-size: 1rem; color: #888;">units</span></div>
                        <div style="font-size: 0.8rem; color: #555555; margin-top: 4px;">Average Waiting Time</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with k3:
                st.markdown(
                    f"""
                    <div class="kpi-horizon-card">
                        <span class="kpi-pill" style="background: rgba(192, 132, 252, 0.25); color: #7E22CE;">Duration</span>
                        <div class="kpi-val">{summary['avg_turnaround_time']:.2f} <span style="font-size: 1rem; color: #888;">units</span></div>
                        <div style="font-size: 0.8rem; color: #555555; margin-top: 4px;">Avg Turnaround Time</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with k4:
                st.markdown(
                    f"""
                    <div class="kpi-horizon-card">
                        <span class="kpi-pill" style="background: rgba(214, 237, 122, 0.5); color: #3F4C00;">Throughput</span>
                        <div class="kpi-val">{summary['makespan']} <span style="font-size: 1rem; color: #888;">units</span></div>
                        <div style="font-size: 0.8rem; color: #555555; margin-top: 4px;">Final Makespan</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # CPU Execution Timeline (Gantt)
            st.markdown(
                """
                <div style="margin-top: 28px;">
                    <div class="section-eyebrow">03 / Timeline</div>
                    <div class="section-headline">CPU Execution Timeline</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

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

            # Stitch / Horizon dynamic theme palette
            stitch_colors = [
                "#FF5E3A",  # Horizon Coral (Primary)
                "#38BDF8",  # Sky Blue
                "#C084FC",  # Lavender Purple
                "#D6ED7A",  # Lime Green
                "#FF8A65",  # Peach
                "#80B1C7",  # Soft Teal
                "#FFD166",  # Warm Sun
            ]
            unique_tasks = sorted(list(set(s["task_id"] for s in slices)))
            task_color_map = {
                tid: stitch_colors[i % len(stitch_colors)]
                for i, tid in enumerate(unique_tasks)
            }

            fig_timeline = go.Figure()

            for item in all_timeline_items:
                tid = item["Task ID"]
                is_idle = item["Is Idle"]

                if is_idle:
                    bar_color = "rgba(0, 0, 0, 0.05)"
                    border_color = "rgba(0, 0, 0, 0.15)"
                    text_color = "#666666"
                    label = f"Idle [{item['Start']}-{item['End']}]"
                else:
                    bar_color = task_color_map.get(tid, "#FF5E3A")
                    border_color = "rgba(255, 255, 255, 0.9)"
                    # Contrast text check
                    text_color = "#3F4C00" if bar_color == "#D6ED7A" else "#FFFFFF"
                    label = f"{tid} [{item['Start']}-{item['End']}]"

                fig_timeline.add_trace(
                    go.Bar(
                        name=tid,
                        y=["CPU"],
                        x=[item["Duration"]],
                        base=[item["Start"]],
                        orientation="h",
                        marker=dict(
                            color=bar_color,
                            line=dict(color=border_color, width=2),
                        ),
                        text=label,
                        textposition="inside",
                        insidetextanchor="middle",
                        textfont=dict(color=text_color, size=12, family="Plus Jakarta Sans, sans-serif"),
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
                height=180,
                paper_bgcolor="rgba(255, 255, 255, 0.5)",
                plot_bgcolor="rgba(255, 255, 255, 0.5)",
                font=dict(color="#111111", family="Plus Jakarta Sans, sans-serif"),
                xaxis=dict(
                    title="Simulation Time (Units)",
                    title_font=dict(color="#555555", size=12),
                    tickfont=dict(color="#555555", size=11),
                    linecolor="rgba(0, 0, 0, 0.1)",
                    linewidth=1,
                    tickmode="linear",
                    tick0=0,
                    dtick=1 if summary["makespan"] <= 30 else max(1, summary["makespan"] // 20),
                    range=[0, summary["makespan"] + 0.3],
                    showgrid=True,
                    gridcolor="rgba(0, 0, 0, 0.04)",
                ),
                yaxis=dict(
                    showticklabels=False,
                    showgrid=False,
                    linecolor="rgba(0, 0, 0, 0.1)",
                ),
                margin=dict(l=16, r=16, t=10, b=42),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.05,
                    xanchor="left",
                    x=0,
                    font=dict(size=11, color="#111111"),
                ),
            )
            st.plotly_chart(fig_timeline, use_container_width=True)

            # Results Section: Table and Grouped Comparison Chart
            st.markdown(
                """
                <div style="margin-top: 28px;">
                    <div class="section-eyebrow">04 / Deep Dive</div>
                    <div class="section-headline">Task Analysis & Distribution</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

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

                    # Sky Blue for Waiting, Horizon Coral for Turnaround
                    fig_comp.add_trace(
                        go.Bar(
                            x=comp_df["Task ID"],
                            y=comp_df["Waiting Time"],
                            name="Waiting Time",
                            marker=dict(
                                color="#38BDF8",
                                line=dict(color="rgba(255, 255, 255, 0.8)", width=1.5),
                            ),
                            text=comp_df["Waiting Time"],
                            textposition="auto",
                            textfont=dict(color="#00293B", family="Plus Jakarta Sans"),
                        )
                    )
                    fig_comp.add_trace(
                        go.Bar(
                            x=comp_df["Task ID"],
                            y=comp_df["Turnaround Time"],
                            name="Turnaround Time",
                            marker=dict(
                                color="#FF5E3A",
                                line=dict(color="rgba(255, 255, 255, 0.8)", width=1.5),
                            ),
                            text=comp_df["Turnaround Time"],
                            textposition="auto",
                            textfont=dict(color="#FFFFFF", family="Plus Jakarta Sans"),
                        )
                    )

                    fig_comp.update_layout(
                        barmode="group",
                        height=290,
                        paper_bgcolor="rgba(255, 255, 255, 0.5)",
                        plot_bgcolor="rgba(255, 255, 255, 0.5)",
                        font=dict(color="#111111", family="Plus Jakarta Sans, sans-serif"),
                        xaxis=dict(
                            title="Task ID",
                            title_font=dict(color="#555555", size=12),
                            tickfont=dict(color="#555555", size=11),
                            linecolor="rgba(0, 0, 0, 0.1)",
                            linewidth=1,
                            showgrid=False,
                        ),
                        yaxis=dict(
                            title="Time Units",
                            title_font=dict(color="#555555", size=12),
                            tickfont=dict(color="#555555", size=11),
                            linecolor="rgba(0, 0, 0, 0.1)",
                            linewidth=1,
                            showgrid=True,
                            gridcolor="rgba(0, 0, 0, 0.04)",
                        ),
                        margin=dict(l=16, r=16, t=10, b=42),
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.04,
                            xanchor="right",
                            x=1,
                            font=dict(size=11, color="#111111"),
                        ),
                    )
                    st.plotly_chart(fig_comp, use_container_width=True)

        except Exception as sim_err:
            st.error(f"Error during simulation execution: {sim_err}")
else:
    if not st.session_state.sim_run:
        st.markdown(
            """
            <div class="horizon-empty">
                <div style="font-weight: 700; font-size: 1.15rem; color: #000000; margin-bottom: 6px;">
                    Ready to Simulate
                </div>
                <div style="font-size: 0.9rem; color: #555555; max-width: 480px; margin: 0 auto;">
                    Configure your task parameters above or click <b style="color: #FF5E3A;">Run Simulation</b> in the sidebar to visualize the execution timeline.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
