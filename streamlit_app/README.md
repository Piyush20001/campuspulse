# 🎓 Campus Pulse - AI-Powered Campus Intelligence

**Campus Pulse** is a comprehensive real-time campus crowd and event intelligence platform built with Streamlit and Python. It helps University of Florida students make informed decisions about when and where to visit campus locations.

## ✨ Features

### 🗺️ Live Crowd Heatmap
- **Interactive Folium Map**: Visual heatmap of crowd density across UF campus
- **Real-time Updates**: Current occupancy levels for 15+ campus locations
- **Location Details**: Click markers for detailed information, forecasts, and events
- **Smart Filtering**: Filter by category (Libraries, Gyms, Dining, Academic, etc.)
- **Historical Trends**: View past crowd patterns with interactive charts

### 🎉 Campus Events
- **Event Discovery**: Browse 30+ upcoming campus events
- **AI Categorization**: Automatic event classification using Transformer-based NLP
- **Smart Filtering**: Filter by category, time range, and location
- **Event Creation**: Create new events with AI-powered categorization
- **Crowd Forecasts**: See predicted crowd levels at event times
- **Category Distribution**: Visual analytics of event types

### ⭐ Saved Locations
- **Personalize Experience**: Save your favorite campus spots
- **Smart Recommendations**: Get suggestions for available locations
- **Alert Settings**: Configure notifications for occupancy changes
- **Quick Overview**: Dashboard of all saved locations
- **Forecast Integration**: See 1-hour predictions for each location

## 🤖 AI-Powered Features

### 1️⃣ LSTM Time Series Forecaster
- **Architecture**: 2-layer LSTM neural network
- **Purpose**: Predict crowd levels for the next hour (6 time steps of 10 minutes each)
- **Features**:
  - Learns temporal patterns from historical data
  - Provides confidence levels (Light, Normal, Busy, Very Busy)
  - Handles multiple locations simultaneously

### 2️⃣ Transformer-based Event Classifier
- **Model**: DistilBERT (lightweight transformer encoder)
- **Purpose**: Auto-categorize events into Academic, Social, Sports, or Cultural
- **Features**:
  - Analyzes event title and description
  - Provides confidence scores for all categories
  - Suggests relevant tags automatically
  - Fallback to rule-based classifier if transformer unavailable

### 3️⃣ Autoencoder Anomaly Detector
- **Architecture**: Neural network autoencoder
- **Purpose**: Detect unusual crowd patterns
- **Features**:
  - Trained on normal baseline patterns
  - Flags spikes, drops, and irregular behavior
  - Provides severity levels (Medium, High, Critical)
  - Human-readable explanations

## 📁 Project Structure

```
streamlit_app/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── pages/                      # Multi-page app pages
│   ├── 1_🗺️_Crowd_Heatmap.py  # Heatmap page
│   ├── 2_🎉_Events.py          # Events page
│   └── 3_⭐_Saved_Locations.py # Saved locations page
│
├── models/                     # ML models
│   ├── lstm_forecaster.py     # LSTM time series model
│   ├── event_classifier.py    # Transformer NLP classifier
│   └── anomaly_detector.py    # Autoencoder anomaly detection
│
├── data/                       # Data generation and management
│   ├── simulator.py           # Crowd data simulator
│   ├── events_data.py         # Event data generator
│   └── locations.py           # UF campus locations
│
├── utils/                      # Utility functions
│   ├── config.py              # Configuration constants
│   ├── map_utils.py           # Folium map utilities
│   └── chart_utils.py         # Plotly chart utilities
│
└── trained_models/             # Saved model checkpoints (created at runtime)
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Navigate to the streamlit_app directory**:
   ```bash
   cd streamlit_app
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**:
   The app will automatically open at `http://localhost:8501`

## 🎮 Usage Guide

### Crowd Heatmap Page
1. Use filter buttons to select location categories
2. View the interactive map with color-coded markers
3. Click markers to see detailed popup information
4. Select a location from dropdown for detailed analysis
5. View historical trends and 1-hour forecasts

### Events Page
1. **Browse Events Tab**:
   - Filter events by category, time, or location
   - View event cards with AI-generated categories and tags
   - Check crowd forecasts for event times

2. **Create Event Tab**:
   - Fill in event details (title, description, location, time)
   - Submit to get AI categorization
   - View confidence scores and suggested tags

3. **AI Classifier Tab**:
   - Learn about the classifier
   - Test with custom event titles/descriptions
   - Train the model (optional)

### Saved Locations Page
1. Add locations using the dropdown and "Save Location" button
2. View dashboard with metrics for all saved locations
3. Check forecasts and anomaly alerts
4. Configure alert settings for each location
5. View smart recommendations

## 🔧 Configuration

### Adjusting Thresholds
Edit `utils/config.py` to customize:
- Crowd level thresholds (Light, Normal, Busy, Very Busy)
- Anomaly detection sensitivity
- Forecast time steps
- Map center coordinates

### Adding Locations
Edit `data/locations.py` to add new UF locations:
```python
{
    'id': 16,
    'name': 'New Location',
    'category': 'ACADEMIC',
    'lat': 29.6500,
    'lon': -82.3450,
    'capacity': 100,
    'description': 'Description here'
}
```

### Customizing Crowd Patterns
Edit methods in `data/simulator.py` to adjust:
- Daily crowd patterns for different location types
- Peak hours and occupancy levels
- Weekend variations
- Random noise levels

## 🧠 ML Model Details

### Training the LSTM Forecaster
```python
from models.lstm_forecaster import CrowdForecaster
from data.simulator import CrowdDataSimulator

simulator = CrowdDataSimulator()
forecaster = CrowdForecaster()

# Generate training data
location = UF_LOCATIONS[0]
hist_data = simulator.generate_historical_data(location, days=7)

# Train
forecaster.train(hist_data, epochs=50)

# Save
forecaster.save_model('trained_models/lstm_forecaster.pth')
```

### Training the Event Classifier
```python
from models.event_classifier import EventCategorizer
from data.events_data import TRAINING_EVENTS

classifier = EventCategorizer()
classifier.train(TRAINING_EVENTS, epochs=10)
classifier.save_model('trained_models/event_classifier.pth')
```

### Training the Anomaly Detector
```python
from models.anomaly_detector import AnomalyDetector

detector = AnomalyDetector()

# Train on normal data (no anomalies)
normal_data = simulator.generate_historical_data(location, days=7)
detector.train(normal_data, epochs=100)

detector.save_model('trained_models/anomaly_detector.pth')
```

## 📊 Data Simulation

All crowd data is **simulated** using realistic patterns:
- Time-of-day variations (morning rush, evening peaks, etc.)
- Location-specific patterns (library vs gym vs dining)
- Day-of-week effects (weekdays vs weekends)
- Random noise for realism

Events are **randomly generated** from templates with realistic details.

## 🎨 Customization

### Changing UF Colors
The app uses UF's official colors:
- Blue: `#0021A5`
- Orange: `#FA4616`

Update these in the CSS sections of each page for different branding.

### Adding More Event Categories
1. Add category to `utils/config.py`:
   ```python
   EVENT_CATEGORIES = ['Academic', 'Social', 'Sports', 'Cultural', 'Recreation']
   ```

2. Update classifier in `models/event_classifier.py`

3. Add templates to `data/events_data.py`

## 🐛 Troubleshooting

### Map Not Displaying
- Check that `streamlit-folium` is installed
- Clear browser cache
- Restart Streamlit server

### Transformer Model Errors
- The app falls back to rule-based classification if transformers are unavailable
- Ensure `transformers` and `torch` are properly installed
- For CPU-only machines, PyTorch CPU version is sufficient

### Import Errors
- Ensure you're running from the `streamlit_app` directory
- Check Python path includes the app directory

## 📝 Future Enhancements

Potential additions:
- [ ] Real sensor integration (replace simulation)
- [ ] User authentication and profiles
- [ ] Push notifications (email/SMS)
- [ ] Historical data export
- [ ] Mobile app version
- [ ] Integration with UF calendar
- [ ] Parking availability tracking
- [ ] Study room booking

## 📄 License

This project is for educational purposes. UF branding and data are property of the University of Florida.

## 👥 Credits

Built with:
- **Streamlit**: Web framework
- **PyTorch**: Deep learning models
- **Transformers**: NLP models (Hugging Face)
- **Folium**: Interactive maps
- **Plotly**: Data visualization

## 🙋 Support

For questions or issues:
1. Check this README
2. Review code comments
3. Check Streamlit documentation: https://docs.streamlit.io

---

**Campus Pulse** - Making campus navigation smarter with AI 🎓✨
