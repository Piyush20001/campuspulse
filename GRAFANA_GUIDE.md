# 📊 Grafana Monitoring Guide for Campus Pulse

Complete guide to set up and use Grafana dashboards for real-time monitoring.

## 🚀 Quick Start (All-in-One)

### Option 1: Automated Startup Script

```bash
cd /home/user/campuspulse
./start_with_monitoring.sh
```

This will start:
- ✅ Prometheus (metrics collection)
- ✅ Grafana (visualization)
- ✅ Metrics Server (exposes app metrics)
- ✅ Campus Pulse App (Streamlit)

### Option 2: Manual Setup

**Step 1: Start Monitoring Stack**
```bash
cd /home/user/campuspulse/monitoring
docker-compose -f docker-compose.monitoring.yml up -d
```

**Step 2: Start Metrics Server**
```bash
cd /home/user/campuspulse/streamlit_app
pip install flask prometheus-client
python metrics_server.py &
```

**Step 3: Start Streamlit App**
```bash
streamlit run app.py
```

---

## 🌐 Accessing Services

Once started, open these URLs:

| Service | URL | Login |
|---------|-----|-------|
| **Grafana Dashboard** | http://localhost:3000 | admin/admin |
| **Campus Pulse App** | http://localhost:8501 | - |
| **Prometheus** | http://localhost:9090 | - |
| **Metrics Endpoint** | http://localhost:8000/metrics | - |

---

## 📊 Using Grafana

### First Time Setup

1. **Open Grafana**: http://localhost:3000
2. **Login**:
   - Username: `admin`
   - Password: `admin`
   - Change password when prompted (or skip)

3. **Access Dashboard**:
   - Click **Dashboards** (left sidebar)
   - Select **Campus Pulse - Real-Time Monitoring**

   Or directly: http://localhost:3000/d/campus-pulse

### Dashboard Overview

The dashboard has **15 panels** organized in sections:

#### 📈 Top Row - Key Metrics (4 Panels)
- **Active Users**: Current users on platform
- **Total Events**: Upcoming events count
- **Average Crowd Level**: Campus-wide occupancy gauge (0-100%)
- **Locations Monitored**: Number of tracked locations

#### 📊 Activity Charts (2 Panels)
- **Page Views**: Real-time page traffic (last 5 minutes)
- **Model Predictions Rate**: ML prediction frequency

#### 🏢 Crowd & Events (2 Panels)
- **Top 10 Busiest Locations**: Horizontal bar chart
- **Event Classifications**: Pie chart by category (Academic, Social, Sports, Cultural)

#### ⚡ Performance (2 Panels)
- **Model Prediction Latency**: 95th percentile response times
- **Error Rate**: Application errors over time (with alerts)

#### 👥 User & Database (2 Panels)
- **User Activity**: Signups and logins timeline
- **Database Query Performance**: p50 and p95 query latencies

#### 🔍 Advanced Metrics (3 Panels)
- **Anomalies Detected**: Count in last hour
- **Cache Hit Rate**: Percentage gauge
- **Crowd Level Heatmap**: By location type

---

## 🎯 Understanding the Metrics

### What Each Metric Means

**Active Users**
- Shows current number of users using the app
- Updates in real-time as users navigate

**Total Events**
- Count of all upcoming campus events
- Changes when events are created/deleted

**Average Crowd Level**
- Mean occupancy across all locations
- **Green** (0-60%): Normal
- **Yellow** (60-80%): Busy
- **Orange** (80-90%): Very Busy
- **Red** (90-100%): Critical

**Page Views**
- Shows which pages are most popular
- Useful for understanding user behavior

**Top 10 Busiest Locations**
- Real-time ranking of crowded spots
- Color-coded by occupancy percentage

**Model Latency**
- Time it takes for ML predictions
- Lower is better (< 100ms is excellent)

**Error Rate**
- Application errors per second
- Should be near zero in normal operation

**Cache Hit Rate**
- Percentage of requests served from cache
- Higher is better (> 80% is good)

---

## 🔔 Alerts & Notifications

### Pre-Configured Alerts

The system monitors and alerts for:

| Alert | Threshold | Action |
|-------|-----------|--------|
| High Error Rate | > 0.1 errors/sec for 2min | Investigate logs |
| High Model Latency | p95 > 1 second for 5min | Check model server |
| Critical Crowd Level | > 95% for 10min | Notify campus security |
| Location Over Capacity | > 100% for 5min | Send alert |
| Slow DB Queries | p95 > 0.5s for 5min | Optimize queries |
| Application Down | 1 minute downtime | Immediate restart |

### Viewing Alerts

1. In Grafana, go to **Alerting** → **Alert Rules**
2. See all active alerts and their status
3. Click any alert to see details and history

---

## 🛠️ Customizing the Dashboard

### Add a New Panel

1. Click **Add** → **Visualization**
2. Select **Prometheus** as data source
3. Enter a PromQL query (examples below)
4. Choose visualization type (graph, gauge, stat, etc.)
5. Click **Apply**

### Example PromQL Queries

**Total page views in last hour:**
```promql
sum(increase(campus_pulse_page_views_total[1h]))
```

**Average crowd by location type:**
```promql
avg by (location_type) (campus_pulse_location_crowd_level)
```

**Model success rate:**
```promql
sum(rate(campus_pulse_model_predictions_total[5m])) -
sum(rate(campus_pulse_model_errors_total[5m]))
```

**Top 5 busiest locations:**
```promql
topk(5, campus_pulse_location_crowd_level)
```

**Database queries per second:**
```promql
sum(rate(campus_pulse_db_queries_total[5m]))
```

---

## 📱 Mobile Access

### Grafana Mobile App

1. Download **Grafana** app (iOS/Android)
2. Add server: `http://YOUR_IP:3000`
3. Login with credentials
4. View dashboards on mobile

### Remote Access Setup

For production, set up HTTPS:

```nginx
server {
    listen 443 ssl;
    server_name monitoring.campuspulse.uf.edu;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🐛 Troubleshooting

### Grafana shows "No Data"

**Check 1: Is Prometheus running?**
```bash
curl http://localhost:9090/-/healthy
```

**Check 2: Is metrics endpoint working?**
```bash
curl http://localhost:8000/metrics
```

**Check 3: Is Prometheus scraping the app?**
- Go to http://localhost:9090/targets
- Check if `campus-pulse-metrics` target is UP

**Check 4: Time range**
- In Grafana, check time range selector (top right)
- Try "Last 5 minutes" or "Last 1 hour"

### Prometheus not scraping

Edit `monitoring/prometheus.yml`:
```yaml
scrape_configs:
  - job_name: 'campus-pulse-metrics'
    static_configs:
      - targets: ['localhost:8000']  # Change to your IP if needed
```

Restart Prometheus:
```bash
cd monitoring
docker-compose -f docker-compose.monitoring.yml restart prometheus
```

### Metrics server won't start

Install dependencies:
```bash
pip install flask prometheus-client
```

Check if port 8000 is available:
```bash
lsof -i :8000
```

### Dashboard not appearing

1. Go to **Configuration** → **Data Sources**
2. Click **Prometheus**
3. Test connection (should be green)
4. If failed, check URL: `http://prometheus:9090`

---

## 📈 Advanced Features

### Creating Custom Dashboards

1. Click **+ → Dashboard**
2. Click **Add new panel**
3. Configure query and visualization
4. Save dashboard with a name

### Exporting Data

**Export to CSV:**
- Click any panel → **Inspect** → **Data** → **Download CSV**

**Export Dashboard:**
- Dashboard settings → **JSON Model** → Copy

### Setting Up Alerts

1. Edit a panel → **Alert** tab
2. Create alert rule with conditions
3. Choose notification channel
4. Save

**Example Alert:**
```
WHEN last() OF query(A, 5m, now)
IS ABOVE 0.9
FOR 5m
```

---

## 🔒 Security Best Practices

### Change Default Passwords

```bash
# Edit docker-compose.monitoring.yml
environment:
  - GF_SECURITY_ADMIN_PASSWORD=your_strong_password
```

### Enable HTTPS

Use reverse proxy (nginx/Traefik) with SSL certificates

### Restrict Access

Add authentication to Prometheus:
```yaml
basic_auth_users:
  admin: $2y$10$... # bcrypt hash
```

---

## 📚 Additional Resources

- [Grafana Documentation](https://grafana.com/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [PromQL Tutorial](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Grafana Dashboard Best Practices](https://grafana.com/docs/grafana/latest/best-practices/)

---

## 🛑 Stopping Services

**Stop monitoring stack:**
```bash
cd monitoring
docker-compose -f docker-compose.monitoring.yml down
```

**Stop metrics server:**
```bash
pkill -f metrics_server.py
```

**Stop Streamlit:**
```bash
pkill -f streamlit
```

**Stop everything:**
```bash
# Kill processes
pkill -f metrics_server.py
pkill -f streamlit

# Stop Docker containers
cd monitoring
docker-compose -f docker-compose.monitoring.yml down
```

---

## ✅ Health Check

To verify everything is working:

```bash
# Check Grafana
curl http://localhost:3000/api/health

# Check Prometheus
curl http://localhost:9090/-/healthy

# Check Metrics
curl http://localhost:8000/metrics | head -20

# Check Campus Pulse
curl http://localhost:8501
```

All should return HTTP 200 OK.

---

**Need Help?**
- Check logs: `docker logs campus-pulse-grafana`
- Check Prometheus targets: http://localhost:9090/targets
- Check metrics endpoint: http://localhost:8000/metrics
