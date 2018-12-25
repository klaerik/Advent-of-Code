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

    def move(self, point):
        self.grid[point] = grid.pop(self.loc)
        self.loc = point
        
    def push(self, point):
        thing = self.grid.get(point, None)
        if thing is None:
            pushed = True
        else:
            pushed = thing.pushed(self)
            
        if pushed:
            self.move(point)
            return True
        else:
            return False
    
    def pushed(self, pusher):
        if self.locked:
            return False
        
        dx = self.loc.x - pusher.loc.x
        dy = self.loc.y - pusher.loc.y
        push_to = Point(self.loc.x + dx, self.loc.y + dy)

        if push_to == self.down:
            push_status = self.flow()
        else:
            push_status = self.push(self.down)
            if not push_status:
                push_status = self.push(push_to)
        print(self.loc, push_status)
        return push_status

    def flow(self):
        '''Try down, left, right pushes. Lock if can't move'''
        if self.locked:
            return False
        else:
            flow_status = self.push(self.down)
            print(flow_status)
            if not flow_status:
                sides = [self.left, self.right]
                for d in sides:
                    neighbor = self.grid.get(d, None)
                    if neighbor is None:
                        Water(*d, self.grid)
                for d in sides:
                    flow_status = self.push(d)
                    if flow_status:
                        break
            if not flow_status:
                self.locked = True
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


file = 'input/day17-test.txt'
raw = import_file(file)
grid = {}
grid = find_clay(raw, grid)

for i in range(50):
    Water(500, 0, grid)
    water = [thing for point,thing in grid.items() if thing.type == 'w']
    water.sort(key=lambda i: (i.loc.y), reverse=True)
    for drop in water:
        drop.flow()
    print(represent_grid(grid))



