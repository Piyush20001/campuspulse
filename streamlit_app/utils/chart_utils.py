"""
Chart utilities using Plotly
"""
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd

def create_sparkline(historical_data, height=100):
    """Create a small sparkline chart"""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=historical_data.index,
        y=historical_data.values,
        mode='lines',
        line=dict(color='#1f77b4', width=2),
        fill='tozeroy',
        fillcolor='rgba(31, 119, 180, 0.2)'
    ))

    fig.update_layout(
        height=height,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False, range=[0, 1]),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    return fig

def create_forecast_chart(historical_data, forecast_data, location_name):
    """Create forecast chart with historical context"""
    fig = go.Figure()

    # Historical data
    fig.add_trace(go.Scatter(
        x=historical_data['timestamp'],
        y=historical_data['crowd_level'],
        mode='lines',
        name='Historical',
        line=dict(color='#1f77b4', width=2),
        fill='tozeroy',
        fillcolor='rgba(31, 119, 180, 0.1)'
    ))

    # Forecast data
    if len(forecast_data) > 0:
        fig.add_trace(go.Scatter(
            x=forecast_data['timestamp'],
            y=forecast_data['crowd_level'],
            mode='lines',
            name='Forecast',
            line=dict(color='#ff7f0e', width=2, dash='dash'),
            fill='tozeroy',
            fillcolor='rgba(255, 127, 14, 0.1)'
        ))

    fig.update_layout(
        title=f"Crowd Level Forecast - {location_name}",
        xaxis_title="Time",
        yaxis_title="Crowd Level",
        yaxis=dict(range=[0, 1], tickformat='.0%'),
        hovermode='x unified',
        height=400,
        template='plotly_white'
    )

    return fig

def create_crowd_gauge(crowd_level, capacity, headcount):
    """Create a gauge chart for crowd level"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=crowd_level * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"Occupancy<br><sub>{headcount}/{capacity} people</sub>"},
        delta={'reference': 50},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 30], 'color': "lightgreen"},
                {'range': [30, 60], 'color': "yellow"},
                {'range': [60, 85], 'color': "orange"},
                {'range': [85, 100], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))

    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    return fig

def create_category_distribution(events_df):
    """Create pie chart of event categories"""
    category_counts = events_df['category'].value_counts()

    fig = px.pie(
        values=category_counts.values,
        names=category_counts.index,
        title='Events by Category',
        color_discrete_sequence=px.colors.qualitative.Set3
    )

    fig.update_layout(height=350)
    return fig

def create_timeline_chart(events_df):
    """Create timeline of upcoming events"""
    if len(events_df) == 0:
        return None

    fig = px.timeline(
        events_df,
        x_start='start_time',
        x_end='end_time',
        y='location_name',
        color='category',
        hover_data=['title'],
        title='Event Timeline'
    )

    fig.update_layout(
        height=400,
        xaxis_title='Time',
        yaxis_title='Location'
    )

    return fig

def create_comparison_bar_chart(locations_data):
    """Create bar chart comparing crowd levels across locations"""
    df = pd.DataFrame(locations_data)

    fig = px.bar(
        df,
        x='location_name',
        y='percentage',
        color='percentage',
        color_continuous_scale=['green', 'yellow', 'orange', 'red'],
        title='Current Crowd Levels by Location',
        labels={'percentage': 'Occupancy %', 'location_name': 'Location'}
    )

    fig.update_layout(
        height=400,
        xaxis_tickangle=-45,
        showlegend=False
    )

    return fig
