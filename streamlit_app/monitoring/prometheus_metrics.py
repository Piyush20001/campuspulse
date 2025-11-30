"""
Prometheus Metrics Collection for Campus Pulse
Exports application metrics for monitoring and alerting
"""
from prometheus_client import Counter, Gauge, Histogram, Summary, Info, generate_latest, REGISTRY
import time
from functools import wraps
from datetime import datetime


# Application Info
app_info = Info('campus_pulse_app', 'Campus Pulse Application Info')
app_info.info({
    'version': '2.0',
    'environment': 'production',
    'university': 'University of Florida'
})

# Request Counters
page_views = Counter(
    'campus_pulse_page_views_total',
    'Total page views by page',
    ['page_name']
)

api_requests = Counter(
    'campus_pulse_api_requests_total',
    'Total API requests',
    ['endpoint', 'method', 'status']
)

errors_total = Counter(
    'campus_pulse_errors_total',
    'Total errors by type',
    ['error_type', 'component']
)

# Gauges for Current State
active_users = Gauge(
    'campus_pulse_active_users',
    'Number of currently active users'
)

locations_monitored = Gauge(
    'campus_pulse_locations_monitored',
    'Number of locations being monitored'
)

avg_crowd_level = Gauge(
    'campus_pulse_avg_crowd_level_percent',
    'Average crowd level across all locations'
)

total_events = Gauge(
    'campus_pulse_total_events',
    'Total number of upcoming events'
)

# Per-location Metrics
location_crowd_level = Gauge(
    'campus_pulse_location_crowd_level',
    'Current crowd level at specific location',
    ['location_id', 'location_name', 'location_type']
)

location_capacity = Gauge(
    'campus_pulse_location_capacity',
    'Capacity of specific location',
    ['location_id', 'location_name']
)

# Model Metrics
model_predictions = Counter(
    'campus_pulse_model_predictions_total',
    'Total number of crowd predictions made',
    ['model_type']
)

model_latency = Histogram(
    'campus_pulse_model_prediction_latency_seconds',
    'Time taken for model predictions',
    ['model_type'],
    buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0]
)

model_error_rate = Counter(
    'campus_pulse_model_errors_total',
    'Total model prediction errors',
    ['model_type', 'error_type']
)

# Event Classification Metrics
event_classifications = Counter(
    'campus_pulse_event_classifications_total',
    'Total event classifications by category',
    ['category']
)

event_classification_confidence = Histogram(
    'campus_pulse_event_classification_confidence',
    'Confidence scores for event classifications',
    buckets=[0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99, 1.0]
)

# User Activity Metrics
user_events_created = Counter(
    'campus_pulse_user_events_created_total',
    'Total events created by users'
)

user_locations_saved = Counter(
    'campus_pulse_user_locations_saved_total',
    'Total locations saved by users'
)

user_signups = Counter(
    'campus_pulse_user_signups_total',
    'Total user sign-ups'
)

user_logins = Counter(
    'campus_pulse_user_logins_total',
    'Total user logins'
)

# Database Metrics
db_queries = Counter(
    'campus_pulse_db_queries_total',
    'Total database queries',
    ['query_type', 'table']
)

db_query_duration = Histogram(
    'campus_pulse_db_query_duration_seconds',
    'Database query duration',
    ['query_type'],
    buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0]
)

# Anomaly Detection Metrics
anomalies_detected = Counter(
    'campus_pulse_anomalies_detected_total',
    'Total crowd anomalies detected',
    ['location_type', 'anomaly_type']
)

# Response Time Metrics
page_load_time = Summary(
    'campus_pulse_page_load_seconds',
    'Page load time',
    ['page_name']
)

# Cache Metrics
cache_hits = Counter(
    'campus_pulse_cache_hits_total',
    'Total cache hits',
    ['cache_type']
)

cache_misses = Counter(
    'campus_pulse_cache_misses_total',
    'Total cache misses',
    ['cache_type']
)


class MetricsCollector:
    """Helper class to collect and update metrics"""

    @staticmethod
    def record_page_view(page_name):
        """Record a page view"""
        page_views.labels(page_name=page_name).inc()

    @staticmethod
    def record_api_request(endpoint, method, status):
        """Record an API request"""
        api_requests.labels(endpoint=endpoint, method=method, status=status).inc()

    @staticmethod
    def record_error(error_type, component):
        """Record an error"""
        errors_total.labels(error_type=error_type, component=component).inc()

    @staticmethod
    def update_active_users(count):
        """Update active users count"""
        active_users.set(count)

    @staticmethod
    def update_location_metrics(crowds_data):
        """
        Update location-specific metrics

        Args:
            crowds_data: List of dicts with keys: location_id, location_name, location_type, headcount, capacity, percentage
        """
        if not crowds_data:
            return

        # Update individual location metrics
        for crowd in crowds_data:
            location_crowd_level.labels(
                location_id=crowd['location_id'],
                location_name=crowd['location_name'],
                location_type=crowd.get('location_type', 'unknown')
            ).set(crowd['percentage'])

            location_capacity.labels(
                location_id=crowd['location_id'],
                location_name=crowd['location_name']
            ).set(crowd['capacity'])

        # Update average crowd level
        avg_crowd = sum(c['percentage'] for c in crowds_data) / len(crowds_data)
        avg_crowd_level.set(avg_crowd)

        # Update monitored locations count
        locations_monitored.set(len(crowds_data))

    @staticmethod
    def record_model_prediction(model_type, duration=None):
        """Record a model prediction"""
        model_predictions.labels(model_type=model_type).inc()
        if duration is not None:
            model_latency.labels(model_type=model_type).observe(duration)

    @staticmethod
    def record_model_error(model_type, error_type):
        """Record a model error"""
        model_error_rate.labels(model_type=model_type, error_type=error_type).inc()

    @staticmethod
    def record_event_classification(category, confidence):
        """Record an event classification"""
        event_classifications.labels(category=category).inc()
        event_classification_confidence.observe(confidence)

    @staticmethod
    def record_user_action(action_type):
        """Record user actions"""
        if action_type == 'event_created':
            user_events_created.inc()
        elif action_type == 'location_saved':
            user_locations_saved.inc()
        elif action_type == 'signup':
            user_signups.inc()
        elif action_type == 'login':
            user_logins.inc()

    @staticmethod
    def record_db_query(query_type, table, duration=None):
        """Record a database query"""
        db_queries.labels(query_type=query_type, table=table).inc()
        if duration is not None:
            db_query_duration.labels(query_type=query_type).observe(duration)

    @staticmethod
    def record_anomaly(location_type, anomaly_type):
        """Record an anomaly detection"""
        anomalies_detected.labels(location_type=location_type, anomaly_type=anomaly_type).inc()

    @staticmethod
    def update_events_count(count):
        """Update total events count"""
        total_events.set(count)


def track_execution_time(metric_func):
    """
    Decorator to track execution time of functions

    Usage:
        @track_execution_time(lambda duration: model_latency.labels(model_type='lstm').observe(duration))
        def my_function():
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                metric_func(duration)
                return result
            except Exception as e:
                duration = time.time() - start_time
                metric_func(duration)
                raise e
        return wrapper
    return decorator


def get_metrics():
    """Get current metrics in Prometheus format"""
    return generate_latest(REGISTRY)


# Example usage
if __name__ == "__main__":
    print("Prometheus Metrics Example")
    print("=" * 60)

    # Simulate some metrics
    MetricsCollector.record_page_view("Home")
    MetricsCollector.record_page_view("Events")
    MetricsCollector.record_page_view("Home")

    MetricsCollector.update_active_users(15)
    MetricsCollector.update_events_count(42)

    # Simulate location metrics
    crowds = [
        {'location_id': 1, 'location_name': 'Library West', 'location_type': 'LIBRARIES',
         'headcount': 120, 'capacity': 150, 'percentage': 80},
        {'location_id': 2, 'location_name': 'SW Rec', 'location_type': 'GYMS',
         'headcount': 150, 'capacity': 180, 'percentage': 83},
    ]
    MetricsCollector.update_location_metrics(crowds)

    # Simulate model prediction
    MetricsCollector.record_model_prediction('random_forest', duration=0.05)
    MetricsCollector.record_event_classification('Academic', confidence=0.92)

    # Print metrics
    print("\nGenerated Metrics:")
    print("-" * 60)
    metrics_output = get_metrics().decode('utf-8')
    print(metrics_output[:1000])  # Print first 1000 chars
    print("\n... (truncated)")
    print("\n✓ Metrics collection working!")
