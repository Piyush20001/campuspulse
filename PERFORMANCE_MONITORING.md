# Performance Monitoring System

## Overview

Campus Pulse now includes a comprehensive performance monitoring system that tracks:
- **Response Times**: How long endpoints take to respond
- **API Latency**: Time taken for API operations and data retrievals
- **Page Load Times**: How fast pages load for users
- **Model Inference Times**: LSTM and AI model prediction performance
- **Database Query Performance**: SQL execution times

This satisfies your professor's requirement for tracking additional metrics beyond user feedback.

## What's Being Tracked

### 1. Response Times
- Tracks: All major endpoints (Home, Heatmap, Events, Profile, Admin Panel)
- Metrics: Average, Median, P95, P99 percentiles
- Stores: Endpoint name, response time, user email, timestamp, status

### 2. API Latency
- Tracks: Data retrieval operations (get_all_current_crowds, etc.)
- Metrics: Average latency, min/max latency per operation
- Stores: Operation name, latency in ms, metadata

### 3. Page Load Times
- Tracks: How long each page takes to fully load
- Metrics: Average load time per page
- Stores: Page name, load time, user email

### 4. Model Inference
- Tracks: LSTM crowd forecasting, Event classification
- Metrics: Average inference time, predictions per second
- Stores: Model name, inference time, number of predictions

### 5. Database Queries
- Tracks: All database operations
- Metrics: Execution time, rows affected
- Stores: Query type, execution time, row count

## How to Access

### For Admins:
1. Login as admin (use Admin Login tab)
2. Navigate to **Performance Metrics** page from the sidebar
3. View real-time performance dashboards

### Dashboard Features:
- **Time Range Selector**: Last Hour, 6 Hours, 24 Hours, 7 Days
- **Interactive Charts**: Plotly visualizations of trends
- **Detailed Tables**: Per-endpoint, per-operation breakdowns
- **Statistics**: Avg, Median, P95, P99 percentiles

## Data Storage

All metrics are stored in SQLite database: `campus_pulse_performance.db`

### Tables:
- `response_times`: Endpoint response times
- `api_latency`: API call latencies
- `page_loads`: Page load times
- `model_inference`: ML model inference times
- `db_queries`: Database query execution times

### Data Retention:
- Metrics are automatically cleaned up after **7 days**
- Prevents database bloat
- Keeps only relevant recent data

## Integration

The performance tracker is integrated throughout the application:

### In app.py:
```python
# Track page load
metrics_tracker.record_page_load("Home", load_time_ms, user_email)

# Track API latency
metrics_tracker.record_api_latency("get_all_current_crowds", latency_ms)
```

### Usage Pattern:
```python
# Context manager for automatic tracking
with metrics_tracker.track_response_time("endpoint_name"):
    # Your code here
    process_data()
```

## For Your Professor

This implementation provides:

1. **Response Time Tracking**: Monitors how fast the application responds to user requests
2. **Latency Measurements**: Tracks backend operation performance
3. **System Performance Insights**: Identifies bottlenecks
4. **Historical Analysis**: View trends over time
5. **Percentile Statistics**: P95/P99 for SLA monitoring

### Key Metrics Explained:

- **P95 (95th Percentile)**: 95% of requests complete faster than this time
- **P99 (99th Percentile)**: 99% of requests complete faster than this time
- **Median**: Middle value, less affected by outliers than average
- **Average**: Mean response time across all requests

## Benefits

1. **Performance Optimization**: Identify slow endpoints
2. **User Experience**: Monitor and improve page load times
3. **Model Performance**: Track AI/ML inference speeds
4. **Database Optimization**: Find slow queries
5. **SLA Monitoring**: Ensure app meets performance targets

## Future Enhancements

- Export metrics to Prometheus/Grafana
- Set up automated alerts for slow performance
- Add confidence score tracking for ML models
- Track user session duration
- Monitor error rates and retry logic
