"""
Saved Locations Page - Track your favorite campus spots
"""
import streamlit as st
import sys
import os
import pandas as pd
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.simulator import CrowdDataSimulator
from data.locations import UF_LOCATIONS, get_location_by_id
from data.uf_events_real import UFEventGenerator
from models.lstm_forecaster import CrowdForecaster
from models.anomaly_detector import AnomalyDetector
from utils.map_utils import get_crowd_color, get_crowd_label
from utils.chart_utils import create_forecast_chart, create_crowd_gauge
from utils.navigation import create_top_navbar

st.set_page_config(page_title="Saved Locations - Campus Pulse", page_icon="⭐", layout="wide")

# Set current page
st.session_state.current_page = 'Saved'

# Top navigation
create_top_navbar()

# Modern saved locations page styling
st.markdown("""
<style>
    /* Saved location cards */
    .saved-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 24px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,33,165,0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .saved-card:hover {
        box-shadow: 0 8px 32px rgba(0,0,0,0.12);
        transform: translateY(-4px);
        border-color: rgba(0,33,165,0.2);
    }

    /* Add location section */
    .add-location-section {
        background: rgba(0,33,165,0.05);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        border: 2px dashed rgba(0,33,165,0.2);
    }

    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 3rem;
        background: rgba(255,255,255,0.02);
        border-radius: 16px;
        border: 1px solid rgba(0,33,165,0.08);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'simulator' not in st.session_state:
    st.session_state.simulator = CrowdDataSimulator()
if 'forecaster' not in st.session_state:
    st.session_state.forecaster = CrowdForecaster()
if 'anomaly_detector' not in st.session_state:
    st.session_state.anomaly_detector = AnomalyDetector()
if 'event_generator' not in st.session_state:
    st.session_state.event_generator = UFEventGenerator()
    st.session_state.events = st.session_state.event_generator.generate_semester_events(50)
if 'saved_locations' not in st.session_state:
    st.session_state.saved_locations = []

# Page header
st.title("⭐ Saved Locations")
st.markdown("Track crowd levels and events at your favorite campus spots")

# Add location section
st.markdown("### ➕ Add a Location")

add_col1, add_col2 = st.columns([3, 1])

with add_col1:
    # Show locations not already saved
    available_locations = [loc for loc in UF_LOCATIONS if loc['id'] not in st.session_state.saved_locations]

    if available_locations:
        location_to_add = st.selectbox(
            "Select a location to save:",
            [loc['name'] for loc in available_locations],
            key="location_selector"
        )
    else:
        st.info("You've saved all available locations!")
        location_to_add = None

with add_col2:
    if location_to_add:
        if st.button("⭐ Save Location", type="primary", use_container_width=True):
            location = next((loc for loc in UF_LOCATIONS if loc['name'] == location_to_add), None)
            if location and location['id'] not in st.session_state.saved_locations:
                st.session_state.saved_locations.append(location['id'])
                st.success(f"Added {location['name']}!")
                st.rerun()

st.markdown("---")

# Display saved locations
if len(st.session_state.saved_locations) == 0:
    st.info("👆 You haven't saved any locations yet. Add one above to get started!")
else:
    st.markdown(f"### 📍 Your Saved Locations ({len(st.session_state.saved_locations)})")

    # Quick summary
    summary_col1, summary_col2, summary_col3 = st.columns(3)

    saved_locations_data = []
    for loc_id in st.session_state.saved_locations:
        location = get_location_by_id(loc_id)
        if location:
            crowd = st.session_state.simulator.get_current_crowd(location)
            saved_locations_data.append({
                'location': location,
                'crowd': crowd
            })

    with summary_col1:
        avg_occupancy = sum(d['crowd']['percentage'] for d in saved_locations_data) / len(saved_locations_data)
        st.metric("Average Occupancy", f"{avg_occupancy:.0f}%")

    with summary_col2:
        available_spots = sum(1 for d in saved_locations_data if d['crowd']['percentage'] < 60)
        st.metric("Available Spots", f"{available_spots}/{len(saved_locations_data)}")

    with summary_col3:
        busy_spots = sum(1 for d in saved_locations_data if d['crowd']['percentage'] > 85)
        if busy_spots > 0:
            st.metric("Very Busy", busy_spots, delta="Avoid", delta_color="inverse")
        else:
            st.metric("Very Busy", 0, delta="None", delta_color="normal")

    st.markdown("---")

    # Display each saved location
    for loc_data in saved_locations_data:
        location = loc_data['location']
        crowd = loc_data['crowd']

        with st.container():
            # Header with location name and remove button
            header_col1, header_col2 = st.columns([4, 1])

            with header_col1:
                crowd_label = get_crowd_label(crowd['crowd_level'])
                crowd_color = get_crowd_color(crowd['crowd_level'])

                st.markdown(f"""
                <h3 style="margin: 0;">
                    {location['name']}
                    <span style="color: {crowd_color}; font-size: 0.8em; margin-left: 1rem;">● {crowd_label}</span>
                </h3>
                <p style="margin: 0; color: #666;">{location['description']} | {location['category']}</p>
                """, unsafe_allow_html=True)

            with header_col2:
                if st.button("🗑️ Remove", key=f"remove_{location['id']}", use_container_width=True):
                    st.session_state.saved_locations.remove(location['id'])
                    st.rerun()

            # Metrics and charts
            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

            with metric_col1:
                st.metric("Current Occupancy", f"{crowd['percentage']}%", f"{crowd['headcount']} people")

            with metric_col2:
                # Get forecast
                hist_data = st.session_state.simulator.generate_historical_data(location, days=1, interval_minutes=10)
                recent_levels = hist_data['crowd_level'].values[-12:]
                predictions = st.session_state.forecaster.predict(recent_levels)
                label, emoji = st.session_state.forecaster.get_forecast_label(predictions)

                st.metric("1h Forecast", f"{emoji} {label}")

            with metric_col3:
                # Check for anomaly
                anomaly_result = st.session_state.anomaly_detector.detect(recent_levels)

                if anomaly_result['is_anomaly']:
                    severity_emoji = {'medium': '⚠️', 'high': '🚨', 'critical': '🔴'}
                    emoji = severity_emoji.get(anomaly_result['severity'], '⚠️')
                    st.metric("Status", f"{emoji} Anomaly", delta=anomaly_result['severity'].title(), delta_color="inverse")
                else:
                    st.metric("Status", "✅ Normal", delta="No issues", delta_color="normal")

            with metric_col4:
                # Count events at this location
                location_events = [e for e in st.session_state.events
                                 if e['location_id'] == location['id'] and e['start_time'] > datetime.now()]
                st.metric("Upcoming Events", len(location_events))

            # Expandable sections
            detail_col1, detail_col2 = st.columns(2)

            with detail_col1:
                with st.expander("📊 View Forecast Chart"):
                    # Generate historical data
                    hist_data = st.session_state.simulator.generate_historical_data(location, days=1, interval_minutes=10)

                    # Create forecast timestamps
                    last_timestamp = hist_data['timestamp'].iloc[-1]
                    forecast_timestamps = [last_timestamp + timedelta(minutes=10 * (i + 1)) for i in range(6)]

                    forecast_df = pd.DataFrame({
                        'timestamp': forecast_timestamps,
                        'crowd_level': predictions
                    })

                    # Plot
                    fig = create_forecast_chart(hist_data.tail(36), forecast_df, location['name'])
                    st.plotly_chart(fig, use_container_width=True)

            with detail_col2:
                if location_events:
                    with st.expander(f"🎉 View {len(location_events)} Upcoming Event(s)"):
                        for event in location_events[:5]:
                            st.markdown(f"""
                            **{event['title']}**
                            📅 {event['start_time'].strftime('%B %d, %I:%M %p')}
                            🏷️ {event['category']}
                            """)
                            st.markdown("---")

            # Alert settings
            with st.expander("🔔 Alert Settings"):
                alert_col1, alert_col2 = st.columns(2)

                with alert_col1:
                    st.checkbox(
                        f"Notify when occupancy < 50%",
                        key=f"alert_low_{location['id']}",
                        help="Get notified when this location is relatively empty"
                    )

                    st.checkbox(
                        f"Notify when occupancy > 85%",
                        key=f"alert_high_{location['id']}",
                        help="Get notified when this location is very busy"
                    )

                with alert_col2:
                    st.checkbox(
                        f"Notify of anomalies",
                        key=f"alert_anomaly_{location['id']}",
                        help="Get notified of unusual crowd patterns"
                    )

                    st.checkbox(
                        f"Notify of new events",
                        key=f"alert_events_{location['id']}",
                        help="Get notified when new events are scheduled"
                    )

            st.markdown("---")

    # Recommendations
    st.markdown("### 💡 Smart Recommendations")

    # Find best locations based on criteria
    rec_col1, rec_col2 = st.columns(2)

    with rec_col1:
        st.markdown("#### 🟢 Available Now")
        available = [d for d in saved_locations_data if d['crowd']['percentage'] < 50]

        if available:
            for d in sorted(available, key=lambda x: x['crowd']['percentage'])[:3]:
                st.success(f"**{d['location']['name']}** - Only {d['crowd']['percentage']}% full")
        else:
            st.info("No saved locations are lightly occupied right now")

    with rec_col2:
        st.markdown("#### 🔮 Good to Visit in 1 Hour")

        future_available = []
        for loc_data in saved_locations_data:
            location = loc_data['location']
            hist_data = st.session_state.simulator.generate_historical_data(location, days=1)
            recent_levels = hist_data['crowd_level'].values[-12:]
            predictions = st.session_state.forecaster.predict(recent_levels)

            avg_prediction = predictions.mean()
            if avg_prediction < 0.6:
                future_available.append({
                    'location': location,
                    'prediction': avg_prediction
                })

        if future_available:
            for d in sorted(future_available, key=lambda x: x['prediction'])[:3]:
                label, emoji = st.session_state.forecaster.get_forecast_label([d['prediction']])
                st.success(f"**{d['location']['name']}** - {emoji} {label}")
        else:
            st.info("All saved locations expected to be busy")

# Quick actions
st.markdown("---")
action_col1, action_col2, action_col3 = st.columns(3)

with action_col1:
    if st.button("🔄 Refresh All Data", use_container_width=True, type="primary"):
        st.session_state.simulator = CrowdDataSimulator()
        st.rerun()

with action_col2:
    if len(st.session_state.saved_locations) > 0:
        if st.button("🗑️ Clear All Saved Locations", use_container_width=True):
            st.session_state.saved_locations = []
            st.rerun()

with action_col3:
    if st.button("➕ Add More Locations", use_container_width=True):
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem 0;">
    <p>⭐ Saved Locations | Last updated: {}</p>
</div>
""".format(datetime.now().strftime('%I:%M:%S %p')), unsafe_allow_html=True)
