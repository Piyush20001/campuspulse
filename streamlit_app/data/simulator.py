"""
Data simulator for generating realistic crowd levels and historical data
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from data.locations import UF_LOCATIONS

class CrowdDataSimulator:
    def __init__(self, seed=42):
        np.random.seed(seed)
        self.locations = UF_LOCATIONS
        self.base_patterns = self._generate_base_patterns()

    def _generate_base_patterns(self):
        """Generate base daily patterns for each location category"""
        patterns = {
            'LIBRARIES': self._library_pattern(),
            'GYMS': self._gym_pattern(),
            'DINING': self._dining_pattern(),
            'ACADEMIC': self._academic_pattern(),
            'HOUSING': self._housing_pattern(),
            'STUDY SPOTS': self._study_pattern(),
            'OUTDOORS': self._outdoor_pattern()
        }
        return patterns

    def _library_pattern(self):
        """Library crowd pattern (busy during study hours)"""
        hours = np.arange(24)
        pattern = np.zeros(24)
        pattern[8:12] = 0.5  # Morning moderate
        pattern[12:14] = 0.4  # Lunch dip
        pattern[14:22] = 0.8  # Afternoon/evening peak
        pattern[22:24] = 0.3  # Late night
        return pattern

    def _gym_pattern(self):
        """Gym crowd pattern (peaks morning and evening)"""
        hours = np.arange(24)
        pattern = np.zeros(24)
        pattern[6:9] = 0.7  # Morning rush
        pattern[9:16] = 0.4  # Midday moderate
        pattern[16:21] = 0.9  # Evening peak
        pattern[21:23] = 0.5  # Late evening
        return pattern

    def _dining_pattern(self):
        """Dining hall pattern (peaks at meal times)"""
        pattern = np.zeros(24)
        pattern[7:9] = 0.8  # Breakfast
        pattern[11:14] = 0.95  # Lunch peak
        pattern[17:20] = 0.9  # Dinner
        pattern[20:22] = 0.3  # Late snacks
        return pattern

    def _academic_pattern(self):
        """Academic building pattern (busy during class hours)"""
        pattern = np.zeros(24)
        pattern[8:12] = 0.8  # Morning classes
        pattern[12:13] = 0.5  # Lunch
        pattern[13:17] = 0.85  # Afternoon classes
        pattern[17:20] = 0.4  # Evening classes
        return pattern

    def _housing_pattern(self):
        """Housing pattern (inverse of academic)"""
        pattern = np.zeros(24)
        pattern[0:8] = 0.9  # Night/early morning
        pattern[12:14] = 0.6  # Lunch break
        pattern[17:19] = 0.7  # After class
        pattern[22:24] = 0.95  # Night
        return pattern

    def _study_pattern(self):
        """Study spot pattern (similar to libraries but more evening heavy)"""
        pattern = np.zeros(24)
        pattern[10:14] = 0.6  # Late morning
        pattern[14:18] = 0.7  # Afternoon
        pattern[18:24] = 0.9  # Evening/night peak
        return pattern

    def _outdoor_pattern(self):
        """Outdoor area pattern (weather and daylight dependent)"""
        pattern = np.zeros(24)
        pattern[10:13] = 0.6  # Late morning
        pattern[13:17] = 0.7  # Afternoon
        pattern[17:19] = 0.5  # Early evening
        return pattern

    def get_current_crowd(self, location):
        """Get current crowd level for a location"""
        current_hour = datetime.now().hour
        current_minute = datetime.now().minute

        # Get base pattern for this location's category
        base_pattern = self.base_patterns.get(location['category'], np.zeros(24))

        # Interpolate between hours
        hour_value = base_pattern[current_hour]
        next_hour = (current_hour + 1) % 24
        next_hour_value = base_pattern[next_hour]
        interpolated = hour_value + (next_hour_value - hour_value) * (current_minute / 60)

        # Add random noise
        noise = np.random.normal(0, 0.05)
        crowd_level = np.clip(interpolated + noise, 0, 1)

        # Scale to location capacity
        headcount = int(crowd_level * location['capacity'])

        return {
            'location_id': location['id'],
            'location_name': location['name'],
            'headcount': headcount,
            'capacity': location['capacity'],
            'crowd_level': crowd_level,
            'percentage': int(crowd_level * 100),
            'timestamp': datetime.now()
        }

    def get_all_current_crowds(self):
        """Get current crowd levels for all locations"""
        return [self.get_current_crowd(loc) for loc in self.locations]

    def generate_historical_data(self, location, days=7, interval_minutes=10):
        """Generate historical crowd data for a location"""
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)

        # Generate timestamps
        timestamps = []
        current = start_time
        while current <= end_time:
            timestamps.append(current)
            current += timedelta(minutes=interval_minutes)

        # Generate crowd levels
        data = []
        base_pattern = self.base_patterns.get(location['category'], np.zeros(24))

        for ts in timestamps:
            hour = ts.hour
            minute = ts.minute

            # Interpolate
            hour_value = base_pattern[hour]
            next_hour = (hour + 1) % 24
            next_hour_value = base_pattern[next_hour]
            interpolated = hour_value + (next_hour_value - hour_value) * (minute / 60)

            # Add noise and day-of-week variation
            day_factor = 1.0
            if ts.weekday() >= 5:  # Weekend
                if location['category'] in ['ACADEMIC', 'LIBRARIES']:
                    day_factor = 0.6
                elif location['category'] in ['GYMS', 'DINING', 'OUTDOORS']:
                    day_factor = 1.2

            noise = np.random.normal(0, 0.05)
            crowd_level = np.clip((interpolated * day_factor) + noise, 0, 1)
            headcount = int(crowd_level * location['capacity'])

            data.append({
                'timestamp': ts,
                'headcount': headcount,
                'crowd_level': crowd_level,
                'capacity': location['capacity']
            })

        return pd.DataFrame(data)

    def inject_anomaly(self, location, probability=0.05):
        """Randomly inject an anomaly into current crowd data"""
        if np.random.random() < probability:
            # Create spike or drop
            anomaly_type = np.random.choice(['spike', 'drop'])
            normal_crowd = self.get_current_crowd(location)

            if anomaly_type == 'spike':
                factor = np.random.uniform(1.5, 2.5)
            else:
                factor = np.random.uniform(0.2, 0.5)

            anomalous_headcount = int(normal_crowd['headcount'] * factor)
            anomalous_headcount = np.clip(anomalous_headcount, 0, location['capacity'])

            normal_crowd['headcount'] = anomalous_headcount
            normal_crowd['crowd_level'] = anomalous_headcount / location['capacity']
            normal_crowd['percentage'] = int(normal_crowd['crowd_level'] * 100)
            normal_crowd['is_anomaly'] = True

            return normal_crowd
        else:
            crowd = self.get_current_crowd(location)
            crowd['is_anomaly'] = False
            return crowd
