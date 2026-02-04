# 1. Configurar entorno Docker
& minikube -p minikube docker-env --shell powershell | Invoke-Expression

Write-Host "Construyendo imágenes..." -ForegroundColor Cyan

docker build -t productor:v1 ./apps/productor

Write-Host "Limpiando cluster..." -ForegroundColor Yellow
kubectl delete all --all

# 3. Despliegue
Write-Host "Desplegando en Kubernetes..." -ForegroundColor Cyan
kubectl apply -f k8s/

# 4. Espera
Write-Host "Esperando a que los pods arranquen..." -ForegroundColor Cyan
kubectl wait --for=condition=ready pod --all --timeout=120s

Write-Host "Sistema Listo" -ForegroundColor Green
Write-Host "Acceder a la web con: minikube service cliente-svc" -ForegroundColor White