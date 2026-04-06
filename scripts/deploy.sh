#!/bin/bash

# 🏗️ EU-Jobs: Sovereign Deployment Pipeline
# Destino: NUC (192.168.1.247)
# Modelo: Atómico (Tar -> SCP -> Build -> Up)

set -e

# Configuración
PROJECT_NAME="eu-jobs"
REMOTE_HOST="alex@192.168.1.247"
REMOTE_PATH="/home/alex/projects/${PROJECT_NAME}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
ARCHIVE_NAME="${PROJECT_NAME}_${TIMESTAMP}.tar.gz"

echo "🚀 Iniciando despliegue de ${PROJECT_NAME}..."

# 1. Empaquetado quirúrgico (excluyendo basura)
echo "📦 Empaquetando archivos..."
tar -czf "${ARCHIVE_NAME}" \
    --exclude=".git" \
    --exclude="node_modules" \
    --exclude="__pycache__" \
    --exclude=".venv" \
    --exclude="*.tar.gz" \
    --exclude=".env" \
    --exclude=".python-version" \
    .

# 2. Transferencia al NUC
echo "📡 Transfiriendo al NUC (192.168.1.247)..."
ssh "${REMOTE_HOST}" "mkdir -p ${REMOTE_PATH}"
scp "${ARCHIVE_NAME}" "${REMOTE_HOST}:${REMOTE_PATH}/"

# 3. Despliegue Remoto
echo "🛠️ Ejecutando build y despliegue remoto..."
ssh "${REMOTE_HOST}" << EOF
    cd "${REMOTE_PATH}"
    
    # Descomprimir
    tar -xzf "${ARCHIVE_NAME}"
    rm "${ARCHIVE_NAME}"
    
    # Build y Up Atómico
    docker compose up --build -d
    
    # Limpieza de imágenes huérfanas
    docker image prune -f
EOF

# 4. Limpieza local
echo "🧹 Limpiando archivos temporales..."
rm "${ARCHIVE_NAME}"

echo "✅ ¡Despliegue completado satisfactoriamente!"
echo "🌐 URL: https://eu-jobs.alexandrucruceanu.com"
