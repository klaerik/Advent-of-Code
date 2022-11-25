import shared

## Data
raw = shared.read_file('2021/input/day09.txt')

test = '''2199943210
3987894921
9856789892
8767896789
9899965678'''.split('\n')

## Functions
def find_neighbors(x, y, map):
    neighbors = ((x+1, y), (x-1, y), (x, y+1), (x, y-1))
    out = set()
    for x1,y1 in neighbors:
        if x1 < 0 or x1 >= len(map[0]) or y1 < 0 or y1 >= len(map):
            continue
        else:
            out.add((x1,y1))
    return out

def is_low(x, y, map):
    return int(map[y][x]) < min([int(map[y1][x1]) for x1,y1 in find_neighbors(x,y,map)])

def find_low_points(map):
    low = {}
    for y,row in enumerate(map):
        for x,val in enumerate(row):
            if is_low(x,y,map):
                low[(x,y)] = int(val) + 1
    return low

def map_basin(x,y,map):
    seen = set([(x,y)])
    neighbors = find_neighbors(x,y,map)
    while neighbors:
        x1,y1 = neighbors.pop()
        val = int(map[y1][x1])
        if val != 9:
            seen.add((x1,y1))
            new_neighbors = find_neighbors(x1, y1, map) - seen
            neighbors.update(new_neighbors)
    return seen

def calc_risk_levels(map):
    low_points = find_low_points(map)
    return sum(low_points.values())

def find_basin_product(map):
    basins = []
    seen = set()
    for y,row in enumerate(map):
        for x,val in enumerate(row):
            if int(val) != 9 and (x,y) not in seen:
                basin = map_basin(x, y, map)
                seen.update(basin)
                basins.append(len(basin))
    out = 1
    basins.sort(reverse=True)
    for basin in basins[:3]:
        out *= basin
    return out

## Testing
assert is_low(9, 0, test) is True
assert is_low(8, 0, test) is False
assert calc_risk_levels(test) == 15
assert find_basin_product(test) == 1134

## Solutions
print(f'Part 1: risk levels sum is {calc_risk_levels(raw)}')
print(f'Part 2: basin size multiple is {find_basin_product(raw)}')
