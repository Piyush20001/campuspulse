"""
Autoencoder-based anomaly detector for crowd patterns
"""
import torch
import torch.nn as nn
import numpy as np
from sklearn.preprocessing import StandardScaler
import os

class Autoencoder(nn.Module):
    def __init__(self, input_size=12, encoding_dim=4):
        super(Autoencoder, self).__init__()

        # Encoder
        self.encoder = nn.Sequential(
            nn.Linear(input_size, 8),
            nn.ReLU(),
            nn.Linear(8, encoding_dim),
            nn.ReLU()
        )

        # Decoder
        self.decoder = nn.Sequential(
            nn.Linear(encoding_dim, 8),
            nn.ReLU(),
            nn.Linear(8, input_size),
            nn.Sigmoid()
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded


class AnomalyDetector:
    def __init__(self, model_path=None, window_size=12, threshold=0.15):
        """
        Initialize anomaly detector
        Args:
            model_path: Path to saved model (optional)
            window_size: Size of the time window to analyze
            threshold: Reconstruction error threshold for anomaly
        """
        self.window_size = window_size
        self.threshold = threshold
        self.model = Autoencoder(input_size=window_size, encoding_dim=4)
        self.scaler = StandardScaler()
        self.is_trained = False

        if model_path and os.path.exists(model_path):
            self.load_model(model_path)

    def prepare_windows(self, data):
        """Prepare sliding windows from time series data"""
        windows = []
        for i in range(len(data) - self.window_size + 1):
            window = data[i:i + self.window_size]
            windows.append(window)
        return np.array(windows)

    def train(self, historical_data, epochs=100, lr=0.001):
        """
        Train the autoencoder on normal baseline data
        Args:
            historical_data: DataFrame with 'crowd_level' column (normal patterns only)
            epochs: Number of training epochs
            lr: Learning rate
        """
        # Extract crowd levels
        crowd_levels = historical_data['crowd_level'].values

        # Create windows
        windows = self.prepare_windows(crowd_levels)

        if len(windows) == 0:
            print("Not enough data to train")
            return

        # Normalize
        windows_scaled = self.scaler.fit_transform(windows)

        # Convert to tensor
        X_tensor = torch.FloatTensor(windows_scaled)

        # Training setup
        criterion = nn.MSELoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)

        # Training loop
        self.model.train()
        for epoch in range(epochs):
            optimizer.zero_grad()
            reconstructed = self.model(X_tensor)
            loss = criterion(reconstructed, X_tensor)
            loss.backward()
            optimizer.step()

            if (epoch + 1) % 20 == 0:
                print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')

        self.is_trained = True
        print("Anomaly detector training completed!")

    def detect(self, recent_data):
        """
        Detect if recent pattern is anomalous
        Args:
            recent_data: List or array of recent crowd levels (at least window_size points)
        Returns:
            Dictionary with is_anomaly, reconstruction_error, and confidence
        """
        if not self.is_trained:
            # If not trained, use simple threshold-based detection
            return self._simple_detect(recent_data)

        self.model.eval()

        # Ensure we have enough data
        if len(recent_data) < self.window_size:
            # Pad with median value if needed
            median_val = np.median(recent_data) if len(recent_data) > 0 else 0.5
            padding = [median_val] * (self.window_size - len(recent_data))
            recent_data = padding + list(recent_data)

        # Take last window
        window = recent_data[-self.window_size:]
        window_array = np.array(window).reshape(1, -1)

        # Normalize
        window_scaled = self.scaler.transform(window_array)

        # Convert to tensor
        X = torch.FloatTensor(window_scaled)

        # Reconstruct
        with torch.no_grad():
            reconstructed = self.model(X)

        # Calculate reconstruction error
        error = nn.MSELoss()(reconstructed, X).item()

        # Determine if anomalous
        is_anomaly = error > self.threshold

        # Calculate confidence (how far from threshold)
        if is_anomaly:
            confidence = min((error - self.threshold) / self.threshold, 1.0)
        else:
            confidence = 1.0 - (error / self.threshold)

        return {
            'is_anomaly': is_anomaly,
            'reconstruction_error': error,
            'threshold': self.threshold,
            'confidence': confidence,
            'severity': self._get_severity(error)
        }

    def _simple_detect(self, recent_data):
        """Simple rule-based anomaly detection as fallback"""
        if len(recent_data) < 2:
            return {
                'is_anomaly': False,
                'reconstruction_error': 0.0,
                'threshold': self.threshold,
                'confidence': 0.5,
                'severity': 'normal'
            }

        # Check for sudden spikes or drops
        recent_array = np.array(recent_data)
        mean = np.mean(recent_array)
        std = np.std(recent_array)

        # Calculate z-score for last value
        if std > 0:
            z_score = abs((recent_array[-1] - mean) / std)
            is_anomaly = z_score > 2.5  # 2.5 standard deviations
        else:
            is_anomaly = False
            z_score = 0

        error = z_score / 10  # Normalize to similar scale

        return {
            'is_anomaly': is_anomaly,
            'reconstruction_error': error,
            'threshold': self.threshold,
            'confidence': min(z_score / 2.5, 1.0) if is_anomaly else 0.5,
            'severity': self._get_severity(error)
        }

    def _get_severity(self, error):
        """Determine severity level based on error"""
        if error > self.threshold * 3:
            return 'critical'
        elif error > self.threshold * 2:
            return 'high'
        elif error > self.threshold:
            return 'medium'
        else:
            return 'normal'

    def get_anomaly_explanation(self, recent_data, location_name):
        """Generate human-readable explanation of anomaly"""
        result = self.detect(recent_data)

        if not result['is_anomaly']:
            return "Normal crowd pattern detected."

        # Analyze pattern
        recent_array = np.array(recent_data[-self.window_size:])
        mean_level = np.mean(recent_array)
        trend = "increasing" if recent_array[-1] > recent_array[0] else "decreasing"

        severity_emoji = {
            'medium': '⚠️',
            'high': '🚨',
            'critical': '🔴'
        }

        emoji = severity_emoji.get(result['severity'], '⚠️')

        if mean_level > 0.7:
            pattern_type = "unusually high crowd levels"
        elif mean_level < 0.3:
            pattern_type = "unusually low crowd levels"
        else:
            pattern_type = f"unusual {trend} pattern"

        explanation = f"{emoji} Anomaly detected at {location_name}: {pattern_type}. "
        explanation += f"Confidence: {result['confidence']*100:.0f}%"

        return explanation

    def save_model(self, path):
        """Save model and scaler"""
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'scaler': self.scaler,
            'window_size': self.window_size,
            'threshold': self.threshold
        }, path)
        print(f"Anomaly detector saved to {path}")

    def load_model(self, path):
        """Load model and scaler"""
        checkpoint = torch.load(path, map_location=torch.device('cpu'))
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.scaler = checkpoint['scaler']
        self.window_size = checkpoint['window_size']
        self.threshold = checkpoint['threshold']
        self.is_trained = True
        print(f"Anomaly detector loaded from {path}")
