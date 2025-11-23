"""
Session Manager for persistent login using browser localStorage
Handles saving and restoring user sessions across page refreshes
"""
import streamlit as st
from streamlit_javascript import st_javascript
import json
from datetime import datetime, timedelta


class SessionManager:
    """Manages persistent user sessions using browser localStorage"""

    def __init__(self, storage_key="campus_pulse_session", session_expiry_days=30):
        """
        Initialize session manager

        Args:
            storage_key: Key to use in localStorage
            session_expiry_days: Number of days before session expires
        """
        self.storage_key = storage_key
        self.session_expiry_days = session_expiry_days

    def save_session(self, user_data):
        """
        Save user session to browser localStorage

        Args:
            user_data: Dictionary containing user information

        Returns:
            True if successful, False otherwise
        """
        try:
            # Add expiry timestamp
            session_data = {
                'user': user_data,
                'expires_at': (datetime.now() + timedelta(days=self.session_expiry_days)).isoformat()
            }

            # Convert to JSON
            session_json = json.dumps(session_data)

            # Save to localStorage using JavaScript
            js_code = f"""
            localStorage.setItem('{self.storage_key}', '{session_json.replace("'", "\\'")}');
            """
            st_javascript(js_code)

            return True

        except Exception as e:
            print(f"Error saving session: {str(e)}")
            return False

    def load_session(self):
        """
        Load user session from browser localStorage

        Returns:
            Dictionary containing user data or None if no valid session
        """
        try:
            # Get data from localStorage using JavaScript
            js_code = f"""
            localStorage.getItem('{self.storage_key}');
            """
            session_json = st_javascript(js_code)

            if not session_json or session_json == "null":
                return None

            # Parse JSON
            session_data = json.loads(session_json)

            # Check if expired
            expires_at = datetime.fromisoformat(session_data['expires_at'])
            if datetime.now() > expires_at:
                self.clear_session()
                return None

            return session_data['user']

        except Exception as e:
            print(f"Error loading session: {str(e)}")
            return None

    def clear_session(self):
        """Clear user session from browser localStorage"""
        try:
            js_code = f"""
            localStorage.removeItem('{self.storage_key}');
            """
            st_javascript(js_code)
            return True

        except Exception as e:
            print(f"Error clearing session: {str(e)}")
            return False

    def restore_session_state(self):
        """
        Restore session state from localStorage if not already logged in
        Should be called at the start of each page

        Returns:
            True if session was restored, False otherwise
        """
        # If user is already logged in session state, do nothing
        if 'user' in st.session_state and st.session_state.user:
            return False

        # Try to load session from localStorage
        user_data = self.load_session()

        if user_data:
            # Restore to session state
            st.session_state.user = user_data
            return True

        return False
