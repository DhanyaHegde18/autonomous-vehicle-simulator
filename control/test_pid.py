"""
test_pid.py

Basic test for PIDController.
"""

import time

from control.pid_controller import PIDController


def main():

    pid = PIDController(
        kp=0.3,
        ki=0.02,
        kd=0.05
    )

    target_speed = 30
    current_speed = 0

    print("=" * 50)
    print("Testing PID Controller")
    print("=" * 50)

    for step in range(20):

        error = target_speed - current_speed

        output = pid.run_step(error)

        current_speed += output * 0.2

        print(
            f"Step {step+1:02d} | "
            f"Error: {error:.2f} | "
            f"Control: {output:.2f} | "
            f"Speed: {current_speed:.2f}"
        )

        time.sleep(0.1)

    print("\nPID Test Completed Successfully ")


if __name__ == "__main__":
    main()