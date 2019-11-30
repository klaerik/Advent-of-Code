from typing import NamedTuple

class Point(NamedTuple):
    x: int
    y: int
    
class Clay():
    def __init__(self, x, y, grid):
        self.loc = Point(x, y)
        self.grid = grid
        grid[self.loc] = self
        self.type = '#'
        self.locked = True
    
    def pushed(self, pusher):
        return False


class Water(Clay):
    def __init__(self, x, y, grid):
        super().__init__(x, y, grid)
        self.locked = False
        self.type = 'w'
    
    @property
    def left(self):
        return Point(self.loc.x - 1, self.loc.y)
    @property
    def right(self):
        return Point(self.loc.x + 1, self.loc.y)
    @property
    def down(self):
        return Point(self.loc.x, self.loc.y + 1)

    def is_locked(self):
        down_thing = self.grid.get(self.down, None)
        row_status = {down_thing.locked,}
        for side in [self.left, self.right]:
            thing = self.grid.get(side, None)
            if thing is not None:
                row_status.add(self.check_row(self.loc))
            else:
                row_status.add(False)
        if row_status == {True,}:
            self.locked = True
        return self.locked

    def check_row(self, last_point):
        next_point = self.left if last_point == self.right else self.right
        next_thing = self.grid.get(next_point, None)
        down_thing = self.grid.get(self.down, None)
        print(self.loc, next_point, next_thing, down_thing)
        if self.type == '#':
            return True
        elif next_thing is None or down_thing is None:
            return False
        elif down_thing.locked is not True:
            return False
        else:
            return self.row_status(self.lock)
    
    def move(self, point):
        self.grid[point] = self.grid.pop(self.loc)
        self.loc = point
        
    def drip(self):
        if self.grid.get(self.down, None) is None:
            self.move(self.down)
            return True
        else:
            return False
            
    def spread(self):
        sides = [self.left, self.right]
        spread = False
        for side in sides:
            neighbor = self.grid.get(side, None)
            if neighbor is None:
                spread = Water(*side, self.grid)
        if spread:
            self.move(spread.loc)
            return True
        else:
            return False
            
    def flow(self):
        '''Try down, left, right pushes. Lock if can't move'''
        if self.locked:
            return False
#        elif self.check_row == True:
#            self
        else:
            flow_status = self.drip()
            if not flow_status:
                flow_status = self.spread()
            return flow_status


def import_file(file):
    raw = []
    with open(file) as f:
        for line in f:
            raw.append(line.rstrip('\n'))
    return raw

def find_clay(raw, grid):
    for group in raw:
        a,b = group.split(', ')
        a = a.split('=')
        a = {a[0]: [int(a[1]),]}
        b = b.split('=')
        b[1] = b[1].split('..')
        b = {b[0]: range(int(b[1][0]), int(b[1][1]) + 1)}
        a.update(b)
        for x in a['x']:
            for y in a['y']:
                Clay(x, y, grid)
    return grid

def represent_grid(grid):
    clay = {thing for thing in grid.values() if thing.type == '#'}
    xs = {i.loc.x for i in clay}
    ys = {i.loc.y for i in clay}
    start = Point(min(xs) - 1, 0)
    stop = Point(max(xs) + 1, max(ys) + 1)
    pretty = []
    for y in range(start.y, stop.y + 1):
        row = []
        for x in range(start.x, stop.x + 1):
            point = Point(x, y)
            thing = grid.get(point, None)
            if thing is None:
                thing = '.'
            else:
                thing = thing.type
            row.append(thing)
        pretty.append(''.join(row))
    return '\n'.join(pretty)

def in_range_drops(grid, start_y, end_y):
    return {Point(thing.loc.x, thing.loc.y) for thing in grid.values() if thing.type == 'w' and start_y <= thing.loc.y <= end_y}

def solve(file):
    raw = import_file(file)
    grid = {}
    grid = find_clay(raw, grid)
    clay_y = {thing.loc.y for thing in grid.values() if thing.type == '#'}
    start_y = min(clay_y)
    end_y = max(clay_y)    
    last = 0
    current = 1
    print(represent_grid(grid) + '\n')
    while last != current:
        last = current
        Water(500, 0, grid)
        water = [thing for point,thing in grid.items() if thing.type == 'w']
        water.sort(key=lambda i: (i.loc.y), reverse=True)
        for drop in water:
            drop.flow()
        current = in_range_drops(grid, start_y, end_y)
        current = current if len(current) > 0 else last + 1
        del_list = []
        for point in grid:
            if grid[point].type != 'w':
                continue
            elif point.y > end_y:
                del_list.append(point)
        for point in del_list:
            del grid[point]
            
    print(represent_grid(grid))
    solution = len(in_range_drops(grid, start_y, end_y))
    print(f"Found {solution} in range drops")
    return solution, grid

# Test cases
assert solve('input/day17-test.txt')[0] == 57
file = 'input/day17-test.txt'

# Part 1
file = 'input/day17.txt'
solution = solve('input/day17.txt')
print(f"Solution 1: {solution[0]}")

