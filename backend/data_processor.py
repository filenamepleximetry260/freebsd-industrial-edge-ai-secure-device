# LICENSE UPL
# Author: Mauro Risonho de Paula Assumpção
# Description: 
import logging
import os
import sys
import sqlite3
import json

# Adiciona a pasta ai/ no path para podermos importar
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ai')))
from attack_detection import detect_attack
from anomaly_detection import detect_anomaly

logger = logging.getLogger("DataProcessor")

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'telemetry.db')

def init_db():
    """Initializes SQLite3 Database for persistence."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT,
            temperature REAL,
            vibration REAL,
            current REAL,
            timestamp INTEGER,
            malicious_flag TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Inicia o BD assim que o módulo é importado
init_db()

def process_telemetry(data: dict):
    """
    Simulates saving data to a database or passing to an AI pipeline.
    """
    logger.info(f"Received Telemetry: {data}")
    
    # 1. Armazenamento em Arquivo (Legado / Treino Local)
    jsonl_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'telemetry_data.jsonl')
    with open(jsonl_path, "a") as f:
        f.write(json.dumps(data) + "\n")
        
    # 2. Real-time AI execution
    is_attack = detect_attack(data)
    is_anomaly = False
    if not is_attack:
        # Só checa anomalia estatística se não for um ataque claro
        is_anomaly = detect_anomaly(data)

    incoming_flag = data.get('malicious_flag')
    detected_flag = None
    if is_attack:
        detected_flag = 'ATTACK_DETECTED'
    elif is_anomaly:
        detected_flag = 'ANOMALY_DETECTED'

    if incoming_flag and detected_flag and incoming_flag != detected_flag:
        final_flag = f"{incoming_flag};{detected_flag}"
    else:
        final_flag = incoming_flag or detected_flag

    # 3. Persistência em Banco de Dados Relacional (SQLite3)
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO telemetry (device_id, temperature, vibration, current, timestamp, malicious_flag)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data.get('device_id'),
            data.get('temperature'),
            data.get('vibration'),
            data.get('current'),
            data.get('timestamp'),
            final_flag
        ))
        conn.commit()
    except Exception as e:
        logger.error(f"Database insertion failed: {e}")
    finally:
        if conn:
            conn.close()
