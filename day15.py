from typing import NamedTuple
import os


def read_file(file):
    grid = []
    with open(file) as f:
        for line in f:
            grid.append(list(line.rstrip('\n')))
    return grid

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class Point(NamedTuple):
    x: int
    y: int

def view_grid(grid):
    return '\n'.join([''.join(i) for i in grid])

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
#    explored = {start,}
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
#                if point in explored:
#                    continue
#                explored.add(point)
                if point in search.keys():
                    continue
                thing = lookup(point, grid)
#                print(current, level, point, thing)
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
            nxt = [k for k,v in search.items() if last in v]
#            print(nxt)
            nxt.sort(key = lambda i: (i.y, i.x))
            path.append(nxt[0])
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

    def __str__(self):
        return f"Unit: {self.unit_type}, HP: {self.hp}, Loc: {self.loc}"
    
    @property
    def alive(self):
        return True if self.hp > 0 else False

    def attack(self, enemy):
        enemy.damage(self.ap)
    
    def damage(self, attack):
        self.hp -= attack
        if not self.alive:
            self.unit_type = '.'
            self.move(self.loc)
    
    def move(self, point):
        self.grid[self.loc.y][self.loc.x] = '.'
        self.loc = point
        self.grid[self.loc.y][self.loc.x] = self.unit_type

    def turn(self, units):
        self.idle = True
        if not self.alive:
            return "Dead"
        
        #Movement phase
        path = find_path(self.loc, self.enemy_type, self.grid)
#        print(f"Move {self.loc} to {path}")
        if len(path) > 0:
            self.move(path[-1])
            self.idle = False
        
        #Attack phase
        in_range = [loc for loc in next_steps(self.loc) if lookup(loc, self.grid) == self.enemy_type]
        enemies = [unit for unit in units if unit.loc in in_range]
        enemies.sort(key=lambda i: (i.hp, i.loc.y, i.loc.x))
        if len(enemies) > 0:
#            print(in_range)
#            print(in_range[0])
            self.attack(enemies[0])
            self.idle = False
        # end turn

def setup_combatants(unit_type, enemy_type, grid):
    units = []
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            point = Point(x,y)
            thing = lookup(point, grid)
            if thing in unit_type:
                units.append(Combatant(unit_type, enemy_type, point, grid))
    return units

def combat_complete(units):
    active = {i.unit_type for i in units if i.unit_type in {'G','E'}}
    return True if len(active) == 1 else False

def solve_puzzle(puzzle):
    grid = read_file(puzzle)    
    print(view_grid(grid))
    elves = setup_combatants('E','G',grid)
    goblins = setup_combatants('G','E',grid)
    units = elves + goblins
    rounds = 0
    while not combat_complete(units):
        print(f"Round {rounds}")
        units.sort(key=lambda i: (i.loc.y, i.loc.x))
        for unit in units:
            unit.turn(units)
        print(view_grid(grid))
        for unit in units:
            print(unit)
        rounds += 1
#        if rounds == 28:
#            break
#    rounds -= 1
    hp = sum([i.hp for i in units if i.unit_type in ('E','G')])
    solution = rounds * hp
    print(solution)
    return solution, rounds, hp, grid, units

solved = solve_puzzle('input/day15-test.txt')

solved2 = solve_puzzle('input/day15-test2.txt')

solved3 = solve_puzzle('input/day15-test3.txt')

solved4 = solve_puzzle('input/day15-test4.txt')
assert solved4[0] == 27730

solved5 = solve_puzzle('input/day15-test5.txt')
assert solved4[0] == 36334


