"""
Session Manager for persistent login using cookies
Handles saving and restoring user sessions across page refreshes
"""
import streamlit as st
import extra_streamlit_components as stx
import json
from datetime import datetime, timedelta


class SessionManager:
    """Manages persistent user sessions using cookies"""

    def __init__(self, cookie_name="campus_pulse_session", cookie_expiry_days=30):
        """
        Initialize session manager

        Args:
            cookie_name: Name of the cookie to store session data
            cookie_expiry_days: Number of days before cookie expires
        """
        self.cookie_name = cookie_name
        self.cookie_expiry_days = cookie_expiry_days
        self.cookie_manager = stx.CookieManager()

    def save_session(self, user_data):
        """
        Save user session to cookie

        Args:
            user_data: Dictionary containing user information
        """
        try:
            # Convert user data to JSON string
            session_data = json.dumps(user_data)

            # Calculate expiry date
            expiry_date = datetime.now() + timedelta(days=self.cookie_expiry_days)

            # Save to cookie
            self.cookie_manager.set(
                self.cookie_name,
                session_data,
                expires_at=expiry_date
            )

            return True
        except Exception as e:
            print(f"Error saving session: {str(e)}")
            return False

    def load_session(self):
        """
        Load user session from cookie

        Returns:
            Dictionary containing user data or None if no valid session
        """
        try:
            # Get all cookies
            cookies = self.cookie_manager.get_all()

            if not cookies:
                return None

            # Get session cookie
            session_data = cookies.get(self.cookie_name)

            if not session_data:
                return None

            # Parse JSON
            user_data = json.loads(session_data)

            return user_data

        except Exception as e:
            print(f"Error loading session: {str(e)}")
            return None

    def clear_session(self):
        """Clear user session from cookie"""
        try:
            self.cookie_manager.delete(self.cookie_name)
            return True
        except Exception as e:
            print(f"Error clearing session: {str(e)}")
            return False

    def restore_session_state(self):
        """
        Restore session state from cookie if not already logged in
        Should be called at the start of each page

        Returns:
            True if session was restored, False otherwise
        """
        # If user is already logged in session state, do nothing
        if 'user' in st.session_state and st.session_state.user:
            return False

        # Try to load session from cookie
        user_data = self.load_session()

        if user_data:
            # Restore to session state
            st.session_state.user = user_data
            return True

        return False
