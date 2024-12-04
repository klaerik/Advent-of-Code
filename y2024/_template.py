import y2024.shared as shared
from dataclasses import dataclass

## Data
raw = shared.read_file("dayXX.txt")
test = shared.read_file("dayXX-test.txt")

## Functions


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
