import re
import typing

import y2025.shared as shared

## Data
raw = shared.read_file("day02.txt")[0].split(",")
test = shared.read_file("day02-test.txt")[0].split(",")


## Functions
def is_repeated(num: int | str) -> bool:
    num = str(num)
    quotient, remainder = divmod(len(num), 2)
    if remainder != 0:
        return False
    left, right = num[:quotient], num[quotient:]
    return left == right


def is_repeated2(num: int | str) -> bool:
    return bool(re.match(r"^(\d+)\1+$", str(num)))


def start_stop(num_range: str) -> tuple[int, int]:
    start, stop = num_range.split("-")
    return int(start), int(stop)


def get_range(num_range: str):
    start, stop = start_stop(num_range)
    for i in range(start, stop + 1):
        yield i


def get_invalid_nums(num_range: str, func: typing.Callable = is_repeated) -> list[int]:
    out = []
    for i in get_range(num_range):
        if func(i):
            out.append(i)
    return out


def solve(test):
    out = 0
    for rng in test:
        out += sum(get_invalid_nums(rng))
    return out


def solve2(test):
    out = 0
    for rng in test:
        out += sum(get_invalid_nums(rng, is_repeated2))
    return out


## Testing
assert is_repeated(123) is False
assert is_repeated(55) is True
assert is_repeated(123123) is True
assert is_repeated2(123) is False
assert is_repeated2(55) is True
assert is_repeated2(123123123) is True
assert solve(test) == 1227775554
assert solve2(test) == 4174379265


## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve2(raw)}")
