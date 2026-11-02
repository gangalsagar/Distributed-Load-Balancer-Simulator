from typing import Any, Dict, List

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from metrics import (
    calculate_metrics_summary,
    identify_idle_intervals,
    run_algorithm_comparison,
)
from schedulers.fcfs import fcfs_schedule
from schedulers.round_robin import round_robin_schedule
from schedulers.sjf import sjf_schedule
from task_manager import generate_sample_tasks, validate_tasks

st.set_page_config(
    page_title="Distributed Load Balancer Simulator",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(
    '\n    <style>\n    /* Global Base */\n    .stApp {\n        background-color: #FFFFFF;\n        color: #111111;\n        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;\n    }\n\n    /* Headings */\n    h1, h2, h3, h4, h5, h6 {\n        color: #111111 !important;\n        font-weight: 600 !important;\n        letter-spacing: -0.01em;\n    }\n\n    /* Compact Header */\n    .app-header {\n        border-bottom: 1px solid #111111;\n        padding-bottom: 12px;\n        margin-bottom: 24px;\n    }\n    .app-title {\n        font-size: 1.5rem;\n        font-weight: 700;\n        color: #111111;\n        margin: 0;\n        line-height: 1.2;\n    }\n    .app-subtitle {\n        font-size: 0.9rem;\n        color: #444444;\n        margin: 4px 0 0 0;\n    }\n\n    /* Metric Cards: clean rectangular with thin border */\n    .kpi-card {\n        border: 1px solid #111111;\n        border-radius: 4px;\n        padding: 14px 16px;\n        background-color: #FFFFFF;\n        text-align: left;\n    }\n    .kpi-label {\n        font-size: 0.75rem;\n        text-transform: uppercase;\n        letter-spacing: 0.05em;\n        color: #555555;\n        font-weight: 600;\n    }\n    .kpi-value {\n        font-size: 1.6rem;\n        font-weight: 700;\n        color: #111111;\n        margin-top: 4px;\n    }\n\n    /* Section Subheadings */\n    .section-title {\n        font-size: 1.05rem;\n        font-weight: 600;\n        color: #111111;\n        margin-top: 20px;\n        margin-bottom: 10px;\n        border-bottom: 1px solid #E5E7EB;\n        padding-bottom: 4px;\n    }\n\n    /* Primary and Secondary Buttons */\n    button[kind="primary"] {\n        background-color: #2563EB !important;\n        color: #FFFFFF !important;\n        border: 1px solid #2563EB !important;\n        border-radius: 4px !important;\n        font-weight: 600 !important;\n    }\n    button[kind="primary"]:hover {\n        background-color: #1D4ED8 !important;\n        border-color: #1D4ED8 !important;\n    }\n\n    button[kind="secondary"] {\n        background-color: #FFFFFF !important;\n        color: #111111 !important;\n        border: 1px solid #111111 !important;\n        border-radius: 4px !important;\n    }\n    button[kind="secondary"]:hover {\n        background-color: #F8FAFC !important;\n        border-color: #2563EB !important;\n        color: #2563EB !important;\n    }\n\n    /* Empty state box */\n    .empty-state {\n        border: 1px dashed #999999;\n        border-radius: 4px;\n        padding: 24px;\n        text-align: center;\n        color: #444444;\n        background-color: #FAFAFA;\n        margin-top: 16px;\n    }\n\n    /* Comparison highlight badge */\n    .best-badge {\n        background-color: #EFF6FF;\n        color: #1D4ED8;\n        border: 1px solid #2563EB;\n        padding: 2px 6px;\n        border-radius: 4px;\n        font-size: 0.8rem;\n        font-weight: 600;\n    }\n    </style>\n    ',
    unsafe_allow_html=True,
)


def get_default_tasks_df() -> pd.DataFrame:
    sample = generate_sample_tasks()
    return pd.DataFrame(
        [
            {
                "Task ID": t["task_id"],
                "Arrival Time": t["arrival_time"],
                "Burst Time": t["burst_time"],
            }
            for t in sample
        ]
    )


if "tasks_df" not in st.session_state:
    st.session_state.tasks_df = get_default_tasks_df()
if "sim_run" not in st.session_state:
    st.session_state.sim_run = False
with st.sidebar:
    st.markdown("### Navigation")
    app_mode = st.radio(
        "Select Mode",
        options=["Individual Simulation", "Algorithm Comparison"],
        index=0,
        help="Run a single scheduling algorithm or compare RR, FCFS, and SJF side-by-side on the same workload.",
    )
    st.markdown(
        "<hr style='border: none; border-top: 1px solid #E5E7EB; margin: 16px 0;'>",
        unsafe_allow_html=True,
    )
    st.markdown("### Controls")
    if app_mode == "Individual Simulation":
        algorithm = st.selectbox(
            "Scheduling Algorithm",
            options=[
                "Round Robin (RR)",
                "First Come, First Served (FCFS)",
                "Shortest Job First (SJF — Non-Preemptive)",
            ],
            index=0,
            help="Select CPU scheduler. RR is preemptive; FCFS and SJF are non-preemptive.",
        )
        if algorithm == "Round Robin (RR)":
            time_quantum = st.number_input(
                "Time Quantum (q)",
                min_value=1,
                max_value=100,
                value=2,
                step=1,
                help="Positive integer time slice allocated per execution slice.",
            )
        else:
            time_quantum = None
    else:
        time_quantum = st.number_input(
            "Round Robin Quantum (q)",
            min_value=1,
            max_value=100,
            value=2,
            step=1,
            help="Time quantum applied to Round Robin during the side-by-side comparison.",
        )
        algorithm = None
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    btn_label = (
        "Run Simulation" if app_mode == "Individual Simulation" else "Run Comparison"
    )
    if st.button(btn_label, type="primary", use_container_width=True):
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
    st.markdown(
        "<hr style='border: none; border-top: 1px solid #E5E7EB; margin: 20px 0;'>",
        unsafe_allow_html=True,
    )
    st.caption("OS Mini-Project · CPU Scheduling Simulator")
st.markdown(
    '\n    <div class="app-header">\n        <h1 class="app-title">Distributed Load Balancer Simulator</h1>\n        <p class="app-subtitle">Single-node CPU scheduling and performance analysis</p>\n    </div>\n    ',
    unsafe_allow_html=True,
)
if app_mode == "Individual Simulation":
    if algorithm == "First Come, First Served (FCFS)":
        st.info(
            "**FCFS:** Executes tasks in arrival order. It is non-preemptive, so a task runs until completion once execution begins."
        )
    elif algorithm == "Shortest Job First (SJF — Non-Preemptive)":
        st.info(
            "**SJF (Non-Preemptive):** At each scheduling decision, selects the available arrived task with the smallest burst time. Once execution begins, the task runs to completion without preemption."
        )
    else:
        st.info(
            "**Round Robin:** Gives tasks CPU time in turns using a configurable time quantum. Tasks that are not finished return to the ready queue."
        )
else:
    st.info(
        "**Algorithm Comparison:** Executes Round Robin, FCFS, and SJF against the **exact same workload** and compares their metrics, Gantt timelines, and CPU utilization fairly side-by-side."
    )
st.markdown(
    '<div class="section-title">Workload Configuration</div>', unsafe_allow_html=True
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
validated_tasks: List[Dict[str, Any]] = []
validation_error: str = ""
try:
    raw_records = edited_df.to_dict("records")
    clean_records: List[Dict[str, Any]] = []
    for r in raw_records:
        task_id = (
            str(r.get("Task ID", "")).strip() if r.get("Task ID") is not None else ""
        )
        arr_val = r.get("Arrival Time")
        burst_val = r.get("Burst Time")
        if not task_id and arr_val is None and (burst_val is None):
            continue
        if not task_id:
            raise ValueError("Task ID cannot be empty.")
        if arr_val is None or pd.isna(arr_val):
            raise ValueError(f"Task '{task_id}' has missing Arrival Time.")
        if burst_val is None or pd.isna(burst_val):
            raise ValueError(f"Task '{task_id}' has missing Burst Time.")
        clean_records.append(
            {
                "task_id": task_id,
                "arrival_time": int(arr_val),
                "burst_time": int(burst_val),
            }
        )
    if clean_records:
        validate_tasks(clean_records)
    validated_tasks = clean_records
except Exception as e:
    validation_error = str(e)
if validation_error:
    st.error(f"Input validation error: {validation_error}")


def create_gantt_figure(slices: List[Dict[str, Any]], makespan: int) -> go.Figure:
    idle_slices = identify_idle_intervals(slices)
    all_items = []
    for s in slices:
        all_items.append(
            {
                "Task ID": s["task_id"],
                "Start": s["start_time"],
                "End": s["end_time"],
                "Duration": s["duration"],
                "Is Idle": False,
            }
        )
    for idle in idle_slices:
        all_items.append(
            {
                "Task ID": "Idle",
                "Start": idle["start_time"],
                "End": idle["end_time"],
                "Duration": idle["duration"],
                "Is Idle": True,
            }
        )
    all_items.sort(key=lambda x: x["Start"])
    unique_tasks = sorted(list(set((s["task_id"] for s in slices))))
    blue_shades = ["#2563EB", "#1D4ED8", "#3B82F6", "#60A5FA", "#1E40AF", "#93C5FD"]
    color_map = {
        tid: blue_shades[i % len(blue_shades)] for i, tid in enumerate(unique_tasks)
    }
    fig = go.Figure()
    for item in all_items:
        tid = item["Task ID"]
        is_idle = item["Is Idle"]
        if is_idle:
            bar_color = "#FFFFFF"
            border_color = "#111111"
            text_color = "#111111"
            label = f"Idle [{item['Start']}-{item['End']}]"
        else:
            bar_color = color_map.get(tid, "#2563EB")
            border_color = "#111111"
            text_color = "#FFFFFF"
            label = f"{tid} [{item['Start']}-{item['End']}]"
        fig.add_trace(
            go.Bar(
                name=tid,
                y=["CPU"],
                x=[item["Duration"]],
                base=[item["Start"]],
                orientation="h",
                marker=dict(color=bar_color, line=dict(color=border_color, width=1.5)),
                text=label,
                textposition="inside",
                insidetextanchor="middle",
                textfont=dict(color=text_color, size=11, family="sans-serif"),
                hovertemplate=f"<b>{('Task ' + tid if not is_idle else 'CPU Idle')}</b><br>Start Time: {item['Start']}<br>End Time: {item['End']}<br>Duration: {item['Duration']} units<extra></extra>",
                showlegend=item["Start"]
                == min((x["Start"] for x in all_items if x["Task ID"] == tid)),
            )
        )
    fig.update_layout(
        barmode="stack",
        height=140,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(color="#111111", family="sans-serif"),
        xaxis=dict(
            title="Simulation Time (Units)",
            title_font=dict(color="#111111", size=11),
            tickfont=dict(color="#111111", size=10),
            linecolor="#111111",
            linewidth=1,
            tickmode="linear",
            tick0=0,
            dtick=1 if makespan <= 25 else max(1, makespan // 15),
            range=[0, makespan + 0.2 if makespan > 0 else 1],
            showgrid=True,
            gridcolor="#F3F4F6",
        ),
        yaxis=dict(
            showticklabels=False, linecolor="#111111", linewidth=1, showgrid=False
        ),
        margin=dict(l=10, r=10, t=10, b=35),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="left",
            x=0,
            font=dict(size=10, color="#111111"),
        ),
    )
    return fig


if st.session_state.sim_run and (not validation_error):
    if not validated_tasks:
        st.warning(
            "No tasks configured. Please enter at least one task or click 'Load Sample'."
        )
    elif app_mode == "Individual Simulation":
        try:
            if algorithm == "Round Robin (RR)":
                slices, metrics = round_robin_schedule(
                    validated_tasks, time_quantum=int(time_quantum)
                )
            elif algorithm == "First Come, First Served (FCFS)":
                slices, metrics = fcfs_schedule(validated_tasks)
            else:
                slices, metrics = sjf_schedule(validated_tasks)
            summary = calculate_metrics_summary(metrics, slices)
            st.markdown(
                '<div class="section-title">Performance Summary</div>',
                unsafe_allow_html=True,
            )
            k1, k2, k3, k4 = st.columns(4)
            with k1:
                st.markdown(
                    f"""\n                    <div class="kpi-card">\n                        <div class="kpi-label">Tasks Scheduled</div>\n                        <div class="kpi-value">{summary["total_tasks"]}</div>\n                    </div>\n                    """,
                    unsafe_allow_html=True,
                )
            with k2:
                st.markdown(
                    f"""\n                    <div class="kpi-card">\n                        <div class="kpi-label">Average Waiting Time</div>\n                        <div class="kpi-value">{summary["avg_waiting_time"]:.2f} <span style="font-size:0.9rem; font-weight:normal; color:#555555;">units</span></div>\n                    </div>\n                    """,
                    unsafe_allow_html=True,
                )
            with k3:
                st.markdown(
                    f"""\n                    <div class="kpi-card">\n                        <div class="kpi-label">Average Turnaround Time</div>\n                        <div class="kpi-value">{summary["avg_turnaround_time"]:.2f} <span style="font-size:0.9rem; font-weight:normal; color:#555555;">units</span></div>\n                    </div>\n                    """,
                    unsafe_allow_html=True,
                )
            with k4:
                st.markdown(
                    f"""\n                    <div class="kpi-card">\n                        <div class="kpi-label">Makespan</div>\n                        <div class="kpi-value">{summary["makespan"]} <span style="font-size:0.9rem; font-weight:normal; color:#555555;">units</span></div>\n                    </div>\n                    """,
                    unsafe_allow_html=True,
                )
            st.markdown(
                '<div class="section-title">CPU Execution Timeline</div>',
                unsafe_allow_html=True,
            )
            fig_timeline = create_gantt_figure(slices, summary["makespan"])
            st.plotly_chart(fig_timeline, use_container_width=True)
            st.markdown(
                '<div class="section-title">Task Results & Comparison</div>',
                unsafe_allow_html=True,
            )
            col_tbl, col_plot = st.columns([1, 1], gap="medium")
            with col_tbl:
                results_rows = []
                for tid in sorted(metrics.keys()):
                    m = metrics[tid]
                    results_rows.append(
                        {
                            "Task ID": m["task_id"],
                            "Arrival": m["arrival_time"],
                            "Burst": m["burst_time"],
                            "Completion": m["completion_time"],
                            "Waiting Time": m["waiting_time"],
                            "Turnaround Time": m["turnaround_time"],
                        }
                    )
                results_df = pd.DataFrame(results_rows)
                st.dataframe(results_df, use_container_width=True, hide_index=True)
            with col_plot:
                if results_rows:
                    comp_df = pd.DataFrame(results_rows)
                    fig_comp = go.Figure()
                    fig_comp.add_trace(
                        go.Bar(
                            x=comp_df["Task ID"],
                            y=comp_df["Waiting Time"],
                            name="Waiting Time",
                            marker=dict(
                                color="#FFFFFF", line=dict(color="#111111", width=1.5)
                            ),
                            text=comp_df["Waiting Time"],
                            textposition="auto",
                            textfont=dict(color="#111111"),
                        )
                    )
                    fig_comp.add_trace(
                        go.Bar(
                            x=comp_df["Task ID"],
                            y=comp_df["Turnaround Time"],
                            name="Turnaround Time",
                            marker=dict(
                                color="#2563EB", line=dict(color="#111111", width=1.5)
                            ),
                            text=comp_df["Turnaround Time"],
                            textposition="auto",
                            textfont=dict(color="#FFFFFF"),
                        )
                    )
                    fig_comp.update_layout(
                        barmode="group",
                        height=280,
                        paper_bgcolor="#FFFFFF",
                        plot_bgcolor="#FFFFFF",
                        font=dict(color="#111111", family="sans-serif"),
                        xaxis=dict(
                            title="Task ID",
                            title_font=dict(color="#111111", size=12),
                            tickfont=dict(color="#111111", size=11),
                            linecolor="#111111",
                            linewidth=1,
                            showgrid=False,
                        ),
                        yaxis=dict(
                            title="Time Units",
                            title_font=dict(color="#111111", size=12),
                            tickfont=dict(color="#111111", size=11),
                            linecolor="#111111",
                            linewidth=1,
                            showgrid=True,
                            gridcolor="#F3F4F6",
                        ),
                        margin=dict(l=10, r=10, t=10, b=40),
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1,
                            font=dict(size=11, color="#111111"),
                        ),
                    )
                    st.plotly_chart(fig_comp, use_container_width=True)
        except Exception as sim_err:
            st.error(f"Error during simulation execution: {sim_err}")
    else:
        try:
            comparison_results = run_algorithm_comparison(
                validated_tasks, time_quantum=int(time_quantum)
            )
            comp_rows = comparison_results["comparison_rows"]
            best = comparison_results["best_performers"]
            algos_data = comparison_results["algorithms"]
            st.markdown(
                '<div class="section-title">Comparative Performance Overview</div>',
                unsafe_allow_html=True,
            )
            comp_df = pd.DataFrame(comp_rows)
            st.dataframe(
                comp_df.style.format(
                    {
                        "Avg Waiting Time": "{:.2f}",
                        "Avg Turnaround Time": "{:.2f}",
                        "Makespan": "{:d}",
                        "CPU Utilization (%)": "{:.2f}%",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )
            st.markdown(
                '<div class="section-title">Automated Performance Summary</div>',
                unsafe_allow_html=True,
            )

            def format_winners(names: List[str]) -> str:
                return ", ".join(names) if len(names) > 1 else names[0]

            wait_str = format_winners(best["lowest_waiting"]) + (
                " (Tied)" if len(best["lowest_waiting"]) > 1 else ""
            )
            tat_str = format_winners(best["lowest_turnaround"]) + (
                " (Tied)" if len(best["lowest_turnaround"]) > 1 else ""
            )
            span_str = format_winners(best["shortest_makespan"]) + (
                " (Tied)" if len(best["shortest_makespan"]) > 1 else ""
            )
            util_str = format_winners(best["highest_utilization"]) + (
                " (Tied)" if len(best["highest_utilization"]) > 1 else ""
            )
            st.markdown(
                f"""\n                <div style="background-color: #F8FAFC; border: 1px solid #111111; border-radius: 4px; padding: 16px; margin-bottom: 20px;">\n                    <ul style="margin: 0; padding-left: 20px; line-height: 1.8;">\n                        <li><b>Lowest Average Waiting Time:</b> <span class="best-badge">{wait_str}</span> ({(comp_rows[0]["Avg Waiting Time"] if len(best["lowest_waiting"]) == 3 else min((r["Avg Waiting Time"] for r in comp_rows))):.2f} units)</li>\n                        <li><b>Lowest Average Turnaround Time:</b> <span class="best-badge">{tat_str}</span> ({min((r["Avg Turnaround Time"] for r in comp_rows)):.2f} units)</li>\n                        <li><b>Shortest Makespan:</b> <span class="best-badge">{span_str}</span> ({min((r["Makespan"] for r in comp_rows))} units)</li>\n                        <li><b>Highest CPU Utilization:</b> <span class="best-badge">{util_str}</span> ({max((r["CPU Utilization (%)"] for r in comp_rows)):.2f}%)</li>\n                    </ul>\n                    <p style="margin: 12px 0 0 0; font-size: 0.85rem; color: #444444;">\n                        <i>Note: Scheduling performance is heavily workload-dependent and influenced by the Round Robin quantum ($q={time_quantum}$). Shortest Job First typically minimizes average waiting time when burst variances are high, while Round Robin provides fair CPU sharing.</i>\n                    </p>\n                </div>\n                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="section-title">Comparative Metric Charts</div>',
                unsafe_allow_html=True,
            )
            chart_col1, chart_col2 = st.columns(2)
            chart_algos = comp_df["Algorithm"].tolist()
            with chart_col1:
                fig_wait = go.Figure(
                    go.Bar(
                        x=chart_algos,
                        y=comp_df["Avg Waiting Time"],
                        marker=dict(
                            color="#2563EB", line=dict(color="#111111", width=1.5)
                        ),
                        text=comp_df["Avg Waiting Time"].apply(lambda v: f"{v:.2f}"),
                        textposition="auto",
                    )
                )
                fig_wait.update_layout(
                    title="Average Waiting Time (Lower is Better)",
                    title_font=dict(size=13, color="#111111"),
                    height=240,
                    paper_bgcolor="#FFFFFF",
                    plot_bgcolor="#FFFFFF",
                    font=dict(color="#111111", family="sans-serif"),
                    xaxis=dict(linecolor="#111111", linewidth=1, showgrid=False),
                    yaxis=dict(
                        title="Time Units",
                        linecolor="#111111",
                        linewidth=1,
                        showgrid=True,
                        gridcolor="#F3F4F6",
                    ),
                    margin=dict(l=10, r=10, t=35, b=20),
                )
                st.plotly_chart(fig_wait, use_container_width=True)
            with chart_col2:
                fig_tat = go.Figure(
                    go.Bar(
                        x=chart_algos,
                        y=comp_df["Avg Turnaround Time"],
                        marker=dict(
                            color="#3B82F6", line=dict(color="#111111", width=1.5)
                        ),
                        text=comp_df["Avg Turnaround Time"].apply(lambda v: f"{v:.2f}"),
                        textposition="auto",
                    )
                )
                fig_tat.update_layout(
                    title="Average Turnaround Time (Lower is Better)",
                    title_font=dict(size=13, color="#111111"),
                    height=240,
                    paper_bgcolor="#FFFFFF",
                    plot_bgcolor="#FFFFFF",
                    font=dict(color="#111111", family="sans-serif"),
                    xaxis=dict(linecolor="#111111", linewidth=1, showgrid=False),
                    yaxis=dict(
                        title="Time Units",
                        linecolor="#111111",
                        linewidth=1,
                        showgrid=True,
                        gridcolor="#F3F4F6",
                    ),
                    margin=dict(l=10, r=10, t=35, b=20),
                )
                st.plotly_chart(fig_tat, use_container_width=True)
            chart_col3, chart_col4 = st.columns(2)
            with chart_col3:
                fig_span = go.Figure(
                    go.Bar(
                        x=chart_algos,
                        y=comp_df["Makespan"],
                        marker=dict(
                            color="#1D4ED8", line=dict(color="#111111", width=1.5)
                        ),
                        text=comp_df["Makespan"],
                        textposition="auto",
                    )
                )
                fig_span.update_layout(
                    title="Makespan / Total Duration",
                    title_font=dict(size=13, color="#111111"),
                    height=240,
                    paper_bgcolor="#FFFFFF",
                    plot_bgcolor="#FFFFFF",
                    font=dict(color="#111111", family="sans-serif"),
                    xaxis=dict(linecolor="#111111", linewidth=1, showgrid=False),
                    yaxis=dict(
                        title="Time Units",
                        linecolor="#111111",
                        linewidth=1,
                        showgrid=True,
                        gridcolor="#F3F4F6",
                    ),
                    margin=dict(l=10, r=10, t=35, b=20),
                )
                st.plotly_chart(fig_span, use_container_width=True)
            with chart_col4:
                fig_util = go.Figure(
                    go.Bar(
                        x=chart_algos,
                        y=comp_df["CPU Utilization (%)"],
                        marker=dict(
                            color="#60A5FA", line=dict(color="#111111", width=1.5)
                        ),
                        text=comp_df["CPU Utilization (%)"].apply(
                            lambda v: f"{v:.1f}%"
                        ),
                        textposition="auto",
                    )
                )
                fig_util.update_layout(
                    title="CPU Utilization (%)",
                    title_font=dict(size=13, color="#111111"),
                    height=240,
                    paper_bgcolor="#FFFFFF",
                    plot_bgcolor="#FFFFFF",
                    font=dict(color="#111111", family="sans-serif"),
                    xaxis=dict(linecolor="#111111", linewidth=1, showgrid=False),
                    yaxis=dict(
                        title="Percentage (%)",
                        range=[0, 105],
                        linecolor="#111111",
                        linewidth=1,
                        showgrid=True,
                        gridcolor="#F3F4F6",
                    ),
                    margin=dict(l=10, r=10, t=35, b=20),
                )
                st.plotly_chart(fig_util, use_container_width=True)
            st.markdown(
                '<div class="section-title">Execution Timelines (Gantt Comparison)</div>',
                unsafe_allow_html=True,
            )
            max_span = max((r["Makespan"] for r in comp_rows))
            tab_rr, tab_fcfs, tab_sjf = st.tabs(
                [
                    "Round Robin (RR)",
                    "First Come, First Served (FCFS)",
                    "Shortest Job First (SJF)",
                ]
            )
            with tab_rr:
                fig_rr = create_gantt_figure(
                    algos_data["Round Robin (RR)"]["slices"], max_span
                )
                st.plotly_chart(fig_rr, use_container_width=True, key="gantt_comp_rr")
            with tab_fcfs:
                fig_fcfs = create_gantt_figure(
                    algos_data["First Come, First Served (FCFS)"]["slices"], max_span
                )
                st.plotly_chart(
                    fig_fcfs, use_container_width=True, key="gantt_comp_fcfs"
                )
            with tab_sjf:
                fig_sjf = create_gantt_figure(
                    algos_data["Shortest Job First (SJF)"]["slices"], max_span
                )
                st.plotly_chart(fig_sjf, use_container_width=True, key="gantt_comp_sjf")
        except Exception as comp_err:
            st.error(f"Error during algorithm comparison execution: {comp_err}")
elif not st.session_state.sim_run:
    prompt_text = (
        "Run Simulation" if app_mode == "Individual Simulation" else "Run Comparison"
    )
    st.markdown(
        f'\n            <div class="empty-state">\n                <p style="margin: 0; font-weight: 500; font-size: 1rem; color: #111111;">Ready to Simulate</p>\n                <p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #555555;">\n                    Configure the task workload above and click <b>{prompt_text}</b> in the sidebar to execute.\n                </p>\n            </div>\n            ',
        unsafe_allow_html=True,
    )
