# LICENSE UPL
# Author: Mauro Risonho de Paula Assumpção
# Description: RedTeam AI - White-Box Adversarial ML Evasion Fuzzer

import os
import sys
import time
import json
import socket
import joblib
import random
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s - Adversarial AI - %(levelname)s - %(message)s")

# Tenta carregar o modelo de ML do diretório raiz
MODEL_PATH = os.environ.get("MODEL_PATH", os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'isolation_forest.pkl')))
TARGET_HOST = os.environ.get("TARGET_HOST", "127.0.0.1")
TARGET_PORT = int(os.environ.get("TARGET_PORT", 8080))

def send_payload(payload):
    """Envia o payload forjado diretamente para o Backend (bypass no embedded)."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((TARGET_HOST, TARGET_PORT))
            s.sendall(json.dumps(payload).encode('utf-8'))
            logging.info(f"Adversarial Payload Injected: {payload}")
    except ConnectionRefusedError:
        logging.error("Failed to connect to the backend server. Make sure it is running on port 8080.")

def adversarial_fuzzer():
    """
    Simula uma AI Otimizadora (Atacante) procurando um "ponto cego" matemático no Isolation Forest.
    Queremos introduzir uma Temperatura Crítica e Corrente Alta que são tipicamente Anomalias,
    mas manipulamos a vibração para uma margem que engane a árvore de decisão.
    """
    
    if not os.path.exists(MODEL_PATH):
        logging.error(f"Cannot perform White-Box attack. Model file not found at: {MODEL_PATH}")
        sys.exit(1)

    logging.info("Loading target Isolation Forest model for White-Box Evasion Analysis...")
    try:
        model = joblib.load(MODEL_PATH)
    except Exception as e:
        logging.error(f"Error loading model: {e}")
        sys.exit(1)
        
    logging.info("Hunting for a benign-classified adversarial pattern...")
    
    # Parâmetros de ataque desejados
    # Queremos passar uma temperatura de 75°C (geralmente classificada como anomalia/ataque se vibração for alta)
    # Ajustamos para fuzzer ampliado de corrente
    target_temperature = 65.0
    
    evasion_payload = None
    attempts = 0
    max_attempts = 5000
    
    # Busca gradiente fuzzer: Tentamos ajustar a vibração e corrente o ponto cego
    while attempts < max_attempts:
        test_vibration = round(random.uniform(0.1, 2.0), 2)
        test_current = round(random.uniform(2.0, 10.0), 2)
        
        # Testamos a predição através do modelo (1 = Normal, -1 = Anomalia)
        # O modelo Isolation Forest usa o formato df[[temperature, vibration, current]]
        feature_vector = pd.DataFrame([{
            'temperature': target_temperature,
            'vibration': test_vibration,
            'current': test_current
        }])
        
        prediction = model.predict(feature_vector)[0]
        
        if prediction == 1:
            # SUCESSO! Encontramos uma combinação catastrófica que a IA acha "Normal"
            evasion_payload = {
                "device_id": "adversarial-bot",
                "temperature": target_temperature,
                "vibration": test_vibration,
                "current": test_current,
                "timestamp": int(time.time()),
                "malicious_flag": "AI_EVASION_SUCCESS"
            }
            logging.warning(f"Adversarial payload crafted after {attempts} attempts!")
            break
            
        attempts += 1
        
    if evasion_payload:
        logging.info("Bypassing Cyber Defenses... Injecting...")
        for _ in range(5):
            evasion_payload["timestamp"] = int(time.time())
            send_payload(evasion_payload)
            time.sleep(1)
    else:
        logging.error("Failed to craft evasion payload within limits. The model is highly robust to this vector.")

if __name__ == "__main__":
    adversarial_fuzzer()
