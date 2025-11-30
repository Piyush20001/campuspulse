# 📊 Grafana Monitoring Guide for Campus Pulse

Complete guide to set up and use Grafana dashboards for real-time monitoring.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Step-by-Step Setup](#step-by-step-setup)
4. [Using Grafana](#using-grafana)
5. [Using Prometheus](#using-prometheus)
6. [Docker Management](#docker-management)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Features](#advanced-features)

---

## 🔧 Prerequisites

Before starting, ensure you have:

1. **Docker & Docker Compose** installed
   ```bash
   # Check Docker version
   docker --version
   # Should show: Docker version 20.x or higher

   # Check Docker Compose version
   docker-compose --version
   # Should show: docker-compose version 1.29.x or higher
   ```

2. **Python packages** (will be installed automatically)
   - flask
   - prometheus-client

3. **Ports available**:
   - 3000 (Grafana)
   - 9090 (Prometheus)
   - 8000 (Metrics Server)
   - 8501 (Streamlit App)

4. **Check if Docker is running**:
   ```bash
   docker info
   # If error, start Docker Desktop or run: sudo systemctl start docker
   ```

---

## 🚀 Quick Start

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

## 📖 Step-by-Step Setup

### Complete Setup from Scratch

**Step 1: Navigate to Project Directory**
```bash
cd /home/user/campuspulse
```

**Step 2: Make Startup Script Executable (if needed)**
```bash
chmod +x start_with_monitoring.sh
```

**Step 3: Start Docker Services**
```bash
cd monitoring
docker-compose -f docker-compose.monitoring.yml up -d
```

This command will:
- Download Docker images (first time only): Prometheus, Grafana
- Create containers: `campus-pulse-prometheus`, `campus-pulse-grafana`
- Create network: `monitoring-network`
- Start services in detached mode (`-d` flag)

**Output you should see:**
```
Creating network "monitoring_monitoring-network" with the default driver
Creating campus-pulse-prometheus ... done
Creating campus-pulse-grafana     ... done
```

**Step 4: Verify Containers are Running**
```bash
docker ps
```

You should see:
```
CONTAINER ID   IMAGE              PORTS                    NAMES
abc12345       grafana/grafana    0.0.0.0:3000->3000/tcp   campus-pulse-grafana
def67890       prom/prometheus    0.0.0.0:9090->9090/tcp   campus-pulse-prometheus
```

**Step 5: Install Python Dependencies**
```bash
cd /home/user/campuspulse/streamlit_app
pip install flask prometheus-client
```

**Step 6: Start Metrics Server**
```bash
python metrics_server.py &
```

**Output you should see:**
```
Starting Prometheus Metrics Server...
Metrics available at: http://localhost:8000/metrics
 * Running on http://0.0.0.0:8000
```

**Step 7: Verify Metrics Endpoint**
```bash
curl http://localhost:8000/metrics | head -20
```

You should see Prometheus-formatted metrics:
```
# HELP campus_pulse_page_views_total Total page views by page
# TYPE campus_pulse_page_views_total counter
campus_pulse_page_views_total{page_name="Home"} 0.0
...
```

**Step 8: Start Campus Pulse App**
```bash
streamlit run app.py
```

**Step 9: Access Services**

Open these URLs in your browser:
- **Grafana**: http://localhost:3000 (login: admin/admin)
- **Prometheus**: http://localhost:9090
- **Campus Pulse**: http://localhost:8501
- **Metrics**: http://localhost:8000/metrics

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

## 🔍 Using Prometheus

Prometheus is the metrics collection and time-series database powering your monitoring.

### Accessing Prometheus

Open http://localhost:9090 in your browser.

### Prometheus UI Walkthrough

**1. Status Page**
- Go to **Status** → **Targets**
- Check if `campus-pulse-metrics` target is **UP** (green)
- If DOWN (red), metrics server isn't running or unreachable

**2. Metrics Explorer**
- Go to **Graph** tab
- Click **Metrics Explorer** (🔍 icon) to browse available metrics
- All Campus Pulse metrics start with `campus_pulse_`

**3. Running Queries**

Enter queries in the expression box and click **Execute**.

#### Example Queries to Try:

**See all page views:**
```promql
campus_pulse_page_views_total
```

**Current active users:**
```promql
campus_pulse_active_users
```

**Top 5 busiest locations right now:**
```promql
topk(5, campus_pulse_location_crowd_level)
```

**Average crowd level across all locations:**
```promql
avg(campus_pulse_location_crowd_level)
```

**Total predictions made in last 5 minutes:**
```promql
sum(rate(campus_pulse_model_predictions_total[5m])) * 300
```

**Error rate per second:**
```promql
rate(campus_pulse_errors_total[1m])
```

**Page views per second (last 5 min):**
```promql
rate(campus_pulse_page_views_total[5m])
```

**Crowd level by location type:**
```promql
avg by (location_type) (campus_pulse_location_crowd_level)
```

**95th percentile model latency:**
```promql
histogram_quantile(0.95, campus_pulse_model_prediction_duration_seconds)
```

### Understanding PromQL Time Ranges

- `[5m]` = last 5 minutes
- `[1h]` = last 1 hour
- `[1d]` = last 1 day

### Common PromQL Functions

- `rate()` = per-second rate over time range
- `sum()` = total across all labels
- `avg()` = average across all labels
- `topk(N, ...)` = top N values
- `increase()` = total increase over time range
- `histogram_quantile()` = percentile calculation

### Checking Scrape Status

**Are metrics being collected?**

1. Go to **Status** → **Targets**
2. Look for `campus-pulse-metrics` job
3. Check **State** column:
   - ✅ **UP** = Working perfectly
   - ❌ **DOWN** = Problem (check Last Error column)
4. Check **Last Scrape** time (should be < 15 seconds ago)

**View raw metrics being scraped:**

1. Click on the endpoint URL (http://localhost:8000/metrics)
2. You'll see the raw Prometheus-formatted metrics

---

## 🐳 Docker Management

Complete guide to managing Docker containers for the monitoring stack.

### Checking Docker Status

**View all running containers:**
```bash
docker ps
```

**View all containers (including stopped):**
```bash
docker ps -a
```

**Check container logs:**
```bash
# Grafana logs
docker logs campus-pulse-grafana

# Prometheus logs
docker logs campus-pulse-prometheus

# Follow logs in real-time (-f flag)
docker logs -f campus-pulse-grafana

# Last 50 lines
docker logs --tail 50 campus-pulse-prometheus
```

**Check container resource usage:**
```bash
docker stats

# Press Ctrl+C to stop monitoring
```

### Restarting Containers

**Restart individual container:**
```bash
# Restart Grafana
docker restart campus-pulse-grafana

# Restart Prometheus
docker restart campus-pulse-prometheus
```

**Restart all monitoring containers:**
```bash
cd /home/user/campuspulse/monitoring
docker-compose -f docker-compose.monitoring.yml restart
```

**Restart with logs output:**
```bash
docker-compose -f docker-compose.monitoring.yml restart && docker-compose -f docker-compose.monitoring.yml logs -f
```

### Stopping Containers

**Stop individual container:**
```bash
docker stop campus-pulse-grafana
docker stop campus-pulse-prometheus
```

**Stop all monitoring containers:**
```bash
cd /home/user/campuspulse/monitoring
docker-compose -f docker-compose.monitoring.yml stop
```

**Stop and remove containers:**
```bash
docker-compose -f docker-compose.monitoring.yml down
```

### Starting Containers

**Start stopped containers:**
```bash
docker start campus-pulse-grafana
docker start campus-pulse-prometheus
```

**Start all with docker-compose:**
```bash
cd /home/user/campuspulse/monitoring
docker-compose -f docker-compose.monitoring.yml up -d
```

**Start in foreground (see logs):**
```bash
docker-compose -f docker-compose.monitoring.yml up
# Press Ctrl+C to stop
```

### Complete Docker Reset

**⚠️ WARNING: This will delete ALL monitoring data including:**
- All Grafana dashboards (custom ones)
- All Grafana users and settings
- All Prometheus historical metrics
- Container volumes and networks

**Step 1: Stop and remove containers**
```bash
cd /home/user/campuspulse/monitoring
docker-compose -f docker-compose.monitoring.yml down
```

**Step 2: Remove volumes (deletes all data)**
```bash
docker-compose -f docker-compose.monitoring.yml down -v
```

**Step 3: Remove images (optional - forces re-download)**
```bash
docker rmi grafana/grafana:latest
docker rmi prom/prometheus:latest
```

**Step 4: Clean up dangling resources**
```bash
# Remove unused containers
docker container prune -f

# Remove unused volumes
docker volume prune -f

# Remove unused networks
docker network prune -f

# Remove unused images
docker image prune -a -f
```

**Step 5: Verify clean state**
```bash
docker ps -a
# Should NOT show campus-pulse-grafana or campus-pulse-prometheus

docker volume ls
# Should NOT show monitoring-related volumes

docker images
# Should NOT show grafana or prometheus (if you removed images)
```

**Step 6: Fresh start**
```bash
cd /home/user/campuspulse/monitoring
docker-compose -f docker-compose.monitoring.yml up -d
```

This will:
- Download fresh images
- Create new containers
- Set up clean volumes
- Configure networks from scratch

**Step 7: Wait for services to start**
```bash
# Wait 30 seconds
sleep 30

# Check if services are up
docker ps
curl http://localhost:3000/api/health
curl http://localhost:9090/-/healthy
```

**Step 8: Access Grafana and reconfigure**
1. Go to http://localhost:3000
2. Login with admin/admin
3. Dashboard should be auto-provisioned
4. If not, manually import from `monitoring/grafana_dashboard.json`

### Soft Reset (Keep Data, Refresh Containers)

If you want to restart without losing data:

```bash
cd /home/user/campuspulse/monitoring

# Stop containers
docker-compose -f docker-compose.monitoring.yml stop

# Remove containers (but keep volumes)
docker-compose -f docker-compose.monitoring.yml rm -f

# Recreate and start
docker-compose -f docker-compose.monitoring.yml up -d
```

This preserves:
✅ Grafana dashboards
✅ Grafana settings
✅ Prometheus metrics history

### Nuclear Option (Complete Docker System Reset)

**⚠️ EXTREME WARNING: This removes EVERYTHING from Docker**
- All containers (not just monitoring)
- All volumes (all projects)
- All images
- All networks

**Only use if Docker is completely broken:**

```bash
# Stop all running containers
docker stop $(docker ps -q)

# Remove all containers
docker rm $(docker ps -a -q)

# Remove all volumes
docker volume rm $(docker volume ls -q)

# Remove all images
docker rmi $(docker images -q)

# Remove all networks
docker network rm $(docker network ls -q)

# System-wide prune
docker system prune -a --volumes -f

# Restart Docker
# On Linux:
sudo systemctl restart docker

# On Mac/Windows:
# Restart Docker Desktop from the menu
```

### Docker Troubleshooting

**Container won't start:**
```bash
# Check logs
docker logs campus-pulse-grafana

# Check if port is already in use
lsof -i :3000  # For Grafana
lsof -i :9090  # For Prometheus

# If port is in use, kill the process or change port in docker-compose.yml
```

**Container keeps restarting:**
```bash
# Check logs for errors
docker logs --tail 100 campus-pulse-grafana

# Check resource usage
docker stats

# Inspect container
docker inspect campus-pulse-grafana
```

**Can't connect to container:**
```bash
# Get container IP
docker inspect campus-pulse-grafana | grep IPAddress

# Test network
docker exec campus-pulse-grafana ping prometheus

# Check if service is running inside container
docker exec campus-pulse-grafana ps aux
```

**Volume permission issues:**
```bash
# Check volume ownership
docker volume inspect monitoring_grafana_data

# Fix permissions (Linux only)
sudo chown -R 472:472 /var/lib/docker/volumes/monitoring_grafana_data/_data
```

### Complete Restart Procedure

When things go wrong, follow this sequence:

```bash
# 1. Stop everything
cd /home/user/campuspulse/monitoring
docker-compose -f docker-compose.monitoring.yml down

# Stop Python processes
pkill -f metrics_server.py
pkill -f streamlit

# 2. Clean up
docker-compose -f docker-compose.monitoring.yml down -v

# 3. Wait a moment
sleep 5

# 4. Restart Docker services
docker-compose -f docker-compose.monitoring.yml up -d

# 5. Wait for startup
sleep 30

# 6. Verify
docker ps
curl http://localhost:3000/api/health
curl http://localhost:9090/-/healthy

# 7. Restart Python services
cd /home/user/campuspulse/streamlit_app
python metrics_server.py &
sleep 3
streamlit run app.py
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

## ⚡ Quick Reference

### One-Command Cheatsheet

**Start everything:**
```bash
cd /home/user/campuspulse && ./start_with_monitoring.sh
```

**Stop everything:**
```bash
pkill -f streamlit; pkill -f metrics_server.py; cd /home/user/campuspulse/monitoring && docker-compose -f docker-compose.monitoring.yml down
```

**Restart Docker services:**
```bash
cd /home/user/campuspulse/monitoring && docker-compose -f docker-compose.monitoring.yml restart
```

**View all logs:**
```bash
docker logs -f campus-pulse-grafana
```

**Complete reset (CAUTION - deletes data):**
```bash
cd /home/user/campuspulse/monitoring && docker-compose -f docker-compose.monitoring.yml down -v && docker-compose -f docker-compose.monitoring.yml up -d
```

### Important URLs

| Service | URL | Credentials |
|---------|-----|-------------|
| Grafana | http://localhost:3000 | admin / admin |
| Prometheus | http://localhost:9090 | - |
| Campus Pulse | http://localhost:8501 | - |
| Metrics | http://localhost:8000/metrics | - |
| Prometheus Targets | http://localhost:9090/targets | - |

### Common Tasks

**Check if services are running:**
```bash
docker ps | grep campus-pulse
```

**See real-time metrics:**
```bash
watch -n 2 "curl -s http://localhost:8000/metrics | grep campus_pulse_active_users"
```

**Follow all container logs:**
```bash
cd /home/user/campuspulse/monitoring && docker-compose -f docker-compose.monitoring.yml logs -f
```

**Restart just Grafana:**
```bash
docker restart campus-pulse-grafana
```

**Restart just Prometheus:**
```bash
docker restart campus-pulse-prometheus
```

**Check container health:**
```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

### Troubleshooting Commands

**Service won't start - check what's using the port:**
```bash
lsof -i :3000  # Grafana
lsof -i :9090  # Prometheus
lsof -i :8000  # Metrics
lsof -i :8501  # Streamlit
```

**Kill process on port:**
```bash
# Find PID
lsof -i :3000
# Kill it (replace 12345 with actual PID)
kill -9 12345
```

**Check Docker disk usage:**
```bash
docker system df
```

**Free up Docker disk space:**
```bash
docker system prune -a --volumes
```

**Verify Prometheus is scraping:**
```bash
curl http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | {job: .labels.job, health: .health, lastError: .lastError}'
```

**Test metrics endpoint:**
```bash
curl http://localhost:8000/metrics | grep -E "campus_pulse_(active_users|page_views|location_crowd)"
```

### Grafana Tips

**Import dashboard manually:**
1. Go to http://localhost:3000
2. Click **+** → **Import**
3. Upload `/home/user/campuspulse/monitoring/grafana_dashboard.json`
4. Select Prometheus data source
5. Click **Import**

**Reset Grafana password:**
```bash
docker exec -it campus-pulse-grafana grafana-cli admin reset-admin-password newpassword
```

**Backup Grafana data:**
```bash
docker cp campus-pulse-grafana:/var/lib/grafana ./grafana-backup
```

**Restore Grafana data:**
```bash
docker cp ./grafana-backup/. campus-pulse-grafana:/var/lib/grafana
docker restart campus-pulse-grafana
```

### Prometheus Tips

**Check Prometheus config:**
```bash
docker exec campus-pulse-prometheus cat /etc/prometheus/prometheus.yml
```

**Reload Prometheus config (without restart):**
```bash
curl -X POST http://localhost:9090/-/reload
```

**Check Prometheus storage size:**
```bash
docker exec campus-pulse-prometheus du -sh /prometheus
```

**Delete old Prometheus data:**
```bash
# WARNING: This deletes historical metrics
docker exec campus-pulse-prometheus rm -rf /prometheus/*
docker restart campus-pulse-prometheus
```

### Environment Variables

**Check Grafana environment:**
```bash
docker exec campus-pulse-grafana env | grep GF_
```

**Check Prometheus environment:**
```bash
docker exec campus-pulse-prometheus env | grep PROMETHEUS
```

### Performance Tuning

**Increase Prometheus retention:**

Edit `monitoring/prometheus.yml`:
```yaml
command:
  - '--storage.tsdb.retention.time=30d'  # Keep metrics for 30 days
```

Then restart:
```bash
cd /home/user/campuspulse/monitoring
docker-compose -f docker-compose.monitoring.yml restart prometheus
```

**Limit Grafana memory:**

Edit `monitoring/docker-compose.monitoring.yml`:
```yaml
services:
  grafana:
    mem_limit: 512m
```

---

**Need Help?**
- Check logs: `docker logs campus-pulse-grafana`
- Check Prometheus targets: http://localhost:9090/targets
- Check metrics endpoint: http://localhost:8000/metrics
- Check Docker status: `docker ps -a`
- View this guide: `/home/user/campuspulse/GRAFANA_GUIDE.md`
