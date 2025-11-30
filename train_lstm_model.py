#!/usr/bin/env python3
"""
Train LSTM RNN model for crowd prediction time series forecasting
"""
import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime

# Add streamlit_app to path
sys.path.insert(0, 'streamlit_app')

from models.lstm_forecaster import CrowdForecaster
from data.simulator import CrowdDataSimulator
from data.locations import UF_LOCATIONS

def generate_training_data():
    """Generate comprehensive time series data for all locations"""
    print("📊 Generating time series training data...")

    simulator = CrowdDataSimulator()
    all_data = []

    for location in UF_LOCATIONS:
        print(f"  - Generating data for {location['name']}...")
        # Generate 30 days of historical data at 10-minute intervals
        hist_data = simulator.generate_historical_data(
            location,
            days=30,
            interval_minutes=10
        )
        all_data.append(hist_data)

    # Combine all location data
    combined_data = pd.concat(all_data, ignore_index=True)
    print(f"✓ Generated {len(combined_data)} time series data points")

    return combined_data

def train_lstm():
    """Train LSTM model on time series data"""
    print("="*60)
    print("Training LSTM RNN Model for Crowd Prediction")
    print("="*60)

    # Generate training data
    training_data = generate_training_data()

    # Initialize LSTM forecaster
    print("\n🧠 Initializing LSTM model...")
    print("  - Architecture: 2-layer LSTM with 64 hidden units")
    print("  - Sequence length: 12 time steps (2 hours)")
    print("  - Forecast horizon: 6 time steps (1 hour)")

    forecaster = CrowdForecaster(sequence_length=12)

    # Train the model
    print("\n🚀 Training LSTM model...")
    forecaster.train(training_data, epochs=100, lr=0.001)

    # Save the trained model
    model_path = 'streamlit_app/models/lstm_crowd_model.pth'
    forecaster.save_model(model_path)

    print(f"\n{'='*60}")
    print(f"✅ SUCCESS!")
    print(f"{'='*60}")
    print(f"✓ LSTM model trained and saved to {model_path}")
    print(f"✓ Model type: 2-layer LSTM (PyTorch)")
    print(f"✓ Ready for real-time crowd forecasting")
    print(f"\n🚀 Now restart your Streamlit app to use the LSTM model!")
    print(f"{'='*60}\n")

    # Test prediction
    print("\n🧪 Testing prediction...")
    test_sequence = training_data['crowd_level'].values[-12:]
    predictions = forecaster.predict(test_sequence)
    label, emoji = forecaster.get_forecast_label(predictions)
    print(f"  Sample forecast: {emoji} {label}")
    print(f"  Predicted levels: {predictions}")

if __name__ == "__main__":
    train_lstm()
