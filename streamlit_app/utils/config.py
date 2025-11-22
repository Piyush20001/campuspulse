"""
Configuration file for Campus Pulse application
"""

# UF Campus Center Coordinates
UF_CENTER = [29.6436, -82.3549]

# Map Configuration
MAP_CONFIG = {
    'zoom_start': 15,
    'tiles': 'OpenStreetMap',
    'center': UF_CENTER
}

# Crowd Level Thresholds
CROWD_THRESHOLDS = {
    'light': 30,
    'normal': 60,
    'busy': 85,
    'very_busy': 100
}

# Anomaly Detection Threshold
ANOMALY_THRESHOLD = 0.15

# Forecast Settings
FORECAST_STEPS = 6  # 6 x 10 minutes = 1 hour
TIME_INTERVAL = 10  # minutes

# Event Categories
EVENT_CATEGORIES = ['Academic', 'Social', 'Sports', 'Cultural', 'Other']

# Model Paths
MODEL_PATHS = {
    'lstm': 'trained_models/lstm_forecaster.pth',
    'autoencoder': 'trained_models/autoencoder.pth',
    'event_classifier': 'trained_models/event_classifier.pth'
}
