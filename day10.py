from typing import NamedTuple
import re
import scipy.signal


class Star(NamedTuple):
    x: int
    y: int
    dx: int = 0
    dy: int = 0

class FieldAttrs(NamedTuple):
    tips: int
    occluded: int
    area: int

#class Validate(NamedTuple):
    
def read_file(file):
    raw = []
    with open(file) as file:
        for line in file:
            raw.append(line.rstrip('\n'))
    
    regex = re.compile(r'^.*<\s?(-?\d+),\s*(-?\d+)>.*<\s?(-?\d+),\s*(-?\d+)>$')
    stars = {Star(int(x), int(y), int(dx), int(dy)) for record in raw for x,y,dx,dy in regex.findall(record)}
    return stars

def increment(stars, reverse=False):
    if reverse:
        return {Star(x-dx, y-dy, dx, dy) for x,y,dx,dy in stars}
    else:
        return {Star(x+dx, y+dy, dx, dy) for x,y,dx,dy in stars}

def validate(stars):
    sky = {Star(star.x, star.y) for star in stars}
    occluded = len(stars) - len(sky)
    neighbors = []
    for star in stars:
        possible = {Star(star.x + xi, star.y + yi) for xi in [-1, 0, 1] for yi in [-1, 0, 1] if not (xi, yi) == (0, 0)}
        star_neighbors = len(possible) - len(possible - sky)
        neighbors.append(star_neighbors)
    tips = len([tip for tip in neighbors if tip == 1])
    minmax = field_size(stars)
    area = abs(minmax['bottom_right'].x - minmax['top_left'].x) * abs(minmax['bottom_right'].y - minmax['top_left'].y)
    return(FieldAttrs(tips, occluded, area))

def field_size(stars):
    x = {x for x,y,dx,dy in stars}
    y = {y for x,y,dx,dy in stars}
    top_left = Star(min(x), min(y))
    bottom_right = Star(max(x), max(y))
    minmax = {'top_left': top_left, 'bottom_right': bottom_right}
    return minmax

def starfield(stars):
    size = field_size(stars)
    sky = {Star(star.x, star.y) for star in stars}
    field = []
    for y in range(size['top_left'].y, size['bottom_right'].y + 1):
        row = []
        for x in range(size['top_left'].x, size['bottom_right'].x + 1):
            if Star(x, y) in sky:
                row.append('#')
            else:
                row.append(' ')
        field.append(''.join(row))
    return field
                
def find_word(history):
    recent = history[-3:]
    candidate = recent[-2]
    if candidate.occluded != 0:
        return False
    min_tips = min([f.tips for f in recent])
    min_area = min([f.area for f in recent])
    if candidate == FieldAttrs(tips = min_tips, occluded = 0, area = min_area):
        return True
    else:
        return False

def solve_puzzle(file):
    stars = read_file(file)
    solved = False
    history = [validate(stars),]
    i = 0
    while not solved:
        stars = increment(stars)    
        i += 1
        history.append(validate(stars))
#        solved = find_word(history)
        if history[-1].area > history[-2].area:
            solved = True
    stars = increment(stars, reverse=True)
    i -= 1
    return i, stars


test_solution = ['#   #  ###',
                 '#   #   # ',
                 '#   #   # ',
                 '#####   # ',
                 '#   #   # ',
                 '#   #   # ',
                 '#   #   # ',
                 '#   #  ###']

assert starfield(solve_puzzle('input/day10-test.txt')[1]) == test_solution

# Puzzle 1
age, stars = solve_puzzle('input/day10.txt')
print(f"Solution 1:")
starfield(stars)

print(f"Solution 2: {age}")


stars = increment(stars, reverse=True)
starfield(stars)

stars = increment(stars, reverse=False)
starfield(stars)

