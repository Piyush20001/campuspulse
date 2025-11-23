"""
Performance Metrics Dashboard
Monitor response times, latency, and system performance
"""
import streamlit as st
import sys
import os
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from monitoring.performance_metrics import get_metrics_tracker
from database.feedback_db import get_user_role
from utils.navigation import create_top_navbar
from auth.session_manager import SessionManager

st.set_page_config(page_title="Performance Metrics - Campus Pulse", layout="wide")

# Initialize session manager
if 'session_manager' not in st.session_state:
    st.session_state.session_manager = SessionManager()

# Restore session from cookie if available
st.session_state.session_manager.restore_session_state()

# Set current page
st.session_state.current_page = 'Performance'

# Top navigation
create_top_navbar()

# Check if user is admin
is_admin = False
current_user_email = None

if 'user' in st.session_state and st.session_state.user:
    current_user_email = st.session_state.user.get('email', '')
    user_role = get_user_role(current_user_email)
    is_admin = (user_role == 'admin')

if not is_admin:
    st.error("Access Denied: This page is only accessible to administrators.")
    st.info("If you believe you should have admin access, please contact the system administrator.")
    st.stop()

# Performance Metrics Dashboard
st.markdown("# Performance Metrics Dashboard")
st.markdown(f"**Monitoring:** Response Time, Latency, Model Inference, and System Performance")

# Initialize metrics tracker
metrics_tracker = get_metrics_tracker()

# Time range selector
time_range = st.selectbox(
    "Time Range",
    ["Last Hour", "Last 6 Hours", "Last 24 Hours", "Last 7 Days"],
    index=2
)

hours_map = {
    "Last Hour": 1,
    "Last 6 Hours": 6,
    "Last 24 Hours": 24,
    "Last 7 Days": 168
}
hours = hours_map[time_range]

# Tabs for different metrics
tab1, tab2, tab3, tab4 = st.tabs([
    "Response Times",
    "API Latency",
    "Model Performance",
    "Database Queries"
])

# TAB 1: Response Times
with tab1:
    st.markdown("### Response Time Metrics")
    st.markdown("Tracks how long it takes for endpoints to respond to requests")

    # Get overall stats
    overall_stats = metrics_tracker.get_response_time_stats(hours=hours)

    if overall_stats.get('count', 0) > 0:
        # Summary metrics
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("Total Requests", f"{overall_stats['count']:,}")

        with col2:
            st.metric("Avg Response", f"{overall_stats['avg_ms']:.1f}ms")

        with col3:
            st.metric("Median Response", f"{overall_stats['median_ms']:.1f}ms")

        with col4:
            st.metric("95th Percentile", f"{overall_stats['p95_ms']:.1f}ms")

        with col5:
            st.metric("99th Percentile", f"{overall_stats['p99_ms']:.1f}ms")

        st.markdown("---")

        # Per-endpoint stats
        st.markdown("### Response Times by Endpoint")

        endpoint_stats = metrics_tracker.get_all_endpoint_stats(hours=hours)

        if endpoint_stats:
            # Create DataFrame for display
            df = pd.DataFrame(endpoint_stats)

            # Display table
            st.dataframe(
                df[['endpoint', 'count', 'avg_ms', 'median_ms', 'p95_ms', 'p99_ms']].round(2),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "endpoint": "Endpoint",
                    "count": st.column_config.NumberColumn("Requests", format="%d"),
                    "avg_ms": st.column_config.NumberColumn("Avg (ms)", format="%.1f"),
                    "median_ms": st.column_config.NumberColumn("Median (ms)", format="%.1f"),
                    "p95_ms": st.column_config.NumberColumn("P95 (ms)", format="%.1f"),
                    "p99_ms": st.column_config.NumberColumn("P99 (ms)", format="%.1f")
                }
            )

            # Bar chart of average response times
            fig = px.bar(
                df,
                x='endpoint',
                y='avg_ms',
                title='Average Response Time by Endpoint',
                labels={'endpoint': 'Endpoint', 'avg_ms': 'Avg Response Time (ms)'},
                color='avg_ms',
                color_continuous_scale='RdYlGn_r'
            )
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No response time data available for the selected time range.")

# TAB 2: API Latency
with tab2:
    st.markdown("### API Call Latency")
    st.markdown("Measures the time taken for API operations and data retrievals")

    # Get API latency data from database
    import sqlite3
    conn = sqlite3.connect(metrics_tracker.db_path)
    cursor = conn.cursor()

    since_time = (datetime.now() - timedelta(hours=hours)).isoformat()

    cursor.execute("""
        SELECT operation, latency_ms, timestamp
        FROM api_latency
        WHERE timestamp >= ?
        ORDER BY timestamp DESC
    """, (since_time,))

    latency_data = cursor.fetchall()
    conn.close()

    if latency_data:
        # Calculate stats per operation
        operations = {}
        for op, latency, _ in latency_data:
            if op not in operations:
                operations[op] = []
            operations[op].append(latency)

        # Display metrics
        if operations:
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total API Calls", len(latency_data))

            with col2:
                all_latencies = [l for l in [lat for _, lat, _ in latency_data]]
                avg_latency = sum(all_latencies) / len(all_latencies)
                st.metric("Avg Latency", f"{avg_latency:.1f}ms")

            with col3:
                max_latency = max(all_latencies)
                st.metric("Max Latency", f"{max_latency:.1f}ms")

            st.markdown("---")

            # Per-operation stats
            st.markdown("### Latency by Operation")

            op_stats = []
            for op, latencies in operations.items():
                op_stats.append({
                    'operation': op,
                    'count': len(latencies),
                    'avg_ms': sum(latencies) / len(latencies),
                    'min_ms': min(latencies),
                    'max_ms': max(latencies)
                })

            df_ops = pd.DataFrame(op_stats)
            st.dataframe(
                df_ops.round(2),
                use_container_width=True,
                hide_index=True
            )

            # Timeline chart
            df_timeline = pd.DataFrame(latency_data, columns=['operation', 'latency_ms', 'timestamp'])
            df_timeline['timestamp'] = pd.to_datetime(df_timeline['timestamp'])

            fig = px.scatter(
                df_timeline,
                x='timestamp',
                y='latency_ms',
                color='operation',
                title='API Latency Over Time',
                labels={'timestamp': 'Time', 'latency_ms': 'Latency (ms)'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No API latency data available for the selected time range.")

# TAB 3: Model Performance
with tab3:
    st.markdown("### ML Model Inference Performance")
    st.markdown("Tracks inference times for LSTM crowd forecasting and event classification models")

    # Get model performance data
    model_stats = metrics_tracker.get_model_performance_stats(hours=hours)

    if model_stats:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Inferences", model_stats.get('count', 0))

        with col2:
            st.metric("Total Predictions", model_stats.get('total_predictions', 0))

        with col3:
            st.metric("Avg Inference Time", f"{model_stats.get('avg_inference_ms', 0):.1f}ms")

        with col4:
            st.metric("Max Inference Time", f"{model_stats.get('max_inference_ms', 0):.1f}ms")

        st.markdown("---")

        # Get per-model stats from database
        conn = sqlite3.connect(metrics_tracker.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT model_name, inference_time_ms, num_predictions, timestamp
            FROM model_inference
            WHERE timestamp >= ?
            ORDER BY timestamp DESC
        """, (since_time,))

        model_data = cursor.fetchall()
        conn.close()

        if model_data:
            # Group by model
            models = {}
            for model_name, inf_time, num_preds, _ in model_data:
                if model_name not in models:
                    models[model_name] = []
                models[model_name].append(inf_time)

            # Stats by model
            st.markdown("### Performance by Model")

            model_stats_list = []
            for model, times in models.items():
                model_stats_list.append({
                    'model': model,
                    'inferences': len(times),
                    'avg_ms': sum(times) / len(times),
                    'min_ms': min(times),
                    'max_ms': max(times)
                })

            df_models = pd.DataFrame(model_stats_list)
            st.dataframe(
                df_models.round(2),
                use_container_width=True,
                hide_index=True
            )

    else:
        st.info("No model performance data available for the selected time range.")

# TAB 4: Database Queries
with tab4:
    st.markdown("### Database Query Performance")
    st.markdown("Monitors execution times for database operations")

    # Get database query stats
    conn = sqlite3.connect(metrics_tracker.db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT query_type, execution_time_ms, rows_affected, timestamp
        FROM db_queries
        WHERE timestamp >= ?
        ORDER BY timestamp DESC
    """, (since_time,))

    db_data = cursor.fetchall()
    conn.close()

    if db_data:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Queries", len(db_data))

        with col2:
            avg_exec = sum(row[1] for row in db_data) / len(db_data)
            st.metric("Avg Execution Time", f"{avg_exec:.1f}ms")

        with col3:
            total_rows = sum(row[2] for row in db_data)
            st.metric("Total Rows Affected", total_rows)

        st.markdown("---")

        # Group by query type
        query_types = {}
        for query_type, exec_time, rows, _ in db_data:
            if query_type not in query_types:
                query_types[query_type] = []
            query_types[query_type].append(exec_time)

        # Stats by query type
        st.markdown("### Performance by Query Type")

        query_stats = []
        for q_type, times in query_types.items():
            query_stats.append({
                'query_type': q_type,
                'count': len(times),
                'avg_ms': sum(times) / len(times),
                'min_ms': min(times),
                'max_ms': max(times)
            })

        df_queries = pd.DataFrame(query_stats)
        st.dataframe(
            df_queries.round(2),
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No database query data available for the selected time range.")

# Footer
st.markdown("---")
st.caption(f"Performance Metrics Dashboard | Logged in as {current_user_email}")
st.caption("Data is automatically cleaned up after 7 days")
