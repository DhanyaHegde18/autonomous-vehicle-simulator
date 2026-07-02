"""
pid_controller.py

Implements a generic PID (Proportional-Integral-Derivative)
controller for speed and steering control.
"""

import time


class PIDController:
    def __init__(self, kp, ki, kd):
        """
        Initialize PID gains.

        kp -> Proportional Gain
        ki -> Integral Gain
        kd -> Derivative Gain
        """

        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.previous_error = 0.0
        self.integral = 0.0
        self.previous_time = time.time()

    def run_step(self, error):
        """
        Computes PID output based on current error.
        """

        current_time = time.time()
        dt = current_time - self.previous_time

        # Prevent extremely small time intervals
        if dt < 0.05:
            dt = 0.05

        # Integral term
        self.integral += error * dt

        # Derivative term
        derivative = (error - self.previous_error) / dt

        # PID Output
        output = (
            self.kp * error +
            self.ki * self.integral +
            self.kd * derivative
        )
        # Limit controller output
        output = max(-1.0, min(output, 1.0))

        # Update previous values
        self.previous_error = error
        self.previous_time = current_time

        return output

    def reset(self):
        """
        Resets PID controller state.
        """

        self.previous_error = 0.0
        self.integral = 0.0
        self.previous_time = time.time()
          