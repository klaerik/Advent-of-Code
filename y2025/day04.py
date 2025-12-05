from dataclasses import dataclass

import y2025.shared as shared

## Data
raw = shared.read_file("day04.txt")
test = shared.read_file("day04-test.txt")


## Functions
@dataclass
class Grid:
    raw: list[str]

    def __post_init__(self):
        self.grid = self.map_grid()

    def map_grid(self) -> dict:
        out = {}
        for y, row in enumerate(self.raw[::-1]):
            for x, val in enumerate(row):
                coord = (x, y)
                out[coord] = val
        return out

    def get_neighbor_coordinates(self, x, y) -> list[tuple]:
        out = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                out.append((x + dx, y + dy))
        return out

    def get_neighbors(self, x: int, y: int) -> list[str]:
        coords = self.get_neighbor_coordinates(x, y)
        out = []
        for coord in coords:
            if coord in self.grid:
                out.append(self.grid[coord])
        return out

    def is_accessible(self, x: int, y: int) -> bool:
        rolls = 0
        for coord in self.get_neighbor_coordinates(x, y):
            thing = self.grid.get(coord, ".")
            if thing == "@":
                rolls += 1
        return rolls < 4

    def count_accessible_rolls(self) -> int:
        count = 0
        for point, thing in self.grid.items():
            if thing == "@" and self.is_accessible(*point):
                count += 1
        return count

    def remove_rolls(self) -> int:
        removed = 0
        for coord in self.grid.keys():
            if self.grid[coord] == "@" and self.is_accessible(*coord):
                self.grid[coord] = "."
                removed += 1
        return removed


def solve(test) -> int:
    grid = Grid(test)
    return grid.count_accessible_rolls()


def solve2(test) -> int:
    grid = Grid(test)
    total_removed = 0
    while removed := grid.remove_rolls():
        total_removed += removed
    return total_removed


## Testing
assert solve(test) == 13
assert solve2(test) == 43


## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve2(raw)}")
