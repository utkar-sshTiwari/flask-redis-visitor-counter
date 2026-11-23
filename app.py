import os
import socket
from flask import Flask, jsonify
import redis

app = Flask(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
CLUSTER_NAME = os.getenv("CLUSTER_NAME", "local-cluster")

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True, socket_connect_timeout=2)

@app.route("/")
def index():
    try:
        count = r.incr("visitor_count")
        return jsonify({
            "message": "Visitor Counter Service",
            "visitor_count": count,
            "pod_hostname": socket.gethostname(),
            "cluster": CLUSTER_NAME
        }), 200
    except redis.RedisError as e:
        return jsonify({"error": "Redis connection failed", "details": str(e)}), 500

@app.route("/health")
def health():
    try:
        r.ping()
        return jsonify({"status": "healthy"}), 200
    except redis.RedisError:
        return jsonify({"status": "unhealthy"}), 503

@app.route("/load")
def cpu_load():
    # Generates brief CPU work to trigger HPA scaling
    total = 0
    for i in range(5_000_000):
        total += i * i
    return jsonify({"status": "load_complete", "pod": socket.gethostname()}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
