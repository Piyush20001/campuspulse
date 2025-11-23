"""
User Profile and Authentication Page
"""
import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.auth_manager import AuthManager
from auth.email_verification import EmailVerification
from utils.navigation import create_top_navbar
from database.feedback_db import get_user_role, request_organizer_access, get_organizer_requests

st.set_page_config(page_title="Profile - Campus Pulse", page_icon="👤", layout="wide")

# Set current page
st.session_state.current_page = 'Profile'

# Top navigation
create_top_navbar()

# Modern profile page styling
st.markdown("""
<style>
    /* Modern card containers */
    .profile-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(0,33,165,0.1);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }

    .profile-card:hover {
        box-shadow: 0 12px 48px rgba(0,0,0,0.15);
        transform: translateY(-4px);
    }

    /* Student card in directory */
    .student-card {
        background: rgba(255,255,255,0.03);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(0,33,165,0.08);
        transition: all 0.3s ease;
    }

    .student-card:hover {
        background: rgba(255,255,255,0.06);
        border-color: rgba(0,33,165,0.2);
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
    }

    /* Form styling */
    .stForm {
        background: rgba(255,255,255,0.02);
        border-radius: 16px;
        padding: 2rem;
        border: 1px solid rgba(0,33,165,0.1);
    }

    /* Info/Success/Error boxes */
    .stAlert {
        border-radius: 12px !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Radio buttons */
    .stRadio > div {
        gap: 1rem;
    }

    .stRadio > div > label {
        background: rgba(255,255,255,0.03);
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        border: 2px solid rgba(0,33,165,0.1);
        transition: all 0.3s ease;
    }

    .stRadio > div > label:hover {
        border-color: rgba(0,33,165,0.3);
        background: rgba(255,255,255,0.06);
    }
</style>
""", unsafe_allow_html=True)

# Initialize auth manager and email verification
if 'auth_manager' not in st.session_state:
    st.session_state.auth_manager = AuthManager()
if 'email_verifier' not in st.session_state:
    st.session_state.email_verifier = EmailVerification()
if 'verification_email' not in st.session_state:
    st.session_state.verification_email = None
if 'verification_code_sent' not in st.session_state:
    st.session_state.verification_code_sent = False
if 'signup_data' not in st.session_state:
    st.session_state.signup_data = None

# Check if user is logged in
if 'user' not in st.session_state or st.session_state.user is None:
    # Show login/signup page
    st.title("Welcome to Campus Pulse")
    st.markdown("Sign in or create an account to get the full Campus Pulse experience!")

    tab1, tab2 = st.tabs(["🔑 Sign In", "📝 Sign Up"])

    # Sign In Tab
    with tab1:
        st.markdown("### Sign In to Your Account")

        with st.form("signin_form"):
            email = st.text_input("UFL Email", placeholder="yourname@ufl.edu")
            password = st.text_input("Password", type="password")

            submit = st.form_submit_button("Sign In", type="primary", use_container_width=True)

            if submit:
                if email and password:
                    success, user_data, message = st.session_state.auth_manager.sign_in(email, password)
                    if success:
                        st.session_state.user = user_data
                        st.success(message)
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Please fill in all fields")

        st.markdown("---")
        st.info("📧 Use your UFL email address (@ufl.edu) to sign in")

    # Sign Up Tab
    with tab2:
        st.markdown("### Create Your Account")
        st.markdown("Join the Campus Pulse community and personalize your experience!")

        with st.form("signup_form"):
            col1, col2 = st.columns(2)

            with col1:
                signup_email = st.text_input("UFL Email*", placeholder="yourname@ufl.edu",
                                            help="Must be a valid @ufl.edu email")
                signup_password = st.text_input("Password*", type="password",
                                               help="Min 8 chars, 1 uppercase, 1 lowercase, 1 number")
                signup_password_confirm = st.text_input("Confirm Password*", type="password")

            with col2:
                full_name = st.text_input("Full Name*", placeholder="John Doe")
                major = st.text_input("Major (Optional)", placeholder="Computer Science")
                year = st.selectbox("Year (Optional)", ["", "Freshman", "Sophomore", "Junior", "Senior", "Graduate"])

            bio = st.text_area("Bio (Optional)", placeholder="Tell us about yourself...",
                             help="This will be visible on your profile", max_chars=500)

            interests = st.text_input("Interests (Optional)", placeholder="Sports, Music, Technology...",
                                     help="Comma-separated list of your interests")

            st.markdown("#### Profile Visibility")
            profile_visibility = st.radio(
                "Who can see your profile?",
                ["public", "private"],
                format_func=lambda x: "🌍 Public - Visible to all students" if x == "public" else "🔒 Private - Only you can see",
                horizontal=True
            )

            show_in_directory = st.checkbox("Show my profile in student directory", value=True,
                                          help="If checked, other students can find you when browsing profiles")

            st.markdown("---")
            agree_terms = st.checkbox("I agree to Campus Pulse Terms of Service and Privacy Policy")

            submit_signup = st.form_submit_button("📧 Send Verification Code", type="primary", use_container_width=True)

            if submit_signup:
                if not agree_terms:
                    st.error("Please agree to the Terms of Service to continue")
                elif not all([signup_email, signup_password, signup_password_confirm, full_name]):
                    st.error("Please fill in all required fields (marked with *)")
                elif signup_password != signup_password_confirm:
                    st.error("Passwords do not match")
                else:
                    # Validate email and password first
                    if not st.session_state.auth_manager.validate_ufl_email(signup_email):
                        st.error("Please use a valid UFL email address (@ufl.edu)")
                    else:
                        is_valid, msg = st.session_state.auth_manager.validate_password(signup_password)
                        if not is_valid:
                            st.error(msg)
                        else:
                            # Send verification code
                            success, code, message = st.session_state.email_verifier.send_verification_email(signup_email)

                            if success:
                                # Store signup data temporarily
                                st.session_state.signup_data = {
                                    'email': signup_email,
                                    'password': signup_password,
                                    'full_name': full_name,
                                    'bio': bio,
                                    'profile_visibility': profile_visibility,
                                    'major': major,
                                    'year': year,
                                    'interests': interests
                                }
                                st.session_state.verification_email = signup_email
                                st.session_state.verification_code_sent = True

                                st.success(message)
                                st.info("💡 Check your email for the 4-digit verification code!")
                                st.rerun()
                            else:
                                st.error(message)

        # Email Verification Section (shown after code is sent)
        if st.session_state.verification_code_sent and st.session_state.signup_data:
            st.markdown("---")
            st.markdown("### Email Verification")
            st.info(f"A 4-digit code has been sent to **{st.session_state.verification_email}**")

            verification_code = st.text_input(
                "Enter 4-Digit Code",
                max_chars=4,
                placeholder="1234",
                help="Check your email for the verification code"
            )

            col_verify1, col_verify2 = st.columns(2)

            with col_verify1:
                if st.button("✅ Verify & Create Account", type="primary", use_container_width=True):
                    if len(verification_code) != 4:
                        st.error("Please enter the complete 4-digit code")
                    else:
                        # Verify the code
                        success, message = st.session_state.email_verifier.verify_code(
                            st.session_state.verification_email,
                            verification_code
                        )

                        if success:
                            # Create the account
                            signup_data = st.session_state.signup_data
                            success, message = st.session_state.auth_manager.sign_up(
                                email=signup_data['email'],
                                password=signup_data['password'],
                                full_name=signup_data['full_name'],
                                bio=signup_data['bio'],
                                profile_visibility=signup_data['profile_visibility']
                            )

                            if success:
                                # Update profile with additional info
                                _, user_data, _ = st.session_state.auth_manager.sign_in(
                                    signup_data['email'],
                                    signup_data['password']
                                )
                                if user_data:
                                    st.session_state.auth_manager.update_profile(user_data['id'], {
                                        'major': signup_data['major'],
                                        'year': signup_data['year'],
                                        'interests': signup_data['interests']
                                    })

                                # Clear verification state
                                st.session_state.verification_code_sent = False
                                st.session_state.signup_data = None
                                st.session_state.verification_email = None

                                st.success("🎉 Account created successfully!")
                                st.info("💡 Please switch to the 'Sign In' tab to log in")
                                st.balloons()
                            else:
                                st.error(message)
                        else:
                            st.error(message)

            with col_verify2:
                if st.button("🔄 Resend Code", use_container_width=True):
                    success, code, message = st.session_state.email_verifier.send_verification_email(
                        st.session_state.verification_email
                    )
                    if success:
                        st.success(message)
                    else:
                        st.error(message)

        st.markdown("---")
        st.markdown("""
        **Password Requirements:**
        - At least 8 characters long
        - Contains uppercase and lowercase letters
        - Contains at least one number
        """)

else:
    # User is logged in - show profile page
    user = st.session_state.user

    st.title(f"👤 {user['full_name']}'s Profile")

    # Logout button
    col1, col2, col3 = st.columns([6, 1, 1])
    with col3:
        if st.button("🚪 Logout", type="secondary"):
            st.session_state.user = None
            st.success("Logged out successfully")
            st.rerun()

    st.markdown("---")

    # Profile tabs
    profile_tab1, profile_tab2, profile_tab3 = st.tabs(["📋 My Profile", "✏️ Edit Profile", "🔍 Find Students"])

    # My Profile Tab
    with profile_tab1:
        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown("### Profile Picture")
            st.markdown('<div style="width: 150px; height: 150px; background: linear-gradient(135deg, #0021A5 0%, #FA4616 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 60px; color: white; font-weight: bold;">' + user['full_name'][0].upper() + '</div>', unsafe_allow_html=True)

            st.markdown("### Student Info")
            if user.get('major'):
                st.markdown(f"**Major:** {user['major']}")
            if user.get('year'):
                st.markdown(f"**Year:** {user['year']}")
            st.markdown(f"**Email:** {user['email']}")

            st.markdown("### Privacy")
            visibility_emoji = "🌍" if user['profile_visibility'] == 'public' else "🔒"
            st.markdown(f"{visibility_emoji} **Profile:** {user['profile_visibility'].title()}")

            # User role and organizer request
            st.markdown("### Role & Permissions")
            user_role = get_user_role(user['email'])

            if user_role == 'admin':
                st.success("👑 Administrator")
                st.caption("Full system access")
            elif user_role == 'organizer':
                st.success("🎫 Event Organizer")
                st.caption("Can create and manage events")
            else:
                st.info("👤 Standard User")

                # Check if user has pending request
                user_requests = [r for r in get_organizer_requests() if r['user_email'] == user['email']]

                if user_requests and user_requests[0]['status'] == 'pending':
                    st.warning("🕐 Organizer access request pending")
                    st.caption("Your request is under review")
                elif user_requests and user_requests[0]['status'] == 'rejected':
                    st.error("❌ Previous request was rejected")
                    st.caption("Please contact admin for more information")
                else:
                    if st.button("🎫 Request Organizer Access", use_container_width=True):
                        st.session_state.show_organizer_request = True
                        st.rerun()

            # Organizer request form
            if st.session_state.get('show_organizer_request', False):
                with st.form("organizer_request_form"):
                    st.markdown("#### Request Organizer Access")
                    st.write("Organizers can create and manage campus events.")

                    reason = st.text_area(
                        "Why do you want to become an organizer?",
                        placeholder="I'm a club president and want to create events for our organization...",
                        max_chars=500
                    )

                    col_a, col_b = st.columns(2)

                    with col_a:
                        if st.form_submit_button("Submit Request", type="primary", use_container_width=True):
                            if reason and len(reason) > 20:
                                if request_organizer_access(user['email'], user['full_name'], reason):
                                    st.success("✅ Request submitted! An admin will review it soon.")
                                    st.session_state.show_organizer_request = False
                                    st.rerun()
                                else:
                                    st.error("You already have a pending request")
                            else:
                                st.error("Please provide a detailed reason (at least 20 characters)")

                    with col_b:
                        if st.form_submit_button("Cancel", use_container_width=True):
                            st.session_state.show_organizer_request = False
                            st.rerun()

        with col2:
            st.markdown("### About Me")
            if user.get('bio'):
                st.markdown(f"*{user['bio']}*")
            else:
                st.info("No bio added yet. Click 'Edit Profile' to add one!")

            if user.get('interests'):
                st.markdown("### Interests")
                interests_list = user['interests'].split(',')
                cols = st.columns(min(len(interests_list), 4))
                for idx, interest in enumerate(interests_list[:8]):
                    with cols[idx % 4]:
                        st.markdown(f'<span style="background: #F0F2F6; padding: 0.5rem 1rem; border-radius: 20px; display: inline-block; margin: 0.25rem;">🏷️ {interest.strip()}</span>', unsafe_allow_html=True)

            st.markdown("### Activity Stats")
            stat_col1, stat_col2, stat_col3 = st.columns(3)

            with stat_col1:
                user_created_count = len(st.session_state.get('user_created_events', []))
                st.metric("Events Created", user_created_count)

            with stat_col2:
                saved_locations_count = len(st.session_state.get('saved_locations', []))
                st.metric("Saved Locations", saved_locations_count)

            with stat_col3:
                st.metric("Member Since", user['created_at'][:10] if user.get('created_at') else "N/A")

    # Edit Profile Tab
    with profile_tab2:
        st.markdown("### Update Your Profile")

        with st.form("update_profile_form"):
            col1, col2 = st.columns(2)

            with col1:
                new_full_name = st.text_input("Full Name", value=user['full_name'])
                new_major = st.text_input("Major", value=user.get('major', ''))
                new_year = st.selectbox("Year", ["", "Freshman", "Sophomore", "Junior", "Senior", "Graduate"],
                                       index=0 if not user.get('year') else
                                       ["", "Freshman", "Sophomore", "Junior", "Senior", "Graduate"].index(user['year']))

            with col2:
                new_bio = st.text_area("Bio", value=user.get('bio', ''), max_chars=500)
                new_interests = st.text_input("Interests (comma-separated)",
                                             value=user.get('interests', ''))

            new_visibility = st.radio(
                "Profile Visibility",
                ["public", "private"],
                index=0 if user['profile_visibility'] == 'public' else 1,
                format_func=lambda x: "🌍 Public" if x == "public" else "🔒 Private",
                horizontal=True
            )

            submit_update = st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True)

            if submit_update:
                updates = {
                    'full_name': new_full_name,
                    'bio': new_bio,
                    'major': new_major,
                    'year': new_year,
                    'interests': new_interests,
                    'profile_visibility': new_visibility
                }

                success, message = st.session_state.auth_manager.update_profile(user['id'], updates)

                if success:
                    # Refresh user data
                    st.session_state.user.update(updates)
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

    # Find Students Tab
    with profile_tab3:
        st.markdown("### Discover UF Students")

        search_query = st.text_input("🔎 Search by name or major", placeholder="Search students...")

        if search_query:
            results = st.session_state.auth_manager.search_students(search_query)

            if results:
                st.markdown(f"### Found {len(results)} student(s)")
                for student in results:
                    with st.container():
                        col1, col2 = st.columns([1, 4])

                        with col1:
                            st.markdown(f'<div style="width: 60px; height: 60px; background: linear-gradient(135deg, #0021A5 0%, #FA4616 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; color: white; font-weight: bold;">{student["full_name"][0].upper()}</div>', unsafe_allow_html=True)

                        with col2:
                            st.markdown(f"**{student['full_name']}**")
                            if student.get('major'):
                                st.markdown(f"📚 {student['major']}")
                            if student.get('year'):
                                st.markdown(f"🎓 {student['year']}")
                            if student.get('bio'):
                                st.caption(student['bio'][:100] + "..." if len(student.get('bio', '')) > 100 else student.get('bio', ''))

                        st.markdown("---")
            else:
                st.info("No students found matching your search")
        else:
            # Show public profiles
            public_profiles = st.session_state.auth_manager.get_public_profiles(limit=20)

            if public_profiles:
                st.markdown(f"### Student Directory ({len(public_profiles)} students)")

                for student in public_profiles:
                    with st.container():
                        col1, col2 = st.columns([1, 4])

                        with col1:
                            st.markdown(f'<div style="width: 60px; height: 60px; background: linear-gradient(135deg, #0021A5 0%, #FA4616 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; color: white; font-weight: bold;">{student["full_name"][0].upper()}</div>', unsafe_allow_html=True)

                        with col2:
                            st.markdown(f"**{student['full_name']}**")
                            if student.get('major'):
                                st.markdown(f"📚 {student['major']}")
                            if student.get('year'):
                                st.markdown(f"🎓 {student['year']}")
                            if student.get('bio'):
                                st.caption(student['bio'][:100] + "..." if len(student.get('bio', '')) > 100 else student.get('bio', ''))
                            if student.get('interests'):
                                interests = student['interests'].split(',')[:3]
                                st.markdown(' '.join([f'`{i.strip()}`' for i in interests]))

                        st.markdown("---")
            else:
                st.info("No public student profiles yet. Be the first to create one!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem 0;">
    <p>👤 Campus Pulse Profiles | Powered by AI</p>
    <p style="font-size: 0.8rem;">🔒 Your privacy is important to us. Profile visibility settings can be changed anytime.</p>
</div>
""", unsafe_allow_html=True)
