#!/usr/bin/env bash
# LICENSE UPL
# Author: Mauro Risonho de Paula Assumpção
# Description: RedTeam Evasion Attack via Docker

set -e

echo "=========================================================="
echo " Starting RedTeam Adversarial Evasion on Rocky Linux 9    "
echo "=========================================================="

if command -v docker-compose &> /dev/null; then
    docker-compose --profile redteam up --build redteam
else
    docker compose --profile redteam up --build redteam
fi
