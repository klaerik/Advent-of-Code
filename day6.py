from collections import Counter


raw = []
with open('input/day6.txt') as file:
    for line in file:
        raw.append(tuple([int(x) for x in line.rstrip('\n').replace(' ','').split(',')]))

coordinates = raw

x_values = [x for x,y in coordinates]
y_values = [y for x,y in coordinates]
max_x = max(x_values)
max_y = max(y_values)

def dist(x1, y1, x2, y2):
    x = x1 - x2
    y = y1 - y2
    return abs(x) + abs(y)

def collect_distances(x, y, coordinates):
    distances = {}
    for x_i, y_i in coordinates:
        distance = dist(x, y, x_i, y_i)
        distances[(x_i, y_i)] = distance
    return distances

def closest(x, y, coordinates):
    distances = collect_distances(x, y, coordinates)
    vals = distances.values()
    min_val = min(vals)
    min_key = [k for k,v in distances.items() if v == min_val]
    if len(min_key) == 1:
        return min_key[0]
    else:
        None

def total_distance(x, y, coordinates):
    distances = collect_distances(x, y, coordinates)
    return sum(distances.values())

       
grid = []
ttl_dist_ok = 0
for y in range(max_y + 3):
    row = []
    for x in range(max_x + 3):
        row.append(closest(x, y, coordinates))
        # a bit inefficient here - checking distances twice...
        if total_distance(x, y, coordinates) < 10000:
            ttl_dist_ok += 1
    grid.append(row)


infinites = {i[-1] for i in grid} | {i[0] for i in grid} | set(grid[-1]) | set(grid[0])
infinites.remove(None)


flat = [coordinate for row in grid for coordinate in row if coordinate is not None and coordinate not in infinites]
counts = Counter(flat)
solution = counts.most_common(1)
print(f"Solution 1 - Max non-infinite area x/y and size: {solution}")

print(f"Solution 2 - Total distance under max - Area: {ttl_dist_ok}")
