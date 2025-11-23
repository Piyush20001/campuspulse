#!/usr/bin/env python3
"""
Grant admin access to a user
Run this script once to make yourself an admin
"""
import sys
import os

# Add streamlit_app to path
sys.path.insert(0, 'streamlit_app')

from database.feedback_db import grant_role, get_user_role

def main():
    print("="*60)
    print("Campus Pulse - Grant Admin Access")
    print("="*60)
    print()

    email = input("Enter your UFL email address: ").strip()

    if not email:
        print("❌ Email cannot be empty")
        return

    if not email.endswith('@ufl.edu'):
        confirm = input(f"⚠️  '{email}' doesn't look like a UFL email. Continue anyway? (yes/no): ")
        if confirm.lower() not in ['yes', 'y']:
            print("Cancelled.")
            return

    # Check current role
    current_role = get_user_role(email)
    print(f"\nCurrent role: {current_role}")

    # Grant admin role
    print(f"\nGranting admin role to: {email}")
    grant_role(email, 'admin', 'system')

    # Verify
    new_role = get_user_role(email)

    print()
    print("="*60)
    print("✅ SUCCESS!")
    print("="*60)
    print(f"User: {email}")
    print(f"Role: {new_role}")
    print()
    print("You can now access the Admin Panel in Campus Pulse!")
    print("Navigate to: 👑 Admin Panel (page 5)")
    print("="*60)

if __name__ == "__main__":
    main()
