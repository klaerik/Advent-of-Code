import y2022.shared as shared
from dataclasses import dataclass, field
from typing import Set, Dict, Tuple, Deque
from collections import deque


## Data
raw = shared.read_file("day17.txt")[0]
test = shared.read_file("day17-test.txt")[0]

## Functions
@dataclass
class Cavern:
    jets: Deque[Tuple[int]]
    grid: Set[Tuple[int]] = None
    height: int = 0
    rock_shapes: Deque[str] = ('-','+','J','|','.')
    rock: "Rock" = None
    pattern: str = None
    pattern_height: int = None
    pattern_i: int = None

    def __post_init__(self):
        self.rock_shapes = deque(self.rock_shapes)
        self.jets = deque(self.jets)
        self.grid = {(i,0) for i in range(7)}

    def make_rock(self):
        shape = self.rock_shapes[0]
        self.rock_shapes.rotate(-1)
        self.rock = Rock(shape=shape, start_y=self.height+4, cavern=self)

    def move_rock(self):
        jet = self.jets[0]
        self.jets.rotate(-1)
        self.rock.move(jet) # Push rock
        self.rock.move('v') # Rock falls
        if not self.rock.falling:
            self.grid |= self.rock.coordinates
            self.height = max(self.height, max([y for _,y in self.rock.coordinates]))
            self.rock = None
        
    def drop_rock(self):
        self.make_rock()
        while self.rock:
            self.move_rock()

    def scale_up(self, i, count) -> int:
        repeat_iterations = i - self.pattern_i
        repeat_height = self.height - self.pattern_height
        remain_count = count - i
        multiplier = remain_count // repeat_iterations
        i += repeat_iterations * multiplier
        height_increase = repeat_height * multiplier
        print(f"Increasing height: {height_increase}")
        print(f"Increasing rocks: {i}")
        self.height += height_increase
        self.grid = {(x,y+height_increase) for x,y in self.grid}
        return i

    def drop_rocks(self, count: int):
        i = 0
        while i < count:
            if i == len(self.jets) * 10:
                self.pattern = self.snapshot()
                self.pattern_height = self.height
                self.pattern_i = i
            elif self.pattern and i % len(self.jets) == 0:
                snapshot = self.snapshot()
                if snapshot == self.pattern:
                    print(f"Repeat! Found at\n\titeration: {i}\n\theight: {self.height}")
                    i = self.scale_up(i, count)
                else:
                    print("Iteration: ", i)
            self.drop_rock()
            i += 1

    def snapshot(self):
        view = []
        for y in range(self.height-99, self.height+1):
            row = ''
            for x in range(7):
                if (x,y) in self.grid:
                    row += '#'
                else:
                    row += '.'
        return '\n'.join(view)


    def viz(self):
        view = []
        for y in range(self.height+10):
            row = ''
            for x in range(7):
                if (x,y) in self.grid:
                    row += '#'
                elif self.rock and (x,y) in self.rock.coordinates:
                    row += '@'
                else:
                    row += '.'
            view.append(row)
        return view[::-1]


@dataclass
class Rock:
    shape: str
    start_y: int
    cavern: Cavern
    coordinates: Set[Tuple[int]] = None
    falling: bool = True

    def __post_init__(self):
        self.build()

    def hits_cavern(self, coordinates: set):
        if coordinates & self.cavern.grid:
            return True
        elif any((not 0<=x<7 for x,_ in coordinates)):
            return True
        else:
            return False

    def move(self, direction: str):
        opts = {'<': (-1, 0), '>': (1, 0), 'v': (0, -1)}
        dx, dy = opts[direction]
        out = set()
        for x,y in self.coordinates:
            out.add((x+dx, y+dy))
        if not self.hits_cavern(out):
            self.coordinates = out
        elif direction == 'v':
            self.falling = False 
    
    def build(self):
        shapes = {
            '-': {(2,0), (3,0), (4,0), (5,0)},
            '+': {(3,0), (2,1), (3,1), (4,1), (3,2)},
            'J': {(2,0), (3,0), (4,0), (4,1), (4,2)},
            '|': {(2,0), (2,1), (2,2), (2,3)},
            '.': {(2,0), (3,0), (2,1), (3,1)},
        }
        self.coordinates = {(x, y+self.start_y) for x,y in shapes[self.shape]}


def solve(raw, rocks=2022):
    cavern = Cavern(jets=raw)
    cavern.drop_rocks(rocks)
    return cavern.height

def solve2(raw):
    pass


## Testing
assert solve(test) == 3068
assert solve(test, 1000000000000) == 1514285714288  


## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve(raw, 1000000000000)}")
