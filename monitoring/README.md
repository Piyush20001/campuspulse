# Campus Pulse - Prometheus & Grafana Monitoring

Complete monitoring stack for Campus Pulse with Prometheus metrics collection and Grafana dashboards.

## 📊 Features

### Prometheus Metrics Collected

- **Application Metrics**:
  - Page views by page name
  - API requests with status codes
  - Active users count
  - Error rates by component

- **Crowd Monitoring Metrics**:
  - Average crowd level across campus
  - Per-location crowd levels
  - Location capacities
  - Anomaly detections

- **ML Model Metrics**:
  - Prediction counts by model type
  - Prediction latency histograms
  - Model error rates
  - Event classification confidence

- **Database Metrics**:
  - Query counts by type
  - Query duration histograms
  - Connection pool stats

- **User Activity Metrics**:
  - User signups and logins
  - Events created
  - Locations saved

- **Performance Metrics**:
  - Page load times
  - Cache hit/miss rates
  - Response times

### Grafana Dashboards

Pre-configured dashboard with 15+ panels:
- Active users and events stats
- Real-time crowd level gauge
- Page views timeline
- Top 10 busiest locations bar chart
- Event classification pie chart
- Model latency graphs
- Error rate monitoring with alerts
- Database performance metrics
- Anomaly detection stats
- Cache performance

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

1. **Start the monitoring stack**:
   ```bash
   cd monitoring
   docker-compose -f docker-compose.monitoring.yml up -d
   ```

2. **Access the services**:
   - Grafana: http://localhost:3000 (admin/admin)
   - Prometheus: http://localhost:9090
   - Alertmanager: http://localhost:9093

3. **View the dashboard**:
   - Navigate to Dashboards → Campus Pulse - Real-Time Monitoring

### Option 2: Manual Setup

1. **Install Prometheus**:
   ```bash
   # Download and extract Prometheus
   wget https://github.com/prometheus/prometheus/releases/latest/download/prometheus-*.tar.gz
   tar xvfz prometheus-*.tar.gz
   cd prometheus-*

   # Copy config
   cp ../prometheus.yml .
   cp ../alert_rules.yml .

   # Start Prometheus
   ./prometheus --config.file=prometheus.yml
   ```

2. **Install Grafana**:
   ```bash
   # Add Grafana repository (Ubuntu/Debian)
   sudo apt-get install -y software-properties-common
   sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
   wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
   sudo apt-get update
   sudo apt-get install grafana

   # Start Grafana
   sudo systemctl start grafana-server
   ```

3. **Configure Grafana**:
   - Add Prometheus datasource (http://localhost:9090)
   - Import dashboard from `grafana_dashboard.json`

## 🔧 Integration with Campus Pulse

### 1. Add Metrics to Your Streamlit App

```python
# In your main app.py or page files
from monitoring.prometheus_metrics import MetricsCollector

# Record page views
MetricsCollector.record_page_view("Home")

# Update location metrics
crowds_data = st.session_state.simulator.get_all_current_crowds()
MetricsCollector.update_location_metrics(crowds_data)

# Record model predictions
MetricsCollector.record_model_prediction('random_forest', duration=0.05)

# Record event classifications
MetricsCollector.record_event_classification('Academic', confidence=0.92)
```

### 2. Expose Metrics Endpoint

Create a separate metrics server or add endpoint to your app:

```python
# metrics_server.py
from flask import Flask, Response
from monitoring.prometheus_metrics import get_metrics

app = Flask(__name__)

@app.route('/metrics')
def metrics():
    return Response(get_metrics(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

Run alongside Streamlit:
```bash
python metrics_server.py &
streamlit run app.py
```

### 3. Docker Compose Integration

Add to your main `docker-compose.yml`:

```yaml
services:
  app:
    # ... your app config
    ports:
      - "8501:8501"
      - "8000:8000"  # Metrics endpoint
    networks:
      - app_network
      - monitoring

networks:
  monitoring:
    external: true
    name: monitoring_monitoring
```

## 📈 Dashboard Panels Explained

### Panel 1-4: Key Metrics
- **Active Users**: Current active users on the platform
- **Total Events**: Number of upcoming events
- **Average Crowd Level**: Campus-wide crowd percentage (gauge)
- **Locations Monitored**: Number of locations being tracked

### Panel 5-6: Activity Trends
- **Page Views**: Real-time page views rate by page
- **Model Predictions**: ML model prediction rate

### Panel 7-8: Crowd & Events
- **Top 10 Busiest Locations**: Bar chart of highest crowd levels
- **Event Classifications**: Pie chart of event categories

### Panel 9-10: Performance & Errors
- **Model Latency**: 95th percentile prediction times
- **Error Rate**: Application errors with alerting

### Panel 11-12: User & Database
- **User Activity**: Signups and logins over time
- **Database Performance**: Query latency percentiles

### Panel 13-15: Advanced Metrics
- **Anomalies Detected**: Count of crowd anomalies
- **Cache Hit Rate**: Percentage of cache hits
- **Crowd Heatmap**: Average crowd by location type

## 🚨 Alerts Configuration

Pre-configured alerts in `alert_rules.yml`:

- **HighErrorRate**: Triggers when error rate > 0.1/sec for 2 minutes
- **HighModelLatency**: Triggers when p95 latency > 1 second for 5 minutes
- **CriticalCrowdLevel**: Triggers when average crowd > 95% for 10 minutes
- **LocationOverCapacity**: Triggers when any location > 100% for 5 minutes
- **SlowDatabaseQueries**: Triggers when p95 query time > 0.5s for 5 minutes
- **ApplicationDown**: Triggers immediately when app is unreachable
- **LowCacheHitRate**: Triggers when cache hit rate < 50% for 10 minutes
- **AnomalySpikeDetected**: Triggers when > 5 anomalies in 10 minutes
- **HighModelErrorRate**: Triggers when model error rate > 0.05/sec

## 🔍 Querying Metrics

### Useful PromQL Queries

```promql
# Average crowd level across all locations
avg(campus_pulse_location_crowd_level)

# Top 5 busiest locations right now
topk(5, campus_pulse_location_crowd_level)

# Page view rate in last hour
rate(campus_pulse_page_views_total[1h])

# Model prediction success rate
sum(rate(campus_pulse_model_predictions_total[5m])) -
sum(rate(campus_pulse_model_errors_total[5m]))

# 99th percentile model latency
histogram_quantile(0.99, rate(campus_pulse_model_prediction_latency_seconds_bucket[5m]))

# Database query rate by type
sum by (query_type) (rate(campus_pulse_db_queries_total[5m]))
```

## 📱 Mobile & Remote Access

### Grafana Mobile App
- Download Grafana mobile app (iOS/Android)
- Add server: http://your-server-ip:3000
- Login and view dashboards on the go

### Secure Remote Access
Set up reverse proxy with SSL:

```nginx
# nginx.conf
server {
    listen 443 ssl;
    server_name monitoring.campuspulse.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
    }
}
```

## 🛠️ Troubleshooting

### Prometheus Not Scraping Metrics
- Check if metrics endpoint is accessible: `curl http://localhost:8000/metrics`
- Verify target status in Prometheus: http://localhost:9090/targets
- Check prometheus.yml configuration

### Grafana Dashboard Not Showing Data
- Verify Prometheus datasource connection in Grafana settings
- Check time range selector (top right)
- Ensure metrics are being generated by the app

### High Memory Usage
- Reduce Prometheus retention period:
  ```bash
  --storage.tsdb.retention.time=7d
  ```
- Decrease scrape frequency in prometheus.yml

## 📊 Performance Recommendations

- **Scrape Interval**: 10-15s for application metrics
- **Evaluation Interval**: 15s for alert rules
- **Retention Period**: 15-30 days for production
- **Dashboard Refresh**: 10s for real-time monitoring
- **Alert Buffer**: 2-5 minutes to avoid false positives

## 🔐 Security Best Practices

1. **Change Default Passwords**:
   - Grafana: admin/admin → strong password
   - Update in docker-compose environment variables

2. **Enable Authentication**:
   - Prometheus: Use `--web.enable-admin-api=false` for production
   - Grafana: Enable OAuth or LDAP

3. **Network Isolation**:
   - Use Docker networks to isolate monitoring stack
   - Expose only necessary ports

4. **HTTPS**:
   - Use reverse proxy (nginx/Traefik) with SSL certificates
   - Enable HTTPS in Grafana settings

## 📚 Additional Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [PromQL Basics](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Grafana Dashboard Best Practices](https://grafana.com/docs/grafana/latest/best-practices/best-practices-for-creating-dashboards/)

## 🤝 Support

For issues or questions:
- Check Prometheus logs: `docker logs campus-pulse-prometheus`
- Check Grafana logs: `docker logs campus-pulse-grafana`
- Review metrics endpoint output: `curl http://localhost:8000/metrics`

---

**Campus Pulse Monitoring Stack** - Real-time observability for campus intelligence
