# main.py — Entry point for the AV Simulator

import carla
import time
from path_planning.route_planner import RoutePlanner
from control.vehicle_agent import VehicleAgent
from lane_detection.lane_detector import LaneDetector
from object_detection.object_detector import ObstacleDetector
from dashboard.monitor import Dashboard

# --- Config ---
START = (-10.0, 10.0, 0.5)
END   = (120.0, 10.0, 0.5)
TARGET_SPEED = 30.0  # km/h

def main():
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    world = client.get_world()
    print("[Main] Connected to CARLA server.")

    # Spawn ego vehicle
    bp_lib = world.get_blueprint_library()
    vehicle_bp = bp_lib.filter('vehicle.tesla.model3')[0]
    spawn_point = world.get_map().get_spawn_points()[0]
    vehicle = world.spawn_actor(vehicle_bp, spawn_point)
    print(f"[Main] Ego vehicle spawned: {vehicle.id}")

    # Initialize modules
    planner  = RoutePlanner(world)
    agent    = VehicleAgent(vehicle, target_speed=TARGET_SPEED)
    lane_det = LaneDetector(world, vehicle)
    obs_det  = ObstacleDetector(world, vehicle)
    dash     = Dashboard()

    # Plan route
    route = planner.get_route(START, END)
    waypoints = planner.get_waypoint_locations(route)

    try:
        step = 0
        while step < len(waypoints) - 1:
            target_wp = waypoints[min(step + 5, len(waypoints) - 1)]

            if obs_det.is_obstacle_ahead():
                print("[Main] Obstacle detected — braking!")
                vehicle.apply_control(carla.VehicleControl(brake=1.0))
            else:
                status = agent.run_step(target_wp)

            loc = vehicle.get_transform().location
            dash.update(agent.get_speed(), loc)

            step += 1
            time.sleep(0.05)

    finally:
        print("[Main] Cleaning up...")
        lane_det.destroy()
        obs_det.destroy()
        vehicle.destroy()
        dash.save()
        print("[Main] Done.")

if __name__ == '__main__':
    main()