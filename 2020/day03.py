import shared
#from math import prod

# Go right 3, down 1, count trees
def sled(right, down, field):
    count = 0
    x,y = 0, 0
    bottom = len(field)
    while y < bottom:
        thing = field[y][x]
        if thing == '#':
            count += 1
        y += down
        x += right
        if x >= len(field[0]):
            x -= len(field[0])
    return count


file = 'input/day03.txt'
raw = shared.read_file(file)

# Part 1
part1 = sled(3, 1, raw)
print(f'Part 1: Hit {part1} trees')

# Part 2
slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
tree_hits = [sled(right, down, raw) for right,down in slopes]
part2 = shared.product(tree_hits)
print(f'Part 2: Multiple is {part2}')
