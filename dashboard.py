"""Planning Agent Performance Dashboard - Streamlit web dashboard for RL and tool metrics."""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from planning_agent.config import config
from planning_agent.services.feedback_service import (
    init_feedback_service,
    get_feedback_service,
)
from planning_agent.services.rl_service import (
    init_rl_service,
    get_rl_service,
)


def init_dashboard():
    """Initialize dashboard, feedback service, and RL service."""
    try:
        feedback_service = init_feedback_service(config.database_url)
        
        # Initialize RL service if enabled
        rl_service = None
        if config.rl_enabled:
            try:
                rl_service = init_rl_service(
                    feedback_service,
                    config.database_url,
                    exploration_rate=config.rl_exploration_rate,
                    learning_rate=config.rl_learning_rate,
                    discount_factor=config.rl_discount_factor,
                    min_samples=config.rl_min_samples
                )
            except Exception as e:
                # RL service initialization is optional
                pass
        
        return feedback_service, rl_service, True
    except Exception as e:
        st.error(f"[FAIL] Failed to initialize dashboard: {e}")
        return None, None, False


def format_time(ms: float) -> str:
    """Format milliseconds to human-readable time."""
    if ms < 1000:
        return f"{ms:.1f} ms"
    elif ms < 60000:
        return f"{ms/1000:.2f} s"
    else:
        return f"{ms/60000:.2f} min"


def run_dashboard():
    """Run the Streamlit dashboard."""
    st.set_page_config(
        page_title="Planning Agent Performance Dashboard",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Planning Agent Performance Dashboard")
    st.markdown("Oracle EPM Cloud Planning - Tool Performance & RL Analytics")
    st.markdown("---")
    
    # Initialize services
    feedback_service, rl_service, connected = init_dashboard()
    
    if not connected or not feedback_service:
        st.error("[FAIL] Failed to connect to database")
        st.info("""
        Please check:
        1. Your `.env` file has correct `DATABASE_URL`
        2. PostgreSQL database is running
        3. Database has been initialized: `python scripts/init_db.py`
        """)
        st.stop()
    
    st.success("[OK] Connected to database")
    
    # Show RL status
    if rl_service:
        st.info("🤖 Reinforcement Learning Engine: **Enabled**")
    else:
        st.warning("⚠️ Reinforcement Learning Engine: **Disabled** (Set RL_ENABLED=true in .env to enable)")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Time range filter
        time_range = st.selectbox(
            "Time Range",
            ["All Time", "Last 24 Hours", "Last 7 Days", "Last 30 Days"],
            index=0
        )
        
        # Tool filter
        st.subheader("Filters")
        show_all_tools = st.checkbox("Show All Tools", value=True)
        
        st.markdown("---")
        st.header("ℹ️ Info")
        st.info("""
        This dashboard shows:
        - Tool execution statistics
        - Success rates and performance
        - RL learning metrics
        - Q-values and policy insights
        """)
        
        if st.button("🔄 Refresh Data", type="primary"):
            st.cache_data.clear()
            st.rerun()
    
    # Get tool metrics
    metrics = feedback_service.get_tool_metrics()
    
    if not metrics:
        st.warning("No tool execution data available yet. Execute some tools to see metrics!")
        st.info("Try executing a tool via the API or MCP server to start collecting data.")
        st.stop()
    
    # Calculate aggregate statistics
    total_tools = len(metrics)
    total_calls = sum(m.get("total_calls", 0) for m in metrics)
    total_success = sum(int(m.get("success_rate", 0) * m.get("total_calls", 0)) for m in metrics)
    overall_success_rate = (total_success / total_calls * 100) if total_calls > 0 else 0
    avg_execution_time = sum(m.get("avg_execution_time_ms", 0) for m in metrics) / total_tools if total_tools > 0 else 0
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Tools", total_tools)
    
    with col2:
        st.metric("Total Executions", f"{total_calls:,}")
    
    with col3:
        st.metric(
            "Overall Success Rate",
            f"{overall_success_rate:.1f}%",
            delta=f"{overall_success_rate - 95:.1f}%" if overall_success_rate >= 95 else None
        )
    
    with col4:
        st.metric("Avg Execution Time", format_time(avg_execution_time))
    
    st.markdown("---")
    
    # Tool Metrics Table and Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Tool Performance Overview")
        
        # Prepare data for visualization
        df_metrics = pd.DataFrame(metrics)
        df_metrics = df_metrics.sort_values("total_calls", ascending=False)
        
        # Bar chart: Total calls per tool
        fig_calls = px.bar(
            df_metrics.head(15),
            x="tool_name",
            y="total_calls",
            title="Total Executions by Tool (Top 15)",
            labels={"tool_name": "Tool", "total_calls": "Total Calls"},
            color="total_calls",
            color_continuous_scale="Blues"
        )
        fig_calls.update_layout(
            height=400,
            xaxis_tickangle=-45,
            showlegend=False
        )
        st.plotly_chart(fig_calls, use_container_width=True)
    
    with col2:
        st.subheader("✅ Success Rate by Tool")
        
        # Success rate chart
        df_success = df_metrics.copy()
        df_success["success_rate_pct"] = df_success["success_rate"] * 100
        
        fig_success = px.bar(
            df_success.head(15),
            x="tool_name",
            y="success_rate_pct",
            title="Success Rate by Tool (Top 15)",
            labels={"tool_name": "Tool", "success_rate_pct": "Success Rate (%)"},
            color="success_rate_pct",
            color_continuous_scale="Greens",
            range_y=[0, 100]
        )
        fig_success.update_layout(
            height=400,
            xaxis_tickangle=-45,
            showlegend=False
        )
        st.plotly_chart(fig_success, use_container_width=True)
    
    st.markdown("---")
    
    # Execution Time Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⏱️ Execution Time Analysis")
        
        df_time = df_metrics.copy()
        fig_time = px.scatter(
            df_time.head(15),
            x="total_calls",
            y="avg_execution_time_ms",
            size="total_calls",
            color="success_rate",
            title="Execution Time vs Usage",
            labels={
                "total_calls": "Total Calls",
                "avg_execution_time_ms": "Avg Execution Time (ms)",
                "success_rate": "Success Rate"
            },
            color_continuous_scale="RdYlGn"
        )
        fig_time.update_layout(height=400)
        st.plotly_chart(fig_time, use_container_width=True)
    
    with col2:
        st.subheader("⭐ User Ratings")
        
        # Filter tools with ratings
        df_ratings = df_metrics[df_metrics["avg_user_rating"].notna()].copy()
        
        if len(df_ratings) > 0:
            fig_ratings = px.bar(
                df_ratings.head(15),
                x="tool_name",
                y="avg_user_rating",
                title="Average User Rating by Tool",
                labels={"tool_name": "Tool", "avg_user_rating": "Rating (1-5)"},
                color="avg_user_rating",
                color_continuous_scale="YlOrRd",
                range_y=[1, 5]
            )
            fig_ratings.update_layout(
                height=400,
                xaxis_tickangle=-45,
                showlegend=False
            )
            st.plotly_chart(fig_ratings, use_container_width=True)
        else:
            st.info("No user ratings available yet. Provide feedback via the API to see ratings!")
    
    st.markdown("---")
    
    # RL Metrics Section
    if rl_service:
        st.header("🤖 Reinforcement Learning Metrics")
        
        # Get RL metrics
        try:
            policy_dict = rl_service._get_policy_dict()
            total_policies = len(policy_dict)
            
            # Calculate average Q-value
            avg_q_value = sum(policy_dict.values()) / total_policies if total_policies > 0 else 0
            
            # Get episodes
            episodes = rl_service.get_successful_sequences(limit=100)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Policies", total_policies)
            
            with col2:
                st.metric("Avg Q-Value", f"{avg_q_value:.3f}")
            
            with col3:
                st.metric("Successful Episodes", len(episodes))
            
            with col4:
                exploration_rate = config.rl_exploration_rate
                st.metric("Exploration Rate", f"{exploration_rate*100:.1f}%")
            
            st.markdown("---")
            
            # Q-Value Distribution
            if total_policies > 0:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📈 Q-Value Distribution")
                    
                    q_values = list(policy_dict.values())
                    fig_q = px.histogram(
                        x=q_values,
                        title="Distribution of Q-Values",
                        labels={"x": "Q-Value", "y": "Count"},
                        nbins=30
                    )
                    fig_q.update_layout(height=400)
                    st.plotly_chart(fig_q, use_container_width=True)
                
                with col2:
                    st.subheader("🎯 Top Q-Values by Tool")
                    
                    # Group Q-values by tool
                    tool_q_values = {}
                    for key, value in policy_dict.items():
                        tool_name = key.split(":")[0]
                        if tool_name not in tool_q_values:
                            tool_q_values[tool_name] = []
                        tool_q_values[tool_name].append(value)
                    
                    # Calculate average Q-value per tool
                    tool_avg_q = {
                        tool: sum(values) / len(values)
                        for tool, values in tool_q_values.items()
                    }
                    
                    # Sort by average Q-value
                    sorted_tools = sorted(tool_avg_q.items(), key=lambda x: x[1], reverse=True)
                    
                    if sorted_tools:
                        df_q_tools = pd.DataFrame(
                            sorted_tools[:15],
                            columns=["tool_name", "avg_q_value"]
                        )
                        
                        fig_q_tools = px.bar(
                            df_q_tools,
                            x="tool_name",
                            y="avg_q_value",
                            title="Average Q-Value by Tool (Top 15)",
                            labels={"tool_name": "Tool", "avg_q_value": "Avg Q-Value"},
                            color="avg_q_value",
                            color_continuous_scale="Viridis"
                        )
                        fig_q_tools.update_layout(
                            height=400,
                            xaxis_tickangle=-45,
                            showlegend=False
                        )
                        st.plotly_chart(fig_q_tools, use_container_width=True)
            
            # Successful Sequences
            if episodes:
                st.subheader("🔄 Successful Tool Sequences")
                
                # Count sequence patterns
                sequence_counts = {}
                for episode in episodes:
                    sequence = tuple(episode.get("tool_sequence", []))
                    if sequence:
                        if sequence not in sequence_counts:
                            sequence_counts[sequence] = 0
                        sequence_counts[sequence] += 1
                
                # Display top sequences
                sorted_sequences = sorted(sequence_counts.items(), key=lambda x: x[1], reverse=True)
                
                for i, (sequence, count) in enumerate(sorted_sequences[:10], 1):
                    sequence_str = " → ".join(sequence)
                    st.text(f"{i}. {sequence_str} ({count} times)")
            
        except Exception as e:
            st.warning(f"Could not load RL metrics: {e}")
    
    # Detailed Metrics Table
    st.markdown("---")
    st.subheader("📋 Detailed Tool Metrics")
    
    # Prepare table data
    df_table = pd.DataFrame(metrics)
    df_table = df_table.sort_values("total_calls", ascending=False)
    df_table["success_rate_pct"] = (df_table["success_rate"] * 100).round(1)
    df_table["avg_time_formatted"] = df_table["avg_execution_time_ms"].apply(format_time)
    
    # Select columns for display
    display_cols = ["tool_name", "total_calls", "success_rate_pct", "avg_time_formatted", "avg_user_rating"]
    df_display = df_table[display_cols].copy()
    df_display.columns = ["Tool", "Total Calls", "Success Rate (%)", "Avg Time", "Avg Rating"]
    
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True
    )
    
    # Footer
    st.markdown("---")
    st.markdown("**Planning Agent Performance Dashboard** | Data from PostgreSQL database")
    st.markdown(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    run_dashboard()





