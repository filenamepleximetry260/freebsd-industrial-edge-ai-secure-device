#!/usr/bin/env bash
# LICENSE UPL
# Author: Mauro Risonho de Paula Assumpção
# Description: Starts the Enterprise AI Dashboard using Docker Compose

set -euo pipefail

compose_cmd() {
    # Prefer Docker Compose v2 plugin to avoid legacy docker-compose v1 incompatibilities.
    if docker compose version >/dev/null 2>&1; then
        COMPOSE_BAKE=false docker compose "$@"
        return
    fi

    if command -v docker-compose >/dev/null 2>&1; then
        docker-compose "$@"
        return
    fi

    echo "ERROR: Docker Compose not found. Install Docker Compose v2 (docker compose)." >&2
    exit 1
}

cd "$(dirname "$0")/.."

echo "=========================================================="
echo " Booting Edge AI Enterprise Dashboard (Docker)            "
echo "=========================================================="

echo "[1] Checking for sqlite3 baseline..."
mkdir -p data
touch data/telemetry.db
chmod 664 data/telemetry.db

echo "[2] Starting Docker Compose..."

# Clean stale containers that may have been created by legacy compose naming.
stale_backend=$(docker ps -aq --filter "name=edge_ai_backend")
if [ -n "$stale_backend" ]; then
    docker rm -f $stale_backend >/dev/null 2>&1 || true
fi

stale_frontend=$(docker ps -aq --filter "name=edge_ai_frontend")
if [ -n "$stale_frontend" ]; then
    docker rm -f $stale_frontend >/dev/null 2>&1 || true
fi

compose_cmd down --remove-orphans >/dev/null 2>&1 || true
compose_cmd up --build -d

echo "=========================================================="
echo " Services are starting up!"
echo " - FastAPI Backend: http://localhost:8000/docs"
echo " - Vite Frontend:   http://localhost:3000"
echo " - Raw Telemetry:   http://localhost:8000/api/telemetry"
echo ""
echo " NOTE: Run QEMU Emulation (run_qemu_demo.sh or all_in_one.sh)"
echo " to feed live data into the 8080 telemetry receiver."
echo "=========================================================="
echo "To stop: docker compose down"
