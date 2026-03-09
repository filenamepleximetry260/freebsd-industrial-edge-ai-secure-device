# SDD — FreeBSD ARM64 Industrial Edge AI Platform
## System Architecture

Below is the logical and physical architecture of the secure industrial edge monitoring platform.

![Architecture Diagram](architecture.png)

### Core Components Summary

1. **Simulation Layer (`machine_sim.py`)**: Models realistic industrial vibration and temperature curves, generating `/tmp/sensor_data.txt`.
2. **Embedded C Layer (`sensor_reader`, `telemetry_daemon`)**: Reads raw hardware data and safely packages it into JSON format, transmitting it over a socket. Runs inside **FreeBSD 14.4 AArch64**.
3. **Backend / Data Processor (`telemetry_server.py`, `data_processor.py`)**: Receives high-velocity packets and stores a persistent copy into `telemetry.db` (SQLite3).
4. **AI Layer**: Real-time evaluation of telemetry against the trained Machine Learning baseline and direct cyber-attack heuristics, creating an alerting pipeline. 
5. **Red Team Layer**: Tools designed to emulate physical tampering (`sensor_spoof.py`) and network interception/injection attacks (`telemetry_injection.py`).
