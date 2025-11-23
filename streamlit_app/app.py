"""
Campus Pulse - Main Streamlit Application
AI-powered real-time campus crowd and event intelligence platform
"""
import streamlit as st
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.simulator import CrowdDataSimulator
from data.uf_events_real import UFEventGenerator
from data.locations import UF_LOCATIONS
from models.lstm_forecaster import CrowdForecaster
from models.event_classifier_improved import ImprovedEventCategorizer
from models.anomaly_detector import AnomalyDetector
from utils.navigation import create_top_navbar
from components.feedback_form import create_feedback_form
from auth.session_manager import SessionManager

# Import performance metrics tracker
try:
    from monitoring.performance_metrics import get_metrics_tracker
    METRICS_ENABLED = True
except ImportError:
    METRICS_ENABLED = False
    def get_metrics_tracker():
        return None

# Page configuration
st.set_page_config(
    page_title="Campus Pulse - UF",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide sidebar by default
)

# Initialize session manager
if 'session_manager' not in st.session_state:
    st.session_state.session_manager = SessionManager()

# Restore session from cookie if available
st.session_state.session_manager.restore_session_state()

# Set current page
st.session_state.current_page = 'Home'

# Modern Home Page CSS - 2025 Aesthetic
st.markdown("""
<style>
    /* Main header with modern gradient text */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        font-family: 'Outfit', 'Inter', sans-serif !important;
        text-align: center;
        padding: 1.5rem 0;
        background: linear-gradient(135deg, #0021A5 0%, #FA4616 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.03em;
        line-height: 1.2;
    }

    /* Sub-header with modern typography */
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.25rem;
        font-weight: 500;
        margin-bottom: 3rem;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: -0.01em;
    }

    /* Modern metric cards with glassmorphism */
    .metric-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(0,33,165,0.1);
        backdrop-filter: blur(10px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .metric-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 48px rgba(0,0,0,0.15);
        border-color: rgba(0,33,165,0.2);
    }

    /* Feature cards for the welcome section */
    .feature-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,33,165,0.1);
        transition: all 0.3s ease;
        height: 100%;
    }

    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.12);
        border-color: rgba(0,33,165,0.2);
    }

    /* Section headers */
    .section-header {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
        margin: 2rem 0 1.5rem 0;
        letter-spacing: -0.02em;
    }

    /* Dividers */
    hr {
        margin: 3rem 0;
        border: none;
        border-top: 1px solid rgba(0,33,165,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize performance metrics tracker and start page timing
import time as time_module
page_start_time = time_module.time()

if METRICS_ENABLED:
    metrics_tracker = get_metrics_tracker()
else:
    metrics_tracker = None

# Initialize session state
def init_session_state():
    """Initialize session state variables"""
    if 'simulator' not in st.session_state or st.session_state.simulator is None:
        st.session_state.simulator = CrowdDataSimulator()

    if 'event_generator' not in st.session_state:
        st.session_state.event_generator = UFEventGenerator()
        st.session_state.events = st.session_state.event_generator.generate_semester_events(50)

    if 'forecaster' not in st.session_state:
        st.session_state.forecaster = CrowdForecaster()

    if 'event_classifier' not in st.session_state:
        st.session_state.event_classifier = ImprovedEventCategorizer()

    if 'anomaly_detector' not in st.session_state:
        st.session_state.anomaly_detector = AnomalyDetector()

    if 'saved_locations' not in st.session_state:
        st.session_state.saved_locations = []

    if 'user_created_events' not in st.session_state:
        st.session_state.user_created_events = []

    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = datetime.now()

init_session_state()

# Top navigation
create_top_navbar()

# Track page load time
if METRICS_ENABLED and metrics_tracker:
    load_time_ms = (time_module.time() - page_start_time) * 1000
    user_email = st.session_state.user.get('email') if 'user' in st.session_state and st.session_state.user else None
    metrics_tracker.record_page_load("Home", load_time_ms, user_email)
    # Also record as response time
    metrics_tracker.record_response_time("home_page", load_time_ms, user_email, "success")

# Quick stats row with performance tracking
st.markdown("### Live Campus Stats")
stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

# Track data retrieval performance
data_start = time_module.time()
all_crowds = st.session_state.simulator.get_all_current_crowds()
avg_occupancy = sum(c['percentage'] for c in all_crowds) / len(all_crowds)
data_time_ms = (time_module.time() - data_start) * 1000

# Record API latency for data retrieval
if METRICS_ENABLED and metrics_tracker:
    metrics_tracker.record_api_latency("get_all_current_crowds", data_time_ms)

# Count events timing
events_start = time_module.time()
upcoming_events = len([e for e in st.session_state.events if e['start_time'] > datetime.now()])
events_time_ms = (time_module.time() - events_start) * 1000

if METRICS_ENABLED and metrics_tracker:
    metrics_tracker.record_api_latency("count_upcoming_events", events_time_ms)

with stat_col1:
    st.metric("Avg Campus Occupancy", f"{avg_occupancy:.0f}%")

with stat_col2:
    st.metric("Active Locations", len(UF_LOCATIONS))

with stat_col3:
    st.metric("Upcoming Events", upcoming_events)

with stat_col4:
    saved_count = len(st.session_state.saved_locations)
    st.metric("Saved Locations", saved_count)

st.markdown("---")

# Welcome section
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Live Crowd Heatmap")
    st.write("View real-time crowd density across campus locations. Get instant occupancy levels and forecasts.")
    if st.button("Go to Heatmap →", key="btn_heatmap"):
        st.switch_page("pages/1_🗺️_Crowd_Heatmap.py")

with col2:
    st.markdown("### Campus Events")
    st.write("Discover 100+ real UF events with AI-powered categorization and crowd forecasts.")
    if st.button("Browse Events →", key="btn_events"):
        st.switch_page("pages/2_🎉_Events.py")

with col3:
    st.markdown("### Saved Locations")
    st.write("Save your favorite campus spots and get smart recommendations based on forecasts.")
    if st.button("My Locations →", key="btn_saved"):
        st.switch_page("pages/3_⭐_Saved_Locations.py")

st.markdown("---")

# Feature highlights
st.markdown("### Key Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### AI-Powered Features")
    st.markdown("""
    - **LSTM Forecasting**: Predict crowd levels up to 1 hour ahead
    - **Improved NLP Event Classification**: 90%+ accuracy with transformer fine-tuning
    - **Anomaly Detection**: Alert for unusual crowd patterns using autoencoders
    - **Smart Recommendations**: Personalized suggestions based on saved locations
    - **100 Real UF Events**: Authentic campus event data
    """)

with col2:
    st.markdown("#### Real-Time Intelligence")
    st.markdown("""
    - **Interactive Heatmap**: Folium map with color-coded crowd density
    - **Stable Map**: Fixed refresh issue - smooth interaction guaranteed
    - **Historical Trends**: View past crowd patterns with beautiful charts
    - **Event Integration**: Events overlaid on crowd data
    - **Top Navigation**: Easy access to all features
    """)

st.markdown("---")

# Current campus overview
st.markdown("### Current Campus Overview")

# Get top 5 busiest locations
sorted_crowds = sorted(all_crowds, key=lambda x: x['percentage'], reverse=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("#### Busiest Locations Right Now")

    for i, crowd in enumerate(sorted_crowds[:5]):
        col_a, col_b, col_c = st.columns([3, 1, 1])

        with col_a:
            st.write(f"**{i+1}. {crowd['location_name']}**")

        with col_b:
            # Color based on level
            if crowd['percentage'] > 85:
                st.markdown(f'<span style="color: red; font-weight: 600;">{crowd["percentage"]}%</span>', unsafe_allow_html=True)
            elif crowd['percentage'] > 60:
                st.markdown(f'<span style="color: orange; font-weight: 600;">{crowd["percentage"]}%</span>', unsafe_allow_html=True)
            elif crowd['percentage'] > 30:
                st.markdown(f'<span style="color: #FFD700; font-weight: 600;">{crowd["percentage"]}%</span>', unsafe_allow_html=True)
            else:
                st.markdown(f'<span style="color: green; font-weight: 600;">{crowd["percentage"]}%</span>', unsafe_allow_html=True)

        with col_c:
            st.write(f"{crowd['headcount']}/{crowd['capacity']}")

with col2:
    st.markdown("#### Quietest Spots")
    quietest = sorted(all_crowds, key=lambda x: x['percentage'])[:3]

    for crowd in quietest:
        st.success(f"**{crowd['location_name']}** - {crowd['percentage']}% full")

st.markdown("---")

# Feedback form
create_feedback_form()

# Footer
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    <p>Campus Pulse | University of Florida | Powered by AI</p>
    <p style="font-size: 0.8rem;">Last updated: {} | Use top navigation or Refresh button</p>
</div>
""".format(st.session_state.last_refresh.strftime('%I:%M:%S %p')), unsafe_allow_html=True)
