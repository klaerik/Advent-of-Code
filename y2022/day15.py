import y2022.shared as shared
from dataclasses import dataclass, field
import re

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

    def no_beacon(self, x: int, y: int) -> bool:
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


    

tunnels = Tunnels(test)
tunnels.count_unseen_positions(y=10)


def solve(raw, y):
    tunnels = Tunnels(raw)
    return tunnels.count_unseen_positions(y)



def solve2(raw):
    pass


## Testing
assert solve(test) == 26
assert solve2(test) == None


## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve2(raw)}")
