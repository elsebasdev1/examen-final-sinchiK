# Script de despliegue rápido en Kubernetes


Write-Host "Sistema de Monitoreo - Despliegue en Kubernetes" -ForegroundColor Green
Write-Host "============================================`n"

# 1. Construir imágenes
Write-Host "Paso 1: Construir imagenes Docker"
Write-Host "Construccion de productor..." -ForegroundColor Cyan
cd apps/productor
docker build -t productor:v1 .
if ($LASTEXITCODE -ne 0) { Write-Host "Error construyendo productor"; exit 1 }

Write-Host "Construccion de cliente..." -ForegroundColor Cyan
cd ../cliente
docker build -t cliente:v1 .
if ($LASTEXITCODE -ne 0) { Write-Host "Error construyendo cliente"; exit 1 }
cd ../../

# 2. Cargar imágenes en minikube (si aplica)
Write-Host "`nPaso 2: Cargar imagenes en minikube "
$minikubeCheck = minikube status 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "Minikube detectado " -ForegroundColor Cyan
    minikube image load productor:v1
    minikube image load cliente:v1
} else {
    Write-Host "Minikube no detectado." -ForegroundColor Yellow
}

# 3. Aplicar manifiestos
Write-Host "`nPaso 3: Aplicar manifiestos Kubernetes"
kubectl apply -f k8s/

if ($LASTEXITCODE -eq 0) {
    Write-Host "Manifiestos aplicados"
} else {
    Write-Host "Error aplicando manifiestos"; exit 1
}

# 4. Esperar a que los pods estén listos
Write-Host "`nPaso 4: Esperando que los pods estén listos"
Start-Sleep -Seconds 5
kubectl get pods -w --all-namespaces

# 5. Obtener NodePort
Write-Host "`nPaso 5: Información de acceso"
$nodePort = kubectl get svc cliente-svc -o jsonpath='{.spec.ports[0].nodePort}'
Write-Host "NodePort asignado: ${nodePort}"

# Obtener IP del nodo
$nodeIP = kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="ExternalIP")].address}'
if ([string]::IsNullOrEmpty($nodeIP)) {
    $nodeIP = kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="InternalIP")].address}'
}

Write-Host "IP del nodo: ${nodeIP}"
Write-Host "`nAcceder a Redis Commander en: http://${nodeIP}:${nodePort}`n"

# 6. Mostrar estado final
Write-Host "Estado final:"
Write-Host "`nPods:"
kubectl get pods -o wide
Write-Host "`nServicios:"
kubectl get svc
Write-Host "`nVolúmenes:"
kubectl get pvc

Write-Host "`nDespliegue completado"
Write-Host "Monitoreat los logs con: kubectl logs -l app=productor -f"
