# 🚀 Campus Pulse - Quick Start Guide

Get Campus Pulse running in 3 simple steps!

## Step 1: Install Dependencies

Open a terminal and navigate to the `streamlit_app` directory:

```bash
cd streamlit_app
pip install -r requirements.txt
```

This will install:
- Streamlit (web framework)
- PyTorch (ML models)
- Transformers (NLP)
- Folium (maps)
- Plotly (charts)
- And other dependencies

**Note**: Installation may take 2-5 minutes depending on your internet speed.

## Step 2: Run the App

Start the Streamlit server:

```bash
streamlit run app.py
```

You should see output like:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.1.x:8501
```

## Step 3: Explore!

The app will automatically open in your browser at `http://localhost:8501`

### What to Try:

1. **Home Page**: See the overview and current campus status

2. **🗺️ Crowd Heatmap** (sidebar):
   - View the interactive map
   - Filter locations by category
   - Click markers for details
   - Select a location for detailed forecast

3. **🎉 Events** (sidebar):
   - Browse upcoming events
   - Create a new event and watch AI categorize it
   - Try the AI classifier with custom text

4. **⭐ Saved Locations** (sidebar):
   - Save your favorite locations
   - Get smart recommendations
   - View forecasts for all saved spots

## 🎯 Key Features to Demo

### AI Forecasting
1. Go to Crowd Heatmap
2. Select any location from dropdown
3. See the **1-hour forecast chart** (LSTM model prediction)

### AI Event Classification
1. Go to Events → Create Event tab
2. Enter:
   - Title: "Basketball Championship Game"
   - Description: "Final game of the season, free admission"
3. Click "Create Event with AI Categorization"
4. Watch it automatically classify as **Sports** with relevant tags!

### Anomaly Detection
- Check the Crowd Heatmap for anomaly alerts
- Anomalies are randomly injected for demonstration

## 🔄 Refreshing Data

Click the **"🔄 Refresh Data"** button on any page to generate new simulated crowd data.

## ⚙️ Optional: Pre-train Models

For better predictions, you can pre-train the models (optional):

1. Go to **Events → AI Event Classifier tab**
2. Click **"🔄 Train Classifier on Sample Data"**
3. Wait for training to complete (~1 minute)

The LSTM and Autoencoder use simpler fallback methods if not trained.

## 🐛 Common Issues

**"Module not found" error**:
```bash
pip install -r requirements.txt --upgrade
```

**Map not showing**:
- Refresh the browser
- Check internet connection (maps need tiles)

**Port already in use**:
```bash
streamlit run app.py --server.port 8502
```

## 📖 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the code in each module
- Customize locations in `data/locations.py`
- Adjust AI models in `models/`

## 🎉 That's It!

You're now running a fully functional AI-powered campus intelligence platform!

**Enjoy exploring Campus Pulse!** 🎓✨
