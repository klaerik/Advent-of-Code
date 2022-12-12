import y2022.shared as shared
from dataclasses import dataclass, field
from collections import deque
from typing import Set, List, Deque, Dict

## Data
raw = shared.read_file("day12.txt")
test = shared.read_file("day12-test.txt")


## Functions

@dataclass 
class AreaMap:
    raw: List[str]
    grid: Dict[tuple, int] = field(default_factory=dict)
    end: tuple = None
    seen: Set[tuple] = field(default_factory=set)
    hikers: Deque["Hiker"] = field(default_factory=deque)
    solved_steps: int = None


    def build_grid(self, scenic=False):
        for y,row in enumerate(self.raw):
            for x,z in enumerate(row):
                if z == 'S':
                    self.hikers.append(Hiker(grid=self, x=x, y=y, z=0))
                    self.seen.add((x,y))
                    z = 'a'
                elif z.isupper():
                    self.end = (x,y)
                    z = 'z'
                elif scenic is True and z == 'a':
                    self.hikers.append(Hiker(grid=self, x=x, y=y, z=0))
                    self.seen.add((x,y))
                z = ord(z) - ord('a')
                self.grid[(x,y)] = z

    def move_hiker(self):
        hiker = self.hikers.popleft()
        new_hikers = hiker.schrodinger_move()
        for i in new_hikers:
            pos = (i.x,i.y)
            self.seen.add(pos)
            if pos == self.end and not self.solved_steps:
                self.solved_steps = i.steps
        self.hikers.extend(new_hikers)
    
    def solve(self):
        while self.solved_steps is None:
            self.move_hiker()
        return self.solved_steps

@dataclass
class Hiker: 
    grid: AreaMap
    x: int
    y: int
    z: int
    steps: int = 0

    def generate_quadrant(self):
        x,y = self.x, self.y
        return ((x,y+1), (x,y-1), (x+1,y), (x-1,y))

    def possible_routes(self):
        routes = []
        for pos in self.generate_quadrant():
            if pos in self.grid.seen:
                continue
            if pos in self.grid.grid and self.z >= self.grid.grid[pos]-1:
                routes.append(pos)
        return routes
    
    def schrodinger_move(self):
        hikers = []
        for x,y in self.possible_routes():
            z = self.grid.grid[(x,y)]
            hiker = Hiker(self.grid, x, y, z, self.steps + 1)
            hikers.append(hiker)
        return hikers


def solve(raw, scenic=False):
    area = AreaMap(raw)
    area.build_grid(scenic)
    return area.solve()

## Testing
assert solve(test) == 31
assert solve(test, scenic=True) == 29


## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve(raw, scenic=True)}")
