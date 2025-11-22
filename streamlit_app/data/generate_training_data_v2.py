"""
Generate 5000-row training dataset based on REAL data.csv observations
Uses actual UF campus facilities, sub-areas, and observed patterns
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Real facility data extracted from data.csv
FACILITIES = {
    'Southwest Rec Center': {
        'zones': [
            ('Maguire Field', 'Z-SWRC-01', 100),
            ('SWRC Weight Room', 'Z-SWRC-02', 200),
            ('SWRC Cardio Room 1', 'Z-SWRC-03', 60),
            ('SWRC Cardio Room 2', 'Z-SWRC-04', 50),
            ('Multi-Purpose Court 1', 'Z-SWRC-05', 30),
            ('Multi-Purpose Court 2', 'Z-SWRC-06', 30),
            ('Multi-Purpose Court 3', 'Z-SWRC-07', 30),
            ('Multi-Purpose Court 4', 'Z-SWRC-08', 30),
            ('Multi-Purpose Court 5', 'Z-SWRC-09', 30),
            ('Multi-Purpose Court 6', 'Z-SWRC-10', 30),
            ('SWRC Tennis Courts', 'Z-SWRC-11', 40),
            ('UVS Sand Volleyball', 'Z-SWRC-12', 20),
        ],
        'category': 'GYMS',
        'typical_hours': (6, 23)  # Open 6 AM - 11 PM
    },
    'Student Recreation and Fitness Centre': {
        'zones': [
            ('SRFC Squash', 'Z-SRFC-01', 8),
            ('SRFC Table Tennis', 'Z-SRFC-02', 12),
            ('SRFC Weight Room', 'Z-SRFC-03', 80),
            ('SRFC Cardio Room', 'Z-SRFC-04', 50),
            ('SRFC Lower Functional Area', 'Z-SRFC-05', 30),
            ('SRFC Multi-purpose Court', 'Z-SRFC-06', 40),
            ('SRFC Racquetball', 'Z-SRFC-07', 20),
        ],
        'category': 'GYMS',
        'typical_hours': (6, 23)
    },
    'Smathers Libraries': {
        'zones': [
            ('Library West', 'Z-SL-01', 1564),
            ('Marston Science Library', 'Z-SL-02', 2208),
            ('Health Science Center Library', 'Z-SL-03', 761),
            ('Architecture and Fine Arts Library', 'Z-SL-04', 124),
            ('Education Library', 'Z-SL-05', 560),
            ('Smathers Library', 'Z-SL-06', 231),
        ],
        'category': 'LIBRARIES',
        'typical_hours': (7, 24)  # Open 7 AM - midnight
    },
    'Aquatics': {
        'zones': [
            ('Florida Pool', 'Z-AQ-01', 50),
            ('O\'Connell Center Pool', 'Z-AQ-02', 40),
        ],
        'category': 'AQUATICS',
        'typical_hours': (6, 22)
    },
    'Lake Wauberg': {
        'zones': [
            ('LW North', 'LW', 100),
        ],
        'category': 'OUTDOORS',
        'typical_hours': (8, 20)
    },
}

def generate_realistic_crowd_data(num_rows=5000):
    """
    Generate realistic crowd training data based on actual UF observations
    """

    data = []

    # Start date: 90 days ago
    start_date = datetime.now() - timedelta(days=90)

    # Create time series data
    for i in range(num_rows):
        # Random date within past 90 days
        days_offset = random.randint(0, 90)

        # Random time (weighted towards business hours)
        hour_weights = [0.1] * 6 + [0.5] * 4 + [1.0] * 8 + [0.8] * 4 + [0.3] * 2  # 24 hours
        hour = int(np.random.choice(range(24), p=np.array(hour_weights) / sum(hour_weights)))
        minute = int(np.random.choice([0, 15, 30, 45]))  # Quarter hours

        timestamp = start_date + timedelta(days=days_offset, hours=hour, minutes=minute)

        # Random facility
        facility_name = random.choice(list(FACILITIES.keys()))
        facility = FACILITIES[facility_name]

        # Random zone within facility
        sub_area, zone_id, capacity = random.choice(facility['zones'])
        category = facility['category']

        # Time features
        day_of_week = timestamp.weekday()  # 0=Monday, 6=Sunday
        is_weekend = day_of_week >= 5
        month = timestamp.month

        # Academic calendar features
        is_exam_period = (month == 12 and timestamp.day > 10) or (month == 5 and timestamp.day < 15)
        is_holiday = (month == 11 and 20 < timestamp.day < 30) or \
                     (month == 12 and 15 < timestamp.day) or \
                     (month == 1 and timestamp.day < 10) or \
                     (month == 3 and 10 < timestamp.day < 20)

        # Weather (Florida)
        weather_options = ['clear', 'clear', 'clear', 'cloudy', 'rain']
        weather_condition = random.choice(weather_options)

        # Temperature
        if month in [12, 1, 2]:
            temperature = np.random.normal(65, 10)
        elif month in [6, 7, 8]:
            temperature = np.random.normal(88, 5)
        else:
            temperature = np.random.normal(75, 8)
        temperature = np.clip(temperature, 45, 98)

        # Generate crowd count based on category and time
        base_occupancy = 0.1

        if category == 'LIBRARIES':
            # Libraries pattern (observed: 0-1286, capacity 124-2208)
            if 8 <= hour < 12:  # Morning
                base_occupancy = np.random.normal(0.15, 0.05)
            elif 12 <= hour < 14:  # Lunch dip
                base_occupancy = np.random.normal(0.12, 0.04)
            elif 14 <= hour < 22:  # Afternoon/evening peak
                base_occupancy = np.random.normal(0.50, 0.15)
            elif 22 <= hour < 24:  # Late night
                base_occupancy = np.random.normal(0.20, 0.10)
            else:  # Early morning
                base_occupancy = np.random.normal(0.05, 0.03)

            # Exam period boost
            if is_exam_period:
                base_occupancy *= 1.5

        elif category == 'GYMS':
            # Gym pattern (observed: 0-173 for weight rooms, lower for courts)
            if 'Weight Room' in sub_area or 'Cardio' in sub_area:
                if 6 <= hour < 9:  # Morning rush
                    base_occupancy = np.random.normal(0.60, 0.15)
                elif 16 <= hour < 21:  # Evening peak
                    base_occupancy = np.random.normal(0.80, 0.12)
                else:
                    base_occupancy = np.random.normal(0.30, 0.15)
            elif 'Court' in sub_area or 'Field' in sub_area:
                if 16 <= hour < 21:  # Evening for sports
                    base_occupancy = np.random.normal(0.50, 0.20)
                else:
                    base_occupancy = np.random.normal(0.15, 0.15)
            else:  # Other gym areas
                base_occupancy = np.random.normal(0.25, 0.15)

        elif category == 'AQUATICS':
            # Pool pattern (observed: 0-13)
            if 12 <= hour < 18:  # Afternoon swimming
                base_occupancy = np.random.normal(0.30, 0.15)
            else:
                base_occupancy = np.random.normal(0.10, 0.10)

        elif category == 'OUTDOORS':
            # Outdoor areas (observed: mostly 0)
            if 13 <= hour < 17 and weather_condition == 'clear':
                base_occupancy = np.random.normal(0.20, 0.15)
            else:
                base_occupancy = np.random.normal(0.05, 0.05)

        # Weekend adjustments
        if is_weekend:
            if category in ['LIBRARIES']:
                base_occupancy *= 0.5  # Less busy
            elif category in ['GYMS', 'AQUATICS', 'OUTDOORS']:
                base_occupancy *= 1.3  # More busy

        # Holiday adjustments
        if is_holiday:
            base_occupancy *= 0.2  # Much quieter

        # Weather adjustments
        if weather_condition == 'rain':
            if category == 'OUTDOORS':
                base_occupancy *= 0.2
            elif category in ['LIBRARIES']:
                base_occupancy *= 1.3  # More people indoors

        # Operating hours check
        open_hour, close_hour = facility['typical_hours']
        if hour < open_hour or hour >= close_hour:
            base_occupancy *= 0.1  # Mostly closed

        # Add noise
        occupancy_rate = np.clip(base_occupancy + np.random.normal(0, 0.05), 0, 1)

        # Calculate crowd count
        crowd_count = int(occupancy_rate * capacity)

        # Add some zero observations (facilities can be empty)
        if random.random() < 0.15:  # 15% chance of being empty/very low
            crowd_count = int(crowd_count * random.uniform(0, 0.2))

        # Create data point
        data.append({
            'timestamp': timestamp,
            'facility': facility_name,
            'sub_area': sub_area,
            'zone_id': zone_id,
            'capacity': capacity,
            'category': category,
            'hour': hour,
            'day_of_week': day_of_week,
            'is_weekend': int(is_weekend),
            'is_exam_period': int(is_exam_period),
            'is_holiday': int(is_holiday),
            'weather_condition': weather_condition,
            'temperature': round(temperature, 1),
            'count_in_area': crowd_count,
            'occupancy_rate': round(occupancy_rate * 100, 2)
        })

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Sort by timestamp
    df = df.sort_values('timestamp').reset_index(drop=True)

    return df


if __name__ == "__main__":
    print("Generating 5000-row crowd dataset from REAL data.csv patterns...")
    df = generate_realistic_crowd_data(5000)

    # Save to CSV
    output_path = "crowd_training_data_5000_v2.csv"
    df.to_csv(output_path, index=False)

    print(f"✓ Dataset saved to {output_path}")
    print(f"\nDataset Info:")
    print(f"- Total rows: {len(df)}")
    print(f"- Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    print(f"- Facilities: {df['facility'].nunique()} ({', '.join(df['facility'].unique())})")
    print(f"- Categories: {', '.join(df['category'].unique())}")
    print(f"- Sub-areas: {df['sub_area'].nunique()}")

    print(f"\nFacility distribution:")
    print(df['facility'].value_counts())

    print(f"\nSample statistics:")
    print(df[['count_in_area', 'occupancy_rate', 'temperature']].describe())

    print(f"\nSample by category:")
    for category in df['category'].unique():
        cat_data = df[df['category'] == category]
        print(f"\n{category}:")
        print(f"  Count range: {cat_data['count_in_area'].min()}-{cat_data['count_in_area'].max()}")
        print(f"  Avg occupancy: {cat_data['occupancy_rate'].mean():.1f}%")

    print(f"\nFirst 10 rows:")
    print(df.head(10).to_string())
