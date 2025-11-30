"""
User Authentication and Profile Management for Campus Pulse
"""
import sqlite3
import hashlib
import re
from datetime import datetime
from typing import Optional, Dict, Any
import os


class AuthManager:
    """Manages user authentication and profiles"""

    def __init__(self, db_path: str = "campus_pulse_users.db"):
        """Initialize the authentication manager with database"""
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Create database tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                bio TEXT,
                profile_visibility TEXT DEFAULT 'public',
                profile_picture TEXT,
                major TEXT,
                year TEXT,
                interests TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        """)

        # User settings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_settings (
                user_id INTEGER PRIMARY KEY,
                email_notifications BOOLEAN DEFAULT 1,
                show_in_directory BOOLEAN DEFAULT 1,
                theme TEXT DEFAULT 'light',
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)

        conn.commit()
        conn.close()

    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_ufl_email(self, email: str) -> bool:
        """Validate if email is a UFL edu email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@ufl\.edu$'
        return re.match(pattern, email.lower()) is not None

    def validate_password(self, password: str) -> tuple[bool, str]:
        """
        Validate password strength
        Returns: (is_valid, message)
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        if not re.search(r'[0-9]', password):
            return False, "Password must contain at least one number"
        return True, "Password is valid"

    def sign_up(self, email: str, password: str, full_name: str, bio: str = "",
                profile_visibility: str = "public") -> tuple[bool, str]:
        """
        Create a new user account
        Returns: (success, message)
        """
        # Validate UFL email
        if not self.validate_ufl_email(email):
            return False, "Please use a valid UFL email address (@ufl.edu)"

        # Validate password
        is_valid, msg = self.validate_password(password)
        if not is_valid:
            return False, msg

        # Validate full name
        if not full_name or len(full_name.strip()) < 2:
            return False, "Please enter your full name"

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Check if email already exists
            cursor.execute("SELECT id FROM users WHERE email = ?", (email.lower(),))
            if cursor.fetchone():
                conn.close()
                return False, "An account with this email already exists"

            # Create user
            password_hash = self._hash_password(password)
            cursor.execute("""
                INSERT INTO users (email, password_hash, full_name, bio, profile_visibility)
                VALUES (?, ?, ?, ?, ?)
            """, (email.lower(), password_hash, full_name.strip(), bio.strip(), profile_visibility))

            user_id = cursor.lastrowid

            # Create default settings
            cursor.execute("""
                INSERT INTO user_settings (user_id)
                VALUES (?)
            """, (user_id,))

            conn.commit()
            conn.close()

            return True, "Account created successfully! Please sign in."

        except Exception as e:
            return False, f"Error creating account: {str(e)}"

    def sign_in(self, email: str, password: str) -> tuple[bool, Optional[Dict[str, Any]], str]:
        """
        Sign in user
        Returns: (success, user_data, message)
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            password_hash = self._hash_password(password)

            cursor.execute("""
                SELECT id, email, full_name, bio, profile_visibility,
                       profile_picture, major, year, interests, created_at
                FROM users
                WHERE email = ? AND password_hash = ?
            """, (email.lower(), password_hash))

            user = cursor.fetchone()

            if not user:
                conn.close()
                return False, None, "Invalid email or password"

            # Update last login
            cursor.execute("""
                UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
            """, (user[0],))
            conn.commit()

            # Get user settings
            cursor.execute("""
                SELECT email_notifications, show_in_directory, theme
                FROM user_settings WHERE user_id = ?
            """, (user[0],))
            settings = cursor.fetchone()

            conn.close()

            user_data = {
                'id': user[0],
                'email': user[1],
                'full_name': user[2],
                'bio': user[3],
                'profile_visibility': user[4],
                'profile_picture': user[5],
                'major': user[6],
                'year': user[7],
                'interests': user[8],
                'created_at': user[9],
                'settings': {
                    'email_notifications': settings[0] if settings else True,
                    'show_in_directory': settings[1] if settings else True,
                    'theme': settings[2] if settings else 'light'
                }
            }

            return True, user_data, "Sign in successful!"

        except Exception as e:
            return False, None, f"Error signing in: {str(e)}"

    def update_profile(self, user_id: int, updates: Dict[str, Any]) -> tuple[bool, str]:
        """
        Update user profile
        Returns: (success, message)
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            allowed_fields = ['full_name', 'bio', 'profile_visibility', 'major', 'year', 'interests']
            update_fields = []
            values = []

            for field, value in updates.items():
                if field in allowed_fields:
                    update_fields.append(f"{field} = ?")
                    values.append(value)

            if not update_fields:
                return False, "No valid fields to update"

            values.append(user_id)
            query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = ?"

            cursor.execute(query, values)
            conn.commit()
            conn.close()

            return True, "Profile updated successfully!"

        except Exception as e:
            return False, f"Error updating profile: {str(e)}"

    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user data by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, email, full_name, bio, profile_visibility,
                       profile_picture, major, year, interests, created_at
                FROM users WHERE id = ?
            """, (user_id,))

            user = cursor.fetchone()
            conn.close()

            if not user:
                return None

            return {
                'id': user[0],
                'email': user[1],
                'full_name': user[2],
                'bio': user[3],
                'profile_visibility': user[4],
                'profile_picture': user[5],
                'major': user[6],
                'year': user[7],
                'interests': user[8],
                'created_at': user[9]
            }

        except Exception as e:
            return None

    def get_public_profiles(self, limit: int = 50) -> list:
        """Get list of public student profiles"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT u.id, u.email, u.full_name, u.bio, u.major, u.year, u.interests
                FROM users u
                JOIN user_settings s ON u.id = s.user_id
                WHERE u.profile_visibility = 'public' AND s.show_in_directory = 1
                ORDER BY u.created_at DESC
                LIMIT ?
            """, (limit,))

            profiles = []
            for row in cursor.fetchall():
                profiles.append({
                    'id': row[0],
                    'email': row[1],
                    'full_name': row[2],
                    'bio': row[3],
                    'major': row[4],
                    'year': row[5],
                    'interests': row[6]
                })

            conn.close()
            return profiles

        except Exception as e:
            return []

    def search_students(self, query: str) -> list:
        """Search for students by name or major"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            search_pattern = f"%{query}%"
            cursor.execute("""
                SELECT u.id, u.email, u.full_name, u.bio, u.major, u.year
                FROM users u
                JOIN user_settings s ON u.id = s.user_id
                WHERE (u.full_name LIKE ? OR u.major LIKE ?)
                AND u.profile_visibility = 'public'
                AND s.show_in_directory = 1
                LIMIT 20
            """, (search_pattern, search_pattern))

            results = []
            for row in cursor.fetchall():
                results.append({
                    'id': row[0],
                    'email': row[1],
                    'full_name': row[2],
                    'bio': row[3],
                    'major': row[4],
                    'year': row[5]
                })

            conn.close()
            return results

        except Exception as e:
            return []
