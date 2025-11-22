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
        bg_gradient = 'linear-gradient(90deg, #000000 0%, #1a1a1a 50%, #000000 100%)'
        bg_color = '#000000'
        text_color = '#FFFFFF'
        secondary_bg = '#1a1a1a'
        card_bg = '#0d0d0d'
    else:
        bg_gradient = 'linear-gradient(90deg, #0021A5 0%, #FA4616 100%)'
        bg_color = '#FFFFFF'
        text_color = '#262730'
        secondary_bg = '#F0F2F6'
        card_bg = '#FAFAFA'

    # Custom CSS for top navbar - MODERN 2025 AESTHETIC
    st.markdown(f"""
    <style>
        /* Import modern fonts from Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap');

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

        /* Text elements - NO aggressive font overrides */
        .stMarkdown, .stText {{
            color: {text_color} !important;
        }}

        p {{
            color: {text_color} !important;
            line-height: 1.6;
        }}

        /* Headings with modern font */
        h1, h2, h3, h4, h5, h6 {{
            color: {text_color} !important;
            font-family: 'Outfit', 'Inter', sans-serif !important;
            font-weight: 700 !important;
            line-height: 1.4 !important;
            margin-top: 1rem !important;
            margin-bottom: 0.75rem !important;
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

        /* Top navbar styles - Modern with smooth animations */
        .top-navbar {{
            background: {bg_gradient};
            padding: 1.5rem 2.5rem;
            margin: -6rem -4rem 2rem -4rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            backdrop-filter: blur(10px);
            min-height: 100px;
            height: auto;
            overflow: visible;
            border-bottom: 2px solid rgba(255,255,255,0.1);
            animation: slideDown 0.5s ease-out;
            position: relative;
            z-index: 1000;
        }}

        @keyframes slideDown {{
            from {{
                transform: translateY(-100%);
                opacity: 0;
            }}
            to {{
                transform: translateY(0);
                opacity: 1;
            }}
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        @keyframes scaleIn {{
            from {{ transform: scale(0.95); opacity: 0; }}
            to {{ transform: scale(1); opacity: 1; }}
        }}

        .navbar-left {{
            display: flex;
            align-items: center;
            gap: 2rem;
            flex-shrink: 0;
            animation: fadeIn 0.7s ease-out 0.2s both;
        }}

        .navbar-center {{
            display: flex;
            align-items: center;
            justify-content: center;
            flex: 1;
            animation: scaleIn 0.6s ease-out 0.1s both;
        }}

        .navbar-right {{
            display: flex;
            align-items: center;
            gap: 1rem;
            flex-shrink: 0;
        }}

        .navbar-logo {{
            height: 75px;
            width: auto;
            max-width: none;
            object-fit: contain;
            filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            animation: scaleIn 0.6s ease-out;
        }}

        .navbar-logo:hover {{
            transform: scale(1.08) rotate(2deg);
            filter: drop-shadow(0 8px 16px rgba(0,0,0,0.4));
        }}

        .campus-pulse-logo {{
            height: 80px !important;
            width: auto !important;
            max-width: none !important;
            object-fit: contain !important;
            filter: drop-shadow(0 6px 12px rgba(0,0,0,0.4));
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            animation: scaleIn 0.6s ease-out 0.1s both;
        }}

        .campus-pulse-logo:hover {{
            transform: scale(1.1) rotate(-2deg);
            filter: drop-shadow(0 10px 20px rgba(0,0,0,0.5));
        }}

        /* Modern button styling with animations */
        .stButton > button {{
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            border-radius: 10px !important;
            padding: 0.65rem 1.2rem !important;
            border: none !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            font-size: 0.9rem !important;
            line-height: 1.4 !important;
            height: 44px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            white-space: nowrap !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.15) !important;
            position: relative !important;
            overflow: hidden !important;
            animation: fadeIn 0.5s ease-out both;
        }}

        .stButton > button::before {{
            content: '' !important;
            position: absolute !important;
            top: 50% !important;
            left: 50% !important;
            width: 0 !important;
            height: 0 !important;
            border-radius: 50% !important;
            background: rgba(255,255,255,0.1) !important;
            transform: translate(-50%, -50%) !important;
            transition: width 0.6s, height 0.6s !important;
        }}

        .stButton > button:hover::before {{
            width: 300px !important;
            height: 300px !important;
        }}

        .stButton > button:hover {{
            transform: translateY(-3px) scale(1.02) !important;
            box-shadow: 0 8px 25px rgba(0,0,0,0.25) !important;
        }}

        .stButton > button:active {{
            transform: translateY(-1px) scale(0.98) !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
        }}

        /* Primary buttons */
        .stButton > button[kind="primary"] {{
            background: linear-gradient(135deg, #0021A5 0%, #FA4616 100%) !important;
            color: white !important;
            box-shadow: 0 4px 15px rgba(0,33,165,0.3) !important;
        }}

        .stButton > button[kind="primary"]:hover {{
            background: linear-gradient(135deg, #001a85 0%, #e63f12 100%) !important;
            box-shadow: 0 8px 30px rgba(0,33,165,0.4) !important;
        }}

        /* Secondary buttons */
        .stButton > button[kind="secondary"] {{
            background-color: {card_bg} !important;
            color: {text_color} !important;
            border: 1.5px solid rgba(128,128,128,0.3) !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
        }}

        .stButton > button[kind="secondary"]:hover {{
            border-color: rgba(0,33,165,0.5) !important;
            background-color: {secondary_bg} !important;
            box-shadow: 0 6px 20px rgba(0,0,0,0.2) !important;
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
            .navbar-left, .navbar-center, .navbar-right {{
                width: 100%;
                justify-content: center;
            }}
            .navbar-logo {{
                height: 50px;
            }}
            .campus-pulse-logo {{
                height: 60px !important;
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

    # Create navbar HTML with centered Campus Pulse logo
    navbar_html = '<div class="top-navbar">'

    # Left side - UF Logo
    navbar_html += '<div class="navbar-left">'
    navbar_html += get_uf_logo_html(css_class="navbar-logo", style="")
    navbar_html += '</div>'

    # Center - Campus Pulse logo (enlarged for readability)
    navbar_html += '<div class="navbar-center">'
    campus_logo = get_campus_pulse_logo_html(css_class="campus-pulse-logo", style="")

    if campus_logo:
        navbar_html += campus_logo
    else:
        # SVG fallback if no custom logo - larger thermal heatmap
        navbar_html += '''
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" class="campus-pulse-logo" style="height: 80px; width: 80px;">
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

    # Right side - Empty for now (could add user quick actions later)
    navbar_html += '<div class="navbar-right"></div>'

    navbar_html += '</div>'
    st.markdown(navbar_html, unsafe_allow_html=True)

    # Create row with navigation buttons (center) and user info (right)
    nav_row = st.columns([1.5, 1, 1, 1, 1, 1, 0.3, 0.8, 1])

    # Navigation buttons in the center
    with nav_row[1]:
        if st.button("Home", key="nav_home", use_container_width=True,
                    type="primary" if current_page == 'Home' else "secondary"):
            st.session_state.current_page = 'Home'
            st.switch_page("app.py")

    with nav_row[2]:
        if st.button("Crowd Map", key="nav_map", use_container_width=True,
                    type="primary" if current_page == 'Crowd Map' else "secondary"):
            st.session_state.current_page = 'Crowd Map'
            st.switch_page("pages/1_🗺️_Crowd_Heatmap.py")

    with nav_row[3]:
        if st.button("Events", key="nav_events", use_container_width=True,
                    type="primary" if current_page == 'Events' else "secondary"):
            st.session_state.current_page = 'Events'
            st.switch_page("pages/2_🎉_Events.py")

    with nav_row[4]:
        if st.button("Saved", key="nav_saved", use_container_width=True,
                    type="primary" if current_page == 'Saved' else "secondary"):
            st.session_state.current_page = 'Saved'
            st.switch_page("pages/3_⭐_Saved_Locations.py")

    with nav_row[5]:
        if st.button("Refresh", key="nav_refresh", use_container_width=True):
            # Trigger data refresh
            if 'last_refresh' in st.session_state:
                del st.session_state['last_refresh']
            if 'cached_crowd_data' in st.session_state:
                del st.session_state['cached_crowd_data']
            st.session_state.simulator = None  # Force regeneration
            st.rerun()

    # Theme toggle
    with nav_row[7]:
        theme_label = "Light" if st.session_state.theme == 'dark' else "Dark"
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
            if st.button(f"{user_name}", key="nav_profile_user", use_container_width=True,
                        type="primary" if current_page == 'Profile' else "secondary"):
                st.session_state.current_page = 'Profile'
                st.switch_page("pages/4_👤_Profile.py")
        else:
            if st.button("Sign In", key="nav_signin", use_container_width=True, type="primary"):
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
