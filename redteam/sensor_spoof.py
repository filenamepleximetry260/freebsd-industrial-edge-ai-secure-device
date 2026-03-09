# LICENSE UPL
# Author: Mauro Risonho de Paula Assumpção
# Description: Red Team Sensor Spoof Script
import time

SENSOR_FILE = "/tmp/sensor_data.txt"

def spoof_sensor():
    print("Simulating Sensor Spoof Attack...")
    print(f"Injecting malicious physics parameters directly into {SENSOR_FILE}...")
    
    with open(SENSOR_FILE, "w") as f:
        # Extreme values that bypass normal operation but cause damage or false alarms
        f.write("temperature=150.0 vibration=55.0 current=22.5\n")
    
    print("Spoofed data injected. Security Monitor / AI should detect this.")

if __name__ == "__main__":
    spoof_sensor()
