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
        bg_gradient = 'linear-gradient(90deg, #0a1929 0%, #1a2332 50%, #0a1929 100%)'
        bg_color = '#0a1929'
        text_color = '#FFFFFF'
        secondary_bg = '#1a2332'
        card_bg = '#162130'
        navbar_bg = '#030712'  # gray-950
        navbar_border = '#1f2937'  # gray-800
        button_text = '#e5e7eb'  # gray-200
        button_hover_bg = '#1f2937'  # gray-800
    else:
        bg_gradient = 'linear-gradient(90deg, #0021A5 0%, #FA4616 100%)'
        bg_color = '#FFFFFF'
        text_color = '#262730'
        secondary_bg = '#F0F2F6'
        card_bg = '#FAFAFA'
        navbar_bg = '#030712'  # gray-950 (dark navbar in light mode too)
        navbar_border = '#1f2937'  # gray-800
        button_text = '#e5e7eb'  # gray-200
        button_hover_bg = '#1f2937'  # gray-800

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

        /* Top navbar styles - Match React design */
        .top-navbar {{
            background: {navbar_bg};
            padding: 0 2.5rem;
            margin: -6rem -4rem 2rem -4rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            height: 80px;
            border-bottom: 1px solid {navbar_border};
            position: sticky;
            top: 0;
            z-index: 50;
        }}

        .navbar-left {{
            display: flex;
            align-items: center;
            flex-shrink: 0;
        }}

        .navbar-center {{
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            cursor: pointer;
        }}

        .navbar-right {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            flex-shrink: 0;
        }}

        .navbar-logo {{
            height: 80px;
            width: auto;
            object-fit: contain;
        }}

        .campus-pulse-logo {{
            height: 72px !important;
            width: auto !important;
            object-fit: contain !important;
        }}

        /* Button styling - Match React ghost variant */
        .stButton > button {{
            font-family: 'Inter', sans-serif !important;
            font-weight: 500 !important;
            border-radius: 6px !important;
            padding: 0.5rem 1rem !important;
            border: none !important;
            transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1) !important;
            font-size: 0.875rem !important;
            line-height: 1.25rem !important;
            height: 36px !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 0.5rem !important;
            white-space: nowrap !important;
            text-transform: uppercase !important;
            letter-spacing: 0.025em !important;
            background: transparent !important;
            color: {button_text} !important;
            box-shadow: none !important;
        }}

        .stButton > button:hover {{
            background-color: {button_hover_bg} !important;
            color: white !important;
        }}

        .stButton > button:active {{
            background-color: {button_hover_bg} !important;
        }}

        /* Primary buttons - Sign In */
        .stButton > button[kind="primary"] {{
            background-color: {button_hover_bg} !important;
            color: white !important;
        }}

        .stButton > button[kind="primary"]:hover {{
            background-color: #374151 !important;
        }}

        /* Secondary buttons - Ghost style */
        .stButton > button[kind="secondary"] {{
            background: transparent !important;
            color: {button_text} !important;
        }}

        .stButton > button[kind="secondary"]:hover {{
            background-color: {button_hover_bg} !important;
            color: white !important;
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
                padding: 0 1rem;
                height: auto;
                min-height: 60px;
            }}
            .navbar-left {{
                position: static;
            }}
            .navbar-center {{
                position: static;
                transform: none;
                left: auto;
                top: auto;
            }}
            .navbar-logo {{
                height: 50px;
            }}
            .campus-pulse-logo {{
                height: 50px !important;
            }}
            .stButton > button {{
                font-size: 0.75rem !important;
                padding: 0.4rem 0.8rem !important;
                height: 32px !important;
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
        # SVG fallback if no custom logo
        navbar_html += '''
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" class="campus-pulse-logo" style="height: 72px; width: 72px;">
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
    navbar_html += '</div>'  # Close navbar-center
    navbar_html += '</div>'  # Close top-navbar
    st.markdown(navbar_html, unsafe_allow_html=True)

    # Create row with CROWD, EVENTS buttons on right and username dropdown
    top_row = st.columns([8, 1, 1, 0.2, 1.2])

    with top_row[1]:
        if st.button("CROWD", key="nav_crowd_top", use_container_width=True, type="secondary"):
            st.session_state.current_page = 'Crowd Map'
            st.switch_page("pages/1_🗺️_Crowd_Heatmap.py")

    with top_row[2]:
        if st.button("EVENTS", key="nav_events_top", use_container_width=True, type="secondary"):
            st.session_state.current_page = 'Events'
            st.switch_page("pages/2_🎉_Events.py")

    with top_row[4]:
        # Username or Sign In button
        if 'user' in st.session_state and st.session_state.user:
            user_name = st.session_state.user.get('full_name', '').split()[0]
            if st.button(f"👤 {user_name.upper()}", key="nav_user_dropdown", use_container_width=True, type="secondary"):
                st.session_state.current_page = 'Profile'
                st.switch_page("pages/4_👤_Profile.py")
        else:
            if st.button("SIGN IN", key="nav_signin_top", use_container_width=True, type="primary"):
                st.session_state.current_page = 'Profile'
                st.switch_page("pages/4_👤_Profile.py")

    # Minimal spacing
    st.markdown("")

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
