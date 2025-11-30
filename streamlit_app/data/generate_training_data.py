"""
Generate 5000-row training dataset for crowd prediction model
Based on realistic UF campus patterns
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_crowd_training_data(num_rows=5000):
    """
    Generate realistic crowd training data based on campus patterns

    Features:
    - timestamp: datetime of observation
    - location_id: campus location identifier
    - location_type: category (LIBRARIES, GYMS, DINING, ACADEMIC, etc.)
    - hour: hour of day (0-23)
    - day_of_week: day (0=Monday, 6=Sunday)
    - is_weekend: boolean
    - is_exam_period: boolean
    - is_holiday: boolean
    - weather_condition: clear/rain/cloudy
    - temperature: temperature in Fahrenheit
    - crowd_count: number of people (target variable)
    - occupancy_rate: percentage full (target variable)
    """

    # Location types with typical capacities
    location_types = {
        'LIBRARIES': {'capacity': 150, 'locations': 5},
        'GYMS': {'capacity': 180, 'locations': 3},
        'DINING': {'capacity': 160, 'locations': 4},
        'ACADEMIC': {'capacity': 200, 'locations': 8},
        'HOUSING': {'capacity': 300, 'locations': 6},
        'STUDY SPOTS': {'capacity': 120, 'locations': 4},
        'OUTDOORS': {'capacity': 100, 'locations': 3}
    }

    # Time patterns for each location type (hourly base occupancy 0-1)
    patterns = {
        'LIBRARIES': {
            'morning': (8, 12, 0.5),    # hours, mean occupancy
            'afternoon': (14, 22, 0.8),
            'night': (22, 24, 0.3)
        },
        'GYMS': {
            'morning': (6, 9, 0.7),
            'midday': (12, 16, 0.4),
            'evening': (16, 21, 0.9)
        },
        'DINING': {
            'breakfast': (7, 9, 0.8),
            'lunch': (11, 14, 0.95),
            'dinner': (17, 20, 0.9)
        },
        'ACADEMIC': {
            'class_hours': (8, 17, 0.8),
            'evening': (17, 20, 0.4)
        },
        'HOUSING': {
            'night': (22, 8, 0.9),
            'midday': (12, 14, 0.6)
        },
        'STUDY SPOTS': {
            'afternoon': (14, 18, 0.7),
            'evening': (18, 24, 0.9)
        },
        'OUTDOORS': {
            'afternoon': (13, 17, 0.7)
        }
    }

    data = []

    # Start date: 90 days ago
    start_date = datetime.now() - timedelta(days=90)

    for i in range(num_rows):
        # Random timestamp within past 90 days
        days_offset = random.randint(0, 90)
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        timestamp = start_date + timedelta(days=days_offset, hours=hour, minutes=minute)

        # Random location
        location_type = random.choice(list(location_types.keys()))
        num_locations = location_types[location_type]['locations']
        location_id = random.randint(1, num_locations)
        capacity = location_types[location_type]['capacity']

        # Time features
        day_of_week = timestamp.weekday()  # 0=Monday, 6=Sunday
        is_weekend = day_of_week >= 5

        # Academic calendar features
        # Exam periods: mid-December, early May, finals weeks
        month = timestamp.month
        is_exam_period = (month == 12 and timestamp.day > 10) or (month == 5 and timestamp.day < 15)

        # Holidays and breaks
        is_holiday = (month == 11 and 20 < timestamp.day < 30) or \
                     (month == 12 and 15 < timestamp.day) or \
                     (month == 1 and timestamp.day < 10) or \
                     (month == 3 and 10 < timestamp.day < 20)  # Spring break

        # Weather (Florida climate)
        weather_options = ['clear', 'clear', 'clear', 'cloudy', 'rain']  # More sunny days
        weather_condition = random.choice(weather_options)

        # Temperature (Florida range)
        if month in [12, 1, 2]:  # Winter
            temperature = np.random.normal(65, 10)
        elif month in [6, 7, 8]:  # Summer
            temperature = np.random.normal(88, 5)
        else:  # Spring/Fall
            temperature = np.random.normal(75, 8)

        temperature = np.clip(temperature, 45, 98)

        # Calculate base crowd level based on time patterns
        base_occupancy = 0.1  # Baseline

        # Apply time pattern for this location type
        if location_type == 'LIBRARIES':
            if 8 <= hour < 12:
                base_occupancy = np.random.normal(0.5, 0.1)
            elif 14 <= hour < 22:
                base_occupancy = np.random.normal(0.8, 0.1)
            elif 22 <= hour < 24:
                base_occupancy = np.random.normal(0.3, 0.1)

        elif location_type == 'GYMS':
            if 6 <= hour < 9:
                base_occupancy = np.random.normal(0.7, 0.15)
            elif 16 <= hour < 21:
                base_occupancy = np.random.normal(0.9, 0.1)
            else:
                base_occupancy = np.random.normal(0.4, 0.1)

        elif location_type == 'DINING':
            if 7 <= hour < 9:
                base_occupancy = np.random.normal(0.8, 0.1)
            elif 11 <= hour < 14:
                base_occupancy = np.random.normal(0.95, 0.05)
            elif 17 <= hour < 20:
                base_occupancy = np.random.normal(0.9, 0.1)
            else:
                base_occupancy = np.random.normal(0.2, 0.1)

        elif location_type == 'ACADEMIC':
            if 8 <= hour < 17:
                base_occupancy = np.random.normal(0.8, 0.1)
            elif 17 <= hour < 20:
                base_occupancy = np.random.normal(0.4, 0.1)
            else:
                base_occupancy = np.random.normal(0.1, 0.05)

        elif location_type == 'HOUSING':
            if 22 <= hour or hour < 8:
                base_occupancy = np.random.normal(0.9, 0.05)
            elif 12 <= hour < 14:
                base_occupancy = np.random.normal(0.6, 0.1)
            else:
                base_occupancy = np.random.normal(0.3, 0.1)

        elif location_type == 'STUDY SPOTS':
            if 14 <= hour < 18:
                base_occupancy = np.random.normal(0.7, 0.1)
            elif 18 <= hour < 24:
                base_occupancy = np.random.normal(0.9, 0.1)
            else:
                base_occupancy = np.random.normal(0.3, 0.1)

        elif location_type == 'OUTDOORS':
            if 13 <= hour < 17:
                base_occupancy = np.random.normal(0.7, 0.15)
            else:
                base_occupancy = np.random.normal(0.2, 0.1)

        # Adjust for day of week
        if is_weekend:
            if location_type in ['ACADEMIC', 'LIBRARIES']:
                base_occupancy *= 0.6  # Less busy on weekends
            elif location_type in ['GYMS', 'DINING', 'OUTDOORS']:
                base_occupancy *= 1.2  # More busy on weekends

        # Adjust for exam period
        if is_exam_period and location_type in ['LIBRARIES', 'STUDY SPOTS']:
            base_occupancy *= 1.3  # Much busier during exams

        # Adjust for holidays
        if is_holiday:
            base_occupancy *= 0.3  # Much quieter during breaks

        # Adjust for weather (mainly affects outdoor spaces)
        if weather_condition == 'rain' and location_type == 'OUTDOORS':
            base_occupancy *= 0.3
        elif weather_condition == 'rain' and location_type in ['LIBRARIES', 'STUDY SPOTS']:
            base_occupancy *= 1.2  # People stay indoors

        # Add random noise
        occupancy_rate = np.clip(base_occupancy + np.random.normal(0, 0.05), 0, 1)

        # Calculate crowd count
        crowd_count = int(occupancy_rate * capacity)

        # Create data point
        data.append({
            'timestamp': timestamp,
            'location_id': location_id,
            'location_type': location_type,
            'capacity': capacity,
            'hour': hour,
            'day_of_week': day_of_week,
            'is_weekend': int(is_weekend),
            'is_exam_period': int(is_exam_period),
            'is_holiday': int(is_holiday),
            'weather_condition': weather_condition,
            'temperature': round(temperature, 1),
            'crowd_count': crowd_count,
            'occupancy_rate': round(occupancy_rate * 100, 2)
        })

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Sort by timestamp
    df = df.sort_values('timestamp').reset_index(drop=True)

    return df


if __name__ == "__main__":
    print("Generating 5000-row crowd training dataset...")
    df = generate_crowd_training_data(5000)

    # Save to CSV
    output_path = "crowd_training_data_5000.csv"
    df.to_csv(output_path, index=False)

    print(f"✓ Dataset saved to {output_path}")
    print(f"\nDataset Info:")
    print(f"- Total rows: {len(df)}")
    print(f"- Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    print(f"- Location types: {df['location_type'].nunique()}")
    print(f"\nSample statistics:")
    print(df[['crowd_count', 'occupancy_rate', 'temperature']].describe())
    print(f"\nFirst 5 rows:")
    print(df.head())
