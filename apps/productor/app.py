import time
import json
import random
import os
import redis
from datetime import datetime

# Configuración
REDIS_HOST = os.getenv('REDIS_HOST', 'bd-svc')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_PASS = os.getenv('REDIS_PASS', None)

def connect_db():
    try:
        # Agregamos 'password=REDIS_PASS' a la conexión
        client = redis.Redis(
            host=REDIS_HOST, 
            port=REDIS_PORT, 
            password=REDIS_PASS, 
            decode_responses=True
        )
        # Probamos conexión (ping)
        client.ping()
        print(f"Conectado a Redis en {REDIS_HOST}")
        return client
    except Exception as e:
        print(f"Error conectando a Redis: {e}")
        return None

def main():
    print("Iniciando Sensor IoT (Productor)...")
    client = connect_db()
    
    # Bucle infinito
    while True:
        if not client:
            client = connect_db()
            time.sleep(3)
            continue

        # Generar datos 
        data = {
            "sensor_id": "rbt-01",
            "valor": round(random.uniform(10.0, 100.0), 2),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

        try:
            # Guardamos en una lista de Redis llamada "sensores"
            client.lpush("sensores", json.dumps(data))
            client.ltrim("sensores", 0, 99)
            print(f"Dato enviado: {data}")
        except Exception as e:
            print(f"Error enviando dato: {e}")
            client = None # Forzar reconexión

        time.sleep(3) # Espera de 3 segundos

if __name__ == "__main__":
    main()