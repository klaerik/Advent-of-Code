import shared
from collections import Counter


def get_neighbors(x, y, grid):
    candidates = ((x+1, y), (x-1, y), (x, y+1), (x, y-1),
                  (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1))
    return [grid[y][x] for x,y in candidates if 0 <= x < len(grid[0]) and 0 <= y < len(grid)]

def get_extended_neighbors(x, y, grid):
    out = []
    candidates = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))
    for candidate in candidates:
        xi, yi = x, y
        status = '.'
        while status not in {'#','L'} and 0 <= xi < len(grid[0]) and 0 <= yi < len(grid):
            if xi != x or yi != y:
                status = grid[yi][xi]
            xi += candidate[0]
            yi += candidate[1]
        out.append(status)
    return out

def decide_seat_status(x, y, grid, extended_neighbors=False):
    current = grid[y][x]
    if current == '.':
        return current
    if extended_neighbors:
        neighbors = get_extended_neighbors(x, y, grid)
    else:
        neighbors = get_neighbors(x, y, grid)
    counts = Counter(neighbors)
    occupied = counts.get('#', 0)
    if current == 'L' and occupied == 0:
        return '#'
    elif current == '#' and occupied >= 4 and not extended_neighbors:
        return 'L'
    elif current == '#' and occupied >= 5 and extended_neighbors:
        return 'L'
    else:
        return current

def process_round(grid, extended_neighbors=False):
    new = []
    for y,row in enumerate(grid):
        new_row = []
        for x, _ in enumerate(row):
            new_row.append(decide_seat_status(x, y, grid, extended_neighbors=extended_neighbors))
        new.append(''.join(new_row))
    return new

def collapse_seating(grid):
    return ''.join(grid)

def count_occupied(grid):
    seats = collapse_seating(grid)
    return seats.count('#')


# Solve the puzzle
raw = shared.read_file('2020/input/day11.txt')

# Part 1:
grid = raw.copy() 
last = ''
current = collapse_seating(grid)
while last != current:
    last = current
    grid = process_round(grid)
    current = collapse_seating(grid)
print(f'Part 1: {count_occupied(grid)} occupied seats after everyone has settled')

# Part 2:
grid = raw.copy() 
last = ''
current = collapse_seating(grid)
while last != current:
    last = current
    grid = process_round(grid, extended_neighbors=True)
    current = collapse_seating(grid)
print(f'Part 2: {count_occupied(grid)} occupied seats after everyone has settled')

            

