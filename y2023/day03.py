import y2023.shared as shared
from dataclasses import dataclass

## Data
raw = shared.read_file("day03.txt")
test = shared.read_file("day03-test.txt")

## Functions

@dataclass
class Grid:
    raw: list[str]
    grid: dict | None = None
    nums: list | None = None

    def __post_init__(self):
        self.raw_to_grid()

    def raw_to_grid(self):
        self.grid = {}
        self.nums = []
        for y,row in enumerate(self.raw):
            num = None
            for x,val in enumerate(row):
                if val.isdigit():
                    if num is None:
                        num = Number(val, [(x,y)], self)
                        self.nums.append(num)
                    else:
                        num.raw += val
                        num.coordinates.append((x,y))
                    self.grid[(x,y)] = num
                else:
                    if val != '.':
                        self.grid[(x,y)] = val
                    num = None

    def get_neighbor_coordinates(self, x, y) -> set[tuple[int, int]]:
        neighbor_coordinates = set()
        options = ((0, 1), (0, -1), (-1, 0), (1, 0), 
                     (-1, 1), (-1, -1), (1, 1), (1, -1))
        for dx,dy in options:
            neighbor_coordinates.add((x+dx, y+dy))
        return neighbor_coordinates
    
    def get_neighbors(self, x, y) -> set:
        coords = self.get_neighbor_coordinates(x, y)
        out = set()
        for point in coords:
            if point in self.grid:
                out.add(self.grid[point])
        return out
    
    def get_part_numbers(self) -> list[int]:
        out = []
        for num in self.nums:
            if num.is_part_number():
                out.append(num.val)
        return out
    
    def find_gear_ratios(self) -> list[int]:
        out = []
        gears = [point for point,val in self.grid.items() if val == '*']
        for gear in gears:
            neighbors = {x for x in self.get_neighbors(*gear) if isinstance(x, Number)}
            if len(neighbors) == 2:
                ratio = neighbors.pop().val * neighbors.pop().val
                out.append(ratio)
        return out


@dataclass
class Number:
    raw: str
    coordinates: list | None = None
    grid: Grid | None = None
  
    @property
    def val(self):
        return int(self.raw)
    
    def is_part_number(self):
        for point in self.coordinates:
            neighbors = self.grid.get_neighbors(*point)
            for neighbor in neighbors:
                if not isinstance(neighbor, Number):
                    return True
        return False

    def __hash__(self):
        return hash(tuple(self.coordinates))
    
    def __repr__(self):
        return f"Number: {self.val}"


def solve(raw):
    grid = Grid(raw)
    return sum(grid.get_part_numbers())


def solve2(raw):
    grid = Grid(raw)
    return sum(grid.find_gear_ratios())


## Testing
assert solve(test) == 4361
assert solve2(test) == 467835


## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve2(raw)}")
