#!/usr/bin/env bash
# LICENSE UPL
# Author: Mauro Risonho de Paula Assumpção
# Description: Starts the Enterprise AI Dashboard using Docker Compose

cd "$(dirname "$0")/.."

echo "=========================================================="
echo " Booting Edge AI Enterprise Dashboard (Docker)            "
echo "=========================================================="

echo "[1] Checking for sqlite3 baseline..."
mkdir -p data
touch data/telemetry.db
chmod 664 data/telemetry.db

echo "[2] Starting Docker Compose..."
# We use docker compose plugin or docker-compose
if command -v docker-compose &> /dev/null; then
    docker-compose up --build -d
else
    docker compose up --build -d
fi

echo "=========================================================="
echo " Services are starting up!"
echo " - FastAPI Backend: http://localhost:8000/docs"
echo " - Vite Frontend:   http://localhost:3000"
echo " - Raw Telemetry:   http://localhost:8000/api/telemetry"
echo ""
echo " NOTE: Run QEMU Emulation (run_qemu_demo.sh or all_in_one.sh)"
echo " to feed live data into the 8080 telemetry receiver."
echo "=========================================================="
echo "To stop: docker-compose down"
