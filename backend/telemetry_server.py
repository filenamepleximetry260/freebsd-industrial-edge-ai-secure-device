# LICENSE UPL
# Author: Mauro Risonho de Paula Assumpção
# Description: Backend telemetry server implementation
import socket
import json
import logging
import threading
from data_processor import process_telemetry

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("TelemetryServer")

HOST = '0.0.0.0'
PORT = 8080

def handle_client(conn, addr):
    logger.info(f"Connected by {addr}")
    with conn:
        buffer = ""
        while True:
            data = conn.recv(1024)
            if not data:
                break
            buffer += data.decode('utf-8')
            
            # Simple line-based JSON parsing
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                if line.strip():
                    try:
                        payload = json.loads(line)
                        process_telemetry(payload)
                    except json.JSONDecodeError:
                        logger.error(f"Invalid JSON received: {line}")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Allow reusing address
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        logger.info(f"Server listening on {HOST}:{PORT}")
        
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    start_server()
