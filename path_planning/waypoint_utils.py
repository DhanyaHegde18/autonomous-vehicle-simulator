"""
waypoint_utils.py

Utility functions for A* Path Planning
"""

import math


class Waypoint:
    """
    Represents a waypoint (grid coordinate).
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def position(self):
        return (self.x, self.y)

    def __repr__(self):
        return f"Waypoint({self.x}, {self.y})"


def euclidean_distance(p1, p2):
    """
    Calculates Euclidean distance between two coordinates.
    """
    return math.sqrt((p1[0] - p2[0]) ** 2 +
                     (p1[1] - p2[1]) ** 2)


def manhattan_distance(p1, p2):
    """
    Manhattan heuristic for A*.
    """
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def get_neighbors(node, grid):
    """
    Returns valid neighbouring cells.
    0 = free cell
    1 = obstacle
    """

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    neighbors = []

    rows = len(grid)
    cols = len(grid[0])

    for dx, dy in directions:

        nx = node[0] + dx
        ny = node[1] + dy

        if 0 <= nx < rows and 0 <= ny < cols:

            if grid[nx][ny] == 0:
                neighbors.append((nx, ny))

    return neighbors


def convert_path_to_waypoints(path):
    """
    Converts coordinate path into Waypoint objects.
    """

    return [Waypoint(x, y) for x, y in path]