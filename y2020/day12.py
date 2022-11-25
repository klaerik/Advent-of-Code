import shared
from collections import deque


class Ship():
    def __init__(self):
        self.dir = deque(['E','S','W','N'])
        self.x = 0
        self.y = 0

    def loc(self):
        return self.x, self.y

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


class WaypointShip(Ship):
    def __init__(self, waypoint_x=10, waypoint_y=1):
        super().__init__()
        self.x = waypoint_x
        self.y = waypoint_y
        self.ship_x = 0
        self.ship_y = 0
    
    def loc(self):
        return self.ship_x, self.ship_y

    def turn(self, dir, degrees):
        times = degrees // 90
        for _ in range(times):
            if dir == 'L':
                self.x, self.y = -self.y,  self.x
            elif dir == 'R':
                self.x, self.y =  self.y, -self.x

    def forward(self, dist):
        self.ship_x += self.x * dist
        self.ship_y += self.y * dist


def manhattan_dist(x, y):
    return abs(x) + abs(y)

def traverse_commands(commands, model):
    ship = model()
    for command in commands:
        ship.step(command)
    return manhattan_dist(*ship.loc())


# Solve puzzle
raw = shared.read_file('2020/input/day12.txt')

# Part 1
print(f'Part 1: ship dist = {traverse_commands(raw, model=Ship)}')

print(f'Part 2: ship dist = {traverse_commands(raw, model=WaypointShip)} if waypoints are used')
