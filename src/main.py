"""
main.py
Entry point for the Autonomous Vehicle Simulator
Integrates all modules: path planning, control, lane detection,
object detection, and dashboard.
"""

import carla
import time
import sys
import os

# Module imports — matching each member's actual code
from path_planning.route_planner import AStarPlanner       # Vasundhara
from path_planning.waypoint_utils import Waypoint          # Vasundhara
from control.vehicle_agent import VehicleAgent             # Medini
from dashboard.monitor import Dashboard                    # Dhanya

# Lane & object detection — plain functions (Thejaswini)
from lane_detection.lane_detector import average_lines, detect_lanes
from object_detection.object_detector import detect_objects

# ── Config ────────────────────────────────────────────────
START       = (0, 0)        # grid start (col, row)
GOAL        = (5, 5)        # grid goal  (col, row)
TARGET_SPEED = 30.0         # km/h

# Simple grid: 0=free, 1=obstacle
GRID = [
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0]
]

# ── Helpers ───────────────────────────────────────────────

def waypoint_to_carla_location(wp, world):
    """
    Converts our Waypoint(x,y) into a real CARLA waypoint
    so VehicleAgent.run_step() gets the object it expects.
    """
    carla_map = world.get_map()
    location  = carla.Location(x=float(wp.x) * 2.0,
                                y=float(wp.y) * 2.0,
                                z=0.5)
    return carla_map.get_waypoint(location)


def get_camera_frame(vehicle, world):
    """
    Captures a single RGB frame from a temporary camera sensor.
    Used for lane & object detection checks.
    Returns a numpy array or None.
    """
    import numpy as np
    frame_data = {"frame": None}

    bp  = world.get_blueprint_library().find('sensor.camera.rgb')
    bp.set_attribute('image_size_x', '640')
    bp.set_attribute('image_size_y', '480')
    spawn_tf = carla.Transform(carla.Location(x=1.5, z=2.4))
    cam = world.spawn_actor(bp, spawn_tf, attach_to=vehicle)

    def on_image(img):
        arr = __import__('numpy').frombuffer(img.raw_data,
                                              dtype='uint8')
        frame_data["frame"] = arr.reshape(
            (img.height, img.width, 4))[:, :, :3]

    cam.listen(on_image)
    time.sleep(0.1)          # wait for one frame
    cam.stop()
    cam.destroy()
    return frame_data["frame"]


# ── Main ──────────────────────────────────────────────────

def main():
    # 1. Connect to CARLA
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    world  = client.get_world()
    print("[Main] Connected to CARLA server.")

    # 2. Spawn ego vehicle
    bp_lib     = world.get_blueprint_library()
    vehicle_bp = bp_lib.filter('vehicle.tesla.model3')[0]
    spawn_pts  = world.get_map().get_spawn_points()
    vehicle    = world.spawn_actor(vehicle_bp, spawn_pts[0])
    print(f"[Main] Ego vehicle spawned: {vehicle.id}")

    # 3. Plan route using Vasundhara's AStarPlanner
    planner  = AStarPlanner(GRID)
    waypoints = planner.plan(START, GOAL)   # list of Waypoint objects
    print(f"[Main] Route planned: {len(waypoints)} waypoints.")

    if not waypoints:
        print("[Main] ERROR: No path found! Check grid/start/goal.")
        vehicle.destroy()
        return

    # 4. Init VehicleAgent (Medini) and Dashboard (Dhanya)
    agent = VehicleAgent(vehicle, target_speed=TARGET_SPEED)
    dash  = Dashboard()

    # 5. Make outputs folder
    os.makedirs('outputs', exist_ok=True)

    # ── Main simulation loop ──────────────────────────────
    try:
        for step, wp in enumerate(waypoints):

            # Convert our Waypoint → CARLA waypoint for VehicleAgent
            carla_wp = waypoint_to_carla_location(wp, world)

            # ── Thejaswini: object detection every 10 steps ──
            if step % 10 == 0:
                frame = get_camera_frame(vehicle, world)
                if frame is not None:
                    import cv2
                    tmp_path = 'outputs/tmp_frame.jpg'
                    cv2.imwrite(tmp_path, frame)
                    print(f"[Step {step}] Running object detection...")
                    detect_objects(tmp_path)   # prints detections

            # ── Thejaswini: lane detection every 10 steps ───
            if step % 10 == 0:
                frame = get_camera_frame(vehicle, world)
                if frame is not None:
                    import cv2, numpy as np
                    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    blur  = cv2.GaussianBlur(gray, (5, 5), 0)
                    edges = cv2.Canny(blur, 50, 150)
                    h, w  = edges.shape
                    mask  = np.zeros_like(edges)
                    poly  = np.array([[(0,h),(w,h),(w,h//2),(0,h//2)]])
                    cv2.fillPoly(mask, poly, 255)
                    masked = cv2.bitwise_and(edges, mask)
                    lines  = cv2.HoughLinesP(masked, 1,
                                              __import__('numpy').pi/180,
                                              50, minLineLength=50,
                                              maxLineGap=150)
                    if lines is not None:
                        clean = average_lines(frame, lines)
                        print(f"[Step {step}] Lane lines detected: "
                              f"{len(clean)}")

            # ── Medini: apply PID control toward next waypoint ──
            status = agent.run_step(carla_wp)

            # ── Dhanya: update dashboard ─────────────────────
            loc = vehicle.get_transform().location
            dash.update(status['speed'], loc)

            print(f"[Step {step+1}/{len(waypoints)}] "
                  f"Speed: {status['speed']:.1f} km/h | "
                  f"Throttle: {status['throttle']:.2f} | "
                  f"Steer: {status['steer']:.2f}")

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\n[Main] Interrupted by user.")

    finally:
        print("[Main] Cleaning up...")
        vehicle.destroy()
        dash.save('outputs/dashboard.png')
        print("[Main] Simulation complete. Dashboard saved.")


if __name__ == '__main__':
    main()