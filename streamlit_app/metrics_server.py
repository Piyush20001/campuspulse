"""
Metrics Server - Exposes Prometheus metrics endpoint
Run this alongside your Streamlit app
"""
from flask import Flask, Response
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from monitoring.prometheus_metrics import get_metrics

app = Flask(__name__)

@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint"""
    return Response(get_metrics(), mimetype='text/plain')

@app.route('/health')
def health():
    """Health check endpoint"""
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    print("Starting Prometheus Metrics Server...")
    print("Metrics available at: http://localhost:8000/metrics")
    app.run(host='0.0.0.0', port=8000, debug=False)
