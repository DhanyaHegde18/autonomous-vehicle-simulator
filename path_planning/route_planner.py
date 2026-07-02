"""
route_planner.py

A* Path Planning Algorithm
"""

import heapq

from path_planning.waypoint_utils import (
    manhattan_distance,
    get_neighbors,
    convert_path_to_waypoints
)


class Node:
    def __init__(self, position):

        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

        self.parent = None

    def __lt__(self, other):
        return self.f < other.f


class AStarPlanner:

    def __init__(self, grid):

        self.grid = grid

    def reconstruct_path(self, current):

        path = []

        while current is not None:
            path.append(current.position)
            current = current.parent

        path.reverse()

        return convert_path_to_waypoints(path)

    def plan(self, start, goal):

        open_list = []

        closed_set = set()

        start_node = Node(start)
        goal_node = Node(goal)

        heapq.heappush(open_list, start_node)

        while open_list:

            current = heapq.heappop(open_list)

            if current.position == goal_node.position:
                return self.reconstruct_path(current)

            closed_set.add(current.position)

            neighbors = get_neighbors(current.position, self.grid)

            for neighbor in neighbors:

                if neighbor in closed_set:
                    continue

                neighbor_node = Node(neighbor)

                neighbor_node.g = current.g + 1

                neighbor_node.h = manhattan_distance(
                    neighbor,
                    goal_node.position
                )

                neighbor_node.f = (
                    neighbor_node.g +
                    neighbor_node.h
                )

                neighbor_node.parent = current

                skip = False

                for node in open_list:

                    if (
                        node.position == neighbor_node.position
                        and node.g <= neighbor_node.g
                    ):
                        skip = True
                        break

                if not skip:
                    heapq.heappush(open_list, neighbor_node)

        return []