# Script sensor: genera datos cada 3 segundos y los guarda en Redis

import os
import time
import json
import random
from datetime import datetime
import redis

BD_HOST = os.getenv('BD_HOST', os.getenv('REDIS_HOST', 'bd-svc'))
BD_PORT = int(os.getenv('BD_PORT', 6379))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
SENSOR_ID = os.getenv('SENSOR_ID', 'rbt-01')

# Conexión a Redis con autenticación
r = redis.Redis(host=BD_HOST, port=BD_PORT, password=REDIS_PASSWORD, decode_responses=True)

# Bucle infinito: generar y guardar JSON en la lista 'sensores'
while True:
    valor = round(random.uniform(0, 100), 2)
    timestamp = datetime.utcnow().isoformat() + 'Z'
    data = {"sensor_id": SENSOR_ID, "valor": valor, "timestamp": timestamp}
    try:
        # Guardamos al inicio de la lista para ver los más recientes primero
        r.lpush('sensores', json.dumps(data))
        print('guardado:', data, flush=True)
    except Exception as e:
        print('Error escribiendo en Redis:', e, flush=True)
    time.sleep(3)
