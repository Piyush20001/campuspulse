"""
Map utilities for creating Folium heatmaps
"""
import folium
from folium import plugins
import pandas as pd

def create_base_map(center, zoom_start=15):
    """Create base Folium map"""
    m = folium.Map(
        location=center,
        zoom_start=zoom_start,
        tiles='OpenStreetMap',
        prefer_canvas=True
    )
    return m

def add_heatmap_layer(map_obj, crowd_data):
    """Add heatmap layer to map"""
    # Prepare data for heatmap: [lat, lon, intensity]
    heat_data = []
    for crowd in crowd_data:
        lat = crowd['lat']
        lon = crowd['lon']
        intensity = crowd['crowd_level']
        heat_data.append([lat, lon, intensity])

    # Add heatmap layer
    plugins.HeatMap(
        heat_data,
        min_opacity=0.3,
        max_opacity=0.8,
        radius=25,
        blur=20,
        gradient={
            0.0: 'green',
            0.3: 'yellow',
            0.6: 'orange',
            0.85: 'red',
            1.0: 'darkred'
        }
    ).add_to(map_obj)

    return map_obj

def add_location_markers(map_obj, crowd_data, forecasts=None, events_by_location=None):
    """Add markers for each location with popup info"""
    for i, crowd in enumerate(crowd_data):
        # Determine marker color based on crowd level
        if crowd['crowd_level'] < 0.3:
            color = 'green'
            icon = 'ok-sign'
        elif crowd['crowd_level'] < 0.6:
            color = 'lightgreen'
            icon = 'minus-sign'
        elif crowd['crowd_level'] < 0.85:
            color = 'orange'
            icon = 'exclamation-sign'
        else:
            color = 'red'
            icon = 'warning-sign'

        # Build popup HTML
        popup_html = f"""
        <div style="font-family: Arial; width: 250px;">
            <h4 style="margin: 0 0 10px 0; color: #1f77b4;">{crowd['location_name']}</h4>
            <hr style="margin: 5px 0;">
            <p style="margin: 5px 0;"><b>Current Occupancy:</b> {crowd['headcount']} / {crowd['capacity']}</p>
            <p style="margin: 5px 0;"><b>Crowd Level:</b> {crowd['percentage']}%</p>
        """

        # Add forecast if available
        if forecasts and i < len(forecasts):
            forecast = forecasts[i]
            label, emoji = forecast['label'], forecast['emoji']
            popup_html += f"""
            <hr style="margin: 5px 0;">
            <p style="margin: 5px 0;"><b>1h Forecast:</b> {emoji} {label}</p>
            """

        # Add events if available
        if events_by_location and crowd['location_id'] in events_by_location:
            location_events = events_by_location[crowd['location_id']]
            if location_events:
                popup_html += f"""
                <hr style="margin: 5px 0;">
                <p style="margin: 5px 0;"><b>Upcoming Events:</b></p>
                <ul style="margin: 5px 0; padding-left: 20px; font-size: 12px;">
                """
                for event in location_events[:2]:  # Show max 2 events
                    popup_html += f"<li>{event['title']}</li>"
                popup_html += "</ul>"

        popup_html += "</div>"

        # Add marker
        folium.Marker(
            location=[crowd['lat'], crowd['lon']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{crowd['location_name']}: {crowd['percentage']}% full",
            icon=folium.Icon(color=color, icon=icon, prefix='glyphicon')
        ).add_to(map_obj)

    return map_obj

def get_crowd_color(crowd_level):
    """Get color for crowd level"""
    if crowd_level < 0.3:
        return '#28a745'  # Green
    elif crowd_level < 0.6:
        return '#ffc107'  # Yellow
    elif crowd_level < 0.85:
        return '#fd7e14'  # Orange
    else:
        return '#dc3545'  # Red

def get_crowd_label(crowd_level):
    """Get label for crowd level"""
    if crowd_level < 0.3:
        return "Light"
    elif crowd_level < 0.6:
        return "Normal"
    elif crowd_level < 0.85:
        return "Busy"
    else:
        return "Very Busy"
