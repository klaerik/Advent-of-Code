import y2022.shared as shared
from collections import deque, Counter


## Data
raw = shared.read_file("day06.txt")[0]

## Functions
def solve(raw, msg_len=4):
    seen = deque()
    for i, val in enumerate(raw, start=1):
        if len(seen) == msg_len:
            _ = seen.popleft()
        seen.append(val)
        if len(set(seen)) == msg_len:
            return i
    return None


def solve_better(raw, msg_len=4):
    seen = deque()
    counts = Counter()
    for i, val in enumerate(raw, start=1):
        seen.append(val)
        counts[val] += 1
        if len(seen) > msg_len:
            counts[seen.popleft()] -= 1
            if counts.most_common(1)[0][1] == 1:
                return i
    return None


## Testing
assert solve("bvwbjplbgvbhsrlpgdmjqwftvncz") == 5
assert solve("mjqjpqmgbljsphdztnvjfqwrcgsmlb", msg_len=14) == 19

## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve(raw, msg_len=14)}")
