from typing import NamedTuple
from collections import Counter

class Point(NamedTuple):
    x: int
    y: int

class Square():
    def __init__(self, loc, icon, grid):
        self.loc = Point(loc.x, loc.y)
        self.icon = icon
        self.grid = grid
        self.grid[loc] = self
        self.pending = None
    
    @property
    def neighbors(self):
        x_range = [-1, 0, 1]
        y_range = [-1, 0, 1]
        neighbors = []
        for y in y_range:
            for x in x_range:
                if x == 0 and y == 0:
                    continue
                point = Point(self.loc.x + x, self.loc.y + y)
                thing = self.grid.get(point, None)
                if thing is not None:
                    neighbors.append(thing)
        return neighbors
    
    def adjacent(self):
        neighbors = self.neighbors
        icons = []
        for neighbor in neighbors:
            icons.append(neighbor.icon)
        return Counter(icons)
        
    def next_icon(self):
        adjacent = self.adjacent()
        next_icon = self.icon
        if self.icon == '.' and adjacent['|'] >= 3:
            next_icon = '|'
        elif self.icon == '|' and adjacent['#'] >= 3:
            next_icon = '#'
        elif self.icon == '#':
            if adjacent['#'] >= 1 and adjacent['|'] >= 1:
                next_icon = '#'
            else:
                next_icon = '.'
        self.pending = next_icon
        return next_icon
        
    def change(self):
        self.icon = self.pending
        self.pending = None


def resource_value(grid):
    icons = Counter([thing.icon for thing in grid.values()])
    trees = icons['|']
    lumberyards = icons['#']
    rv = trees * lumberyards
    print(f"Found {trees} trees and {lumberyards} lumberyards - {rv} resource value")
    return rv
    

def import_file(file):
    raw = []
    with open(file) as f:
        for line in f:
            raw.append(line.rstrip('\n'))
    return raw

def represent_grid(grid):
    ys = {thing.loc.y for thing in grid.values()}
    xs = {thing.loc.x for thing in grid.values()}
    pretty = []
    for y in range(max(ys) + 1):
        row = []
        for x in range(max(xs) + 1):
            row.append(grid[(x,y)].icon)
        pretty.append(''.join(row))
    return '\n'.join(pretty) + '\n'

    
    

def solve_puzzle(file, length=10):
    raw = import_file(file)
    grid = {}
    for y,row in enumerate(raw):
        for x,icon in enumerate(row):
            point = Point(x,y)
            Square(point, icon, grid)
    scores = []
    print(represent_grid(grid))
    for i in range(length):
        for thing in grid.values():
            thing.next_icon()
        for thing in grid.values():
            thing.change()
        if i % 1000 == 0:
#            print(represent_grid(grid))
            rv = resource_value(grid)
            print(f"Iteration {i}\n\t\tResource value: {rv}")
        scores.append(resource_value(grid))
        print(i)
    solution = resource_value(grid)
    return (solution, grid, scores)
        

test = solve_puzzle('input/day18-test.txt')[0]
assert test == 1147


solution1 = solve_puzzle('input/day18.txt')[0]
print(f"Solution 1: {solution1}")

solution2,grid,scores = solve_puzzle('input/day18.txt', 1000)

# find repeat period - assuming no repeats!!
lookback = 200
counts = Counter(scores[-lookback:])
interval = len(counts)

mod_to_num = {}
for i,score in enumerate(scores):
    score = scores[i]
    mod = i % interval
    #print(i, i % interval, score)
    mod_to_num[mod + 1] = score

ttl_mins = 1000000000
ttl_mod = ttl_mins % interval
ttl_rv = mod_to_num[ttl_mod]
print(f"Solution 2: For {ttl_mins}, RVs are {ttl_rv}")




