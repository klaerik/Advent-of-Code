import y2023.shared as shared
from dataclasses import dataclass
from collections import deque
import re

## Data
raw = shared.read_file("day08.txt")
test = shared.read_file("day08-test.txt")

## Functions


@dataclass
class CamelMap:
    raw_map: str = ""
    instructions: deque | None = None
    network: dict | None = None
    positions: list | None = None
    is_ghost: bool = False

    def __post_init__(self):
        self.parse_map()
        self.positions = ["AAA"]
        if self.is_ghost:
            possible = set()
            for pair in self.network.values():
                possible.union(pair)
            self.positions = [x for x in possible if x.endswith("Z")]

    def parse_map(self):
        self.instructions = deque(self.raw_map[0])
        self.network = {}
        for mapping in self.raw_map[1:]:
            match = re.search(r"(\w+) = \((\w+), (\w+)\)", mapping)
            node = match.group(1)
            left = match.group(2)
            right = match.group(3)
            self.network[node] = (left, right)

    def step(self):
        move = self.instructions[0]
        self.instructions.rotate(-1)
        for i in range(len(self.positions)):
            position = self.positions[i]
            left, right = self.network[position]
            if move == "L":
                position = left
            elif move == "R":
                position = right
            self.positions[i] = position

    def count_steps(self) -> int:
        steps = 0
        while True:
            if steps % 1000000 == 0:
                print(steps)
            self.step()
            steps += 1
            if self.is_done:
                break
        return steps

    @property
    def is_done(self):
        if self.is_ghost:
            return all((x.endswith("Z") for x in self.positions))
        else:
            return self.positions == ["ZZZ"]


def solve(test, is_ghost=False):
    camelmap = CamelMap(test, is_ghost=is_ghost)
    return camelmap.count_steps()


def solve2(test):
    pass


## Testing
camelmap = CamelMap(test)
camelmap.instructions
camelmap.network

assert solve(test) == 2
assert solve(test, True) == 6


## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve2(raw)}")
