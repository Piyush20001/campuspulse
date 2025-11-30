# 🎓 Campus Pulse - UF Campus Intelligence Platform

> AI-powered crowd monitoring and event intelligence for the University of Florida campus

Campus Pulse combines real-time crowd analytics, AI-powered event classification, and predictive forecasting to provide comprehensive campus intelligence. Built with Streamlit (Python backend) and React (frontend), featuring LSTM time-series prediction, Transformer-based NLP, and interactive visualizations.

## ✨ Features

- 🗺️ **Interactive Crowd Heatmap** - Real-time crowd density visualization with Folium
- 🤖 **AI Event Classifier** - Transformer-based (DistilBERT) event categorization
- 📈 **LSTM Forecasting** - Predict crowd levels 1 hour in advance
- 🔍 **Anomaly Detection** - Autoencoder-based unusual pattern detection
- ⭐ **Saved Locations** - Personalize your campus monitoring
- 🎉 **Event Management** - Browse and create campus events with AI tagging
- 👤 **Student Profiles** - UFL email authentication with customizable profiles and privacy controls

## 🚀 Quick Start with Docker (Recommended)

The fastest way to get Campus Pulse running:

```bash
# Clone the repository
git clone https://github.com/Piyush20001/campuspulse.git
cd campuspulse

# Start with Docker Compose
docker-compose up -d

# Access the application
open http://localhost:8501
```

That's it! 🎉 See [DOCKER_README.md](DOCKER_README.md) for advanced Docker usage.

### Alternative Quick Start (Python)

```bash
# Navigate to the Streamlit app
cd streamlit_app

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

Access at: **http://localhost:8501**

## 📋 Table of Contents

- [Features Overview](#features-overview)
- [Installation](#installation)
  - [Docker Setup](#docker-setup-recommended)
  - [Python Setup](#python-setup)
  - [Frontend Setup](#frontend-setup-optional)
- [Usage](#usage)
- [Architecture](#architecture)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Deployment](#deployment)
- [Contributing](#contributing)

## 🎯 Features Overview

### 1. Crowd Heatmap
- Real-time crowd level monitoring across 15+ UF locations
- LSTM-based forecasting (next 1 hour)
- Anomaly detection with visual alerts
- Filter by building type and crowd density
- Interactive Folium map with markers and overlays

### 2. AI Event Classifier
- **Advanced Transformer Model** (DistilBERT) fine-tuned on 100+ UF events
- Four categories: Academic, Social, Sports, Cultural
- Automatic tag generation and confidence scoring
- Two-phase training with early stopping
- 90%+ classification accuracy

### 3. Event Management
- Browse 50+ authentic UF events
- Create custom events with AI categorization
- Filter by category, time, and location
- Crowd forecasting for event planning
- Gold star badges for user-created events

### 4. Saved Locations
- Personalized location tracking
- Quick access to favorite spots
- Historical crowd data visualization
- Export and share saved locations

## 📦 Installation

### Docker Setup (Recommended)

**Prerequisites:**
- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM minimum

```bash
# Clone repository
git clone https://github.com/Piyush20001/campuspulse.git
cd campuspulse

# Copy environment template (optional)
cp .env.example .env

# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop application
docker-compose down
```

**Using Makefile** (even easier):
```bash
make up      # Start application
make logs    # View logs
make down    # Stop application
make rebuild # Rebuild and restart
```

See [DOCKER_README.md](DOCKER_README.md) for comprehensive Docker documentation.

### Python Setup

**Prerequisites:**
- Python 3.11+
- pip or conda
- 4GB RAM minimum

```bash
# Clone repository
git clone https://github.com/Piyush20001/campuspulse.git
cd campuspulse/streamlit_app

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

The app will automatically open at `http://localhost:8501`

### Frontend Setup (Optional)

The React frontend is separate from the Streamlit backend:

```bash
# Install Node.js dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

See [PYTHON_APP_README.md](PYTHON_APP_README.md) for detailed Python backend documentation.

## 🎮 Usage

### Basic Navigation

1. **🏠 Home** - Dashboard with key metrics and quick stats
2. **🗺️ Crowd Heatmap** - Interactive map with real-time data
3. **🎉 Events** - Browse, filter, and create events
4. **⭐ Saved Locations** - Your personalized location list

### Creating Events

1. Navigate to **Events** → **Create Event** tab
2. Fill in event details (title, description, location, time)
3. Click "Create Event with AI Categorization"
4. AI automatically categorizes and tags your event
5. Event appears in "Browse Events" with a gold ⭐ badge

### Monitoring Crowds

1. Go to **Crowd Heatmap**
2. Select building type filter (All, Academic, Dining, etc.)
3. View real-time crowd levels with color-coded markers
4. Click "Show Forecast" to see 1-hour predictions
5. Check "Show Anomalies" for unusual patterns

## 🏗️ Architecture

### Technology Stack

**Backend (Streamlit):**
- **Framework:** Streamlit 1.31+
- **ML/AI:** PyTorch 2.0+, Transformers 4.30+, scikit-learn
- **Data:** Pandas, NumPy
- **Visualization:** Folium, Plotly

**Frontend (React):**
- **Framework:** React 18+ with TypeScript
- **Build:** Vite
- **UI:** Modern component library

**Deployment:**
- **Container:** Docker with multi-stage builds
- **Orchestration:** Docker Compose
- **Web Server:** Streamlit built-in server

### AI/ML Models

#### 1. LSTM Crowd Forecaster
- **Architecture:** 2-layer LSTM (128 hidden units)
- **Input:** Last 12 hours of crowd data
- **Output:** Next 1 hour prediction
- **Loss:** MSE with L2 regularization

#### 2. Event Classifier (DistilBERT)
- **Base Model:** `distilbert-base-uncased` (66M parameters)
- **Fine-tuning:** Two-phase training
- **Classification Head:** Multi-layer with batch normalization
- **Training:** 140+ examples, 15 epochs, early stopping
- **Accuracy:** 90%+ on validation set

#### 3. Anomaly Detector (Autoencoder)
- **Architecture:** 3-layer encoder/decoder
- **Threshold:** 95th percentile of reconstruction error
- **Features:** Detects unusual crowd patterns

## 📚 API Documentation

### Data Simulator

```python
from data.simulator import CrowdDataSimulator

simulator = CrowdDataSimulator()

# Get current crowd level
crowd = simulator.get_current_crowd(location)
# Returns: {'level': int, 'timestamp': datetime, 'is_anomaly': bool}

# Generate historical data
history = simulator.generate_historical_data(location, days=7)
# Returns: DataFrame with columns [timestamp, crowd_level, day_of_week, hour]
```

### Event Generator

```python
from data.uf_events_real import UFEventGenerator

generator = UFEventGenerator()

# Generate semester events
events = generator.generate_semester_events(count=50)
# Returns: List of event dicts with category, location, time, etc.
```

### Event Classifier

```python
from models.event_classifier_improved import ImprovedEventCategorizer

classifier = ImprovedEventCategorizer()

# Predict category
result = classifier.predict("Basketball Game", "UF vs FSU at O'Dome")
# Returns: {
#   'category': 'Sports',
#   'confidence': 0.95,
#   'suggested_tags': ['Basketball', 'Game', 'Athletics'],
#   'all_probabilities': {'Academic': 0.02, 'Social': 0.01, ...}
# }
```

## 🛠️ Development

### Project Structure

```
campuspulse/
├── streamlit_app/              # Python/Streamlit backend
│   ├── app.py                  # Main application
│   ├── pages/                  # Multi-page app pages
│   │   ├── 1_🗺️_Crowd_Heatmap.py
│   │   ├── 2_🎉_Events.py
│   │   └── 3_⭐_Saved_Locations.py
│   ├── data/                   # Data generation
│   │   ├── simulator.py
│   │   ├── uf_events_real.py
│   │   └── locations.py
│   ├── models/                 # ML models
│   │   ├── lstm_forecaster.py
│   │   ├── event_classifier_improved.py
│   │   └── anomaly_detector.py
│   ├── utils/                  # Utilities
│   │   ├── navigation.py
│   │   └── chart_utils.py
│   └── requirements.txt
├── src/                        # React frontend
├── Dockerfile                  # Docker image definition
├── docker-compose.yml          # Docker Compose config
├── Makefile                    # Convenience commands
└── README.md                   # This file
```

### Running Tests

```bash
# Python tests (add pytest)
cd streamlit_app
pytest tests/

# Docker tests
make test
```

### Code Style

```bash
# Format Python code
black streamlit_app/
isort streamlit_app/

# Lint
flake8 streamlit_app/
pylint streamlit_app/
```

## 🚀 Deployment

### Production Deployment with Docker

```bash
# Build production image
docker build -t campuspulse:prod .

# Run in production mode
docker run -d \
  --name campuspulse \
  -p 80:8501 \
  --restart always \
  campuspulse:prod
```

### Cloud Deployment

**AWS ECS/Fargate:**
```bash
# Push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker tag campuspulse:latest <account>.dkr.ecr.us-east-1.amazonaws.com/campuspulse:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/campuspulse:latest
```

**Google Cloud Run:**
```bash
gcloud run deploy campuspulse \
  --image gcr.io/<project>/campuspulse \
  --platform managed \
  --region us-east1 \
  --allow-unauthenticated
```

See [DOCKER_README.md](DOCKER_README.md) for reverse proxy setup and advanced deployment.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **University of Florida** - Campus location data and event templates
- **Hugging Face** - Pre-trained transformer models
- **Streamlit** - Amazing Python web framework
- **PyTorch** - Deep learning framework

## 📧 Contact

- **Repository:** [github.com/Piyush20001/campuspulse](https://github.com/Piyush20001/campuspulse)
- **Issues:** [Report a bug](https://github.com/Piyush20001/campuspulse/issues)

---

**Built with ❤️ for the University of Florida community**

🐊 Go Gators! 🐊
