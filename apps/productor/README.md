## productor: Sensor Simulado para Almacenes Automatizados

Microservicio que actúa como sensor IoT simulado. Genera datos de monitoreo cada 3 segundos y los guarda en Redis.

### Modos de Ejecución

#### Modo Sensor (predeterminado en K8s)

```bash
# Requiere Redis accesible y variables de entorno
export MODE=sensor
export BD_HOST=bd-svc
export BD_PORT=6379
export REDIS_PASSWORD=redispass123
export SENSOR_ID=rbt-01

python sensor.py
```

#### Modo API Flask (debugging)

```bash
# API simple con endpoint /health
python app.py
```

### Construcción de Imagen Docker

```bash
docker build -t productor:v1 .
```

### Ejecución con Docker

```bash
# Modo sensor
docker run --rm \
  -e MODE=sensor \
  -e BD_HOST=redis-host \
  -e REDIS_PASSWORD=redispass123 \
  productor:v1

# Modo API
docker run --rm \
  -e MODE=app \
  -p 5000:5000 \
  productor:v1
```

### Variables de Entorno

- `BD_HOST`: Host de Redis (default: bd-svc)
- `BD_PORT`: Puerto de Redis (default: 6379)
- `REDIS_PASSWORD`: Contraseña para autenticación
- `SENSOR_ID`: ID del sensor (default: rbt-01)
- `MODE`: "sensor" o "app" (default: app)

### Formato de Datos Generados

Cada entrada guardada en la clave Redis `sensores` tiene este formato:

```json
{
  "sensor_id": "rbt-01",
  "valor": 42.15,
  "timestamp": "2026-02-04T12:30:45Z"
}
```

### Dependencias

- flask (para API)
- redis (cliente Python)

