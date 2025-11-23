"""
Feedback database management
Stores user feedback and organizer requests
"""
import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'campus_pulse_feedback.db')

def init_feedback_db():
    """Initialize feedback and organizer request database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Feedback table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            user_name TEXT,
            rating INTEGER,
            feedback_text TEXT,
            category TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pending'
        )
    ''')

    # Organizer requests table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS organizer_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT UNIQUE,
            user_name TEXT,
            reason TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pending',
            reviewed_by TEXT,
            reviewed_at DATETIME
        )
    ''')

    # User roles table (extends user data)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_roles (
            user_email TEXT PRIMARY KEY,
            role TEXT DEFAULT 'user',
            granted_by TEXT,
            granted_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

def submit_feedback(user_email, user_name, rating, feedback_text, category='general'):
    """Submit user feedback"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO feedback (user_email, user_name, rating, feedback_text, category)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_email, user_name, rating, feedback_text, category))

    conn.commit()
    conn.close()
    return True

def get_all_feedback(status=None):
    """Get all feedback, optionally filtered by status"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if status:
        cursor.execute('''
            SELECT id, user_email, user_name, rating, feedback_text, category, timestamp, status
            FROM feedback
            WHERE status = ?
            ORDER BY timestamp DESC
        ''', (status,))
    else:
        cursor.execute('''
            SELECT id, user_email, user_name, rating, feedback_text, category, timestamp, status
            FROM feedback
            ORDER BY timestamp DESC
        ''')

    feedback = cursor.fetchall()
    conn.close()

    return [
        {
            'id': f[0],
            'user_email': f[1],
            'user_name': f[2],
            'rating': f[3],
            'feedback_text': f[4],
            'category': f[5],
            'timestamp': f[6],
            'status': f[7]
        }
        for f in feedback
    ]

def update_feedback_status(feedback_id, new_status):
    """Update feedback status (pending, reviewed, resolved)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE feedback
        SET status = ?
        WHERE id = ?
    ''', (new_status, feedback_id))

    conn.commit()
    conn.close()

def request_organizer_access(user_email, user_name, reason):
    """Submit organizer access request"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO organizer_requests (user_email, user_name, reason)
            VALUES (?, ?, ?)
        ''', (user_email, user_name, reason))

        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # Request already exists
        conn.close()
        return False

def get_organizer_requests(status=None):
    """Get organizer access requests"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if status:
        cursor.execute('''
            SELECT id, user_email, user_name, reason, timestamp, status, reviewed_by, reviewed_at
            FROM organizer_requests
            WHERE status = ?
            ORDER BY timestamp DESC
        ''', (status,))
    else:
        cursor.execute('''
            SELECT id, user_email, user_name, reason, timestamp, status, reviewed_by, reviewed_at
            FROM organizer_requests
            ORDER BY timestamp DESC
        ''')

    requests = cursor.fetchall()
    conn.close()

    return [
        {
            'id': r[0],
            'user_email': r[1],
            'user_name': r[2],
            'reason': r[3],
            'timestamp': r[4],
            'status': r[5],
            'reviewed_by': r[6],
            'reviewed_at': r[7]
        }
        for r in requests
    ]

def approve_organizer_request(request_id, admin_email):
    """Approve organizer request and grant role"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get user email from request
    cursor.execute('SELECT user_email FROM organizer_requests WHERE id = ?', (request_id,))
    result = cursor.fetchone()

    if result:
        user_email = result[0]

        # Update request status
        cursor.execute('''
            UPDATE organizer_requests
            SET status = 'approved', reviewed_by = ?, reviewed_at = ?
            WHERE id = ?
        ''', (admin_email, datetime.now().isoformat(), request_id))

        # Grant organizer role
        cursor.execute('''
            INSERT OR REPLACE INTO user_roles (user_email, role, granted_by)
            VALUES (?, 'organizer', ?)
        ''', (user_email, admin_email))

        conn.commit()
        conn.close()
        return True

    conn.close()
    return False

def reject_organizer_request(request_id, admin_email):
    """Reject organizer request"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE organizer_requests
        SET status = 'rejected', reviewed_by = ?, reviewed_at = ?
        WHERE id = ?
    ''', (admin_email, datetime.now().isoformat(), request_id))

    conn.commit()
    conn.close()

def get_user_role(user_email):
    """Get user's role (user, organizer, admin)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('SELECT role FROM user_roles WHERE user_email = ?', (user_email,))
    result = cursor.fetchone()

    conn.close()

    return result[0] if result else 'user'

def grant_role(user_email, role, admin_email):
    """Manually grant a role to a user"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT OR REPLACE INTO user_roles (user_email, role, granted_by)
        VALUES (?, ?, ?)
    ''', (user_email, role, admin_email))

    conn.commit()
    conn.close()

def get_all_users_with_roles():
    """Get all users and their roles"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT user_email, role, granted_by, granted_at
        FROM user_roles
        ORDER BY granted_at DESC
    ''')

    users = cursor.fetchall()
    conn.close()

    return [
        {
            'user_email': u[0],
            'role': u[1],
            'granted_by': u[2],
            'granted_at': u[3]
        }
        for u in users
    ]

# Initialize database on import
init_feedback_db()
