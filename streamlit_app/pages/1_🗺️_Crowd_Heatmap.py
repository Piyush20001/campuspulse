"""
Crowd Heatmap Page - Interactive map with real-time crowd density
"""
import streamlit as st
import sys
import os
import pandas as pd
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from streamlit_folium import st_folium
from data.simulator import CrowdDataSimulator
from data.locations import UF_LOCATIONS, get_locations_by_category
from data.uf_events_real import UFEventGenerator
from models.lstm_forecaster import CrowdForecaster
from models.anomaly_detector import AnomalyDetector
from utils.map_utils import create_base_map, add_heatmap_layer, add_location_markers, get_crowd_color, get_crowd_label
from utils.chart_utils import create_sparkline, create_forecast_chart, create_comparison_bar_chart
from utils.config import UF_CENTER
from utils.navigation import create_top_navbar

st.set_page_config(page_title="Crowd Heatmap - Campus Pulse", page_icon="🗺️", layout="wide")

# Set current page
st.session_state.current_page = 'Crowd Map'

# Top navigation
create_top_navbar()

# Initialize session state
if 'simulator' not in st.session_state or st.session_state.simulator is None:
    st.session_state.simulator = CrowdDataSimulator()
if 'forecaster' not in st.session_state:
    st.session_state.forecaster = CrowdForecaster()
if 'anomaly_detector' not in st.session_state:
    st.session_state.anomaly_detector = AnomalyDetector()
if 'event_generator' not in st.session_state:
    st.session_state.event_generator = UFEventGenerator()
    st.session_state.events = st.session_state.event_generator.generate_semester_events(50)
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()

# Page header
st.title("🗺️ Live Crowd Heatmap")
st.markdown("Real-time crowd density across UF campus with AI-powered forecasts")

# Filters
st.markdown("### 🔍 Filters")

categories = ["ALL", "GYMS", "LIBRARIES", "DINING", "ACADEMIC", "HOUSING", "STUDY SPOTS", "OUTDOORS"]

selected_filter = st.session_state.get('selected_filter', 'ALL')

# Create filter buttons
filter_buttons = st.columns(8)
for i, category in enumerate(categories):
    with filter_buttons[i]:
        if st.button(
            category,
            key=f"filter_{category}",
            type="primary" if selected_filter == category else "secondary",
            use_container_width=True
        ):
            st.session_state.selected_filter = category
            selected_filter = category
            # Clear cache when filter changes
            if 'cached_crowd_data' in st.session_state:
                del st.session_state['cached_crowd_data']

st.markdown("---")

# Get filtered locations
if selected_filter == "ALL":
    filtered_locations = UF_LOCATIONS
else:
    filtered_locations = get_locations_by_category(selected_filter)

# Cache key that includes the filter
cache_key = f'crowd_data_{selected_filter}'

# Get or generate crowd data (only regenerate on explicit refresh or new filter)
if cache_key not in st.session_state or 'force_refresh' in st.session_state:
    crowd_data = []
    for location in filtered_locations:
        crowd = st.session_state.simulator.get_current_crowd(location)
        crowd['lat'] = location['lat']
        crowd['lon'] = location['lon']
        crowd_data.append(crowd)
    st.session_state[cache_key] = crowd_data
    st.session_state['cached_crowd_data'] = crowd_data
    if 'force_refresh' in st.session_state:
        del st.session_state['force_refresh']
else:
    crowd_data = st.session_state[cache_key]

# Generate forecasts (cached similarly)
forecast_cache_key = f'forecasts_{selected_filter}'
if forecast_cache_key not in st.session_state or 'force_refresh' in st.session_state:
    forecasts = []
    for location in filtered_locations:
        # Generate historical data
        hist_data = st.session_state.simulator.generate_historical_data(location, days=1, interval_minutes=10)

        # Get forecast
        recent_levels = hist_data['crowd_level'].values[-12:]  # Last 2 hours
        predictions = st.session_state.forecaster.predict(recent_levels)
        label, emoji = st.session_state.forecaster.get_forecast_label(predictions)

        forecasts.append({
            'location_id': location['id'],
            'predictions': predictions,
            'label': label,
            'emoji': emoji
        })
    st.session_state[forecast_cache_key] = forecasts
else:
    forecasts = st.session_state[forecast_cache_key]

# Check for anomalies (cached)
anomaly_cache_key = f'anomalies_{selected_filter}'
if anomaly_cache_key not in st.session_state or 'force_refresh' in st.session_state:
    anomalies = []
    for location in filtered_locations:
        hist_data = st.session_state.simulator.generate_historical_data(location, days=1, interval_minutes=10)
        recent_levels = hist_data['crowd_level'].values[-12:]

        anomaly_result = st.session_state.anomaly_detector.detect(recent_levels)

        if anomaly_result['is_anomaly']:
            anomalies.append({
                'location_name': location['name'],
                'severity': anomaly_result['severity'],
                'explanation': st.session_state.anomaly_detector.get_anomaly_explanation(recent_levels, location['name'])
            })
    st.session_state[anomaly_cache_key] = anomalies
else:
    anomalies = st.session_state[anomaly_cache_key]

# Show anomaly alerts if any
if anomalies:
    st.warning(f"⚠️ {len(anomalies)} Anomal{'y' if len(anomalies) == 1 else 'ies'} Detected")
    with st.expander("View Anomalies"):
        for anomaly in anomalies:
            severity_colors = {
                'medium': 'orange',
                'high': 'red',
                'critical': 'darkred'
            }
            st.markdown(f"**{anomaly['location_name']}** - {anomaly['explanation']}")

st.markdown("---")

# Map and table layout
map_col, table_col = st.columns([2, 1])

with map_col:
    st.markdown("### 🌍 Interactive Map")

    # Group events by location (cached)
    events_cache_key = f'events_by_location_{selected_filter}'
    if events_cache_key not in st.session_state:
        events_by_location = {}
        for event in st.session_state.events:
            if event['start_time'] > datetime.now():
                if event['location_id'] not in events_by_location:
                    events_by_location[event['location_id']] = []
                events_by_location[event['location_id']].append(event)
        st.session_state[events_cache_key] = events_by_location
    else:
        events_by_location = st.session_state[events_cache_key]

    # Create map (only when data changes)
    map_cache_key = f'map_object_{selected_filter}'
    if map_cache_key not in st.session_state or 'force_refresh' in st.session_state:
        m = create_base_map(UF_CENTER, zoom_start=15)
        m = add_heatmap_layer(m, crowd_data)
        m = add_location_markers(m, crowd_data, forecasts, events_by_location)
        st.session_state[map_cache_key] = m
    else:
        m = st.session_state[map_cache_key]

    # Display map with minimal re-rendering
    # Don't capture returned data to prevent updates
    st_folium(
        m,
        width=None,
        height=500,
        key=f"folium_map_{selected_filter}",
        returned_objects=[]  # Critical: prevents constant re-rendering!
    )

with table_col:
    st.markdown("### 📊 Current Levels")

    # Create DataFrame for display
    display_data = []
    for i, crowd in enumerate(crowd_data):
        forecast = forecasts[i]
        display_data.append({
            'Location': crowd['location_name'],
            'Current': f"{crowd['percentage']}%",
            'Headcount': f"{crowd['headcount']}/{crowd['capacity']}",
            '1h Forecast': f"{forecast['emoji']} {forecast['label']}"
        })

    df = pd.DataFrame(display_data)

    # Style the dataframe
    st.dataframe(
        df,
        use_container_width=True,
        height=400,
        hide_index=True
    )

st.markdown("---")

# Detailed view section
st.markdown("### 📈 Detailed Location View")

selected_location_name = st.selectbox(
    "Select a location for detailed analysis:",
    [loc['name'] for loc in filtered_locations],
    key="location_detail_select"
)

# Find selected location
selected_location = next((loc for loc in filtered_locations if loc['name'] == selected_location_name), None)

if selected_location:
    detail_col1, detail_col2, detail_col3 = st.columns(3)

    # Get current crowd for this location
    current_crowd = next((c for c in crowd_data if c['location_id'] == selected_location['id']), None)

    with detail_col1:
        st.metric(
            "Current Occupancy",
            f"{current_crowd['percentage']}%",
            f"{current_crowd['headcount']} people"
        )

    with detail_col2:
        # Get forecast for this location
        forecast = next((f for f in forecasts if f['location_id'] == selected_location['id']), None)
        st.metric(
            "1-Hour Forecast",
            f"{forecast['emoji']} {forecast['label']}",
            delta=None
        )

    with detail_col3:
        status_color = get_crowd_color(current_crowd['crowd_level'])
        status_label = get_crowd_label(current_crowd['crowd_level'])
        st.markdown(f"**Status**: <span style='color: {status_color}; font-size: 1.2em;'>{status_label}</span>", unsafe_allow_html=True)
        st.write(f"**Category**: {selected_location['category']}")

    # Historical and forecast chart
    st.markdown("#### 📊 Trend & Forecast")

    # Generate historical data
    hist_data = st.session_state.simulator.generate_historical_data(selected_location, days=1, interval_minutes=10)

    # Create forecast timestamps
    last_timestamp = hist_data['timestamp'].iloc[-1]
    forecast_timestamps = [last_timestamp + timedelta(minutes=10 * (i + 1)) for i in range(6)]

    forecast_df = pd.DataFrame({
        'timestamp': forecast_timestamps,
        'crowd_level': forecast['predictions']
    })

    # Plot
    fig = create_forecast_chart(hist_data.tail(36), forecast_df, selected_location['name'])  # Show last 6 hours
    st.plotly_chart(fig, use_container_width=True)

    # Events at this location
    location_events = events_by_location.get(selected_location['id'], [])
    if location_events:
        st.markdown("#### 🎉 Upcoming Events at This Location")
        for event in location_events[:3]:
            with st.expander(f"{event['title']} - {event['start_time'].strftime('%b %d, %I:%M %p')}"):
                st.write(f"**Category**: {event['category']}")
                st.write(f"**Description**: {event['description']}")
                st.write(f"**Time**: {event['start_time'].strftime('%B %d, %Y at %I:%M %p')} - {event['end_time'].strftime('%I:%M %p')}")
                st.write(f"**Organizer**: {event['organizer']}")

# Footer with manual refresh only
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    if st.button("🔄 Refresh Data", use_container_width=True, type="primary", key="manual_refresh_btn"):
        st.session_state.force_refresh = True
        st.session_state.simulator = CrowdDataSimulator()
        st.session_state.last_refresh = datetime.now()
        # Clear all caches
        keys_to_delete = [k for k in list(st.session_state.keys()) if any(x in k for x in ['crowd_data_', 'forecasts_', 'anomalies_', 'map_object_', 'events_by_location_'])]
        for key in keys_to_delete:
            del st.session_state[key]
        st.rerun()

st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem 0;">
    <p style="font-size: 0.9rem;">Last updated: {} | Click "Refresh Data" to update</p>
</div>
""".format(st.session_state.last_refresh.strftime('%I:%M:%S %p')), unsafe_allow_html=True)
