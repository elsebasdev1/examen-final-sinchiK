## cliente: Interfaz de Visualización para Redis

Microservicio que proporciona una interfaz web para visualizar los datos almacenados en Redis.

### Descripción

En el despliegue actual, utilizamos **Redis Commander** como cliente web para visualizar:
- Claves y valores almacenados en Redis
- La lista `sensores` con los datos generados por el sensor
- Interfaz intuitiva sin necesidad de línea de comandos

### Acceso

Una vez desplegado en Kubernetes con NodePort 30007:

```
http://<NODE_IP>:30007
```

### Contenido Estático

El archivo `index.html` es una página de instrucciones. El componente principal de visualización viene del Deployment que utiliza la imagen `rediscommander/redis-commander:latest`.

### Construcción de Imagen Docker

```bash
docker build -t cliente:v1 .
```

### Variables Clave en Redis para Monitorear

- **Clave**: `sensores` (tipo: List)
- **Contenido**: Objetos JSON con formato:

```json
{
  "sensor_id": "rbt-01",
  "valor": 42.15,
  "timestamp": "2026-02-04T12:30:45Z"
}
```

### Seguridad

La conexión a Redis desde Redis Commander se realiza con autenticación usando la contraseña almacenada en el Secret de Kubernetes.
