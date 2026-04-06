---
description: Deploy the EU-Jobs visualizer to the NUC server (192.168.1.247)
---

# 🏗️ EU-Jobs: Sovereign Deploy Workflow (NUC)

Este workflow automatiza la construcción local de datos, el empaquetado y el despliegue remoto en Docker.

## 1. Validación Local de Datos
Construye los JSONs finales a partir de los CSVs actuales.
// turbo
`python scripts/build_site_data.py`

## 2. Empaquetado Quirúrgico (Tar - Linux Compatible)
Crea el bundle de despliegue preservando la estructura de directorios.
// turbo
`tar -czf deploy.tar.gz --exclude="*.tar.gz" --exclude=".venv" --exclude="node_modules" --exclude=".git" --exclude=".python-version" --exclude=".archive" --exclude=".agent" .`

## 3. Transferencia al NUC (192.168.1.247)
Sincroniza el bundle con el servidor.
// turbo
`scp deploy.tar.gz alex@192.168.1.247:/home/alex/projects/eu-jobs/`

## 4. Orquestación Remota (SSH)
Descomprime, construye y reinicia el servicio dockerizado.
// turbo
`ssh alex@192.168.1.247 'cd /home/alex/projects/eu-jobs && tar -xzf deploy.tar.gz && rm deploy.tar.gz && docker compose up --build -d'`

## 5. Verificación de Salud con Self-Healing
Monitorea los logs y verifica el puerto 3050. Si falla, intenta reiniciar.
// turbo
`ssh alex@192.168.1.247 'sleep 5 && docker logs --tail 20 eu_jobs_app && (curl -s -I http://localhost:3050 | grep "200 OK" || (echo "Warning: Initial health check failed. Restarting..." && docker compose restart && sleep 5 && curl -s -I http://localhost:3050 | grep "200 OK"))'`

## 6. Limpieza Local
Elimina el bundle temporal.
// turbo
`powershell -Command "Remove-Item -Path deploy.zip -Force"`

## 🌐 Resumen del Despliegue
- **Host:** 192.168.1.247 (alex)
- **Puerto:** 3050
- **URL:** https://eu-jobs.alexandrucruceanu.com
