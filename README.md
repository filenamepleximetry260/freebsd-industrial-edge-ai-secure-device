# FreeBSD ARM64 Industrial Edge AI Platform

Demonstration of a secure industrial edge monitoring platform running on FreeBSD ARM64.
The system simulates an embedded device responsible for collecting industrial telemetry, detecting anomalies, and identifying cyber attacks.

## Architecture
- **Embedded Layer (C)**: Runs on FreeBSD ARM64 edge device (simulated via QEMU). Collects sensor data and sends telemetry.
- **Backend Layer (Python)**: Receives telemetry, processes data.
- **AI Layer (Python)**: Uses scikit-learn for anomaly and attack detection.
- **Simulation Layer**: Simulates industrial machine emitting metrics.
- **Red Team Layer**: Scripts to simulate sensor spoofing and telemetry injection attacks.

## Usage
1. Setup QEMU FreeBSD AArch64 Environment (see `qemu/README.md` or scripts).
2. Start backend server.
3. Start simulation to generate telemetry.
4. Run red team attacks to test defensive AI.
