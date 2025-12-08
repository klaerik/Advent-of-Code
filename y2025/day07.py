from dataclasses import dataclass

import y2025.shared as shared

## Data
raw = shared.read_file("day07.txt")
test = shared.read_file("day07-test.txt")


## Functions
@dataclass
class Point[tuple]:
    x: int
    y: int

    def below(self):
        return Point(self.x, self.y - 1)

    def below_sides(self):
        return Point(self.x - 1, self.y - 1), Point(self.x + 1, self.y - 1)


@dataclass
class TeleporterLab:
    raw: list[str]

    def __post_init__(self):
        self.parse()
        self.splits = 0
        self.paths = {}

    def parse(self):
        grid = {}
        for y, row in enumerate(self.raw[::-1]):
            for x, val in enumerate(row):
                grid[(x, y)] = val
        self.grid = grid

    def move_beam_down(self, start_coord: tuple):
        x, y = start_coord
        paths = self.paths.get(start_coord, 1)
        below = (x, y - 1)
        if self.grid.get(below) != "^":
            self.grid[below] = "|"
            self.paths[below] = self.paths.get(below, 0) + paths
        else:
            self.splits += 1
            for coord in [(x - 1, y - 1), (x + 1, y - 1)]:
                if coord in self.grid:
                    self.grid[coord] = "|"
                    self.paths[coord] = self.paths.get(coord, 0) + paths

    def process_row(self, y: int):
        for x in range(len(self.raw[0])):
            coord = (x, y)
            if self.grid.get(coord) in ("|", "S"):
                self.move_beam_down((x, y))

    def process_all_rows(self):
        for y in range(len(self.raw), 0, -1):
            self.process_row(y)

    def get_row_paths(self, y: int = 0) -> int:
        return sum((v for k, v in self.paths.items() if k[1] == y))


def solve(test):
    lab = TeleporterLab(test)
    lab.process_all_rows()
    return lab.splits


def solve2(test):
    lab = TeleporterLab(test)
    lab.process_all_rows()
    return lab.get_row_paths(3)


## Testing
assert solve(test) == 21
assert solve2(test) == 40


## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve2(raw)}")
