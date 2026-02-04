# Sistema de Monitoreo en Tiempo Real - Almacenes Automatizados

## Instalación y Despliegue

### 1. Construir imágenes Docker

```bash
# Construcción de la imagen productor
cd apps/productor
docker build -t productor:v1 .

# Construcción de la imagen cliente
cd ../cliente
docker build -t cliente:v1 .

# Si usas minikube, cargar las imágenes en el cluster
minikube image load productor:v1
minikube image load cliente:v1
```

### 2. Aplicar manifiestos Kubernetes

```bash
# Desde la raíz del proyecto
kubectl apply -f k8s/00-secrets.yaml
kubectl apply -f k8s/01-config.yaml
kubectl apply -f k8s/02-services.yaml
kubectl apply -f k8s/03-deployments.yaml
kubectl apply -f k8s/04-frontend.yaml
kubectl apply -f k8s/05-db-redis.yaml
```

O aplicarlos todos de una vez:

```bash
kubectl apply -f k8s/
```

### 3. Verificar Despliegue

#### Estado de Pods y Servicios:
```bash
kubectl get pods -o wide
kubectl get svc
```

#### Verificar PVC (Persistencia):
```bash
kubectl get pvc
```
Debe mostrar `bd-pvc` en estado **Bound**.

#### Ver logs del sensor:
```bash
kubectl logs -l app=productor -f
```

### 4. Acceder a Redis Commander (cliente)

**Obtener IP del nodo:**
```bash
# Si usas minikube
minikube ip

# Si usas Docker Desktop
localhost

# Otros clusters
kubectl get nodes -o wide
```

**Acceder a la interfaz:**
```
http://<NODE_IP>:30007
```

Deberías ver Redis Commander mostrando la clave `sensores` con una lista JSON de datos generados.

## Verificación de Datos

En Redis Commander, navega a:
1. Selecciona la base de datos (predeterminada: 0)
2. Busca la clave `sensores`
3. Verifica que contiene objetos JSON con formato:

```json
{
  "sensor_id": "rbt-01",
  "valor": 42.15,
  "timestamp": "2026-02-04T12:30:45Z"
}
```

## Prueba de Resiliencia

Simula una caída de la base de datos y verifica la recuperación:

```bash
# Eliminar Pod de bd
kubectl delete pod -l app=bd

# Esperar a que Kubernetes lo recree
kubectl get pods -l app=bd -w

# Verificar que PVC sigue Bound
kubectl get pvc bd-pvc

# Comprobar que los datos persisten en Redis Commander
# http://<NODE_IP>:30007 (actualizar navegador)
```

La lista `sensores` debe mantener los datos anteriores gracias al PersistentVolumeClaim.

## Seguridad

- **Autenticación Redis**: Habilitada mediante Secret `db-credentials` con contraseña `redispass123`.
- **Secrets de Kubernetes**: Las credenciales se inyectan como variables de entorno desde Secret, no hardcodeadas.
- **PVC**: Asegura que los datos no se pierdan al reiniciar Pods.

## Estructura de Archivos

```
.
├── README.md                              # Este archivo
├── setup.ps1                              # Script de setup (opcional)
├── apps/
│   ├── cliente/
│   │   ├── Dockerfile                     # Nginx para servir index.html
│   │   ├── index.html                     # UI estática con instrucciones
│   │   └── README.md
│   └── productor/
│       ├── Dockerfile                     # Image Python slim con entrypoint flexible
│       ├── app.py                         # API Flask para debugging
│       ├── sensor.py                      # Script sensor principal
│       ├── requirements.txt                # flask, redis
│       └── README.md
└── k8s/
    ├── 00-secrets.yaml                    # Secret con redis-password
    ├── 01-config.yaml                     # ConfigMap con script productor
    ├── 02-services.yaml                   # Servicios: productor-svc, cliente-svc (NodePort)
    ├── 03-deployments.yaml                # Deployment productor (sensor mode)
    ├── 04-frontend.yaml                   # Deployment cliente (redis-commander)
    └── 05-db-redis.yaml                   # PVC + Deployment bd (redis) + Servicio
```

## Troubleshooting

### Los datos no aparecen en Redis Commander
```bash
# Verificar logs del productor
kubectl logs -l app=productor

# Verificar conectividad a Redis
kubectl exec -it <productor-pod-name> -- python -c "import redis; r = redis.Redis(host='bd-svc', port=6379, password='redispass123'); print(r.lrange('sensores', 0, 5))"
```

### PVC no está Bound
```bash
# Verificar estado y eventos
kubectl describe pvc bd-pvc
kubectl get events --sort-by='.lastTimestamp'
```

### cliente no se conecta a bd
```bash
# Verificar logs del cliente
kubectl logs -l app=cliente

# Verificar que bd-svc existe y es alcanzable
kubectl get svc bd-svc
kubectl exec -it <cliente-pod-name> -- sh -c "nslookup bd-svc"
```

## Notas Adicionales

- El script `sensor.py` genera datos cada 3 segundos indefinidamente.
- La contraseña de Redis es `redispass123` (definida en `00-secrets.yaml`).
- NodePort del cliente es **30007** (fijo en `02-services.yaml`).
- La imagen Redis de Bitnami espera la contraseña en variable de entorno `REDIS_PASSWORD`.
- Los datos persisten en el volumen `bd-pvc` incluso tras eliminación/recreación del Pod.

## Entregables del Examen

1. **Arquitectura y Justificación Técnica**: Completada en este README (tabla de tecnologías, esquema, decisiones).
2. **Manifiestos Kubernetes**: Archivos en directorio `k8s/` listos para desplegar.
3. **Código Fuente**: 
   - `apps/productor/sensor.py`: Script sensor con autenticación.
   - `apps/cliente/`: UI estática + Dockerfile.
4. **Evidencia de Funcionamiento**:
   - Captura de Redis Commander mostrando `sensores` con JSON.
   - `kubectl get pvc` mostrando `bd-pvc` en estado Bound.
   - Logs de recuperación tras eliminación de Pod.

## Autor
Diseño de sistema distribuido en Kubernetes para examen de Sistemas Distribuidos.
