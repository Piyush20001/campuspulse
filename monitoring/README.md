# Campus Pulse Monitoring Stack

Prometheus + Grafana monitoring for Campus Pulse application.

## Quick Start

```bash
# From project root
cd /home/user/campuspulse
./start_with_monitoring.sh
```

Or manually:

```bash
# Start Docker services
cd monitoring
docker-compose -f docker-compose.monitoring.yml up -d

# Start metrics server
cd ../streamlit_app
python metrics_server.py &

# Start app
streamlit run app.py
```

## Services

- **Grafana** - http://localhost:3000 (admin/admin)
- **Prometheus** - http://localhost:9090
- **Metrics Endpoint** - http://localhost:8000/metrics

## Files

```
monitoring/
├── docker-compose.monitoring.yml  # Docker Compose configuration
├── prometheus.yml                 # Prometheus configuration
├── alert_rules.yml               # Alerting rules
├── grafana_dashboard.json        # Pre-configured dashboard
└── README.md                     # This file
```

## Commands

**Start services:**
```bash
docker-compose -f docker-compose.monitoring.yml up -d
```

**Stop services:**
```bash
docker-compose -f docker-compose.monitoring.yml down
```

**Restart services:**
```bash
docker-compose -f docker-compose.monitoring.yml restart
```

**View logs:**
```bash
docker-compose -f docker-compose.monitoring.yml logs -f
```

**Reset (delete all data):**
```bash
docker-compose -f docker-compose.monitoring.yml down -v
docker-compose -f docker-compose.monitoring.yml up -d
```

## Configuration

### Prometheus

Edit `prometheus.yml` to:
- Change scrape intervals
- Add new targets
- Modify retention settings

After changes:
```bash
docker-compose -f docker-compose.monitoring.yml restart prometheus
```

### Grafana

The dashboard is automatically provisioned from `grafana_dashboard.json`.

To modify:
1. Edit dashboard in Grafana UI
2. Export as JSON
3. Save to `grafana_dashboard.json`

### Alerts

Edit `alert_rules.yml` to add/modify alerts.

After changes:
```bash
docker-compose -f docker-compose.monitoring.yml restart prometheus
```

## Metrics Collected

- **Page views** - by page name
- **Active users** - current count
- **Crowd levels** - by location
- **Events** - total count and by category
- **Model predictions** - count and latency
- **Database queries** - count and latency
- **Errors** - total count
- **Cache hits** - rate
- **User activity** - signups and logins

## Troubleshooting

**No data in Grafana?**
1. Check Prometheus targets: http://localhost:9090/targets
2. Verify metrics endpoint: http://localhost:8000/metrics
3. Check container logs: `docker logs campus-pulse-prometheus`

**Port conflicts?**
```bash
lsof -i :3000  # Grafana
lsof -i :9090  # Prometheus
```

**Container won't start?**
```bash
docker logs campus-pulse-grafana
docker logs campus-pulse-prometheus
```

## Documentation

See `GRAFANA_GUIDE.md` in project root for complete documentation.

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌────────────┐
│  Streamlit  │────▶│   Metrics    │────▶│ Prometheus │
│     App     │     │   Server     │     │            │
└─────────────┘     │  (Port 8000) │     │ (Port 9090)│
                    └──────────────┘     └──────┬─────┘
                                                 │
                                                 ▼
                                         ┌────────────┐
                                         │  Grafana   │
                                         │ (Port 3000)│
                                         └────────────┘
```

## Ports

- 3000 - Grafana web UI
- 9090 - Prometheus web UI
- 8000 - Metrics endpoint
- 8501 - Streamlit app

## Data Persistence

Data is stored in Docker volumes:
- `grafana_data` - Grafana settings and dashboards
- `prometheus_data` - Metrics time-series data

To backup:
```bash
docker run --rm -v monitoring_grafana_data:/data -v $(pwd):/backup alpine tar czf /backup/grafana-backup.tar.gz /data
docker run --rm -v monitoring_prometheus_data:/data -v $(pwd):/backup alpine tar czf /backup/prometheus-backup.tar.gz /data
```

To restore:
```bash
docker run --rm -v monitoring_grafana_data:/data -v $(pwd):/backup alpine tar xzf /backup/grafana-backup.tar.gz -C /
docker run --rm -v monitoring_prometheus_data:/data -v $(pwd):/backup alpine tar xzf /backup/prometheus-backup.tar.gz -C /
```
