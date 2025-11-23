"""
Admin Panel - Feedback Management & Role Assignment
Only accessible to admin users
"""
import streamlit as st
import sys
import os
import pandas as pd
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.feedback_db import (
    get_all_feedback,
    get_organizer_requests,
    approve_organizer_request,
    reject_organizer_request,
    get_all_users_with_roles,
    grant_role,
    update_feedback_status,
    get_user_role
)
from utils.navigation import create_top_navbar
from auth.session_manager import SessionManager
from monitoring.performance_metrics import get_metrics_tracker
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta
import sqlite3

st.set_page_config(page_title="Admin Panel - Campus Pulse", layout="wide")

# Initialize session manager
if 'session_manager' not in st.session_state:
    st.session_state.session_manager = SessionManager()

# Restore session from cookie if available
st.session_state.session_manager.restore_session_state()

# Set current page
st.session_state.current_page = 'Admin'

# Top navigation
create_top_navbar()

# Admin panel styling
st.markdown("""
<style>
    .admin-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
    }

    .stat-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        border: 1px solid rgba(0,33,165,0.1);
    }

    .feedback-card {
        background: rgba(255,255,255,0.02);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #0021A5;
    }

    .request-card {
        background: rgba(255,165,0,0.1);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #FFA500;
    }
</style>
""", unsafe_allow_html=True)

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

# Admin Panel Header
st.markdown('<h1 class="admin-header">Admin Panel</h1>', unsafe_allow_html=True)
st.markdown(f"Welcome, **{st.session_state.user.get('full_name', 'Admin')}**")

# Tabs for different admin functions
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Dashboard", "Feedback Management", "Organizer Requests", "User Roles", "Performance Metrics"])

# TAB 1: Dashboard
with tab1:
    st.markdown("### Admin Dashboard")

    # Get statistics
    all_feedback = get_all_feedback()
    pending_feedback = get_all_feedback(status='pending')
    all_requests = get_organizer_requests()
    pending_requests = get_organizer_requests(status='pending')
    all_users = get_all_users_with_roles()

    # Stats cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.metric("Total Feedback", len(all_feedback))
        st.caption(f"{len(pending_feedback)} pending")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.metric("Organizer Requests", len(all_requests))
        st.caption(f"{len(pending_requests)} pending")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        organizers = len([u for u in all_users if u['role'] == 'organizer'])
        st.metric("Organizers", organizers)
        st.caption("Event creators")
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        admins = len([u for u in all_users if u['role'] == 'admin'])
        st.metric("Admins", admins)
        st.caption("System administrators")
        st.markdown('</div>', unsafe_allow_html=True)

    # Recent feedback overview
    if all_feedback:
        st.markdown("### Recent Feedback")
        avg_rating = sum(f['rating'] for f in all_feedback) / len(all_feedback)
        st.metric("Average Rating", f"{avg_rating:.2f}/5")

        # Feedback by category
        categories = {}
        for f in all_feedback:
            cat = f['category']
            categories[cat] = categories.get(cat, 0) + 1

        st.markdown("**Feedback by Category:**")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            st.write(f"- {cat.replace('_', ' ').title()}: {count}")

# TAB 2: Feedback Management
with tab2:
    st.markdown("### User Feedback")

    filter_status = st.selectbox(
        "Filter by status",
        ["All", "Pending", "Reviewed", "Resolved"],
        key="feedback_filter"
    )

    if filter_status == "All":
        feedback_list = all_feedback
    else:
        feedback_list = get_all_feedback(status=filter_status.lower())

    if not feedback_list:
        st.info(f"No {filter_status.lower()} feedback found.")
    else:
        st.write(f"Showing {len(feedback_list)} feedback submissions")

        for feedback in feedback_list:
            with st.container():
                st.markdown('<div class="feedback-card">', unsafe_allow_html=True)

                col1, col2, col3 = st.columns([3, 1, 1])

                with col1:
                    st.markdown(f"**{feedback['user_name']}** ({feedback['user_email']})")
                    st.caption(f"{feedback['timestamp']} | {feedback['category'].replace('_', ' ').title()}")
                    st.write(f"Rating: {feedback['rating']}/5")
                    st.write(feedback['feedback_text'])

                with col2:
                    st.write(f"**Status:** {feedback['status'].upper()}")

                with col3:
                    new_status = st.selectbox(
                        "Update",
                        ["pending", "reviewed", "resolved"],
                        index=["pending", "reviewed", "resolved"].index(feedback['status']),
                        key=f"feedback_status_{feedback['id']}"
                    )

                    if st.button("Update", key=f"update_feedback_{feedback['id']}"):
                        update_feedback_status(feedback['id'], new_status)
                        st.success("Updated!")
                        st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)

# TAB 3: Organizer Requests
with tab3:
    st.markdown("### Organizer Access Requests")

    filter_request_status = st.selectbox(
        "Filter by status",
        ["Pending", "All", "Approved", "Rejected"],
        key="request_filter"
    )

    if filter_request_status == "All":
        request_list = all_requests
    else:
        request_list = get_organizer_requests(status=filter_request_status.lower())

    if not request_list:
        st.info(f"No {filter_request_status.lower()} requests found.")
    else:
        st.write(f"Showing {len(request_list)} requests")

        for request in request_list:
            with st.container():
                st.markdown('<div class="request-card">', unsafe_allow_html=True)

                col1, col2 = st.columns([4, 1])

                with col1:
                    st.markdown(f"**{request['user_name']}** ({request['user_email']})")
                    st.caption(f"Requested: {request['timestamp']}")
                    st.write(f"**Reason:** {request['reason']}")

                    if request['status'] != 'pending':
                        st.caption(f"Reviewed by {request['reviewed_by']} on {request['reviewed_at']}")

                with col2:
                    st.write(f"**Status:** {request['status'].upper()}")

                    if request['status'] == 'pending':
                        if st.button("Approve", key=f"approve_{request['id']}", type="primary"):
                            if approve_organizer_request(request['id'], current_user_email):
                                st.success("Approved! User is now an organizer.")
                                st.rerun()
                            else:
                                st.error("Error approving request")

                        if st.button("Reject", key=f"reject_{request['id']}"):
                            reject_organizer_request(request['id'], current_user_email)
                            st.warning("Request rejected")
                            st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)

# TAB 4: User Roles
with tab4:
    st.markdown("### User Role Management")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("#### Current Users")

        if not all_users:
            st.info("No users with assigned roles yet.")
        else:
            df = pd.DataFrame(all_users)
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "user_email": "Email",
                    "role": st.column_config.TextColumn("Role", help="User's current role"),
                    "granted_by": "Granted By",
                    "granted_at": st.column_config.DatetimeColumn("Granted Date")
                }
            )

    with col2:
        st.markdown("#### Grant Role")

        with st.form("grant_role_form"):
            user_email_input = st.text_input("User Email")
            role_input = st.selectbox("Role", ["user", "organizer", "admin"])

            if st.form_submit_button("Grant Role", type="primary"):
                if user_email_input:
                    grant_role(user_email_input, role_input, current_user_email)
                    st.success(f"Granted {role_input} role to {user_email_input}")
                    st.rerun()
                else:
                    st.error("Please enter a user email")

        st.markdown("---")
        st.markdown("#### Role Descriptions")
        st.markdown("""
        - **User**: Standard access, can save locations and view data
        - **Organizer**: Can create and manage events
        - **Admin**: Full system access, manage feedback and roles
        """)

# TAB 5: Performance Metrics
with tab5:
    st.markdown("### System Performance Metrics")
    st.markdown("Monitor response times, API latency, and system performance")

    # Initialize metrics tracker
    metrics_tracker = get_metrics_tracker()

    # Export button and time range selector
    col_export, col_time = st.columns([2, 1])

    with col_export:
        st.markdown("#### Export Performance Data")
        if st.button("Download All Metrics as CSV", type="primary", use_container_width=True):
            # Export all metrics to CSV
            conn = sqlite3.connect(metrics_tracker.db_path)

            # Export response times
            df_response = pd.read_sql_query("SELECT * FROM response_times ORDER BY timestamp DESC", conn)

            # Export API latency
            df_api = pd.read_sql_query("SELECT * FROM api_latency ORDER BY timestamp DESC", conn)

            # Export page loads
            df_pages = pd.read_sql_query("SELECT * FROM page_loads ORDER BY timestamp DESC", conn)

            # Export model inference
            df_models = pd.read_sql_query("SELECT * FROM model_inference ORDER BY timestamp DESC", conn)

            # Export database queries
            df_queries = pd.read_sql_query("SELECT * FROM db_queries ORDER BY timestamp DESC", conn)

            conn.close()

            # Create combined CSV with summary
            timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")

            # Save individual CSV files
            csv_response = df_response.to_csv(index=False).encode('utf-8')
            csv_api = df_api.to_csv(index=False).encode('utf-8')
            csv_pages = df_pages.to_csv(index=False).encode('utf-8')
            csv_models = df_models.to_csv(index=False).encode('utf-8')
            csv_queries = df_queries.to_csv(index=False).encode('utf-8')

            # Create download buttons
            st.success("✅ CSV files ready for download!")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button(
                    label="Response Times CSV",
                    data=csv_response,
                    file_name=f"response_times_{timestamp_str}.csv",
                    mime="text/csv"
                )
                st.download_button(
                    label="API Latency CSV",
                    data=csv_api,
                    file_name=f"api_latency_{timestamp_str}.csv",
                    mime="text/csv"
                )

            with col2:
                st.download_button(
                    label="Page Loads CSV",
                    data=csv_pages,
                    file_name=f"page_loads_{timestamp_str}.csv",
                    mime="text/csv"
                )
                st.download_button(
                    label="Model Inference CSV",
                    data=csv_models,
                    file_name=f"model_inference_{timestamp_str}.csv",
                    mime="text/csv"
                )

            with col3:
                st.download_button(
                    label="DB Queries CSV",
                    data=csv_queries,
                    file_name=f"db_queries_{timestamp_str}.csv",
                    mime="text/csv"
                )

            st.info(f"📊 Total records: {len(df_response) + len(df_api) + len(df_pages) + len(df_models) + len(df_queries)}")

    with col_time:
        # Time range selector
        time_range = st.selectbox(
            "Time Range",
            ["Last Hour", "Last 6 Hours", "Last 24 Hours", "Last 7 Days"],
            index=2,
            key="perf_time_range"
        )

    hours_map = {
        "Last Hour": 1,
        "Last 6 Hours": 6,
        "Last 24 Hours": 24,
        "Last 7 Days": 168
    }
    hours = hours_map[time_range]

    st.markdown("---")

    # Response Time Overview
    st.markdown("#### Response Time Overview")

    overall_stats = metrics_tracker.get_response_time_stats(hours=hours)

    if overall_stats.get('count', 0) > 0:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Requests", f"{overall_stats['count']:,}")

        with col2:
            st.metric("Avg Response", f"{overall_stats['avg_ms']:.1f}ms")

        with col3:
            st.metric("P95 Response", f"{overall_stats['p95_ms']:.1f}ms")

        with col4:
            st.metric("P99 Response", f"{overall_stats['p99_ms']:.1f}ms")

        # Per-endpoint breakdown
        st.markdown("---")
        st.markdown("#### Response Times by Endpoint")

        endpoint_stats = metrics_tracker.get_all_endpoint_stats(hours=hours)

        if endpoint_stats:
            df = pd.DataFrame(endpoint_stats)

            st.dataframe(
                df[['endpoint', 'count', 'avg_ms', 'median_ms', 'p95_ms']].round(2),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "endpoint": "Endpoint",
                    "count": st.column_config.NumberColumn("Requests", format="%d"),
                    "avg_ms": st.column_config.NumberColumn("Avg (ms)", format="%.1f"),
                    "median_ms": st.column_config.NumberColumn("Median (ms)", format="%.1f"),
                    "p95_ms": st.column_config.NumberColumn("P95 (ms)", format="%.1f")
                }
            )

            # Chart
            fig = px.bar(
                df,
                x='endpoint',
                y='avg_ms',
                title='Average Response Time by Endpoint',
                labels={'endpoint': 'Endpoint', 'avg_ms': 'Avg Response Time (ms)'},
                color='avg_ms',
                color_continuous_scale='RdYlGn_r'
            )
            fig.update_layout(showlegend=False, height=350)
            st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No performance data available yet. Metrics will appear as users interact with the app.")

    # API Latency
    st.markdown("---")
    st.markdown("#### API Call Latency")

    conn = sqlite3.connect(metrics_tracker.db_path)
    cursor = conn.cursor()

    since_time = (datetime.now() - timedelta(hours=hours)).isoformat()

    cursor.execute("""
        SELECT operation, latency_ms, timestamp
        FROM api_latency
        WHERE timestamp >= ?
        ORDER BY timestamp DESC
        LIMIT 100
    """, (since_time,))

    latency_data = cursor.fetchall()
    conn.close()

    if latency_data:
        operations = {}
        for op, latency, _ in latency_data:
            if op not in operations:
                operations[op] = []
            operations[op].append(latency)

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total API Calls", len(latency_data))

        with col2:
            all_latencies = [lat for _, lat, _ in latency_data]
            avg_latency = sum(all_latencies) / len(all_latencies)
            st.metric("Avg Latency", f"{avg_latency:.1f}ms")

        # Per-operation stats
        op_stats = []
        for op, latencies in operations.items():
            op_stats.append({
                'operation': op,
                'count': len(latencies),
                'avg_ms': sum(latencies) / len(latencies),
                'max_ms': max(latencies)
            })

        df_ops = pd.DataFrame(op_stats)
        st.dataframe(
            df_ops.round(2),
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No API latency data available for the selected time range.")

    # Model Performance
    st.markdown("---")
    st.markdown("#### ML Model Performance")

    model_stats = metrics_tracker.get_model_performance_stats(hours=hours)

    if model_stats:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Inferences", model_stats.get('count', 0))

        with col2:
            st.metric("Avg Inference Time", f"{model_stats.get('avg_inference_ms', 0):.1f}ms")

        with col3:
            st.metric("Total Predictions", model_stats.get('total_predictions', 0))

    else:
        st.info("No model inference data available yet.")

# Footer
st.markdown("---")
st.caption("Campus Pulse Admin Panel | Logged in as " + st.session_state.user.get('email', 'Admin'))
