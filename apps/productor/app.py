import os
import redis
from flask import Flask, jsonify

# Microservicio Productor - Generador de datos en modo sensor
# Se ejecuta en modo sensor (sensor.py) por defecto en K8s
# Esta API Flask queda disponible solo para debugging

app = Flask(__name__)

# Conexión a la BD Redis
DB_HOST = os.getenv("REDIS_HOST", "bd-svc")
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
SENSOR_ID = os.getenv('SENSOR_ID', 'rbt-01')

# Conexión a Redis con autenticación
cache = redis.Redis(host=DB_HOST, port=6379, password=REDIS_PASSWORD, decode_responses=True)

@app.route('/health', methods=['GET'])
def health():
    try:
        cache.ping()
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
