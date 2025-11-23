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

st.set_page_config(page_title="Admin Panel - Campus Pulse", layout="wide")

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
tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Feedback Management", "Organizer Requests", "User Roles"])

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

# Footer
st.markdown("---")
st.caption("Campus Pulse Admin Panel | Logged in as " + st.session_state.user.get('email', 'Admin'))
