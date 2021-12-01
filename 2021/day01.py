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
def track_depth(raw):
    out = 0
    last = None
    for depth in raw:
        if last:
            if last < depth:
                out += 1
        last = depth
    return out

def sliding_window(raw, window):
    nums = deque()
    current = 0
    out = []
    for depth in raw:
        nums.append(depth)
        current += depth
        if len(nums) == window:
            out.append(current)
            current -= nums.popleft()
    return out

def track_depth_sliding(raw, window=3):
    return track_depth(sliding_window(raw, window))


### Solve part 1
assert track_depth(test) == 7
print(f'Part 1: Depth increased {track_depth(raw)} times')

### Solve part 2
assert track_depth_sliding(test) == 5
print(f'Part 2: Depth increased {track_depth_sliding(raw)} times with sliding window of 3')
