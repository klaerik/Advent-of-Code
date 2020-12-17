import shared
from collections import Counter




def build_grid(raw):
    grid = {}
    for y,row in enumerate(raw):
        for x,val in enumerate(row):
            loc = (x, y, 0)
            if val == '#':
                grid[loc] = val
    return grid



def get_neighbor_locs(loc):
    x, y, z = loc
    candidates = ((x+xi, y+yi, z+zi) for xi in (-1,0,1) 
                    for yi in (-1,0,1) 
                    for zi in (-1,0,1) 
                    if (xi, yi, zi) != (0, 0, 0))
    return candidates

def get_neighbors(loc, grid):
    candidates = get_neighbor_locs(loc)
    return [grid.get(loc, '.') for loc in candidates]

def next_loc_state(loc, val, grid):
    neighbors = get_neighbors(loc, grid)
    count = neighbors.count('#')
    if val == '#' and count in (2, 3):
        out = '#'
    elif val == '.' and count == 3:
        out = '#'
    else:
        out = '.'
    return out

def get_all_locs(grid):
    out = set(grid.keys())
    for loc in grid.keys():
        out.update(get_neighbor_locs(loc))
    return out

def take_turn(grid):
    changed = {}
    locs = get_all_locs(grid)
    for loc in locs:
        val = grid.get(loc, '.')
        next_val = next_loc_state(loc, val, grid)
        if val == next_val:
            continue
        else:
            changed[loc] = next_val
    for loc,val in changed.items():
        if val == '.':
            del grid[loc]
        else:
            grid[loc] = val
    return grid

def solve_puzzle(grid, rounds=6):
    for _ in range(6):
        grid = take_turn(grid)
    count = list(grid.values()).count('#')
    return count

# Validate
demo = shared.read_file('2020/input/day17_demo.txt')
assert solve_puzzle(build_grid(demo), 6) == 112

# Solve puzzle
raw = shared.read_file('2020/input/day17.txt')
grid = build_grid(raw)
count = solve_puzzle(grid)
print(f'Part 1: {count} cubes are left in the active state after 6th cycle')


##############################################################
# Part 2 - add 4th dimension

# Redefine this guy
def get_neighbor_locs(loc):
    x, y, z, w = loc
    candidates = ((x+xi, y+yi, z+zi, w+wi) for xi in (-1,0,1) 
                    for yi in (-1,0,1) 
                    for zi in (-1,0,1) 
                    for wi in (-1,0,1)
                    if (xi, yi, zi, wi) != (0, 0, 0, 0))
    return candidates

# Add w dim to grid
def convert_grid(grid):
    out = {}
    for k,v in grid.items():
        loc = *k, 0
        out[loc] = v
    return out

# Validate
assert solve_puzzle(convert_grid(build_grid(demo))) == 848

# Solve
grid = convert_grid(build_grid(raw))
count = solve_puzzle(grid)
print(f'Part 2: {count} cubes are left in the active state after 6th cycle')

