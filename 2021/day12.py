import shared
from collections import deque

## Data
raw = shared.read_file('2021/input/day12.txt')

test = [

]

## Functions
def build_map(raw):
    map = {}
    for row in raw:
        start,stop = row.split('-')
        map.setdefault(start, set()).add(stop)
        map.setdefault(stop, set()).add(start)
    return map

def find_paths(map):
    out = {}
    paths, _ = spelunk(path, map)
    return len(paths)

def spelunk(path, )




## Testing


## Solution