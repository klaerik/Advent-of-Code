import re
from dataclasses import dataclass
from typing import Literal

import y2024.shared as shared

## Data
raw = shared.read_file("day04.txt")
test = shared.read_file("day04-test.txt")
test2 = shared.read_file("day04-test2.txt")


## Functions
@dataclass
class Grid(dict):
    raw: list

    def __post_init__(self):
        self.data = list(reversed(self.raw))
        self.grid = self.parse_grid()
        self.shape_x = len(self.data[0])
        self.shape_y = len(self.data)
        self.shape = self.shape_y, self.shape_x

    def parse_grid(self):
        grid = {}
        for y, row in enumerate(self.data):
            for x, val in enumerate(row):
                point = (x, y)
                grid[point] = val
        return grid

    def __get__(self, point: tuple):
        return self.grid[point]

    def get_rows(self):
        return [row for row in self.data]

    def get_columns(self):
        cols = []
        for i in range(self.shape_x):
            col = []
            for row in self.data:
                col.append(row[i])
            cols.append("".join(col))
        return cols

    def get_diagonal(self, point: tuple, direction: Literal["up", "down"] = "up"):
        out = []
        move = 1 if direction == "up" else -1
        while point in self.grid:
            out.append(self.grid[point])
            point = point[0] + 1, point[1] + move
        return "".join(out)

    def get_diagonals(self):
        out = []
        for y in range(self.shape_y):
            out.append(self.get_diagonal((0, y), direction="up"))
            out.append(self.get_diagonal((0, y), direction="down"))
        out.reverse()
        for x in range(1, self.shape_x):
            out.append(self.get_diagonal((x, 0), direction="up"))
            out.append(self.get_diagonal((x, self.shape_y - 1), direction="down"))
        return out


grid = Grid(test)
grid.shape
grid.data
grid.grid
grid.get_rows()
grid.get_columns()
grid.get_diagonals()

grid.grid[(0, 1)]
grid.get_diagonal((0, 0))


def solve(test):
    grid = Grid(test)
    combos = []
    combos.extend(grid.get_rows())
    combos.extend(grid.get_columns())
    combos.extend(grid.get_diagonals())
    count = 0
    for combo in combos:
        count += len(re.findall(r"(?=XMAS|SAMX)", combo))
        # print(count, combo)
    return count


re.findall("x", "Y")

for combo in combos:
    print(combo.count("XMAS"), combo.count("SAMX"), combo)


def solve2(test):
    pass


## Testing
assert solve(test) == 18
assert solve2(test) == None


## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve2(raw)}")
