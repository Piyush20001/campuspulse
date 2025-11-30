#!/usr/bin/env python3
"""
Retrain ML model with current library versions
Run this script to fix model loading issues
"""
import sys
import os

# Add streamlit_app to path
sys.path.insert(0, 'streamlit_app')

from models.crowd_predictor_ml import MLCrowdPredictor

def main():
    print("="*60)
    print("Retraining ML Crowd Prediction Model (v2)")
    print("="*60)

    # Initialize predictor
    predictor = MLCrowdPredictor(model_type='random_forest')

    # Train on v2 data (real UF campus data)
    data_path = 'streamlit_app/data/crowd_training_data_5000_v2.csv'

    if not os.path.exists(data_path):
        print(f"❌ Error: Training data not found at {data_path}")
        return

    print(f"\n📊 Training on real UF campus data from {data_path}...")
    metrics = predictor.train(data_path, test_size=0.2, random_state=42)

    # Save model
    model_path = 'streamlit_app/models/crowd_predictor_model_v2.pkl'
    predictor.save(model_path)

    print(f"\n{'='*60}")
    print(f"✅ SUCCESS!")
    print(f"{'='*60}")
    print(f"✓ Model retrained and saved to {model_path}")
    print(f"✓ Compatible with your current library versions")
    print(f"✓ Test R²: {metrics['test_r2']:.1%} accuracy")
    print(f"✓ Test MAE: {metrics['test_mae']:.2f}")
    print(f"\n🚀 Now restart your Streamlit app to use the updated model!")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
