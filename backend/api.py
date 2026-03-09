# LICENSE UPL
# Author: Mauro Risonho de Paula Assumpção
# Description: 
import logging
import sqlite3
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI(title="Edge AI Telemetry API")

# Restrict CORS to known local dashboard origins by default.
ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")
    if origin.strip()
]

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'telemetry.db'))

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TelemetryRecord(BaseModel):
    id: int
    device_id: str
    temperature: float
    vibration: float
    current: float
    timestamp: int
    malicious_flag: Optional[str] = None

@app.get("/api/telemetry", response_model=List[TelemetryRecord])
def get_telemetry(limit: int = 50):
    """Fetches the latest telemetry records."""
    if not os.path.exists(DB_PATH):
        return []
    
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM telemetry 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
def get_stats():
    """Returns general statistics of the Edge Device AI Detection."""
    if not os.path.exists(DB_PATH):
        return {"total_packets": 0, "anomalies": 0, "attacks": 0}
        
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM telemetry")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM telemetry WHERE malicious_flag LIKE 'ANOMALY%'")
        anomalies = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM telemetry WHERE malicious_flag LIKE 'ATTACK%'")
        attacks = cursor.fetchone()[0]
        
        conn.close()
        return {
            "total_packets": total,
            "anomalies": anomalies,
            "attacks": attacks
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
