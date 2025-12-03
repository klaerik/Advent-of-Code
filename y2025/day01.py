import y2025.shared as shared
from dataclasses import dataclass
from collections import Counter, deque
import pyperclip

## Data
raw = shared.read_file("day01.txt")
test = shared.read_file("day01-test.txt")


## Functions
@dataclass
class Dial:
    clicks: int = 100
    count: int = 0
    count_any: int = 0
    start: int = 50

    def __post_init__(self):
        self.dial: deque = deque(range(self.clicks))
        while self.dial[0] != self.start:
            self.dial.rotate(1)

    def rotate(self, cmd: str):
        direction, distance = cmd[0], int(cmd[1:])
        for _ in range(distance):
            if direction == "L":
                self.dial.rotate(1)
            elif direction == "R":
                self.dial.rotate(-1)
            if self.dial[0] == 0:
                self.count_any += 1
        if self.dial[0] == 0:
            self.count += 1

    def rotations(self, commands: list[str]):
        for cmd in commands:
            self.rotate(cmd)


def solve(test):
    dial = Dial()
    dial.rotations(test)
    out = dial.count
    return out


def solve2(test):
    dial = Dial()
    dial.rotations(test)
    out = dial.count_any
    return out


## Testing
assert solve(test) == 3
assert solve2(test) == 6


## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve2(raw)}")
