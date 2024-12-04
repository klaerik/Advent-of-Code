import y2024.shared as shared
from dataclasses import dataclass
from collections import Counter
import pyperclip

## Data
raw = shared.read_file("day01.txt")
test = shared.read_file("day01-test.txt")


## Functions
def parse_lists(raw: list[str]) -> tuple[list[int], list[int]]:
    out_left = []
    out_right = []
    for row in raw:
        left, right = row.split()
        out_left.append(int(left))
        out_right.append(int(right))
    return out_left, out_right


def get_dist(left, right) -> int:
    left.sort()
    right.sort()
    dist = 0
    for lnum, rnum in zip(left, right):
        dist += abs(lnum - rnum)
    return dist


def get_similarity(left, right) -> int:
    counts = Counter(right)
    similarity = 0
    for num in left:
        if num in counts:
            similarity += num * counts[num]
    return similarity


def solve(test):
    out = get_dist(*parse_lists(test))
    return out


def solve2(test):
    out = get_similarity(*parse_lists(test))
    return out


## Testing


assert solve(test) == 11
assert solve2(test) == None


## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve2(raw)}")
