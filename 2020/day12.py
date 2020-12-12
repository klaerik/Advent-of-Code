import shared
from collections import deque
from math import gcd


class Ship():
    def __init__(self):
        self.dir = deque(['E','S','W','N'])
        self.x = 0
        self.y = 0

    def turn(self, dir, degrees):
        rotation = {'L': 1, 'R': -1}
        times = degrees // 90
        times *= rotation[dir]
        self.dir.rotate(times)

    def move(self, dir, dist):
        if dir == 'N':
            self.y += dist
        elif dir == 'S':
            self.y -= dist
        elif dir == 'W':
            self.x -= dist
        elif dir == 'E':
            self.x += dist

    def forward(self, dist):
        self.move(self.dir[0], dist)

    def step(self, cmd):
        action = cmd[0]
        dist = int(cmd[1:])
        if action in ('L','R'):
            self.turn(action, dist)
        elif action == 'F':
            self.forward(dist)
        else:
            self.move(action, dist)


class WaypointShip():
    def __init__(self, waypoint_x=10, waypoint_y=1):
        self.x = 0
        self.y = 0
        self.wx = waypoint_x
        self.wy = waypoint_y

    def turn(self, dir, degrees):
        times = degrees // 90
        for i in range(times):
            if dir == 'L':
                self.wx, self.wy = -self.wy,  self.wx
            elif dir == 'R':
                self.wx, self.wy =  self.wy, -self.wx

    def move(self, dir, dist):
        if dir == 'N':
            self.wy += dist
        elif dir == 'S':
            self.wy -= dist
        elif dir == 'W':
            self.wx -= dist
        elif dir == 'E':
            self.wx += dist

    def forward(self, dist):
        self.x += self.wx * dist
        self.y += self.wy * dist

    def step(self, cmd):
        action = cmd[0]
        dist = int(cmd[1:])
        if action in ('L','R'):
            self.turn(action, dist)
        elif action == 'F':
            self.forward(dist)
        else:
            self.move(action, dist)

def manhattan_dist(x, y):
    return abs(x) + abs(y)

def traverse_commands(commands, model):
    ship = model()
    for command in commands:
        ship.step(command)
    return manhattan_dist(ship.x, ship.y)


# Solve puzzle
raw = shared.read_file('2020/input/day12.txt')

# Part 1
print(f'Part 1: ship dist = {traverse_commands(raw, model=Ship)}')

print(f'Part 2: ship dist = {traverse_commands(raw, model=WaypointShip)} if waypoints are used')
