# 🚗 Autonomous Vehicle Simulator

A simulation-based autonomous driving project built on **CARLA 0.9.15**, focused on **path planning and vehicle control**. The system simulates an ego vehicle navigating through a CARLA environment using waypoint-based route planning and PID control, with real-time sensor data and a monitoring dashboard.


## 📌 What This Project Does

This project simulates an autonomous vehicle that:
- **Plans a route** from a start point to a goal using CARLA's Global Route Planner (A* based)
- **Controls the vehicle** along the planned path using a PID controller (steering, throttle, brake)
- **Detects objects and lanes** using camera and lidar sensor data
- **Monitors the simulation** through a real-time dashboard showing speed, trajectory, and sensor feeds
- Runs fully on a **GCP cloud VM (NVIDIA T4 GPU)** in headless mode

### Simulation Environment
- **Simulator:** CARLA 0.9.15
- **Map:** Town03 (intersections + highways)
- **Mode:** Headless (no display required — cloud compatible)
- **Language:** Python 3.8+


## ⚙️ How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/DhanyaHegde18/autonomous-vehicle-simulator.git
cd autonomous-vehicle-simulator
```

### 2. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 3. Launch CARLA Server (GCP / headless)
```bash
cd carla_setup
bash launch_carla.sh
```

### 4. Run the Simulation
```bash
python3 main.py
```

---

## 🧰 Requirements

```
carla==0.9.15
numpy
pygame
matplotlib
scipy
networkx
pyyaml
opencv-python
```

Install with:
```bash
pip3 install -r requirements.txt
```

## 📄 License

This project is developed as part of an academic course. All rights reserved by the team members.