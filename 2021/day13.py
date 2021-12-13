import shared

## Data
raw = shared.read_file('2021/input/day13.txt')

test = '''6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5'''.split('\n')

## Functions
def process_input(raw):
    out = {'map':set(), 'folds':[]}
    for row in raw:
        if row.startswith('fold'):
            dir,val = row.split(' ')[2].split('=')
            out['folds'].append((dir,int(val)))
        else:
            out['map'].add(tuple([int(val) for val in row.split(',')]))
    return out

def fold_paper(dir, val, map):
    x_max = val if dir == 'x' else float('inf')
    y_max = val if dir == 'y' else float('inf')
    keep = set()
    for x,y in map:
        if x == x_max or y == y_max:
            continue # skip
        elif x > x_max:
            x,y = x_max - (x - x_max), y
        elif y > y_max:
            x,y = x, y_max - (y - y_max)
        keep.add((x,y)) 
    return keep

def solve(raw, first_only=True):
    input = process_input(raw)
    if first_only:
        folds = input['folds'][:1]
    else:
        folds = input['folds']
    map = input['map']
    for dir,val in folds:
        map = fold_paper(dir, val, map)
    if first_only:
        return len(map) 
    else:
        return pretty_print(map)

def pretty_print(map):
    x_max = y_max = 0
    for x,y in map:
        x_max = max(x, x_max)
        y_max = max(y, y_max)
    out = []
    for y in range(y_max+1):
        row = ''
        for x in range(x_max+1):
            if (x,y) in map:
                row += '#'
            else:
                row += '.'
        out.append(row)
    return '\n'.join(out)

## Testing
assert process_input(test)['folds'][0] == ('y', 7)
assert solve(test) == 17
assert solve(test, first_only=False) == '''#####
#...#
#...#
#...#
#####'''

## Solutions
print(f'Part 1: There are {solve(raw)} dots visible after the first fold')
print(f'Part 2: Final map looks like:')
print(solve(raw, first_only=False))

