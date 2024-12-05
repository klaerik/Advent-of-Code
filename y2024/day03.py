import re
from dataclasses import dataclass

import y2024.shared as shared

## Data
raw = shared.read_file("day03.txt")
test = shared.read_file("day03-test.txt")
test2 = shared.read_file("day03-test2.txt")


## Functions
def simple_multiply(raw) -> int:
    text = "\n".join(raw)
    groups = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", text)
    out = []
    for left, right in groups:
        out.append(int(left) * int(right))
    return sum(out)


def strip_dont(raw) -> list[str]:
    text = "".join(raw)
    out = ""
    line = ""
    do = True
    for i in text:
        line += i
        if do:
            out += i
        if line.endswith("do()"):
            do = True
            line = ""
        elif line.endswith("don't()"):
            do = False
            line = ""
    return out.split("\n")


class Computer:
    raw: list

    def parse(self):
        pass


def solve(test):
    return simple_multiply(test)


def solve2(test):
    return simple_multiply(strip_dont(test))


## Testing
assert solve(test) == 161
assert solve2(test2) == 48


## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve2(raw)}")
