import y2022.shared as shared
from dataclasses import dataclass, field
from typing import List, Dict

## Data
raw = shared.read_file("day08.txt")
test = shared.read_file("day08-test.txt")

## Functions
@dataclass
class Tree:
    x: int
    y: int
    height: int
    neighbor_height: int = 999
    forest: "Forest" = None

    def add_neighbor(self, new_height):
        if new_height < self.neighbor_height:
            self.neighbor_height = new_height

    def is_visible(self) -> bool:
        return self.height > self.neighbor_height

    def look(self, direction: str) -> int:
        dirs = {"N": (0, 1), "S": (0, -1), "W": (-1, 0), "E": (1, 0)}
        x,y = self.x, self.y
        is_blocked = False
        seen = 0
        while not is_blocked:
            x += dirs[direction][0]
            y += dirs[direction][1]
            if (x,y) not in self.forest.trees:
                is_blocked = True
            else:
                seen += 1
                height = self.forest.trees[(x,y)].height
                if height >= self.height:
                    is_blocked = True
        return seen

    def scenic_score(self):
        score = 1
        for direction in ('N','S','E','W'):
            score *= self.look(direction)
        return score


@dataclass
class Forest:
    grid: List[str]
    trees: Dict[tuple, Tree] = field(default_factory=dict)

    def __post_init__(self):
        self.setup_trees()

    def setup_trees(self):
        for y, row in enumerate(self.grid):
            for x, height in enumerate(row):
                self.trees[(x, y)] = Tree(x, y, int(height), forest=self)

    def step(self, x: int, y: int, direction: str):
        dirs = {"N": (0, 1), "S": (0, -1), "W": (-1, 0), "E": (1, 0)}
        dx, dy = dirs[direction]
        return x + dx, y + dy

    def calc_row_heights(self, start_x: int, start_y: int, direction: str):
        x, y = start_x, start_y
        max_height_seen = -1
        while (x, y) in self.trees:
            tree = self.trees[(x, y)]
            tree.add_neighbor(max_height_seen)
            max_height_seen = max([max_height_seen, tree.height])
            x, y = self.step(x, y, direction)

    def calc_all_heights(self):
        for y in range(len(self.grid)):
            self.calc_row_heights(start_x=0, start_y=y, direction="E")
            self.calc_row_heights(
                start_x=len(self.grid[0]) - 1, start_y=y, direction="W"
            )
        for x in range(len(self.grid[0])):
            self.calc_row_heights(start_x=x, start_y=0, direction="N")
            self.calc_row_heights(start_x=x, start_y=len(self.grid) - 1, direction="S")

    def count_visible(self):
        return len([tree for tree in self.trees.values() if tree.is_visible()])

    def max_scenic_score(self) -> int:
        return max([tree.scenic_score() for tree in self.trees.values()])


def solve(raw):
    forest = Forest(raw)
    forest.calc_all_heights()
    return forest.count_visible()


def solve2(raw):
    forest = Forest(raw)
    return forest.max_scenic_score()


## Testing
assert solve(test) == 21
assert solve2(test) == 8


## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve2(raw)}")
