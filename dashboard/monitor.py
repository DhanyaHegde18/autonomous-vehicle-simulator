# Dhanya G Hegde — Simulation Dashboard

import matplotlib.pyplot as plt

class Dashboard:
    def __init__(self):
        self.speeds = []
        self.x_positions = []
        self.y_positions = []
        plt.ion()
        self.fig, self.axes = plt.subplots(1, 2, figsize=(12, 4))

    def update(self, speed, location):
        self.speeds.append(speed)
        self.x_positions.append(location.x)
        self.y_positions.append(location.y)
        self._render()

    def _render(self):
        self.axes[0].cla()
        self.axes[0].plot(self.speeds, color='blue')
        self.axes[0].set_title('Vehicle Speed (km/h)')
        self.axes[0].set_xlabel('Step')
        self.axes[0].set_ylabel('Speed')

        self.axes[1].cla()
        self.axes[1].plot(self.x_positions, self.y_positions,
                          color='green', marker='o', markersize=2)
        self.axes[1].set_title('Vehicle Trajectory')
        self.axes[1].set_xlabel('X')
        self.axes[1].set_ylabel('Y')

        plt.tight_layout()
        plt.pause(0.001)

    def save(self, path='outputs/dashboard.png'):
        plt.savefig(path)
        print(f"[Dashboard] Saved to {path}")