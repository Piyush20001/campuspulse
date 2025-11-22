"""
Top navigation bar component
"""
import streamlit as st

def create_top_navbar():
    """Create a horizontal navigation bar at the top"""

    # Custom CSS for top navbar
    st.markdown("""
    <style>
        /* Hide default sidebar */
        [data-testid="stSidebar"] {
            display: none;
        }

        /* Top navbar styles */
        .top-navbar {
            background: linear-gradient(90deg, #0021A5 0%, #FA4616 100%);
            padding: 1rem 2rem;
            margin: -6rem -4rem 2rem -4rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .navbar-brand {
            color: white;
            font-size: 1.5rem;
            font-weight: bold;
            text-decoration: none;
        }

        .navbar-links {
            display: flex;
            gap: 1rem;
            align-items: center;
        }

        .nav-button {
            background: rgba(255,255,255,0.2);
            color: white;
            border: 1px solid rgba(255,255,255,0.3);
            padding: 0.5rem 1.5rem;
            border-radius: 5px;
            text-decoration: none;
            transition: all 0.3s;
            cursor: pointer;
            font-weight: 500;
        }

        .nav-button:hover {
            background: rgba(255,255,255,0.3);
            border-color: rgba(255,255,255,0.5);
            transform: translateY(-2px);
        }

        .nav-button.active {
            background: white;
            color: #0021A5;
            border-color: white;
        }

        /* Adjust main content area */
        .main .block-container {
            padding-top: 1rem;
            max-width: 100%;
        }

        /* Mobile responsive */
        @media (max-width: 768px) {
            .top-navbar {
                flex-direction: column;
                gap: 1rem;
            }
            .navbar-links {
                flex-wrap: wrap;
                justify-content: center;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    # Get current page
    try:
        current_page = st.session_state.get('current_page', 'Home')
    except:
        current_page = 'Home'

    # Navigation buttons data
    pages = [
        {'name': 'Home', 'icon': '🏠', 'file': 'app.py'},
        {'name': 'Crowd Map', 'icon': '🗺️', 'file': 'pages/1_🗺️_Crowd_Heatmap.py'},
        {'name': 'Events', 'icon': '🎉', 'file': 'pages/2_🎉_Events.py'},
        {'name': 'Saved', 'icon': '⭐', 'file': 'pages/3_⭐_Saved_Locations.py'},
    ]

    # Create navbar HTML
    navbar_html = '<div class="top-navbar">'
    navbar_html += '<div class="navbar-brand">🎓 Campus Pulse - University of Florida</div>'
    navbar_html += '<div class="navbar-links">'

    # We'll use columns for navigation instead of HTML links
    navbar_html += '</div></div>'
    st.markdown(navbar_html, unsafe_allow_html=True)

    # Create navigation buttons using Streamlit columns
    cols = st.columns([1, 1, 1, 1, 1, 3])

    with cols[0]:
        if st.button("🏠 Home", key="nav_home", use_container_width=True,
                    type="primary" if current_page == 'Home' else "secondary"):
            st.session_state.current_page = 'Home'
            st.switch_page("app.py")

    with cols[1]:
        if st.button("🗺️ Crowd Map", key="nav_map", use_container_width=True,
                    type="primary" if current_page == 'Crowd Map' else "secondary"):
            st.session_state.current_page = 'Crowd Map'
            st.switch_page("pages/1_🗺️_Crowd_Heatmap.py")

    with cols[2]:
        if st.button("🎉 Events", key="nav_events", use_container_width=True,
                    type="primary" if current_page == 'Events' else "secondary"):
            st.session_state.current_page = 'Events'
            st.switch_page("pages/2_🎉_Events.py")

    with cols[3]:
        if st.button("⭐ Saved", key="nav_saved", use_container_width=True,
                    type="primary" if current_page == 'Saved' else "secondary"):
            st.session_state.current_page = 'Saved'
            st.switch_page("pages/3_⭐_Saved_Locations.py")

    with cols[4]:
        if st.button("🔄 Refresh", key="nav_refresh", use_container_width=True):
            # Trigger data refresh
            if 'last_refresh' in st.session_state:
                del st.session_state['last_refresh']
            if 'cached_crowd_data' in st.session_state:
                del st.session_state['cached_crowd_data']
            st.session_state.simulator = None  # Force regeneration
            st.rerun()

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
