from flask import Flask, g, request
from prometheus_flask_exporter import PrometheusMetrics
from time import time
import logging
import json

app = Flask(__name__)
metrics = PrometheusMetrics(app)

logger = logging.getLogger('backend')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(handler)

@app.before_request
def start_timer():
    g.start_time = time()

@app.after_request
def log_request(response):
    latency = time() - g.start_time
    log_data = {
        'method': request.method,
        'path': request.path,
        'status': response.status_code,
        'latency_ms': round(latency * 1000),
        'remote_addr': request.remote_addr,
    }
    logger.info(json.dumps(log_data))
    return response

@app.route("/api/hello")
def hello():
    return "Hello from Backend with Prometheus Metrics!"

@app.route("/api/health")
def health():
    return "Backend is healthy!"

@app.route("/api/greet")
def greet():
    name = request.args.get('name', 'World')
    return f"Hello, {name}!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
