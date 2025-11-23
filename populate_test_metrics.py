"""
Test script to populate performance metrics with sample data
Run this to see the performance dashboard populate with data
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from monitoring.performance_metrics import get_metrics_tracker
import random
import time

def populate_test_metrics():
    """Populate performance metrics with test data"""
    print("Populating performance metrics with test data...")

    metrics_tracker = get_metrics_tracker()

    # Generate sample response times for different endpoints
    endpoints = ['home_page', 'crowd_heatmap', 'events_page', 'profile_page', 'admin_panel']

    print("\n1. Adding response time data...")
    for endpoint in endpoints:
        for _ in range(20):
            # Random response times between 50ms and 500ms
            response_time = random.uniform(50, 500)
            metrics_tracker.record_response_time(endpoint, response_time, None, "success")

    print("   ✓ Added 100 response time records")

    # Generate sample API latency data
    print("\n2. Adding API latency data...")
    operations = ['get_all_current_crowds', 'count_upcoming_events', 'fetch_user_data', 'query_locations']

    for operation in operations:
        for _ in range(15):
            # Random latency between 10ms and 200ms
            latency = random.uniform(10, 200)
            metrics_tracker.record_api_latency(operation, latency)

    print("   ✓ Added 60 API latency records")

    # Generate sample page load data
    print("\n3. Adding page load data...")
    pages = ['Home', 'Crowd Heatmap', 'Events', 'Profile', 'Admin Panel']

    for page in pages:
        for _ in range(10):
            # Random load times between 100ms and 1000ms
            load_time = random.uniform(100, 1000)
            metrics_tracker.record_page_load(page, load_time)

    print("   ✓ Added 50 page load records")

    # Generate sample model inference data
    print("\n4. Adding model inference data...")
    models = ['LSTM_Forecaster', 'Event_Classifier', 'Anomaly_Detector']

    for model in models:
        for _ in range(10):
            # Random inference times between 20ms and 300ms
            inference_time = random.uniform(20, 300)
            num_predictions = random.randint(1, 10)
            metrics_tracker.record_model_inference(model, inference_time, num_predictions)

    print("   ✓ Added 30 model inference records")

    # Generate sample database query data
    print("\n5. Adding database query data...")
    query_types = ['SELECT_users', 'INSERT_feedback', 'UPDATE_roles', 'SELECT_events']

    for query_type in query_types:
        for _ in range(15):
            # Random execution times between 5ms and 150ms
            exec_time = random.uniform(5, 150)
            rows_affected = random.randint(1, 100)
            metrics_tracker.record_db_query(query_type, exec_time, rows_affected)

    print("   ✓ Added 60 database query records")

    print("\n✅ Successfully populated performance metrics!")
    print("📊 You can now view the metrics in the Admin Panel > Performance Metrics tab")
    print("\nTotal records added:")
    print(f"  - Response Times: 100")
    print(f"  - API Latency: 60")
    print(f"  - Page Loads: 50")
    print(f"  - Model Inference: 30")
    print(f"  - Database Queries: 60")
    print(f"\n  TOTAL: 300 metric records")

if __name__ == "__main__":
    populate_test_metrics()
