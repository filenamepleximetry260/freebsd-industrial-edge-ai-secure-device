# LICENSE UPL
# Author: Mauro Risonho de Paula Assumpção
# Description: Machine simulator
import time
import random
import os

SENSOR_FILE = "/tmp/sensor_data.txt"

def simulate_machine():
    print("Starting Industrial Machine Simulator...")
    print(f"Writing to {SENSOR_FILE} (Run this inside the Edge VM)")
    
    try:
        while True:
            # Normal operating parameters
            temperature = 40.0 + random.uniform(-1.0, 1.0)
            vibration = 2.0 + random.uniform(-0.1, 0.1)
            current = 8.0 + random.uniform(-0.25, 0.25)

            with open(SENSOR_FILE, "w") as f:
                f.write(f"temperature={temperature:.2f} vibration={vibration:.2f} current={current:.2f}\n")
            
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping Simulator.")
        if os.path.exists(SENSOR_FILE):
            os.remove(SENSOR_FILE)

if __name__ == "__main__":
    simulate_machine()
