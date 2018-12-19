from typing import NamedTuple

file = 'input/day15-test.txt'
grid = []
with open(file) as f:
    for line in f:
        grid.append(list(line.rstrip('\n')))

class Point(NamedTuple):
    x: int
    y: int

def print_grid(grid=grid):
    print('\n'.join([''.join(i) for i in grid]))

def next_steps(point):
    x, y = point
    return {Point(x-1, y), Point(x, y+1), Point(x+1, y), Point(x, y-1)}

def lookup(point, grid):
    x, y = point
    return grid[y][x]

def find_path(start, enemy, grid):
    '''Returns ([list, of, points, to, target], in_range T/F flag)'''
    search = {}
    current = start
    explored = {start,}
    search[current] = set()
    in_range = set()
    level = 0
    levels = {}
    levels[level] = {start,}
    while len(in_range) == 0 and len(levels[level]) > 0:
        level += 1
        levels[level] = set()    
        for current in levels[level - 1]:
            search[current] = set()
            for point in next_steps(current):
                if point in explored:
                    continue
                explored.add(point)
                thing = lookup(point, grid)
                print(current, level, point, thing)
                if thing in ('#','X'):
                    continue
                elif thing == '.':
                    search[current].add(point)
                    levels[level].add(point)
                elif thing == enemy:
                    in_range.add(current)    
    nearest = sorted(in_range, key = lambda i: (i.y, i.x))
    if len(nearest) == 0:
        return []
    else:
        path = [nearest[0],]
        for i in range(level - 1):
            last = path[-1]
            path.append([k for k,v in search.items() if last in v][0])
        return path[:-1]
        

class Combatant():
    def __init__(self, unit_type, enemy_type, start, grid):
        self.unit_type = unit_type
        self.enemy_type = enemy_type
        self.hp = 200
        self.ap = 3
        self.loc = Point(start.x, start.y)
        self.grid = grid
        self.idle = False
        
    @property
    def alive(self):
        return True if self.hp > 0 else False

    def attack(self, point, units):
        enemy = [unit for unit in units if unit.loc == point][0]
        enemy.hit(self.ap)
    
    def hit(self, attack):
        self.hp -= attack
        if not self.alive:
            self.unit_type = 'X'
            self.move(self.loc)
    
    def move(self, point):
        self.grid[self.loc.y][self.loc.x] = '.'
        self.loc = point
        self.grid[self.loc.y][self.loc.x] = self.unit_type

    def turn(self, units):
        self.idle = False
        in_range = [loc for loc in next_steps(self.loc) if lookup(loc, self.grid) == self.enemy_type]
        in_range.sort(key=lambda i: (i.y, i.x))
        if len(in_range) > 0:
            print(in_range)
            print(in_range[0])
            self.attack(in_range[0], units)
        else:
            path = find_path(self.loc, self.enemy_type, self.grid)
            print(path)
            if len(path) > 0:
                self.move(path[-1])
            else:
                self.idle = True  # end turn

def setup_combatants(unit_type, enemy_type, grid):
    units = []
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            point = Point(x,y)
            thing = lookup(point, grid)
            if thing in unit_type:
                units.append(Combatant(unit_type, enemy_type, point, grid))
    return units


elves = setup_combatants('E','G',grid)
goblins = setup_combatants('G','E',grid)
units = elves + goblins
units.sort(key=lambda i: (i.loc.y, i.loc.x))
for unit in units:
    unit.turn(units)
    print_grid(grid)

units[0].hp


