"""
test_planner.py

Test file for A* Path Planning
"""

from route_planner import AStarPlanner


def main():

    # 0 = free space
    # 1 = obstacle

    grid = [

        [0,0,0,0,0,0],
        [0,1,1,1,0,0],
        [0,0,0,1,0,0],
        [0,1,0,0,0,0],
        [0,1,0,1,1,0],
        [0,0,0,0,0,0]

    ]

    start = (0,0)
    goal = (5,5)

    planner = AStarPlanner(grid)

    path = planner.plan(start, goal)

    print("\nGenerated Path:\n")

    for waypoint in path:
        print(waypoint)


if __name__ == "__main__":
    main()