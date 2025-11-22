#!/bin/bash

echo "=========================================="
echo "  Campus Pulse with Monitoring Stack"
echo "=========================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Start monitoring stack (Prometheus + Grafana)
echo ""
echo "📊 Starting Prometheus + Grafana..."
cd monitoring
docker-compose -f docker-compose.monitoring.yml up -d
cd ..

echo "⏳ Waiting for services to start (30 seconds)..."
sleep 30

# Check if services are running
if docker ps | grep -q "campus-pulse-grafana"; then
    echo "✅ Grafana is running at: http://localhost:3000"
    echo "   Username: admin"
    echo "   Password: admin"
else
    echo "⚠️  Grafana failed to start"
fi

if docker ps | grep -q "campus-pulse-prometheus"; then
    echo "✅ Prometheus is running at: http://localhost:9090"
else
    echo "⚠️  Prometheus failed to start"
fi

echo ""
echo "📈 Starting Metrics Server..."
cd streamlit_app
pip install -q flask prometheus-client 2>/dev/null
python metrics_server.py &
METRICS_PID=$!
echo "✅ Metrics endpoint: http://localhost:8000/metrics"

sleep 3

echo ""
echo "🎓 Starting Campus Pulse Streamlit App..."
streamlit run app.py &
STREAMLIT_PID=$!

echo ""
echo "=========================================="
echo "  All Services Started!"
echo "=========================================="
echo ""
echo "📱 Campus Pulse App:    http://localhost:8501"
echo "📊 Grafana Dashboard:   http://localhost:3000"
echo "📈 Prometheus:          http://localhost:9090"
echo "🔍 Metrics Endpoint:    http://localhost:8000/metrics"
echo ""
echo "To stop all services:"
echo "  kill $STREAMLIT_PID $METRICS_PID"
echo "  cd monitoring && docker-compose -f docker-compose.monitoring.yml down"
echo ""
echo "Press Ctrl+C to stop..."

# Wait for processes
wait
