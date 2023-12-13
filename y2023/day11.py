import y2023.shared as shared
from dataclasses import dataclass

## Data
raw = shared.read_file("day11.txt")
test = shared.read_file("day11-test.txt")

## Functions


@dataclass
class GalaxyMap:
    raw: list[str]
    grid: dict | None = None
    expand_x: set | None = None
    expand_y: set | None = None
    expand_multiplier: int = 2

    def __post_init__(self):
        self.parse_raw()
        self.expansion_points()

    def parse_raw(self):
        out = {}
        id = 0
        raw = self.raw
        for y, row in enumerate(raw):
            for x, val in enumerate(row):
                if val == "#":
                    out[(x, y)] = id
                    id += 1
        self.grid = out

    def expansion_points(self) -> set:
        xs, ys = list(zip(*self.grid))
        xs, ys = set(xs), set(ys)
        self.expand_x = set(range(max(xs))) - xs
        self.expand_y = set(range(max(ys))) - ys

    def dist(self, start, stop, orientation: str) -> int:
        start, stop = sorted((start, stop))
        if start == stop:
            return 0
        diff = stop - start
        expand = self.expand_x if orientation == "x" else self.expand_y
        expand_dist = len(expand.intersection(range(start, stop)))
        expand_dist *= self.expand_multiplier - 1
        return diff + expand_dist

    def get_distance(self, x0: int, y0: int, x1: int, y1: int) -> int:
        dx = self.dist(x0, x1, "x")
        dy = self.dist(y0, y1, "y")
        return dx + dy

    def get_galaxy_pairs(self) -> list:
        galaxies = list(self.grid.keys())
        combos = []
        for i, g0 in enumerate(galaxies[: len(galaxies)]):
            for g1 in galaxies[i + 1 :]:
                combos.append((g0, g1))
        return combos

    def find_shortest_paths(self):
        pairs = self.get_galaxy_pairs()
        out = []
        for pair in pairs:
            coords = [coordinate for galaxy in pair for coordinate in galaxy]
            out.append(self.get_distance(*coords))
        return out


def solve(test, multi=1):
    galaxy = GalaxyMap(test, expand_multiplier=multi)
    return sum(galaxy.find_shortest_paths())


## Testing
assert solve(test) == 374
assert solve(test, 10) == 1030
assert solve(test, 100) == 8410

## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve(raw, 1000000)}")
