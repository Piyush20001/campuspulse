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

    # Dark mode only - matching src/components/Header.tsx design
    bg_color = '#030712'  # gray-950 - main background
    text_color = '#e5e7eb'  # gray-200 - text color
    secondary_bg = '#1f2937'  # gray-800 - secondary elements
    card_bg = '#111827'  # gray-900 - cards and containers
    navbar_bg = '#030712'  # gray-950 - navbar background
    navbar_border = '#1f2937'  # gray-800 - borders
    button_text = '#e5e7eb'  # gray-200 - button text
    button_hover_bg = '#1f2937'  # gray-800 - button hover

    # Custom CSS for top navbar - MODERN 2025 AESTHETIC
    st.markdown(f"""
    <style>
        /* Import Inter font - matching src design */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        /* Set base font for entire app */
        html, body, .stApp, [data-testid="stAppViewContainer"] {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        }}

        /* FORCE DARK MODE COLORS - Override all Streamlit defaults */
        .stApp {{
            background-color: {bg_color} !important;
        }}

        [data-testid="stAppViewContainer"] {{
            background-color: {bg_color} !important;
        }}

        /* Hide Streamlit's default header completely */
        [data-testid="stHeader"] {{
            display: none !important;
        }}

        header[data-testid="stHeader"] {{
            display: none !important;
        }}

        .stApp > header {{
            display: none !important;
        }}

        .main {{
            background-color: {bg_color} !important;
            color: {text_color} !important;
            font-family: 'Inter', sans-serif !important;
        }}

        .main .block-container {{
            padding-top: 1rem;
            max-width: 100%;
            background-color: {bg_color} !important;
            color: {text_color} !important;
        }}

        /* Force all text elements to use dark mode colors and Inter font */
        .main * {{
            color: {text_color} !important;
            font-family: 'Inter', sans-serif !important;
        }}

        /* Override Streamlit's default white backgrounds */
        section[data-testid="stSidebar"] > div {{
            background-color: {bg_color} !important;
        }}

        div[data-testid="stVerticalBlock"] {{
            background-color: {bg_color} !important;
        }}

        div[data-testid="stHorizontalBlock"] {{
            background-color: {bg_color} !important;
        }}

        div[data-testid="column"] {{
            background-color: {bg_color} !important;
        }}

        /* Text elements - NO aggressive font overrides */
        .stMarkdown, .stText {{
            color: {text_color} !important;
        }}

        p {{
            color: {text_color} !important;
            line-height: 1.6;
            font-family: 'Inter', sans-serif !important;
        }}

        /* Headings - Inter font matching src design */
        h1, h2, h3, h4, h5, h6 {{
            color: {text_color} !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            line-height: 1.4 !important;
            margin-top: 1rem !important;
            margin-bottom: 0.75rem !important;
        }}

        h1 {{
            font-size: 2.5rem !important;
            color: {text_color} !important;
            font-weight: 700 !important;
        }}
        h2 {{
            font-size: 2rem !important;
            color: {text_color} !important;
            font-weight: 600 !important;
        }}
        h3 {{
            font-size: 1.5rem !important;
            color: {text_color} !important;
            font-weight: 600 !important;
        }}
        h4, h5, h6 {{
            color: {text_color} !important;
            font-weight: 500 !important;
        }}

        /* Metrics and stats */
        [data-testid="stMetricValue"] {{
            color: {text_color} !important;
            font-family: 'Inter', sans-serif !important;
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

        /* Modern cards and containers - dark mode */
        [data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"] {{
            background-color: {bg_color} !important;
        }}

        /* Hide default sidebar */
        [data-testid="stSidebar"] {{
            display: none !important;
        }}

        /* Hide Streamlit toolbar/hamburger menu */
        #MainMenu {{
            display: none !important;
        }}

        footer {{
            display: none !important;
        }}

        .stDeployButton {{
            display: none !important;
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

        /* Navigation buttons in navbar */
        .nav-button {{
            font-family: 'Inter', sans-serif;
            font-weight: 500;
            font-size: 0.875rem;
            color: {button_text};
            background-color: transparent;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.25rem;
            white-space: nowrap;
            text-transform: uppercase;
            letter-spacing: 0.025em;
        }}

        .nav-button:hover {{
            background-color: {button_hover_bg};
            color: white;
        }}

        .nav-button-primary {{
            background-color: {button_hover_bg} !important;
            color: white !important;
        }}

        .nav-button-primary:hover {{
            background-color: #374151 !important;
        }}

        /* Dropdown styles */
        .dropdown {{
            position: relative;
            display: inline-block;
        }}

        .dropdown-toggle {{
            text-transform: none !important;
        }}

        .dropdown-menu {{
            display: none;
            position: absolute;
            right: 0;
            top: 100%;
            margin-top: 0.5rem;
            background-color: #111827;
            border: 1px solid {navbar_border};
            border-radius: 8px;
            min-width: 200px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
            z-index: 1000;
            padding: 0.5rem 0;
        }}

        .dropdown-menu.show {{
            display: block;
        }}

        .dropdown-item {{
            display: block;
            width: 100%;
            padding: 0.5rem 1rem;
            color: {button_text};
            text-decoration: none;
            font-family: 'Inter', sans-serif;
            font-size: 0.875rem;
            transition: background-color 0.15s;
            cursor: pointer;
            text-align: left;
        }}

        .dropdown-item:hover {{
            background-color: {button_hover_bg};
            color: white;
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
            height: 100px !important;
            width: auto !important;
            object-fit: contain !important;
        }}

        /* Position button row into navbar area */
        .main > .block-container > div:first-of-type {{
            margin-top: -80px !important;
            padding-top: 20px !important;
            padding-right: 2.5rem !important;
            position: relative !important;
            z-index: 100 !important;
            pointer-events: none !important;
        }}

        .main > .block-container > div:first-of-type [data-testid="column"] {{
            pointer-events: auto !important;
            background-color: transparent !important;
        }}

        /* Add spacing after navbar for content */
        .main > .block-container > div:nth-of-type(2) {{
            margin-top: 2rem !important;
        }}

        /* Navbar button styling - Match React ghost variant */
        [data-testid="column"] .stButton > button {{
            font-family: 'Inter', sans-serif !important;
            font-weight: 500 !important;
            background-color: transparent !important;
            border: none !important;
            color: {button_text} !important;
            text-transform: uppercase !important;
            font-size: 0.875rem !important;
            padding: 0.5rem 1rem !important;
            border-radius: 6px !important;
        }}

        [data-testid="column"] .stButton > button:hover {{
            background-color: {button_hover_bg} !important;
            color: white !important;
        }}

        [data-testid="column"] .stButton > button[kind="primary"] {{
            background-color: {button_hover_bg} !important;
            color: white !important;
        }}

        [data-testid="column"] .stButton > button[kind="primary"]:hover {{
            background-color: #374151 !important;
        }}

        /* Expander for user dropdown */
        [data-testid="column"] .streamlit-expanderHeader {{
            background-color: transparent !important;
            border: none !important;
            color: {button_text} !important;
            font-weight: 500 !important;
            padding: 0.5rem 1rem !important;
            border-radius: 6px !important;
            font-size: 0.875rem !important;
        }}

        [data-testid="column"] .streamlit-expanderHeader:hover {{
            background-color: {button_hover_bg} !important;
        }}

        [data-testid="column"] details {{
            border: none !important;
        }}

        [data-testid="column"] details[open] summary {{
            border-bottom: none !important;
        }}

        /* Button styling - Match React ghost variant */
        .stButton > button {{
            font-family: 'Inter', sans-serif !important;
            font-weight: 500 !important;
            border-radius: 6px !important;
            padding: 0.5rem 1rem !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1) !important;
            font-size: 0.875rem !important;
            line-height: 1.25rem !important;
            height: 36px !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 0.5rem !important;
            white-space: nowrap !important;
            text-transform: none !important;
            letter-spacing: 0.025em !important;
            background-color: {secondary_bg} !important;
            color: {text_color} !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
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

        /* Secondary buttons */
        .stButton > button[kind="secondary"] {{
            background-color: {secondary_bg} !important;
            color: {text_color} !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }}

        .stButton > button[kind="secondary"]:hover {{
            background-color: {card_bg} !important;
            color: white !important;
            border-color: rgba(255, 255, 255, 0.2) !important;
        }}

        /* Navbar buttons specific styling */
        [data-testid="column"] .stButton > button {{
            background-color: transparent !important;
            border: none !important;
            color: {button_text} !important;
            text-transform: uppercase !important;
        }}

        [data-testid="column"] .stButton > button:hover {{
            background-color: {button_hover_bg} !important;
            color: white !important;
        }}

        [data-testid="column"] .stButton > button[kind="primary"] {{
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

        /* Fix info/warning/error/success boxes text - dark mode visible */
        .stAlert, .stAlert p, .stAlert div, .stAlert span {{
            color: {text_color} !important;
        }}

        /* Alert boxes - ensure background contrast */
        .stAlert {{
            background-color: rgba(31, 41, 55, 0.5) !important;
            border-left: 4px solid {text_color} !important;
        }}

        /* Warning/Error/Success/Info boxes - all visible in dark mode */
        [data-testid="stNotification"],
        [data-testid="stNotificationContentWarning"],
        [data-testid="stNotificationContentError"],
        [data-testid="stNotificationContentSuccess"],
        [data-testid="stNotificationContentInfo"] {{
            color: {text_color} !important;
        }}

        [data-testid="stNotification"] * {{
            color: {text_color} !important;
        }}

        /* Fix dataframe/table text */
        .stDataFrame, .stDataFrame * {{
            color: {text_color} !important;
        }}

        /* Fix checkbox and radio text */
        .stCheckbox label, .stRadio label {{
            color: {text_color} !important;
        }}

        /* Ensure all labels are visible */
        label {{
            color: {text_color} !important;
        }}

        /* Fix divs and spans */
        div, span {{
            color: inherit;
        }}

        /* Make sure markdown content is visible */
        .stMarkdown {{
            color: {text_color} !important;
        }}

        .stMarkdown * {{
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

    # Create navbar HTML matching React design exactly
    navbar_html = '<div class="top-navbar">'

    # Left side - UF Logo
    navbar_html += '<div class="navbar-left">'
    navbar_html += get_uf_logo_html(css_class="navbar-logo", style="")
    navbar_html += '</div>'

    # Center - Campus Pulse logo
    navbar_html += '<div class="navbar-center">'
    campus_logo = get_campus_pulse_logo_html(css_class="campus-pulse-logo", style="")

    if campus_logo:
        navbar_html += campus_logo
    else:
        # SVG fallback if no custom logo
        navbar_html += '''
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" class="campus-pulse-logo" style="height: 100px; width: 100px;">
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

    # Right side - empty div for spacing (buttons will be Streamlit widgets below)
    navbar_html += '<div class="navbar-right"></div>'
    navbar_html += '</div>'  # Close top-navbar

    # Use components.html for navbar without buttons
    import streamlit.components.v1 as components

    # Wrap navbar in proper HTML structure with CSS
    full_navbar_html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                padding: 0;
                font-family: 'Inter', sans-serif;
                overflow: hidden;
            }}
            .top-navbar {{
                background: {navbar_bg};
                padding: 0 2.5rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
                height: 80px;
                border-bottom: 1px solid {navbar_border};
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
            .navbar-logo {{
                height: 80px;
                width: auto;
                object-fit: contain;
            }}
            .campus-pulse-logo {{
                height: 100px !important;
                width: auto !important;
                object-fit: contain !important;
            }}
        </style>
    </head>
    <body>
        {navbar_html}
    </body>
    </html>
    '''

    components.html(full_navbar_html, height=80, scrolling=False)

    # Add Streamlit buttons below navbar, positioned to appear in navbar
    # Create columns for right-side buttons
    button_cols = st.columns([8.5, 1.2, 1, 1])

    with button_cols[1]:
        # Check if user is logged in
        if 'user' in st.session_state and st.session_state.user:
            # Show username button with dropdown in expander
            user_name = st.session_state.user.get('full_name', 'User').split()[0]
            with st.expander(f"👤 {user_name.upper()}", expanded=False):
                if st.button("📍 Saved Locations", key="nav_saved", use_container_width=True):
                    st.session_state.current_page = 'Saved'
                    st.switch_page("pages/3_📍_Saved_Locations.py")
                if st.button("⚙️ Settings", key="nav_settings", use_container_width=True):
                    st.info("Settings page coming soon!")
                if st.button("🚪 Sign Out", key="nav_signout", use_container_width=True):
                    st.session_state.user = None
                    st.session_state.current_page = 'Home'
                    st.rerun()
        else:
            # Show sign in button
            if st.button("SIGN IN", key="nav_signin", use_container_width=True, type="primary"):
                st.session_state.current_page = 'Profile'
                st.switch_page("pages/4_👤_Profile.py")

    with button_cols[2]:
        if st.button("CROWD", key="nav_crowd", use_container_width=True, type="secondary"):
            st.session_state.current_page = 'Crowd Map'
            st.switch_page("pages/1_🗺️_Crowd_Heatmap.py")

    with button_cols[3]:
        if st.button("EVENTS", key="nav_events", use_container_width=True, type="secondary"):
            st.session_state.current_page = 'Events'
            st.switch_page("pages/2_🎉_Events.py")

    # Handle navigation from URL query parameters
    query_params = st.query_params
    if 'nav' in query_params:
        nav_action = query_params['nav']

        # Clear the nav parameter
        del st.query_params['nav']

        if nav_action == 'crowd':
            st.session_state.current_page = 'Crowd Map'
            st.switch_page("pages/1_🗺️_Crowd_Heatmap.py")
        elif nav_action == 'events':
            st.session_state.current_page = 'Events'
            st.switch_page("pages/2_🎉_Events.py")
        elif nav_action == 'signin':
            st.session_state.current_page = 'Profile'
            st.switch_page("pages/4_👤_Profile.py")
        elif nav_action == 'saved':
            st.session_state.current_page = 'Saved'
            st.switch_page("pages/3_📍_Saved_Locations.py")
        elif nav_action == 'settings':
            st.info("Settings page coming soon!")
        elif nav_action == 'signout':
            st.session_state.user = None
            st.session_state.current_page = 'Home'
            st.rerun()

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
