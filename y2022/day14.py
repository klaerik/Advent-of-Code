from dataclasses import dataclass, field

import y2022.shared as shared

## Data
raw = shared.read_file("day14.txt")
test = shared.read_file("day14-test.txt")

## Functions
@dataclass
class Cavern:
    raw: str
    grid: dict = field(default_factory=dict)
    floor: int = None
    hole: tuple = (500,0)
    endless: bool = True

    def __post_init__(self):
        self.init_grid()
        self.floor = max([y+2 for _,y in self.grid.keys()])
        if not self.endless:
            self.map_path(f"-5000,{self.floor} -> 5000,{self.floor}")

    def map_coordinates(self, start, stop):
        x0, y0 = start
        x1, y1 = stop
        if x0 == x1:
            y0, y1 = sorted([y0, y1])
            for y in range(y0, y1+1):
                self.grid[(x0, y)] = 'rock'
        else:
            x0, x1 = sorted([x0, x1])
            for x in range(x0, x1+1):
                self.grid[(x, y0)] = 'rock'
    
    def map_path(self, path: str):
        # print(path)
        steps = [step.split(',') for step in path.split(' -> ')]
        steps = [(int(x), int(y)) for x,y in steps]
        for coordinates in zip(steps, steps[1:]):
            self.map_coordinates(*coordinates)

    def init_grid(self):
        for path in self.raw:
            self.map_path(path)

    def is_clogged(self):
        return self.hole in self.grid

    def count_sand(self):
        return len([i for i in self.grid.values() if type(i) == Sand])

    def viz(self):
        min_x = min([x for x,_ in self.grid.keys()])
        max_x = max([x for x,_ in self.grid.keys()])
        out = []
        for y in range(0, self.floor+1):
            out.append([])
            for x in range(min_x, max_x+1):
                pos = (x,y)
                if pos not in self.grid:
                    out[-1].append(' ')
                elif self.grid[pos] == 'rock':
                    out[-1].append('#')
                else:
                    out[-1].append('o')
        return '\n'.join(''.join(row) for row in out)

@dataclass
class Sand:
    cavern: Cavern
    x: int = 500
    y: int = 0
    stopped: bool = False

    def next_steps(self):
        return ((self.x, self.y+1), (self.x-1, self.y+1), (self.x+1, self.y+1))

    def step(self):
        # self.cavern.grid[(self.x, self.y)] = 'x'
        self.stopped = True
        for pos in self.next_steps():
            if pos not in self.cavern.grid:
                self.x, self.y = pos[0], pos[1]
                self.stopped = False
                break
        if self.stopped is True:
            self.cavern.grid[(self.x, self.y)] = self
    
    def is_in_freefall(self):
        return self.y > self.cavern.floor

    def fall(self):
        while not self.stopped and not self.is_in_freefall():
            self.step()


def solve(raw, endless=True):
    cavern = Cavern(raw, endless=endless)
    while True:
        sand = Sand(cavern=cavern)
        sand.fall()
        if sand.is_in_freefall() or cavern.is_clogged():
            break
    return cavern.count_sand()

## Testing
assert solve(test) == 24
assert solve(test, endless=False) == 93


## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve(raw, endless=False)}")
