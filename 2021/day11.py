import shared

## Data
raw = shared.read_file('2021/input/day11.txt')

test = '''5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526'''.split('\n')

data = process_input(test)
step(data)

## Functions
def process_input(raw):
    out = []
    for row in raw:
        out.append([int(x) for x in row])
    return out

def find_neighbors(x, y, x_max, y_max):
    neighbors = ((x+1, y), (x-1, y), (x, y+1), (x, y-1), (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1))
    out = set()
    for x1,y1 in neighbors:
        if x1 < 0 or x1 >= x_max or y1 < 0 or y1 >= y_max:
            continue
        else:
            out.add((x1,y1))
    return out

def step(map):
    x_max, y_max = len(map[0]), len(map)
    add_one = []
    to_flash = set()
    flashed = set()
    for y in range(y_max):
        for x in range(x_max):
            map[y][x] += 1
            if map[y][x] > 9:
                to_flash.add((x,y))
    while to_flash:
        while to_flash:
            x,y = to_flash.pop()
            map[y][x] = 0
            flashed.add((x,y))
            neighbors = find_neighbors(x, y, x_max, y_max) - flashed
            add_one.extend(list(neighbors))
        while add_one:
            x,y = add_one.pop()
            if map[y][x] != 0:
                map[y][x] += 1
            if map[y][x] > 9:
                to_flash.add((x,y))
    return flashed, map

def count_flashes(map, steps):
    count = 0
    for i in range(steps):
        flashed, map = step(map)
        count += len(flashed)
    return count

def solve(raw, steps=100):
    map = process_input(raw)
    count = count_flashes(map, steps)
    return count

def solve2(raw, step_max = 1000):
    map = process_input(raw)
    count = 0
    steps = 0
    while steps < step_max and count != len(map[0]) * len(map):
        flashes, map = step(map)
        count = len(flashes)
        steps += 1
    return steps


## Testing
assert process_input(test)[0] == [int(x) for x in '5483143223']
assert solve(test, 10) == 204
assert solve(test, 100) == 1656
assert solve2(test) == 195

## Solutions
print(f'Part 1: After 100 steps, there are {solve(raw)} flashes')
print(f'Part 2: All octopuses flash on the {solve2(raw)} step')