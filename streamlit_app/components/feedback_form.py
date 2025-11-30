"""
Feedback form component
Can be added to any page footer
"""
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.feedback_db import submit_feedback

def create_feedback_form():
    """Create feedback form at bottom of page"""
    st.markdown("---")
    st.markdown("### 💬 Share Your Feedback")

    # Create expander for feedback form
    with st.expander("Help us improve Campus Pulse", expanded=False):
        # Check if user is logged in
        user_email = None
        user_name = "Anonymous"

        if 'user' in st.session_state and st.session_state.user:
            user_email = st.session_state.user.get('email', '')
            user_name = st.session_state.user.get('full_name', 'User')
            st.info(f"Submitting as: {user_name}")
        else:
            st.warning("You're not logged in. Feedback will be submitted anonymously.")

        # Rating
        rating = st.select_slider(
            "How would you rate your experience?",
            options=[1, 2, 3, 4, 5],
            value=4,
            format_func=lambda x: "⭐" * x
        )

        # Category
        category = st.selectbox(
            "Category",
            ["General", "Heatmap Feature", "Events Feature", "Performance", "Bug Report", "Feature Request"]
        )

        # Feedback text
        feedback_text = st.text_area(
            "Your feedback (optional)",
            placeholder="Tell us what you think! Suggestions, bugs, or anything else...",
            max_chars=1000
        )

        col1, col2 = st.columns([1, 5])

        with col1:
            if st.button("Submit Feedback", type="primary", use_container_width=True):
                if not feedback_text and rating < 3:
                    st.error("Please provide feedback for ratings below 3 stars")
                else:
                    try:
                        submit_feedback(
                            user_email=user_email or "anonymous",
                            user_name=user_name,
                            rating=rating,
                            feedback_text=feedback_text or "No additional feedback",
                            category=category.lower().replace(" ", "_")
                        )
                        st.success("✅ Thank you for your feedback!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Error submitting feedback: {str(e)}")

        with col2:
            st.caption("Your feedback helps us improve Campus Pulse for everyone!")
