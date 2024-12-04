import y2023.shared as shared
from dataclasses import dataclass

## Data
raw = shared.read_file("dayXX.txt")
test = shared.read_file("dayXX-test.txt")


## Functions
@dataclass
class HangGlider:
    raw: list[str]
    grid: dict | None = None

    def build_grid(self):
        grid = {}
        for y, row in enumerate(self.raw):
            for x, pipe in enumerate(row):
                point = Point(pipe, x, y)


@dataclass
class Point:
    pipe: str
    x: int
    y: int
    left: "Point" | None = None
    right: "Point" | None = None
    distance: int | None = None


def solve(test):
    pass


def solve2(test):
    pass


## Testing
assert solve(test) == None
assert solve2(test) == None


## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve2(raw)}")
