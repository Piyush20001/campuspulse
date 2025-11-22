"""
Machine Learning Crowd Prediction Model
Trained on 5000-row real-world campus crowd data
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
import pickle
import os
from datetime import datetime, timedelta


class MLCrowdPredictor:
    """
    Advanced ML-based crowd prediction model using Random Forest and Gradient Boosting
    """

    def __init__(self, model_type='random_forest'):
        """
        Initialize predictor with choice of model

        Args:
            model_type: 'random_forest' or 'gradient_boosting'
        """
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.location_encoder = LabelEncoder()
        self.weather_encoder = LabelEncoder()
        self.is_trained = False
        self.feature_names = []
        self.training_history = {}

    def prepare_features(self, df, fit_encoders=False):
        """
        Extract and engineer features from dataframe

        Args:
            df: DataFrame with crowd data
            fit_encoders: Whether to fit label encoders (True for training, False for prediction)

        Returns:
            X: feature matrix
            y: target variable (crowd_count or occupancy_rate)
        """
        # Create a copy to avoid modifying original
        data = df.copy()

        # Handle both old and new column names
        location_col = 'category' if 'category' in data.columns else 'location_type'

        # Encode categorical variables
        if fit_encoders:
            data['location_type_encoded'] = self.location_encoder.fit_transform(data[location_col])
            data['weather_encoded'] = self.weather_encoder.fit_transform(data['weather_condition'])
        else:
            # Handle unknown categories
            location_types = set(self.location_encoder.classes_)
            data[location_col] = data[location_col].apply(
                lambda x: x if x in location_types else self.location_encoder.classes_[0]
            )
            weather_conditions = set(self.weather_encoder.classes_)
            data['weather_condition'] = data['weather_condition'].apply(
                lambda x: x if x in weather_conditions else self.weather_encoder.classes_[0]
            )

            data['location_type_encoded'] = self.location_encoder.transform(data[location_col])
            data['weather_encoded'] = self.weather_encoder.transform(data['weather_condition'])

        # Time-based features
        if 'timestamp' in data.columns:
            data['timestamp'] = pd.to_datetime(data['timestamp'])
            data['month'] = data['timestamp'].dt.month
            data['day_of_month'] = data['timestamp'].dt.day
            data['hour_sin'] = np.sin(2 * np.pi * data['hour'] / 24)
            data['hour_cos'] = np.cos(2 * np.pi * data['hour'] / 24)
            data['day_sin'] = np.sin(2 * np.pi * data['day_of_week'] / 7)
            data['day_cos'] = np.cos(2 * np.pi * data['day_of_week'] / 7)

        # Interaction features
        data['is_peak_hour'] = ((data['hour'] >= 11) & (data['hour'] <= 14) |
                                (data['hour'] >= 17) & (data['hour'] <= 20)).astype(int)
        data['is_class_time'] = ((data['hour'] >= 8) & (data['hour'] <= 17) &
                                 (data['is_weekend'] == 0)).astype(int)
        data['is_late_night'] = ((data['hour'] >= 22) | (data['hour'] <= 5)).astype(int)

        # Weather-time interaction
        data['bad_weather'] = (data['weather_condition'] == 'rain').astype(int)

        # Handle location_id (create if missing)
        if 'location_id' not in data.columns:
            # Create numeric location_id from zone_id or facility
            if 'zone_id' in data.columns:
                # Create a mapping for zone_id to numeric id
                if fit_encoders:
                    unique_zones = data['zone_id'].unique()
                    self.zone_id_map = {zone: idx for idx, zone in enumerate(unique_zones)}
                data['location_id'] = data['zone_id'].map(
                    self.zone_id_map if hasattr(self, 'zone_id_map') else
                    {z: i for i, z in enumerate(data['zone_id'].unique())}
                )
            else:
                data['location_id'] = 0  # Default if no zone info

        # Select features for model
        feature_cols = [
            'location_id', 'location_type_encoded', 'capacity',
            'hour', 'day_of_week', 'month', 'day_of_month',
            'hour_sin', 'hour_cos', 'day_sin', 'day_cos',
            'is_weekend', 'is_exam_period', 'is_holiday',
            'weather_encoded', 'temperature', 'bad_weather',
            'is_peak_hour', 'is_class_time', 'is_late_night'
        ]

        X = data[feature_cols]
        self.feature_names = feature_cols

        # Target variable (handle multiple column names)
        if 'crowd_count' in data.columns:
            y = data['crowd_count']
        elif 'count_in_area' in data.columns:
            y = data['count_in_area']
        elif 'occupancy_rate' in data.columns:
            y = data['occupancy_rate']
        else:
            y = None

        return X, y

    def train(self, csv_path, test_size=0.2, random_state=42):
        """
        Train the model on crowd data from CSV

        Args:
            csv_path: Path to CSV file with training data
            test_size: Fraction of data to use for testing
            random_state: Random seed for reproducibility

        Returns:
            dict: Training metrics and history
        """
        print(f"Loading training data from {csv_path}...")
        df = pd.DataFrame(csv_path) if isinstance(csv_path, dict) else pd.read_csv(csv_path)

        print(f"Dataset shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")

        # Prepare features
        X, y = self.prepare_features(df, fit_encoders=True)

        print(f"Feature matrix shape: {X.shape}")
        print(f"Target shape: {y.shape}")

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )

        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Train model
        print(f"\nTraining {self.model_type} model...")

        if self.model_type == 'random_forest':
            self.model = RandomForestRegressor(
                n_estimators=200,
                max_depth=20,
                min_samples_split=5,
                min_samples_leaf=2,
                max_features='sqrt',
                n_jobs=-1,
                random_state=random_state,
                verbose=1
            )
        elif self.model_type == 'gradient_boosting':
            self.model = GradientBoostingRegressor(
                n_estimators=200,
                max_depth=7,
                learning_rate=0.1,
                subsample=0.8,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=random_state,
                verbose=1
            )

        self.model.fit(X_train_scaled, y_train)

        # Evaluate
        train_pred = self.model.predict(X_train_scaled)
        test_pred = self.model.predict(X_test_scaled)

        train_mae = mean_absolute_error(y_train, train_pred)
        test_mae = mean_absolute_error(y_test, test_pred)

        train_rmse = np.sqrt(mean_squared_error(y_train, train_pred))
        test_rmse = np.sqrt(mean_squared_error(y_test, test_pred))

        train_r2 = r2_score(y_train, train_pred)
        test_r2 = r2_score(y_test, test_pred)

        self.is_trained = True

        # Store metrics
        metrics = {
            'train_mae': train_mae,
            'test_mae': test_mae,
            'train_rmse': train_rmse,
            'test_rmse': test_rmse,
            'train_r2': train_r2,
            'test_r2': test_r2,
            'n_train': len(X_train),
            'n_test': len(X_test),
            'n_features': X.shape[1]
        }

        self.training_history = metrics

        print(f"\n{'='*60}")
        print(f"Training Complete!")
        print(f"{'='*60}")
        print(f"Train MAE: {train_mae:.2f} | Test MAE: {test_mae:.2f}")
        print(f"Train RMSE: {train_rmse:.2f} | Test RMSE: {test_rmse:.2f}")
        print(f"Train R²: {train_r2:.3f} | Test R²: {test_r2:.3f}")
        print(f"{'='*60}\n")

        # Feature importance
        if hasattr(self.model, 'feature_importances_'):
            feature_importance = pd.DataFrame({
                'feature': self.feature_names,
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=False)

            print("Top 10 Most Important Features:")
            print(feature_importance.head(10).to_string(index=False))
            print()

            metrics['feature_importance'] = feature_importance.to_dict()

        return metrics

    def predict(self, features_df):
        """
        Predict crowd levels for given features

        Args:
            features_df: DataFrame with same format as training data

        Returns:
            predictions: Array of predicted crowd counts/occupancy rates
        """
        if not self.is_trained:
            raise ValueError("Model has not been trained yet!")

        X, _ = self.prepare_features(features_df, fit_encoders=False)
        X_scaled = self.scaler.transform(X)

        predictions = self.model.predict(X_scaled)

        # Ensure predictions are non-negative
        predictions = np.maximum(predictions, 0)

        return predictions

    def predict_future(self, location_id, location_type, capacity, hours_ahead=6):
        """
        Predict crowd levels for future time points

        Args:
            location_id: Location identifier
            location_type: Type of location
            capacity: Location capacity
            hours_ahead: Number of hours to predict ahead

        Returns:
            DataFrame with predictions
        """
        if not self.is_trained:
            raise ValueError("Model has not been trained yet!")

        # Create future timestamps
        current_time = datetime.now()
        future_times = [current_time + timedelta(hours=i) for i in range(1, hours_ahead + 1)]

        # Build feature dataframe
        future_data = []
        for ts in future_times:
            future_data.append({
                'timestamp': ts,
                'location_id': location_id,
                'location_type': location_type,
                'capacity': capacity,
                'hour': ts.hour,
                'day_of_week': ts.weekday(),
                'is_weekend': int(ts.weekday() >= 5),
                'is_exam_period': 0,  # Default
                'is_holiday': 0,  # Default
                'weather_condition': 'clear',  # Default
                'temperature': 75  # Default Florida temp
            })

        future_df = pd.DataFrame(future_data)
        predictions = self.predict(future_df)

        future_df['predicted_crowd'] = predictions.astype(int)
        future_df['predicted_occupancy'] = (predictions / capacity * 100).round(2)

        return future_df[['timestamp', 'predicted_crowd', 'predicted_occupancy']]

    def save(self, filepath):
        """Save trained model to file"""
        if not self.is_trained:
            raise ValueError("Cannot save untrained model!")

        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'location_encoder': self.location_encoder,
            'weather_encoder': self.weather_encoder,
            'feature_names': self.feature_names,
            'model_type': self.model_type,
            'training_history': self.training_history,
            'zone_id_map': getattr(self, 'zone_id_map', {})
        }

        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)

        print(f"Model saved to {filepath}")

    def load(self, filepath):
        """Load trained model from file"""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)

        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.location_encoder = model_data['location_encoder']
        self.weather_encoder = model_data['weather_encoder']
        self.feature_names = model_data['feature_names']
        self.model_type = model_data['model_type']
        self.training_history = model_data.get('training_history', {})
        self.zone_id_map = model_data.get('zone_id_map', {})
        self.is_trained = True

        print(f"Model loaded from {filepath}")
        print(f"Model type: {self.model_type}")
        print(f"Training metrics: Test MAE={self.training_history.get('test_mae', 'N/A'):.2f}, "
              f"Test R²={self.training_history.get('test_r2', 'N/A'):.3f}")


if __name__ == "__main__":
    # Train and save the model
    print("="*60)
    print("ML Crowd Prediction Model - Training")
    print("="*60)

    # Initialize predictor
    predictor = MLCrowdPredictor(model_type='random_forest')

    # Train on generated data
    data_path = "../data/crowd_training_data_5000.csv"
    metrics = predictor.train(data_path, test_size=0.2)

    # Save model
    model_path = "crowd_predictor_model.pkl"
    predictor.save(model_path)

    print(f"\n✓ Model training complete!")
    print(f"✓ Model saved to {model_path}")
