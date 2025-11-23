"""
LSTM-based time series forecaster for crowd prediction
"""
import torch
import torch.nn as nn
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import os

class LSTMForecaster(nn.Module):
    def __init__(self, input_size=1, hidden_size=64, num_layers=2, output_size=6, dropout=0.2):
        super(LSTMForecaster, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            dropout=dropout,
            batch_first=True
        )

        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        # x shape: (batch_size, sequence_length, input_size)
        lstm_out, _ = self.lstm(x)
        # Take the last output
        last_output = lstm_out[:, -1, :]
        predictions = self.fc(last_output)
        return predictions


class CrowdForecaster:
    def __init__(self, model_path=None, sequence_length=12):
        """
        Initialize crowd forecaster
        Args:
            model_path: Path to saved model (optional)
            sequence_length: Number of past time steps to use (default: 12 = 2 hours)
        """
        self.sequence_length = sequence_length
        self.forecast_steps = 6  # Predict next 6 steps (1 hour)
        self.model = LSTMForecaster(
            input_size=1,
            hidden_size=64,
            num_layers=2,
            output_size=self.forecast_steps
        )
        self.scaler = MinMaxScaler()
        self.is_trained = False

        if model_path and os.path.exists(model_path):
            self.load_model(model_path)

    def prepare_sequences(self, data):
        """Prepare sequences for training"""
        X, y = [], []

        for i in range(len(data) - self.sequence_length - self.forecast_steps + 1):
            X.append(data[i:i + self.sequence_length])
            y.append(data[i + self.sequence_length:i + self.sequence_length + self.forecast_steps])

        return np.array(X), np.array(y)

    def train(self, historical_data, epochs=50, lr=0.001):
        """
        Train the LSTM model
        Args:
            historical_data: DataFrame with 'crowd_level' column
            epochs: Number of training epochs
            lr: Learning rate
        """
        # Extract crowd levels
        crowd_levels = historical_data['crowd_level'].values.reshape(-1, 1)

        # Normalize data
        scaled_data = self.scaler.fit_transform(crowd_levels)

        # Prepare sequences
        X, y = self.prepare_sequences(scaled_data)

        if len(X) == 0:
            print("Not enough data to train")
            return

        # Convert to tensors
        X_tensor = torch.FloatTensor(X)
        y_tensor = torch.FloatTensor(y)

        # Training setup
        criterion = nn.MSELoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)

        # Training loop
        self.model.train()
        for epoch in range(epochs):
            optimizer.zero_grad()
            outputs = self.model(X_tensor)
            loss = criterion(outputs, y_tensor.squeeze(-1))
            loss.backward()
            optimizer.step()

            if (epoch + 1) % 10 == 0:
                print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')

        self.is_trained = True
        print("Training completed!")

    def predict(self, recent_data):
        """
        Predict future crowd levels
        Args:
            recent_data: List or array of recent crowd levels (at least sequence_length points)
        Returns:
            Array of predicted crowd levels for next forecast_steps
        """
        if not self.is_trained:
            # If not trained, return simple persistence forecast
            return self._persistence_forecast(recent_data)

        self.model.eval()

        # Ensure we have enough data
        if len(recent_data) < self.sequence_length:
            # Pad with zeros if needed
            padding = [0.5] * (self.sequence_length - len(recent_data))
            recent_data = padding + list(recent_data)

        # Take last sequence_length points
        recent_data = recent_data[-self.sequence_length:]

        # Normalize
        recent_array = np.array(recent_data).reshape(-1, 1)
        scaled_data = self.scaler.transform(recent_array)

        # Prepare input
        X = torch.FloatTensor(scaled_data).unsqueeze(0)  # Add batch dimension

        # Predict
        with torch.no_grad():
            predictions = self.model(X)

        # Denormalize
        predictions_array = predictions.numpy().reshape(-1, 1)
        predictions_denorm = self.scaler.inverse_transform(predictions_array)

        # Clip to valid range
        predictions_denorm = np.clip(predictions_denorm, 0, 1)

        return predictions_denorm.flatten()

    def _persistence_forecast(self, recent_data):
        """Simple persistence forecast (use last value)"""
        if len(recent_data) == 0:
            return np.array([0.5] * self.forecast_steps)

        last_value = recent_data[-1]
        # Add slight random variation
        predictions = []
        current = last_value
        for _ in range(self.forecast_steps):
            variation = np.random.normal(0, 0.05)
            current = np.clip(current + variation, 0, 1)
            predictions.append(current)

        return np.array(predictions)

    def save_model(self, path):
        """Save model and scaler"""
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'scaler': self.scaler,
            'sequence_length': self.sequence_length,
            'forecast_steps': self.forecast_steps
        }, path)
        print(f"Model saved to {path}")

    def load_model(self, path):
        """Load model and scaler"""
        # Use weights_only=False to load sklearn scaler (safe for self-trained models)
        checkpoint = torch.load(path, map_location=torch.device('cpu'), weights_only=False)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.scaler = checkpoint['scaler']
        self.sequence_length = checkpoint['sequence_length']
        self.forecast_steps = checkpoint['forecast_steps']
        self.is_trained = True
        print(f"Model loaded from {path}")

    def get_forecast_label(self, predicted_level):
        """Convert predicted level to label"""
        avg_prediction = np.mean(predicted_level)

        if avg_prediction < 0.3:
            return "Light", "🟢"
        elif avg_prediction < 0.6:
            return "Normal", "🟡"
        elif avg_prediction < 0.85:
            return "Busy", "🟠"
        else:
            return "Very Busy", "🔴"
