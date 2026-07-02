# Add this to lane_detector.py — averages all lines into just left & right

import numpy as np
import cv2

def average_lines(image, lines):
    left_lines = []
    right_lines = []

    for line in lines:
        x1, y1, x2, y2 = line[0]
        if x2 == x1:
            continue  # skip vertical
        slope = (y2 - y1) / (x2 - x1)
        intercept = y1 - slope * x1

        if slope < -0.3:          # negative slope = left lane
            left_lines.append((slope, intercept))
        elif slope > 0.3:         # positive slope = right lane
            right_lines.append((slope, intercept))

    def make_line(image, params):
        slope, intercept = np.mean(params, axis=0)
        h = image.shape[0]
        y1 = h
        y2 = int(h * 0.6)
        x1 = int((y1 - intercept) / slope)
        x2 = int((y2 - intercept) / slope)
        return [(x1, y1, x2, y2)]

    averaged = []
    if left_lines:
        averaged.append(make_line(image, left_lines))
    if right_lines:
        averaged.append(make_line(image, right_lines))
    return averaged