from math import atan

atan(-1)

raw = []
with open('input/day10.txt') as f:
    for l in f:
        raw.append(l.strip())

def grid_to_coord(grid):
    points = []
    for y,line in enumerate(grid):
        for x,dot in enumerate(line):
            if dot == '#':
                points.append((x, y))
    return points

def get_slope(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    dx = x1 - x2
    dy = y1 - y2
    dx_scaled = 0 if dx == 0 else dx / abs(dx)
    if dx != 0:
        dy_scaled = dy / abs(dx)
    else:
        dy_scaled = 0 if dy == 0 else dy / abs(dy)
    return (dx_scaled, dy_scaled)

def get_radians(point_start, point_end):
    x1, y1 = point_start
    x2, y2 = point_end
    dx = x2 - x1
    dy = y2 - y1
    rad = atan(abs(dy/dx)) if dx != 0 else 0.5
    if dx < 0 and dy < 0:
        rad += 1
    elif dy < 0:
        rad = 2 - rad
    elif dx < 0:
        rad = 1 - rad
    return rad

def get_dist(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    dx = x2 - x1
    dy = y2 - y1
    dist = (dx ** 2 + dy ** 2) ** (1/2)
    return dist
    
def get_slopes(point, coord):
    out = {}
    for i in coord:
        if i == point:
            continue
        else:
            rads = get_radians(point, i)
            dist = get_dist(point, i)
            out[rads] = dist
    return out

def find_best_location(coord):
    best = 0
    for point in coord:
        visible = len(get_slopes(point, coord))
        #print(point, visible)
        if visible > best:
            best = visible
    return best


test = [x.strip() for x in 
       '''.#..#
          .....
          #####
          ....#
          ...##'''.split('\n')]
coord = grid_to_coord(test)
assert find_best_location(coord) == 8


best = find_best_location(grid_to_coord(raw))
print(f"Part 1: {best}")

