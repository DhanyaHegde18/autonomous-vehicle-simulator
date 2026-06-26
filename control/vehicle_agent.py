"""
vehicle_agent.py

Controls the CARLA vehicle using PID controllers.
"""

import math
import carla

from control.pid_controller import PIDController


class VehicleAgent:

    def __init__(self, vehicle, target_speed=30.0):
        """
        Initializes the vehicle controller.

        Args:
            vehicle: CARLA vehicle actor
            target_speed: Desired speed (km/h)
        """

        self.vehicle = vehicle
        self.target_speed = target_speed

        # Speed PID Controller
        self.speed_pid = PIDController(
            kp=0.3,
            ki=0.02,
            kd=0.05
        )

        # Steering PID Controller
        self.steer_pid = PIDController(
            kp=0.02,
            ki=0.0,
            kd=0.005
        )
    def get_speed(self):
        """
        Returns the current vehicle speed in km/h.
        """

        velocity = self.vehicle.get_velocity()

        speed = math.sqrt(
            velocity.x ** 2 +
            velocity.y ** 2 +
            velocity.z ** 2
        )

        return speed * 3.6
        
    def calculate_heading_error(self, target_location):
        """
        Calculates the heading error between the
        vehicle and the target waypoint.
        """

        transform = self.vehicle.get_transform()

        current_location = transform.location
        current_yaw = transform.rotation.yaw

        dx = target_location.x - current_location.x
        dy = target_location.y - current_location.y

        desired_yaw = math.degrees(math.atan2(dy, dx))

        error = desired_yaw - current_yaw

        while error > 180:
            error -= 360

        while error < -180:
            error += 360

        return error
    
    def run_step(self, target_wp):
        """
        Calculates throttle, steering, and brake commands
        and applies them to the vehicle.
        """

        # Get the waypoint location
        target_location = target_wp.transform.location

        # Current speed
        current_speed = self.get_speed()

        # Speed control
        speed_error = self.target_speed - current_speed
        throttle = self.speed_pid.run_step(speed_error)

        # Keep throttle between 0 and 1
        throttle = max(0.0, min(throttle, 1.0))

        # Steering control
        heading_error = self.calculate_heading_error(target_location)
        steer = self.steer_pid.run_step(heading_error)

        # Keep steering between -1 and 1
        steer = max(-1.0, min(steer, 1.0))

        # Brake logic
        brake = 0.0

        if current_speed > self.target_speed + 5:
            throttle = 0.0
            brake = 0.3

        # Send commands to CARLA
        control = carla.VehicleControl(
            throttle=throttle,
            steer=steer,
            brake=brake
        )

        self.vehicle.apply_control(control)

        return {
            "speed": current_speed,
            "throttle": throttle,
            "steer": steer,
            "brake": brake
        }