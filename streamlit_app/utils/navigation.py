"""
Top navigation bar component
"""
import streamlit as st
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from utils.image_utils import get_uf_logo_html, get_campus_pulse_logo_html
except ImportError:
    # Fallback if image_utils not available
    def get_uf_logo_html(css_class="navbar-logo", style=""):
        return '<img src="https://i.imgur.com/5bZvhKL.png" class="navbar-logo" alt="UF Logo" />'
    def get_campus_pulse_logo_html(css_class="navbar-logo", style=""):
        return ''

def create_top_navbar():
    """Create a horizontal navigation bar at the top"""

    # Initialize theme if not set
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'

    # Apply theme-specific CSS
    theme = st.session_state.theme

    if theme == 'dark':
        bg_gradient = 'linear-gradient(90deg, #001A4D 0%, #8B1E0A 100%)'
        bg_color = '#0A1929'
        text_color = '#FFFFFF'
        secondary_bg = '#1E3A5F'
    else:
        bg_gradient = 'linear-gradient(90deg, #0021A5 0%, #FA4616 100%)'
        bg_color = '#FFFFFF'
        text_color = '#262730'
        secondary_bg = '#F0F2F6'

    # Custom CSS for top navbar - COMPREHENSIVE THEME SUPPORT
    st.markdown(f"""
    <style>
        /* FORCE THEME COLORS - Override all Streamlit defaults */
        .stApp {{
            background-color: {bg_color} !important;
        }}

        [data-testid="stAppViewContainer"] {{
            background-color: {bg_color} !important;
        }}

        [data-testid="stHeader"] {{
            background-color: {bg_color} !important;
        }}

        .main {{
            background-color: {bg_color} !important;
            color: {text_color} !important;
        }}

        .main .block-container {{
            padding-top: 1rem;
            max-width: 100%;
            background-color: {bg_color} !important;
        }}

        /* All text elements */
        .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, span, div {{
            color: {text_color} !important;
        }}

        /* Metrics and stats */
        [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{
            color: {text_color} !important;
        }}

        /* Cards and containers */
        [data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"] {{
            background-color: {secondary_bg} !important;
        }}

        /* Hide default sidebar */
        [data-testid="stSidebar"] {{
            display: none;
        }}

        /* Top navbar styles */
        .top-navbar {{
            background: {bg_gradient};
            padding: 0.75rem 2rem;
            margin: -6rem -4rem 2rem -4rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            min-height: 80px;
        }}

        .navbar-left {{
            display: flex;
            align-items: center;
            gap: 1.5rem;
        }}

        .navbar-logo {{
            height: 70px;
            width: auto;
        }}

        .campus-pulse-logo {{
            height: 65px !important;
            width: auto !important;
        }}

        /* Mobile responsive */
        @media (max-width: 768px) {{
            .top-navbar {{
                flex-direction: column;
                gap: 1rem;
                padding: 1rem;
            }}
            .navbar-left {{
                flex-direction: column;
            }}
            .navbar-logo {{
                height: 45px;
            }}
            .campus-pulse-logo {{
                height: 40px !important;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)

    # Get current page
    try:
        current_page = st.session_state.get('current_page', 'Home')
    except:
        current_page = 'Home'

    # Create navbar HTML with logos only (no text)
    navbar_html = '<div class="top-navbar">'

    # Left side - Logos only (enlarged for readability)
    navbar_html += '<div class="navbar-left">'

    # UF Logo (loads from assets/images/uf_logo.png or falls back to external URL)
    navbar_html += get_uf_logo_html(css_class="navbar-logo", style="")

    # Campus Pulse logo (larger, no text) - using external image
    navbar_html += '<img src="https://i.imgur.com/QzDXZvZ.png" class="campus-pulse-logo" alt="Campus Pulse" />'

    navbar_html += '</div>'
    navbar_html += '</div>'
    st.markdown(navbar_html, unsafe_allow_html=True)

    # Create row with navigation buttons (center) and user info (right)
    nav_row = st.columns([2, 1, 1, 1, 1, 1, 0.5, 1, 1])

    # Navigation buttons in the center
    with nav_row[1]:
        if st.button("🏠 Home", key="nav_home", use_container_width=True,
                    type="primary" if current_page == 'Home' else "secondary"):
            st.session_state.current_page = 'Home'
            st.switch_page("app.py")

    with nav_row[2]:
        if st.button("🗺️ Crowd Map", key="nav_map", use_container_width=True,
                    type="primary" if current_page == 'Crowd Map' else "secondary"):
            st.session_state.current_page = 'Crowd Map'
            st.switch_page("pages/1_🗺️_Crowd_Heatmap.py")

    with nav_row[3]:
        if st.button("🎉 Events", key="nav_events", use_container_width=True,
                    type="primary" if current_page == 'Events' else "secondary"):
            st.session_state.current_page = 'Events'
            st.switch_page("pages/2_🎉_Events.py")

    with nav_row[4]:
        if st.button("⭐ Saved", key="nav_saved", use_container_width=True,
                    type="primary" if current_page == 'Saved' else "secondary"):
            st.session_state.current_page = 'Saved'
            st.switch_page("pages/3_⭐_Saved_Locations.py")

    with nav_row[5]:
        if st.button("🔄 Refresh", key="nav_refresh", use_container_width=True):
            # Trigger data refresh
            if 'last_refresh' in st.session_state:
                del st.session_state['last_refresh']
            if 'cached_crowd_data' in st.session_state:
                del st.session_state['cached_crowd_data']
            st.session_state.simulator = None  # Force regeneration
            st.rerun()

    # Theme toggle
    with nav_row[7]:
        theme_icon = "🌙" if st.session_state.theme == 'light' else "☀️"
        theme_label = f"{theme_icon}"
        if st.button(theme_label, key="theme_toggle", help="Toggle Dark/Light Theme", use_container_width=True):
            st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
            # Update user preference if logged in
            if 'user' in st.session_state and st.session_state.user:
                try:
                    from auth.auth_manager import AuthManager
                    auth = AuthManager()
                    # Note: Would need to add theme update to auth_manager
                except:
                    pass
            st.rerun()

    # User info / Sign in button on the right
    with nav_row[8]:
        if 'user' in st.session_state and st.session_state.user:
            user_name = st.session_state.user.get('full_name', '').split()[0]
            if st.button(f"👤 {user_name}", key="nav_profile_user", use_container_width=True,
                        type="primary" if current_page == 'Profile' else "secondary"):
                st.session_state.current_page = 'Profile'
                st.switch_page("pages/4_👤_Profile.py")
        else:
            if st.button("🔐 Sign In", key="nav_signin", use_container_width=True, type="primary"):
                st.session_state.current_page = 'Profile'
                st.switch_page("pages/4_👤_Profile.py")

    st.markdown("---")

def get_current_page_name():
    """Get the current page name from the script"""
    try:
        # Try to determine from the running script
        import sys
        script_path = sys.argv[0] if sys.argv else ''

        if 'Crowd_Heatmap' in script_path or 'crowd' in script_path.lower():
            return 'Crowd Map'
        elif 'Events' in script_path or 'events' in script_path.lower():
            return 'Events'
        elif 'Saved' in script_path or 'saved' in script_path.lower():
            return 'Saved'
        else:
            return 'Home'
    except:
        return st.session_state.get('current_page', 'Home')
