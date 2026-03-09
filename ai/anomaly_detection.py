# LICENSE UPL
# Author: Mauro Risonho de Paula Assumpção
# Description: AI Anomaly Detection Script
import json
import logging
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("AnomalyDetection")

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'isolation_forest.pkl')

def train_model(data_file):
    """Train the Isolation Forest model on historical telemetry."""
    logger.info("Loading baseline data for training...")
    try:
        df = pd.read_json(data_file, lines=True)
    except Exception as e:
        logger.error(f"Failed to read data: {e}")
        return

    features = df[['temperature', 'vibration', 'current']]
    
    logger.info("Training Isolation Forest...")
    clf = IsolationForest(contamination=0.05, random_state=42)
    clf.fit(features)
    
    joblib.dump(clf, MODEL_PATH)
    logger.info(f"Model saved to {MODEL_PATH}")

def detect_anomaly(telemetry_data):
    """Predict if a new telemetry packet is an anomaly."""
    if not os.path.exists(MODEL_PATH):
        logger.warning(f"Model {MODEL_PATH} not found. Skipping ML detection.")
        return False
        
    clf = joblib.load(MODEL_PATH)
    
    features = pd.DataFrame([{
        'temperature': telemetry_data.get('temperature', 0),
        'vibration': telemetry_data.get('vibration', 0),
        'current': telemetry_data.get('current', 0)
    }])
    
    # Predict returns 1 for inliers, -1 for outliers
    prediction = clf.predict(features)[0]
    
    if prediction == -1:
        logger.warning(f"!!! ML ANOMALY DETECTED !!! Packet: {telemetry_data}")
        return True
    return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", help="Path to JSONL data to train the model", type=str)
    args = parser.parse_args()
    
    if args.train:
        train_model(args.train)
    else:
        print("Usage: python anomaly_detection.py --train ../backend/telemetry_data.jsonl")
