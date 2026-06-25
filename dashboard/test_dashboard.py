import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dashboard.monitor import Dashboard

class MockLocation:
    def __init__(self, x, y):
        self.x = x
        self.y = y

dash = Dashboard()
for i in range(50):
    dash.update(speed=i * 0.6, location=MockLocation(i * 2, i * 0.5))

dash.save('outputs/dashboard_test.png')
print("Dashboard test passed ✅ — check outputs/dashboard_test.png")