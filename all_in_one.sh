#!/usr/bin/env bash
# LICENSE UPL
# Author: Mauro Risonho de Paula Assumpção
# Description: All-in-One E2E Orchestrator (Fully Automates QEMU FreeBSD)

set -e

echo "=========================================================="
echo " Starting All-in-One FreeBSD Edge AI Setup & Execution    "
echo "=========================================================="

cd "$(dirname "$0")"

echo "[1] Downloading FreeBSD ARM64 Image (If missing)..."
./qemu/download_image.sh

echo "[2] Setting up Python Virtual Environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
# Adicionando pexpect para automação do terminal QEMU
./.venv/bin/pip install --prefer-binary -r backend/requirements.txt pexpect > /dev/null 2>&1

echo "[3] Starting Enterprise Dashboard and Telemetry API (Docker)..."
./run_dashboard.sh
sleep 5

echo "[4] Starting Local HTTP Server to expose Embedded Files..."
cd embedded
python3 -m http.server 8081 &
HTTP_PID=$!
cd ..

echo "[5] Automating QEMU FreeBSD Boot and Compile Process (via pexpect)..."
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

# Mostramos o final
echo "=========================================================="
echo "[6] Analyzing AI Models with Telemetry collected from VM..."
./.venv/bin/python ai/anomaly_detection.py --train telemetry_data.jsonl

echo "=========================================================="
echo " All-in-One Execution Fully Completed! Cleaning up..."
echo "=========================================================="
if command -v docker-compose &> /dev/null; then
    docker-compose down > /dev/null 2>&1 || true
else
    docker compose down > /dev/null 2>&1 || true
fi
kill $HTTP_PID > /dev/null 2>&1 || true
rm -f automate_freebsd.py

echo "Done."
