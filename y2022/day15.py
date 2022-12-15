import re
from dataclasses import dataclass, field

import y2022.shared as shared

## Data
raw = shared.read_file("day15.txt")
test = shared.read_file("day15-test.txt")

## Functions
@dataclass
class Sensor:
    raw: str
    x: int = None
    y: int = None
    bx: int = None
    by: int = None
    d: int = None

    def __post_init__(self):
        self.preprocess()

    def preprocess(self):
        coordinates = re.findall(r'[x,y]=(-?\d+)', self.raw)
        x,y,bx,by = [int(i) for i in coordinates]
        self.x = x
        self.y = y
        self.bx = bx
        self.by = by
        self.d = self.calc_dist(bx, by)
        self.raw = ''

    def calc_dist(self, x: int, y: int) -> int:
        return abs(self.x - x) + abs(self.y - y)
    
    def in_range(self, x: int, y: int) -> bool:
        return self.calc_dist(x,y) <= self.d

    def skip_to_x(self, x: int, y: int) -> int:
        """Get the rightmost x."""
        return self.x + (self.d - abs(self.y - y)) + 1

@dataclass
class Tunnels:
    raw: list
    sensors: list = field(default_factory=list)

    def __post_init__(self):
        self.map_tunnels()
        self.raw = ''

    def map_tunnels(self):
        for row in self.raw:
            sensor = Sensor(row)
            self.sensors.append(sensor)
        self.sensors.sort(key=lambda sensor: sensor.x)

    def get_boundaries(self):
        min_x = min_y = float('inf')
        max_x = max_y = max_d = float('-inf')
        for sensor in self.sensors:
            min_x = min([sensor.x, sensor.bx, min_x])
            min_y = min([sensor.y, sensor.by, min_y])
            max_x = max([sensor.x, sensor.bx, max_x])
            max_y = max([sensor.y, sensor.by, max_y])
            max_d = max([sensor.d, max_d])
        return (min_x-max_d, min_y-max_d, max_x+max_d, max_y+max_d)

    def no_beacon(self, x: int, y: int):
        for sensor in self.sensors:
            if sensor.in_range(x, y) and (x,y) != (sensor.bx, sensor.by):
                return True
        return False

    def count_unseen_positions(self, y: int) -> int:
        min_x, min_y, max_x, max_y = self.get_boundaries()
        beacon_free = 0
        for x in range(min_x, max_x+1):
            if self.no_beacon(x,y):
                beacon_free += 1
        return beacon_free
        
    def find_tuning_freq(self, top_n):
        for y in range(0, top_n+1):
            if y % 100000 == 0:
                print("y=", y)
            x = 0
            while 0 <= x <= top_n:
                # print("x=", x)
                found = True
                for sensor in self.sensors:
                    if sensor.in_range(x,y):
                        x = sensor.skip_to_x(x,y)
                        found = False
                        if x >= top_n:
                            break
                if found:
                    return (x * 4000000) + y
                    # return (x,y)


def solve(raw, y):
    tunnels = Tunnels(raw)
    return tunnels.count_unseen_positions(y)

def solve2(raw, top_n):
    tunnels = Tunnels(raw)
    return tunnels.find_tuning_freq(top_n)


## Testing
assert solve(test, 10) == 26
assert solve2(test, 20) == 56000011


## Solutions
print(f"Solution to part 1: {solve(raw, 2000000)}")
print(f"Solution to part 2: {solve2(raw, 4000000)}")
