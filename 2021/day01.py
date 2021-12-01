from shared import read_file
from collections import deque


# Data
raw = read_file('input/day01.txt', convert=int)


test = [
    199,
    200,
    208,
    210,
    200,
    207,
    240,
    269,
    260,
    263,
    ]


# Functions
def track_depth(depths, window=None):
    if window:
        depths = sliding_window(depths, window)
    out = 0
    last = None
    for depth in depths:
        if last and last < depth:
            out += 1
        last = depth
    return out

def sliding_window(depths, window):
    nums = deque()
    total = 0
    out = []
    for depth in depths:
        nums.append(depth)
        total += depth
        if len(nums) == window:
            out.append(total)
            total -= nums.popleft()
    return out

### Solve part 1
assert track_depth(test) == 7
print(f'Part 1: Depth increased {track_depth(raw)} times')

### Solve part 2
window = 3
assert track_depth(test, window) == 5
print(f'Part 2: Depth increased {track_depth(raw, window)} times with sliding window of {window}')
