"""
Email Verification System for Campus Pulse
Sends 4-digit verification codes to UFL email addresses
"""
import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import sqlite3


class EmailVerification:
    """Handles email verification for UFL accounts"""

    def __init__(self, db_path: str = "campus_pulse_users.db"):
        """Initialize email verification system"""
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Create verification codes table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS verification_codes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                code TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                verified BOOLEAN DEFAULT 0
            )
        """)

        conn.commit()
        conn.close()

    def generate_code(self) -> str:
        """Generate a 4-digit verification code"""
        return ''.join(random.choices(string.digits, k=4))

    def send_verification_email(self, email: str) -> tuple[bool, str, str]:
        """
        Send verification code to email address
        Returns: (success, code, message)
        """
        try:
            # Generate verification code
            code = self.generate_code()

            # Store code in database (expires in 10 minutes)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Delete old codes for this email
            cursor.execute("DELETE FROM verification_codes WHERE email = ? AND verified = 0", (email,))

            # Insert new code
            expires_at = (datetime.now() + timedelta(minutes=10)).isoformat()
            cursor.execute("""
                INSERT INTO verification_codes (email, code, expires_at)
                VALUES (?, ?, ?)
            """, (email, code, expires_at))

            conn.commit()
            conn.close()

            # For development/testing - just return the code instead of sending email
            # In production, you would send actual email via SMTP
            print(f"[DEV MODE] Verification code for {email}: {code}")

            # UNCOMMENT FOR PRODUCTION EMAIL SENDING:
            # self._send_smtp_email(email, code)

            return True, code, f"Verification code sent to {email}. (DEV MODE: Code is {code})"

        except Exception as e:
            return False, "", f"Error sending verification email: {str(e)}"

    def _send_smtp_email(self, to_email: str, code: str):
        """
        Send email via SMTP (for production use)
        Configure your SMTP settings here
        """
        # SMTP Configuration - UPDATE THESE FOR PRODUCTION
        smtp_server = "smtp.gmail.com"  # Or your email provider
        smtp_port = 587
        sender_email = "your-email@example.com"  # UPDATE THIS
        sender_password = "your-app-password"  # UPDATE THIS

        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = "Campus Pulse - Email Verification Code"
        message["From"] = sender_email
        message["To"] = to_email

        # HTML email body
        html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
              <div style="text-align: center; margin-bottom: 30px;">
                <h1 style="color: #0021A5; margin: 0;">Campus Pulse</h1>
                <p style="color: #FA4616; font-size: 14px; margin: 5px 0;">University of Florida</p>
              </div>

              <h2 style="color: #333; text-align: center;">Verify Your Email</h2>

              <p style="color: #666; line-height: 1.6;">
                Thank you for signing up for Campus Pulse! To complete your registration, please use the verification code below:
              </p>

              <div style="background: linear-gradient(90deg, #0021A5 0%, #FA4616 100%); padding: 20px; border-radius: 8px; text-align: center; margin: 30px 0;">
                <p style="color: white; font-size: 14px; margin: 0 0 10px 0;">Your Verification Code</p>
                <p style="color: white; font-size: 36px; font-weight: bold; letter-spacing: 8px; margin: 0;">{code}</p>
              </div>

              <p style="color: #666; font-size: 14px; line-height: 1.6;">
                <strong>This code will expire in 10 minutes.</strong><br>
                If you didn't request this code, please ignore this email.
              </p>

              <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">

              <p style="color: #999; font-size: 12px; text-align: center;">
                Campus Pulse - AI-Powered Campus Intelligence<br>
                University of Florida<br>
                🐊 Go Gators!
              </p>
            </div>
          </body>
        </html>
        """

        # Attach HTML content
        part = MIMEText(html, "html")
        message.attach(part)

        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, message.as_string())

    def verify_code(self, email: str, code: str) -> tuple[bool, str]:
        """
        Verify the code entered by user
        Returns: (success, message)
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Get the most recent code for this email
            cursor.execute("""
                SELECT code, expires_at, verified
                FROM verification_codes
                WHERE email = ?
                ORDER BY created_at DESC
                LIMIT 1
            """, (email,))

            result = cursor.fetchone()

            if not result:
                conn.close()
                return False, "No verification code found. Please request a new code."

            stored_code, expires_at, verified = result

            # Check if already verified
            if verified:
                conn.close()
                return False, "This code has already been used."

            # Check if expired
            if datetime.now() > datetime.fromisoformat(expires_at):
                conn.close()
                return False, "Verification code has expired. Please request a new code."

            # Check if code matches
            if code != stored_code:
                conn.close()
                return False, "Invalid verification code. Please try again."

            # Mark as verified
            cursor.execute("""
                UPDATE verification_codes
                SET verified = 1
                WHERE email = ? AND code = ?
            """, (email, code))

            conn.commit()
            conn.close()

            return True, "Email verified successfully!"

        except Exception as e:
            return False, f"Error verifying code: {str(e)}"

    def cleanup_expired_codes(self):
        """Remove expired verification codes (run periodically)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM verification_codes
                WHERE expires_at < ? AND verified = 0
            """, (datetime.now().isoformat(),))

            conn.commit()
            conn.close()

        except Exception as e:
            print(f"Error cleaning up codes: {str(e)}")
