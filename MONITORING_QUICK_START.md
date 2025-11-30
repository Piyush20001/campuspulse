# 🚀 Monitoring Quick Start

## Start Everything (One Command)

```bash
cd /home/user/campuspulse && ./start_with_monitoring.sh
```

This starts:
- ✅ Prometheus (metrics collection)
- ✅ Grafana (visualization)
- ✅ Metrics Server (exposes app metrics)
- ✅ Campus Pulse App (Streamlit)

---

## Access Services

| Service | URL | Login |
|---------|-----|-------|
| **Grafana Dashboard** | http://localhost:3000 | admin/admin |
| **Campus Pulse App** | http://localhost:8501 | - |
| **Prometheus** | http://localhost:9090 | - |
| **Metrics Endpoint** | http://localhost:8000/metrics | - |

---

## Common Commands

### Check Status
```bash
docker ps | grep campus-pulse
```

### View Logs
```bash
# Grafana logs
docker logs -f campus-pulse-grafana

# Prometheus logs
docker logs -f campus-pulse-prometheus
```

### Restart Services
```bash
# Restart Docker containers
cd /home/user/campuspulse/monitoring
docker-compose -f docker-compose.monitoring.yml restart

# Restart just Grafana
docker restart campus-pulse-grafana

# Restart just Prometheus
docker restart campus-pulse-prometheus
```

### Stop Everything
```bash
# Stop Python processes
pkill -f streamlit
pkill -f metrics_server.py

# Stop Docker containers
cd /home/user/campuspulse/monitoring
docker-compose -f docker-compose.monitoring.yml down
```

---

## Docker Reset

### Soft Reset (Keep Data)
```bash
cd /home/user/campuspulse/monitoring
docker-compose -f docker-compose.monitoring.yml stop
docker-compose -f docker-compose.monitoring.yml rm -f
docker-compose -f docker-compose.monitoring.yml up -d
```

### Hard Reset (Delete All Data)
⚠️ **WARNING: This deletes all dashboards, settings, and metrics history**

```bash
cd /home/user/campuspulse/monitoring
docker-compose -f docker-compose.monitoring.yml down -v
docker-compose -f docker-compose.monitoring.yml up -d
sleep 30
```

---

## Troubleshooting

### No Data in Grafana?

**Check Prometheus targets:**
```bash
# Open in browser
http://localhost:9090/targets

# Should show "campus-pulse-metrics" as UP (green)
```

**Check metrics endpoint:**
```bash
curl http://localhost:8000/metrics | head -20
```

**Restart everything:**
```bash
cd /home/user/campuspulse/monitoring
docker-compose -f docker-compose.monitoring.yml restart
sleep 10
cd /home/user/campuspulse/streamlit_app
python metrics_server.py &
```

### Port Already in Use?

```bash
# Check what's using the port
lsof -i :3000  # Grafana
lsof -i :9090  # Prometheus
lsof -i :8000  # Metrics

# Kill the process (replace PID)
kill -9 <PID>
```

### Container Won't Start?

```bash
# Check logs for errors
docker logs campus-pulse-grafana
docker logs campus-pulse-prometheus

# Remove and recreate
cd /home/user/campuspulse/monitoring
docker-compose -f docker-compose.monitoring.yml down
docker-compose -f docker-compose.monitoring.yml up -d
```

---

## Health Check

```bash
# Check if all services are healthy
curl http://localhost:3000/api/health  # Grafana
curl http://localhost:9090/-/healthy   # Prometheus
curl http://localhost:8000/metrics     # Metrics Server
curl http://localhost:8501             # Streamlit
```

All should return HTTP 200 OK.

---

## Full Documentation

For complete documentation, see:
- **GRAFANA_GUIDE.md** - Comprehensive guide with all features
- **start_with_monitoring.sh** - Automated startup script

---

## Need Help?

1. Check logs: `docker logs campus-pulse-grafana`
2. Check Prometheus targets: http://localhost:9090/targets
3. View metrics: http://localhost:8000/metrics
4. Read full guide: `GRAFANA_GUIDE.md`
