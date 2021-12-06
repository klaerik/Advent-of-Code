import shared
from collections import Counter

## Data
raw = shared.read_file('2021/input/day05.txt')

test = '''0,9 -> 5,9
        8,0 -> 0,8
        9,4 -> 3,4
        2,2 -> 2,1
        7,0 -> 7,4
        6,4 -> 2,0
        0,9 -> 2,9
        3,4 -> 1,4
        0,0 -> 8,8
        5,5 -> 8,2'''
test = [x.strip() for x in test.split('\n')]


## Functions
def get_start_stop(raw):
    out = []
    for line in raw:
        if not line:
            continue
        a, _, b = line.split(' ')
        x0,y0 = [int(num) for num in a.split(',')]
        x1,y1 = [int(num) for num in b.split(',')]
        out.append(((x0,y0),(x1,y1)))
    return out

def traverse_segment(start, stop, diagonal=False):
    start,stop = sorted((start,stop))
    x0, y0 = start
    x1, y1 = stop
    if x0 == x1:
        return [(x0,y) for y in range(y0, y1+1)]
    elif y0 == y1:
        return [(x,y0) for x in range(x0, x1+1)]
    elif diagonal:
        if y0 < y1:
            return [(x0+i, y0+i) for i in range(y1 - y0 + 1)]
        else:
            return [(x0+i, y0-i) for i in range(y0 - y1 + 1)]
    else:
        return []

def build_mapping(vent_lines, diagonal=False):
    counts = Counter()
    for start,stop in vent_lines:
        points = traverse_segment(start, stop, diagonal)
        for point in points:
            counts[point] += 1
    return counts

def solve(raw, diagonal=False):
    counts = build_mapping(get_start_stop(raw), diagonal)
    return len([x for x in counts.values() if x > 1])

def pretty_print(counts):
    max_x = max_y = 0
    for x,y in counts:
        max_x = max((x, max_x))
        max_y = max((y, max_y))
    grid = [['.'] * (max_x+1) for y in range(max_y+1)]
    for point,val in counts.items():
        x,y = point
        grid[y][x] = str(val)
    return '\n'.join([''.join(row) for row in grid])


## Testing
assert get_start_stop(test)[0] == ((0,9),(5,9))
assert traverse_segment((0,1), (0,3)) == [(0,1), (0,2), (0,3)]
assert build_mapping(get_start_stop(test))[(1,9)] == 2
assert solve(test) == 5
assert build_mapping(get_start_stop(test), diagonal=True)[(4,4)] == 3
assert solve(test, diagonal=True) == 12
test_result = '''1.1....11.
.111...2..
..2.1.111.
...1.2.2..
.112313211
...1.2....
..1...1...
.1.....1..
1.......1.
222111....'''
assert pretty_print(build_mapping(get_start_stop(test), diagonal=True)) == test_result


## Solution for part 1
print(f'Part 1: two vent cloud lines overlap in {solve(raw)} points')

## Solution for part 2
print(f'Part 2: with diagonals there is overlap in {solve(raw, diagonal=True)} points')
