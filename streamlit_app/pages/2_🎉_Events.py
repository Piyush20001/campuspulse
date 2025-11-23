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
from data.uf_events_real import UFEventGenerator, TRAINING_EVENTS
from data.locations import UF_LOCATIONS, get_location_by_id
from models.event_classifier_improved import ImprovedEventCategorizer
from models.lstm_forecaster import CrowdForecaster
from utils.chart_utils import create_category_distribution
from utils.navigation import create_top_navbar
from database.feedback_db import get_user_role
from auth.session_manager import SessionManager

st.set_page_config(page_title="Events - Campus Pulse", page_icon="🎉", layout="wide")

# Initialize session manager
if 'session_manager' not in st.session_state:
    st.session_state.session_manager = SessionManager()

# Restore session from cookie if available
st.session_state.session_manager.restore_session_state()

# Set current page
st.session_state.current_page = 'Events'

# Top navigation
create_top_navbar()

# Modern events page styling
st.markdown("""
<style>
    /* Event cards */
    .event-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 24px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,33,165,0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .event-card:hover {
        box-shadow: 0 8px 32px rgba(0,0,0,0.12);
        transform: translateY(-4px);
        border-color: rgba(0,33,165,0.2);
    }

    /* Category badges */
    .category-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        letter-spacing: 0.02em;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    /* Metrics cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.03);
        border-radius: 12px;
        font-weight: 600;
        padding: 1rem;
        line-height: 1.5 !important;
        overflow: visible !important;
    }

    .streamlit-expanderHeader p {
        line-height: 1.5 !important;
        margin: 0 !important;
    }

    /* Data editor / table styling */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state with error handling
try:
    if 'simulator' not in st.session_state or st.session_state.simulator is None:
        st.session_state.simulator = CrowdDataSimulator()
    if 'event_generator' not in st.session_state or st.session_state.event_generator is None:
        st.session_state.event_generator = UFEventGenerator()
        st.session_state.events = st.session_state.event_generator.generate_semester_events(50)
    if 'event_classifier' not in st.session_state or st.session_state.event_classifier is None:
        st.session_state.event_classifier = ImprovedEventCategorizer()
    if 'forecaster' not in st.session_state or st.session_state.forecaster is None:
        st.session_state.forecaster = CrowdForecaster()
    if 'user_created_events' not in st.session_state:
        st.session_state.user_created_events = []
except Exception as e:
    st.error(f"Error initializing application components: {str(e)}")
    st.info("Try refreshing the page. If the issue persists, check that all dependencies are installed.")

# Page header
st.title("Campus Events")
st.markdown("Discover upcoming events with AI-powered categorization and crowd forecasts")

# Check if we should show success message for newly created event
if 'show_event_created' in st.session_state and st.session_state.show_event_created:
    st.success(f"Event '{st.session_state.new_event_title}' created successfully! It's now visible in the Browse Events tab below.")
    st.info("**Tip**: If you don't see your event, check that filters (Category/Time/Location) are not hiding it. Set all filters to 'All' to see all events.")
    del st.session_state.show_event_created
    if 'new_event_title' in st.session_state:
        del st.session_state.new_event_title

# Default to Browse Events tab if we just created an event
if 'switch_to_browse' in st.session_state and st.session_state.switch_to_browse:
    default_tab = 0  # Browse Events tab
    del st.session_state.switch_to_browse
else:
    default_tab = 0

# Tabs
tab1, tab2, tab3 = st.tabs(["Browse Events", "Create Event", "AI Classifier"])

# Tab 1: Browse Events
with tab1:
    st.markdown("### Upcoming Events")

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
    stat_col1, stat_col2, stat_col3, stat_col4, stat_col5 = st.columns(5)

    with stat_col1:
        st.metric("Showing", len(filtered_events))

    with stat_col2:
        user_events = len(st.session_state.user_created_events)
        st.metric("Your Events", user_events, delta="Created by you" if user_events > 0 else None)

    with stat_col3:
        free_events = sum(1 for e in filtered_events if e.get('is_free', True))
        st.metric("Free Events", free_events)

    with stat_col4:
        today_events = sum(1 for e in filtered_events if e['start_time'].date() == datetime.now().date())
        st.metric("Today", today_events)

    with stat_col5:
        this_week = sum(1 for e in filtered_events if (e['start_time'] - datetime.now()).days <= 7)
        st.metric("This Week", this_week)

    st.markdown("---")

    # Show warning if user has created events but they're filtered out
    if len(st.session_state.user_created_events) > 0:
        user_events_visible = sum(1 for e in filtered_events if e in st.session_state.user_created_events)
        if user_events_visible == 0:
            st.warning(f"You have {len(st.session_state.user_created_events)} created event(s) that are hidden by current filters. Try setting Category, Time, and Location filters to 'All' to see all your events.")

    # Event cards
    if len(filtered_events) == 0:
        st.info("No events found matching your filters. Try changing the filter settings above.")
    else:
        # Show category distribution
        if len(filtered_events) > 3:
            with st.expander("Event Category Distribution"):
                events_df = pd.DataFrame(filtered_events)
                fig = create_category_distribution(events_df)
                st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"### Showing {len(filtered_events)} Event(s)")

        for event in filtered_events[:20]:  # Show max 20
            # Check if this is a user-created event
            is_user_created = event in st.session_state.user_created_events

            with st.container():
                col1, col2 = st.columns([3, 1])

                with col1:
                    # Category badge color
                    category_colors = {
                        'Academic': '#0021A5',
                        'Social': '#FA4616',
                        'Sports': '#28a745',
                        'Cultural': '#008080'
                    }
                    color = category_colors.get(event['category'], '#6c757d')

                    # Add "Your Event" badge for user-created events
                    user_badge = '<span style="background: #FFD700; color: #333; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.85rem; margin-right: 0.5rem; font-weight: bold;">Your Event</span>' if is_user_created else ''

                    # Add border highlight for user-created events
                    border_style = f"border: 2px solid {color};" if is_user_created else ""

                    # Build tags HTML (no hardcoded colors - inherit from theme)
                    tags_html = ' '.join([f'<span style="background: rgba(0,33,165,0.1); padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.85rem; margin-right: 0.5rem;">{tag}</span>' for tag in event.get('tags', [])[:3]])

                    # Build event card HTML - theme-aware, no hardcoded colors
                    event_html = f"""<div class="event-card" style="border-left: 5px solid {color}; {border_style}">
<h3 style="margin: 0;">{event['title']}</h3>
<p style="margin: 0.5rem 0;">{event['description']}</p>
<div style="margin-top: 0.5rem;">
{user_badge}<span style="background: {color}; color: white; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.85rem; margin-right: 0.5rem;">{event['category']}</span>
{tags_html}
</div>
</div>"""

                    st.markdown(event_html, unsafe_allow_html=True)

                with col2:
                    location = get_location_by_id(event['location_id'])
                    location_name = location['name'] if location else "Unknown"

                    st.write(f"**{location_name}**")
                    st.write(f"**{event['start_time'].strftime('%b %d, %I:%M %p')}**")
                    st.write(f"**{event.get('attendees_expected', 'N/A')}** expected")

                    if event.get('is_free', False):
                        st.success("Free Event")

                    # Get crowd forecast for event time
                    if location and st.session_state.simulator is not None and st.session_state.forecaster is not None:
                        with st.expander("Crowd Forecast"):
                            try:
                                hist_data = st.session_state.simulator.generate_historical_data(location, days=1)
                                recent_levels = hist_data['crowd_level'].values[-12:]
                                predictions = st.session_state.forecaster.predict(recent_levels)
                                label, emoji = st.session_state.forecaster.get_forecast_label(predictions)

                                st.write(f"{emoji} Expected crowd: **{label}**")
                            except Exception as e:
                                st.warning("Crowd forecast temporarily unavailable")

                st.markdown("---")

# Tab 2: Create Event
with tab2:
    st.markdown("### Create New Event")
    st.markdown("Use AI to automatically categorize and tag your event!")

    # Check if user has organizer permissions
    user_email = None
    user_role = 'user'

    if 'user' in st.session_state and st.session_state.user:
        user_email = st.session_state.user.get('email', '')
        user_role = get_user_role(user_email)

    if user_role not in ['organizer', 'admin']:
        st.warning("🔒 Event creation is restricted to organizers only")
        st.info("To create events, you need organizer permissions.")

        col1, col2 = st.columns([1, 2])

        with col1:
            if user_email:
                if st.button("🎫 Request Organizer Access", type="primary", use_container_width=True):
                    st.switch_page("pages/4_👤_Profile.py")
            else:
                if st.button("🔑 Sign In to Request Access", type="primary", use_container_width=True):
                    st.switch_page("pages/4_👤_Profile.py")

        with col2:
            st.markdown("""
            **Why become an organizer?**
            - Create and promote campus events
            - Reach the UF community
            - Build your event portfolio
            """)

        st.stop()

    # User is authorized - show event creation form
    st.success(f"✅ Authorized as {user_role.title()}")

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

        submit_button = st.form_submit_button("Create Event with AI", type="primary", use_container_width=True)

        if submit_button:
            if event_title and event_description and event_location:
                # Use AI to categorize
                if st.session_state.event_classifier is None:
                    st.error("Event classifier not initialized. Please refresh the page.")
                    st.stop()

                try:
                    ai_result = st.session_state.event_classifier.predict(event_title, event_description)
                except Exception as e:
                    st.error(f"Error categorizing event: {str(e)}")
                    st.stop()

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

                # Set flags for success message and tab switching
                st.session_state.show_event_created = True
                st.session_state.new_event_title = event_title
                st.session_state.switch_to_browse = True

                # Force a rerun to show the event and success message
                st.rerun()

            else:
                st.error("Please fill in all required fields (marked with *)")

# Tab 3: AI Classifier Info
with tab3:
    st.markdown("### AI Event Classifier")
    st.markdown("Learn about how the AI categorizes events")

    st.markdown("""
    #### How It Works

    The Campus Pulse event classifier uses an **improved Transformer-based NLP model** (DistilBERT) with
    advanced fine-tuning to categorize events into one of four categories:

    - **Academic**: Workshops, lectures, research presentations, career fairs
    - **Social**: Parties, entertainment, social gatherings, movie nights
    - **Sports**: Games, fitness activities, competitions, recreation
    - **Cultural**: Festivals, performances, international events, heritage celebrations

    #### Advanced Features

    1. **Fine-Tuned Architecture**: Multi-layer classification head with batch normalization
    2. **Smart Training**: Uses validation split, learning rate scheduling, and early stopping
    3. **Transfer Learning**: Freezes encoder initially, then fine-tunes for optimal performance
    4. **Confidence Calibration**: Temperature scaling for better confidence estimates
    5. **Context-Aware**: Uses [SEP] token to distinguish title from description
    6. **Tag Extraction**: Intelligent tag suggestion based on content and context
    7. **Trained on 100+ Real UF Events**: Model learns from actual campus event patterns

    #### Training Techniques

    - **Two-Phase Training**: Classifier head first, then full model fine-tuning
    - **Gradient Clipping**: Prevents exploding gradients
    - **Learning Rate Warmup**: Gradual learning rate increase for stability
    - **Early Stopping**: Prevents overfitting with patience-based stopping
    - **Stratified Split**: Ensures balanced class distribution in train/val sets
    """)

    st.markdown("---")

    st.markdown("#### Try the Classifier")

    test_title = st.text_input("Enter an event title:", placeholder="e.g., Basketball Game vs Georgia")
    test_description = st.text_area("Enter event description:", placeholder="Describe the event...")

    if st.button("Classify This Event", type="primary"):
        if test_title or test_description:
            if st.session_state.event_classifier is None:
                st.error("Event classifier not initialized. Please refresh the page.")
            else:
                try:
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
                            'Cultural': '#008080'
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
                            st.markdown(f"- {tag}")

                    st.markdown("---")
                    st.markdown("**All Category Probabilities:**")

                    for category, prob in sorted(result['all_probabilities'].items(), key=lambda x: x[1], reverse=True):
                        st.progress(prob, text=f"{category}: {prob*100:.1f}%")
                except Exception as e:
                    st.error(f"Error classifying event: {str(e)}")

        else:
            st.warning("Please enter at least a title or description")

    st.markdown("---")

    # Training section
    with st.expander("Model Training Info"):
        st.markdown("""
        The classifier is based on a pretrained transformer model (DistilBERT) and can be fine-tuned
        on campus-specific event data for improved accuracy.

        **Training Data**: The model uses example events from various UF categories
        **Architecture**: Transformer encoder + classification head
        **Fallback**: Rule-based classifier when transformer is unavailable
        """)

        col_train1, col_train2 = st.columns(2)

        with col_train1:
            st.metric("Training Examples", len(TRAINING_EVENTS))
            st.metric("Categories", 4)

        with col_train2:
            st.metric("Model", "DistilBERT")
            st.metric("Parameters", "~66M")

        if st.button("Train Classifier", type="primary", use_container_width=True):
            with st.spinner("Training improved classifier with advanced techniques... This will take 2-3 minutes."):
                try:
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    status_text.text("Initializing model...")
                    progress_bar.progress(10)

                    # Train with improved method
                    st.session_state.event_classifier.train(
                        TRAINING_EVENTS,
                        epochs=15,
                        lr=2e-5,
                        batch_size=16,
                        validation_split=0.15
                    )

                    progress_bar.progress(100)
                    status_text.text("Training complete!")

                    st.success("Improved classifier trained successfully with advanced fine-tuning!")

                    # Show training results
                    st.balloons()

                except Exception as e:
                    st.warning(f"Transformer training unavailable: {str(e)}")
                    st.info("The app will use an enhanced rule-based classifier instead, which still works great!")
                    st.info("To enable full transformer training, ensure PyTorch and Transformers are installed correctly.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem 0;">
    <p>Campus Pulse Events | Powered by AI</p>
</div>
""", unsafe_allow_html=True)
