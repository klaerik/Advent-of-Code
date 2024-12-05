from dataclasses import dataclass

import y2024.shared as shared

## Data
raw = shared.read_file("day02.txt")
test = shared.read_file("day02-test.txt")


## Functions
def parse_reports(reports) -> list[list[int]]:
    out = []
    for report in reports:
        out.append([int(x) for x in report.split()])
    return out


def is_safe(report) -> bool:
    "Is this a safe report?"
    sign = None
    for left, right in zip(report, report[1:]):
        diff = left - right
        if sign is not None:
            if sign == 1 and diff <= 0:
                return False
            elif sign == -1 and diff >= 0:
                return False
        else:
            if diff > 0:
                sign = 1
            elif diff < 0:
                sign = -1
            else:
                return False
        if not (1 <= abs(diff) <= 3):
            return False
    return True


def is_safe_damped(report) -> bool:
    if is_safe(report):
        return True
    for i in range(len(report)):
        temp = report.copy()
        _ = temp.pop(i)
        if is_safe(temp):
            return True
    return False


def solve(test):
    reports = parse_reports(test)
    return sum([is_safe(report) for report in reports])


def solve2(test):
    reports = parse_reports(test)
    return sum([is_safe_damped(report) for report in reports])


## Testing
assert solve(test) == 2
assert solve2(test) == 4


## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve2(raw)}")
