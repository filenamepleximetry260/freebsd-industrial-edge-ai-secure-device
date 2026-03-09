#!/usr/bin/env bash
# LICENSE UPL
# Author: Mauro Risonho de Paula Assumpção
# Description: RedTeam Evasion Attack via Docker

set -e
cd "$(dirname "$0")/.."

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

echo "=========================================================="
echo " Starting RedTeam Adversarial Evasion on Rocky Linux 9    "
echo "=========================================================="

# Clean stale containers that may have been created by legacy compose naming.
stale_containers=$(docker ps -aq --filter "name=edge_ai_redteam")
if [ -n "$stale_containers" ]; then
    docker rm -f $stale_containers >/dev/null 2>&1 || true
fi

compose_cmd --profile redteam up --build redteam
