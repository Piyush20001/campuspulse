"""
Events Page - Campus events with AI-powered categorization
"""
import streamlit as st
import sys
import os
import pandas as pd
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.simulator import CrowdDataSimulator
from data.events_data import EventGenerator, TRAINING_EVENTS
from data.locations import UF_LOCATIONS, get_location_by_id
from models.event_classifier import EventCategorizer
from models.lstm_forecaster import CrowdForecaster
from utils.chart_utils import create_category_distribution

st.set_page_config(page_title="Events - Campus Pulse", page_icon="🎉", layout="wide")

# Initialize session state
if 'simulator' not in st.session_state:
    st.session_state.simulator = CrowdDataSimulator()
if 'event_generator' not in st.session_state:
    st.session_state.event_generator = EventGenerator()
    st.session_state.events = st.session_state.event_generator.generate_random_events(30)
if 'event_classifier' not in st.session_state:
    st.session_state.event_classifier = EventCategorizer()
if 'forecaster' not in st.session_state:
    st.session_state.forecaster = CrowdForecaster()
if 'user_created_events' not in st.session_state:
    st.session_state.user_created_events = []

# Page header
st.title("🎉 Campus Events")
st.markdown("Discover upcoming events with AI-powered categorization and crowd forecasts")

# Tabs
tab1, tab2, tab3 = st.tabs(["📅 Browse Events", "➕ Create Event", "🤖 AI Event Classifier"])

# Tab 1: Browse Events
with tab1:
    st.markdown("### 📅 Upcoming Events")

    # Filters
    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:
        category_filter = st.selectbox(
            "Filter by Category",
            ["All"] + st.session_state.event_classifier.categories
        )

    with filter_col2:
        time_filter = st.selectbox(
            "Time Range",
            ["All Upcoming", "Today", "This Week", "This Month"]
        )

    with filter_col3:
        location_filter = st.selectbox(
            "Filter by Location",
            ["All Locations"] + [loc['name'] for loc in UF_LOCATIONS]
        )

    # Combine generated and user-created events
    all_events = st.session_state.events + st.session_state.user_created_events

    # Apply filters
    filtered_events = []
    for event in all_events:
        # Category filter
        if category_filter != "All" and event['category'] != category_filter:
            continue

        # Location filter
        if location_filter != "All Locations":
            location = get_location_by_id(event['location_id'])
            if location and location['name'] != location_filter:
                continue

        # Time filter
        now = datetime.now()
        if time_filter == "Today" and event['start_time'].date() != now.date():
            continue
        elif time_filter == "This Week" and (event['start_time'] - now).days > 7:
            continue
        elif time_filter == "This Month" and (event['start_time'] - now).days > 30:
            continue

        # Only show future events
        if event['start_time'] > now:
            filtered_events.append(event)

    # Sort by date
    filtered_events.sort(key=lambda x: x['start_time'])

    # Statistics
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

    with stat_col1:
        st.metric("Total Events", len(filtered_events))

    with stat_col2:
        free_events = sum(1 for e in filtered_events if e.get('is_free', True))
        st.metric("Free Events", free_events)

    with stat_col3:
        today_events = sum(1 for e in filtered_events if e['start_time'].date() == datetime.now().date())
        st.metric("Today", today_events)

    with stat_col4:
        this_week = sum(1 for e in filtered_events if (e['start_time'] - datetime.now()).days <= 7)
        st.metric("This Week", this_week)

    st.markdown("---")

    # Event cards
    if len(filtered_events) == 0:
        st.info("No events found matching your filters.")
    else:
        # Show category distribution
        if len(filtered_events) > 3:
            with st.expander("📊 Event Category Distribution"):
                events_df = pd.DataFrame(filtered_events)
                fig = create_category_distribution(events_df)
                st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"### Showing {len(filtered_events)} Event(s)")

        for event in filtered_events[:20]:  # Show max 20
            with st.container():
                col1, col2 = st.columns([3, 1])

                with col1:
                    # Category badge color
                    category_colors = {
                        'Academic': '#0021A5',
                        'Social': '#FA4616',
                        'Sports': '#28a745',
                        'Cultural': '#9C27B0'
                    }
                    color = category_colors.get(event['category'], '#6c757d')

                    st.markdown(f"""
                    <div style="background: white; padding: 1rem; border-radius: 10px; border-left: 5px solid {color}; margin-bottom: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <h3 style="margin: 0; color: #333;">{event['title']}</h3>
                        <p style="margin: 0.5rem 0; color: #666;">{event['description']}</p>
                        <div style="margin-top: 0.5rem;">
                            <span style="background: {color}; color: white; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.85rem; margin-right: 0.5rem;">{event['category']}</span>
                            {' '.join([f'<span style="background: #f0f0f0; color: #333; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.85rem; margin-right: 0.5rem;">{tag}</span>' for tag in event.get('tags', [])[:3]])}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    location = get_location_by_id(event['location_id'])
                    location_name = location['name'] if location else "Unknown"

                    st.write(f"📍 **{location_name}**")
                    st.write(f"🕐 **{event['start_time'].strftime('%b %d, %I:%M %p')}**")
                    st.write(f"👥 **{event.get('attendees_expected', 'N/A')}** expected")

                    if event.get('is_free', False):
                        st.success("✨ Free Event")

                    # Get crowd forecast for event time
                    if location:
                        with st.expander("Crowd Forecast"):
                            hist_data = st.session_state.simulator.generate_historical_data(location, days=1)
                            recent_levels = hist_data['crowd_level'].values[-12:]
                            predictions = st.session_state.forecaster.predict(recent_levels)
                            label, emoji = st.session_state.forecaster.get_forecast_label(predictions)

                            st.write(f"{emoji} Expected crowd: **{label}**")

                st.markdown("---")

# Tab 2: Create Event
with tab2:
    st.markdown("### ➕ Create New Event")
    st.markdown("Use AI to automatically categorize and tag your event!")

    with st.form("create_event_form"):
        event_title = st.text_input("Event Title*", placeholder="e.g., Machine Learning Workshop")

        event_description = st.text_area(
            "Event Description*",
            placeholder="Describe your event...",
            height=100
        )

        col1, col2 = st.columns(2)

        with col1:
            event_location = st.selectbox(
                "Location*",
                [loc['name'] for loc in UF_LOCATIONS]
            )

            event_date = st.date_input(
                "Event Date*",
                min_value=datetime.now().date()
            )

        with col2:
            event_time = st.time_input("Start Time*")

            event_duration = st.selectbox(
                "Duration",
                ["1 hour", "1.5 hours", "2 hours", "2.5 hours", "3 hours", "4 hours"]
            )

        col3, col4 = st.columns(2)

        with col3:
            organizer = st.text_input("Organizer", placeholder="e.g., Computer Science Club")

        with col4:
            expected_attendees = st.number_input("Expected Attendees", min_value=1, value=50)

        is_free = st.checkbox("This is a free event", value=True)
        registration_required = st.checkbox("Registration required")

        submit_button = st.form_submit_button("🤖 Create Event with AI Categorization", type="primary", use_container_width=True)

        if submit_button:
            if event_title and event_description and event_location:
                # Use AI to categorize
                ai_result = st.session_state.event_classifier.predict(event_title, event_description)

                # Create event
                location = next((loc for loc in UF_LOCATIONS if loc['name'] == event_location), UF_LOCATIONS[0])

                # Parse duration
                duration_hours = float(event_duration.split()[0])

                # Create datetime
                start_datetime = datetime.combine(event_date, event_time)
                end_datetime = start_datetime + timedelta(hours=duration_hours)

                new_event = {
                    'id': len(st.session_state.events) + len(st.session_state.user_created_events) + 1,
                    'title': event_title,
                    'description': event_description,
                    'category': ai_result['category'],
                    'tags': ai_result['suggested_tags'],
                    'location_name': location['name'],
                    'location_id': location['id'],
                    'start_time': start_datetime,
                    'end_time': end_datetime,
                    'organizer': organizer if organizer else "User",
                    'attendees_expected': expected_attendees,
                    'is_free': is_free,
                    'registration_required': registration_required
                }

                st.session_state.user_created_events.append(new_event)

                st.success("✅ Event created successfully!")

                # Show AI results
                st.markdown("### 🤖 AI Analysis Results")

                ai_col1, ai_col2 = st.columns(2)

                with ai_col1:
                    st.metric("Category", ai_result['category'])
                    st.metric("Confidence", f"{ai_result['confidence']*100:.1f}%")

                with ai_col2:
                    st.write("**Suggested Tags:**")
                    for tag in ai_result['suggested_tags']:
                        st.markdown(f"- {tag}")

                # Show all probabilities
                with st.expander("View All Category Probabilities"):
                    for cat, prob in ai_result['all_probabilities'].items():
                        st.progress(prob, text=f"{cat}: {prob*100:.1f}%")

            else:
                st.error("Please fill in all required fields (marked with *)")

# Tab 3: AI Classifier Info
with tab3:
    st.markdown("### 🤖 AI Event Classifier")
    st.markdown("Learn about how the AI categorizes events")

    st.markdown("""
    #### How It Works

    The Campus Pulse event classifier uses a **Transformer-based NLP model** (DistilBERT) to automatically
    categorize events into one of four categories:

    - **Academic**: Workshops, lectures, research presentations, career fairs
    - **Social**: Parties, entertainment, social gatherings, movie nights
    - **Sports**: Games, fitness activities, competitions, recreation
    - **Cultural**: Festivals, performances, international events, heritage celebrations

    #### Features

    1. **Text Analysis**: Analyzes both event title and description
    2. **Confidence Scores**: Provides probability distribution across all categories
    3. **Tag Generation**: Automatically suggests relevant tags based on content
    4. **Fast Processing**: Real-time categorization in under a second
    """)

    st.markdown("---")

    st.markdown("#### 🧪 Try the Classifier")

    test_title = st.text_input("Enter an event title:", placeholder="e.g., Basketball Game vs Georgia")
    test_description = st.text_area("Enter event description:", placeholder="Describe the event...")

    if st.button("🔮 Classify This Event", type="primary"):
        if test_title or test_description:
            result = st.session_state.event_classifier.predict(
                test_title or "Untitled Event",
                test_description or ""
            )

            st.markdown("### Results")

            result_col1, result_col2 = st.columns(2)

            with result_col1:
                category_colors = {
                    'Academic': '#0021A5',
                    'Social': '#FA4616',
                    'Sports': '#28a745',
                    'Cultural': '#9C27B0'
                }
                color = category_colors.get(result['category'], '#6c757d')

                st.markdown(f"""
                <div style="text-align: center; padding: 2rem; background: {color}; color: white; border-radius: 10px;">
                    <h2 style="margin: 0;">{result['category']}</h2>
                    <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem;">Confidence: {result['confidence']*100:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)

            with result_col2:
                st.markdown("**Suggested Tags:**")
                for tag in result['suggested_tags']:
                    st.markdown(f"- 🏷️ {tag}")

            st.markdown("---")
            st.markdown("**All Category Probabilities:**")

            for category, prob in sorted(result['all_probabilities'].items(), key=lambda x: x[1], reverse=True):
                st.progress(prob, text=f"{category}: {prob*100:.1f}%")

        else:
            st.warning("Please enter at least a title or description")

    st.markdown("---")

    # Training section
    with st.expander("🎓 Model Training Info"):
        st.markdown("""
        The classifier is based on a pretrained transformer model (DistilBERT) and can be fine-tuned
        on campus-specific event data for improved accuracy.

        **Training Data**: The model uses example events from various UF categories
        **Architecture**: Transformer encoder + classification head
        **Fallback**: Rule-based classifier when transformer is unavailable
        """)

        if st.button("🔄 Train Classifier on Sample Data"):
            with st.spinner("Training classifier... This may take a minute."):
                try:
                    st.session_state.event_classifier.train(TRAINING_EVENTS, epochs=5)
                    st.success("✅ Classifier trained successfully!")
                except Exception as e:
                    st.info(f"Using rule-based classifier (Transformer not available)")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem 0;">
    <p>🎉 Campus Pulse Events | Powered by AI</p>
</div>
""", unsafe_allow_html=True)
