from dataclasses import dataclass

import y2025.shared as shared

## Data
raw = shared.read_file("day03.txt")
test = shared.read_file("day03-test.txt")


## Functions
def get_max_joltage(bank: str) -> int:
    batteries = [int(x) for x in bank]
    right = batteries.pop()
    seen = []
    while batteries:
        left = batteries.pop()
        seen.append((left * 10) + right)
        if left > right:
            right = left
    return max(seen)


def get_max_joltage2(bank: str) -> int:
    batteries = [x for x in bank]
    current = batteries[-12:]
    batteries = batteries[:-12]
    seen = ["".join(current)]
    while batteries:
        left = batteries.pop()
        for i, val in enumerate(current):
            if left > val:
                current[i] = left
                left = val
                seen.append("".join(current))
            else:
                break
    print(seen)
    return max((int(x) for x in seen))


def solve(test):
    return sum((get_max_joltage(x) for x in test))


def solve2(test):
    return sum((get_max_joltage2(x) for x in test))


## Testing
assert get_max_joltage("987654321111111") == 98
assert get_max_joltage("811111111111119") == 89
assert solve(test) == 357

assert get_max_joltage2("987654321111111") == 987654321111
assert get_max_joltage2("811111111111119") == 811111111119
assert get_max_joltage2("234234234234278") == 434234234278
assert solve2(test) == 3121910778619


## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve2(raw)}")
