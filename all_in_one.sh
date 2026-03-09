#!/usr/bin/env bash
# LICENSE UPL
# Author: Mauro Risonho de Paula Assumpção
# Description: All-in-One E2E Orchestrator (Fully Automates QEMU FreeBSD)

set -e

# ANSI Colors for Premium CLI feel
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Stages Configuration
TOTAL_STAGES=7
START_TIME=$(date +%s)

show_progress() {
    local stage=$1
    local title=$2
    local percent=$(( stage * 100 / TOTAL_STAGES ))
    local bar_size=40
    local filled=$(( stage * bar_size / TOTAL_STAGES ))
    local empty=$(( bar_size - filled ))
    
    # Calculate ETA (rough estimates)
    local current_time=$(date +%s)
    local elapsed=$(( current_time - START_TIME ))
    
    # Static weights for estimation (in seconds)
    local total_est=291
    local remaining_est=$(( total_est - (stage * total_est / TOTAL_STAGES) ))
    
    printf "\n${CYAN}----------------------------------------------------------${NC}\n"
    printf "${YELLOW}STAGE %d/%d: ${NC}%s\n" "$stage" "$TOTAL_STAGES" "$title"
    printf "${GREEN}["
    local i
    for ((i=0; i<filled; i++)); do printf "#"; done
    for ((i=0; i<empty; i++)); do printf "-"; done
    printf "] %d%% ${NC}" "$percent"
    
    if [ $stage -lt $TOTAL_STAGES ]; then
        printf " (Est. Remaining: ~%ds)\n" "$remaining_est"
    else
        printf " (COMPLETED in %ds)\n" "$elapsed"
    fi
    printf "${CYAN}----------------------------------------------------------${NC}\n"
}

printf "${BLUE}==========================================================${NC}\n"
printf "${BLUE} Starting All-in-One FreeBSD Edge AI Setup & Execution    ${NC}\n"
printf "${BLUE}==========================================================${NC}\n"

cd "$(dirname "$0")"

show_progress 1 "Downloading FreeBSD ARM64 Image"
./qemu/download_image.sh

show_progress 2 "Setting up Python Virtual Environment"
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
# Adicionando pexpect para automação do terminal QEMU
./.venv/bin/pip install --prefer-binary -r backend/requirements.txt pexpect > /dev/null 2>&1

show_progress 3 "Starting Enterprise Dashboard & API (Docker)"
./scripts/run_dashboard.sh
sleep 5

show_progress 4 "Starting Embedded File Transfer Server"
cd embedded
python3 -m http.server 8081 &
HTTP_PID=$!
cd ..

show_progress 5 "Automating QEMU FreeBSD Boot & Compile"
# Criando script temporário de automação em Python
cat << 'EOF' > automate_freebsd.py
import pexpect
import sys
import time

def run():
    print("-> Starting QEMU. This may take a few minutes to boot completely...")
    # Executa o script que starta a VM nographic
    child = pexpect.spawn('./qemu/start_vm.sh', encoding='utf-8', timeout=600)
    # Mostra o output do QEMU no terminal em tempo real
    child.logfile = sys.stdout

    try:
        # Aguarda o prompt de login do FreeBSD
        child.expect('login:')
        print("\n\n---> Detected Login Prompt, logging in as root...")
        child.sendline('root')
        
        # Aguarda o root prompt
        child.expect('root@.*:~ #')
        print("\n\n---> Installing Clang Compiler (Can take 1-2 minutes)...")
        # Instala pkg e clang sem interatividade
        child.sendline('env ASSUME_ALWAYS_YES=yes pkg bootstrap')
        child.expect('root@.*:~ #', timeout=120)
        
        print("\n\n---> Clang Compiler is part of FreeBSD base system...")
        
        print("\n\n---> Downloading C Embedded Sources from Host...")
        child.sendline('mkdir -p src')
        child.expect('root@.*:~ #')
        child.sendline('fetch http://10.0.2.2:8081/src/sensor_reader.c')
        child.expect('root@.*:~ #')
        child.sendline('fetch http://10.0.2.2:8081/src/telemetry_daemon.c')
        child.expect('root@.*:~ #')
        child.sendline('fetch http://10.0.2.2:8081/src/security_monitor.c')
        child.expect('root@.*:~ #')
        child.sendline('fetch http://10.0.2.2:8081/Makefile')
        child.expect('root@.*:~ #')
        
        print("\n\n---> Compiling Embedded System inside FreeBSD ARM64...")
        child.sendline('mv *.c src/ && make')
        child.expect('root@.*:~ #', timeout=120)
        
        print("\n\n---> Starting Edge Daemon...")
        child.sendline('./sensor_reader | ./telemetry_daemon 10.0.2.2 &')
        
        print("\n\n---> Letting Emulated Edge collect and send data for 10 seconds...")
        time.sleep(10)
        
    except pexpect.exceptions.TIMEOUT as e:
        print(f"\nTimeout occurred: {e}")
    except pexpect.exceptions.EOF as e:
        print(f"\nEOF occurred: {e}")
    finally:
        print("\n\n---> Shutting down QEMU Virtual Machine gracefully...")
        child.sendline('poweroff')
        child.expect(pexpect.EOF, timeout=120)

if __name__ == '__main__':
    run()
EOF

# Roda o script de automação
./.venv/bin/python automate_freebsd.py

show_progress 6 "Simulating Cyber-AI Attack (RedTeam Adversarial ML)"
# Executamos o ataque RedTeam via Docker para demonstrar o bypass da IA em tempo real
./scripts/run_redteam.sh

show_progress 7 "Analyzing AI Security Models & Performance"
./.venv/bin/python ai/anomaly_detection.py --train data/telemetry_data.jsonl

printf "\n${GREEN}==========================================================${NC}\n"
printf "${GREEN} All-in-One Execution Fully Completed Successfully!       ${NC}\n"
printf "${GREEN}==========================================================${NC}\n"
printf "${YELLOW}NOTE: Docker services remain running for inspection.${NC}\n"
printf " - Dashboard: http://localhost:3000\n"
printf " - API Backend: http://localhost:8000/docs\n"
printf "${YELLOW}To stop everything later: docker-compose down${NC}\n\n"

# Only kill the background file transfer server
kill $HTTP_PID > /dev/null 2>&1 || true
rm -f automate_freebsd.py


echo "Done."
