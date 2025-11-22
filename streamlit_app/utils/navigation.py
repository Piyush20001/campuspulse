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

    # Custom CSS for top navbar - MODERN 2025 AESTHETIC
    st.markdown(f"""
    <style>
        /* Import modern fonts from Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap');

        /* FORCE THEME COLORS - Override all Streamlit defaults */
        * {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        }}

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

        /* All text elements with modern typography */
        .stMarkdown, .stText, p, span, div {{
            color: {text_color} !important;
            font-family: 'Inter', sans-serif !important;
            line-height: 1.6 !important;
        }}

        /* Headings with modern font */
        h1, h2, h3, h4, h5, h6 {{
            color: {text_color} !important;
            font-family: 'Outfit', 'Inter', sans-serif !important;
            font-weight: 700 !important;
            line-height: 1.3 !important;
            margin-bottom: 0.5rem !important;
        }}

        h1 {{ font-size: 2.5rem !important; }}
        h2 {{ font-size: 2rem !important; }}
        h3 {{ font-size: 1.5rem !important; }}

        /* Metrics and stats */
        [data-testid="stMetricValue"] {{
            color: {text_color} !important;
            font-family: 'Outfit', sans-serif !important;
            font-weight: 700 !important;
        }}

        [data-testid="stMetricLabel"] {{
            color: {text_color} !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 500 !important;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.05em;
        }}

        /* Modern cards and containers */
        [data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"] {{
            background-color: {secondary_bg} !important;
        }}

        /* Hide default sidebar */
        [data-testid="stSidebar"] {{
            display: none;
        }}

        /* Top navbar styles - Modern glassmorphism */
        .top-navbar {{
            background: {bg_gradient};
            padding: 1rem 2.5rem;
            margin: -6rem -4rem 2rem -4rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 8px 32px rgba(0,0,0,0.15);
            backdrop-filter: blur(10px);
            min-height: 85px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}

        .navbar-left {{
            display: flex;
            align-items: center;
            gap: 2rem;
        }}

        .navbar-logo {{
            height: 75px;
            width: auto;
            filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));
            transition: transform 0.3s ease, filter 0.3s ease;
        }}

        .navbar-logo:hover {{
            transform: scale(1.05);
            filter: drop-shadow(0 6px 12px rgba(0,0,0,0.3));
        }}

        .campus-pulse-logo {{
            height: 70px !important;
            width: auto !important;
            filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));
            transition: transform 0.3s ease, filter 0.3s ease;
        }}

        .campus-pulse-logo:hover {{
            transform: scale(1.05);
            filter: drop-shadow(0 6px 12px rgba(0,0,0,0.3));
        }}

        /* Modern button styling */
        .stButton > button {{
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            border-radius: 12px !important;
            padding: 0.6rem 1.2rem !important;
            border: none !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            font-size: 0.95rem !important;
            line-height: 1.5 !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
        }}

        .stButton > button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(0,0,0,0.2) !important;
        }}

        .stButton > button:active {{
            transform: translateY(0px) !important;
        }}

        /* Primary buttons */
        .stButton > button[kind="primary"] {{
            background: linear-gradient(135deg, #0021A5 0%, #FA4616 100%) !important;
            color: white !important;
        }}

        .stButton > button[kind="primary"]:hover {{
            background: linear-gradient(135deg, #001a85 0%, #e63f12 100%) !important;
        }}

        /* Secondary buttons */
        .stButton > button[kind="secondary"] {{
            background-color: {secondary_bg} !important;
            color: {text_color} !important;
            border: 2px solid rgba(0,33,165,0.2) !important;
        }}

        .stButton > button[kind="secondary"]:hover {{
            border-color: rgba(0,33,165,0.4) !important;
            background-color: {secondary_bg} !important;
        }}

        /* Modern input fields */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {{
            font-family: 'Inter', sans-serif !important;
            border-radius: 10px !important;
            border: 2px solid rgba(0,33,165,0.15) !important;
            padding: 0.75rem !important;
            font-size: 0.95rem !important;
            transition: all 0.3s ease !important;
            background-color: {secondary_bg} !important;
            color: {text_color} !important;
        }}

        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {{
            border-color: #0021A5 !important;
            box-shadow: 0 0 0 3px rgba(0,33,165,0.1) !important;
        }}

        /* Input labels */
        .stTextInput > label, .stTextArea > label, .stSelectbox > label,
        .stNumberInput > label, .stMultiSelect > label, .stRadio > label {{
            color: {text_color} !important;
            font-weight: 500 !important;
        }}

        /* Modern selectbox */
        .stSelectbox > div > div {{
            font-family: 'Inter', sans-serif !important;
            border-radius: 10px !important;
        }}

        .stSelectbox [data-baseweb="select"] {{
            background-color: {secondary_bg} !important;
        }}

        .stSelectbox [data-baseweb="select"] > div {{
            color: {text_color} !important;
            background-color: {secondary_bg} !important;
        }}

        /* Dropdown options */
        [role="option"] {{
            color: {text_color} !important;
            background-color: {secondary_bg} !important;
        }}

        [role="option"]:hover {{
            background-color: {bg_color} !important;
        }}

        /* Fix all text in tabs, expandersexpander headers, etc */
        .stTabs [data-baseweb="tab"] p {{
            color: {text_color} !important;
        }}

        details summary {{
            color: {text_color} !important;
        }}

        /* Fix info/warning/error/success boxes text */
        .stAlert, .stAlert p, .stAlert div {{
            color: #262730 !important;
        }}

        /* Fix dataframe/table text */
        .stDataFrame, .stDataFrame * {{
            color: {text_color} !important;
        }}

        /* Fix checkbox and radio text */
        .stCheckbox label, .stRadio label {{
            color: {text_color} !important;
        }}

        /* Fix Plotly chart elements and text overlap */
        .js-plotly-plot .plotly {{
            line-height: normal !important;
        }}

        /* Fix expander headers globally */
        .streamlit-expanderHeader {{
            line-height: 1.5 !important;
            overflow: visible !important;
        }}

        .streamlit-expanderHeader p, .streamlit-expanderHeader span {{
            line-height: 1.5 !important;
            margin: 0 !important;
            white-space: normal !important;
        }}

        /* Ensure proper text rendering everywhere */
        * {{
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
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
                gap: 1rem;
            }}
            .navbar-logo {{
                height: 50px;
            }}
            .campus-pulse-logo {{
                height: 45px !important;
            }}
            h1 {{ font-size: 1.75rem !important; }}
            h2 {{ font-size: 1.5rem !important; }}
            h3 {{ font-size: 1.25rem !important; }}
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

    # Campus Pulse logo (loads from assets/images/campus_pulse_logo.png or uses SVG fallback)
    campus_logo = get_campus_pulse_logo_html(css_class="campus-pulse-logo", style="")

    if campus_logo:
        navbar_html += campus_logo
    else:
        # SVG fallback if no custom logo - larger thermal heatmap
        navbar_html += '''
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" class="campus-pulse-logo" style="height: 65px; width: 65px;">
          <defs>
            <radialGradient id="heatGradient">
              <stop offset="0%" style="stop-color:#FA4616;stop-opacity:1" />
              <stop offset="50%" style="stop-color:#FFA500;stop-opacity:0.7" />
              <stop offset="100%" style="stop-color:#0021A5;stop-opacity:0.3" />
            </radialGradient>
          </defs>
          <circle cx="50" cy="50" r="45" fill="url(#heatGradient)"/>
          <circle cx="50" cy="50" r="32" fill="none" stroke="white" stroke-width="3" opacity="0.6"/>
          <circle cx="50" cy="50" r="20" fill="none" stroke="white" stroke-width="2" opacity="0.4"/>
          <circle cx="50" cy="50" r="12" fill="white"/>
        </svg>
        '''

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
