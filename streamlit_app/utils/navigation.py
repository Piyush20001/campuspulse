"""
Top navigation bar component
"""
import streamlit as st
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

    # Custom CSS for top navbar
    st.markdown(f"""
    <style>
        /* Hide default sidebar */
        [data-testid="stSidebar"] {{
            display: none;
        }}

        /* Apply theme to body */
        .main {{
            background-color: {bg_color};
            color: {text_color};
        }}

        .stMarkdown, .stText {{
            color: {text_color};
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
            min-height: 70px;
        }}

        .navbar-left {{
            display: flex;
            align-items: center;
            gap: 1rem;
        }}

        .navbar-logo {{
            height: 50px;
            width: auto;
        }}

        .navbar-brand {{
            color: white;
            font-size: 1.3rem;
            font-weight: bold;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .pulse-logo {{
            font-size: 2rem;
        }}

        .navbar-right {{
            display: flex;
            align-items: center;
            gap: 1rem;
            color: white;
        }}

        .user-info {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background: rgba(255,255,255,0.15);
            border-radius: 25px;
            font-weight: 500;
        }}

        .theme-toggle {{
            cursor: pointer;
            padding: 0.5rem;
            background: rgba(255,255,255,0.15);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s;
        }}

        .theme-toggle:hover {{
            background: rgba(255,255,255,0.25);
            transform: scale(1.1);
        }}

        /* Adjust main content area */
        .main .block-container {{
            padding-top: 1rem;
            max-width: 100%;
            background-color: {bg_color};
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
                height: 35px;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)

    # Get current page
    try:
        current_page = st.session_state.get('current_page', 'Home')
    except:
        current_page = 'Home'

    # Create navbar HTML with logos and branding
    navbar_html = '<div class="top-navbar">'

    # Left side - Logos and branding
    navbar_html += '<div class="navbar-left">'
    navbar_html += '<img src="https://i.imgur.com/5bZvhKL.png" class="navbar-logo" alt="UF Logo" />'

    # Campus Pulse logo with heat gradient
    navbar_html += '''
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 60" class="navbar-logo" style="height: 45px; width: 45px; margin: 0 0.5rem;">
      <defs>
        <radialGradient id="heatGradient">
          <stop offset="0%" style="stop-color:#FA4616;stop-opacity:1" />
          <stop offset="50%" style="stop-color:#FFA500;stop-opacity:0.7" />
          <stop offset="100%" style="stop-color:#0021A5;stop-opacity:0.3" />
        </radialGradient>
      </defs>
      <circle cx="30" cy="30" r="25" fill="url(#heatGradient)"/>
      <circle cx="30" cy="30" r="18" fill="none" stroke="white" stroke-width="2" opacity="0.6"/>
      <circle cx="30" cy="30" r="8" fill="white"/>
    </svg>
    '''

    navbar_html += '<div class="navbar-brand">'
    navbar_html += '<span>Campus Pulse</span>'
    navbar_html += '</div>'
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
