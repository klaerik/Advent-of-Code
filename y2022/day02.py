import y2022.shared as shared

## Data
raw = shared.read_file('day02.txt')
test = shared.read_file('day02-test.txt')

## Functions
def split_rounds(raw):
    return [x.split() for x in raw]

map_play = {
    'A': 1,
    'B': 2,
    'C': 3,
    'X': 1,
    'Y': 2,
    'Z': 3,
}

def find_winner(x,y):
    lval = map_play[x]
    rval = map_play[y]
    if lval == rval:
        return 3
    elif lval + 1 == rval or lval - 2 == rval:
        return 6
    else:
        return 0

def score_rounds(rounds):
    out = []
    for left,right in rounds:
        out.append(map_play[right] + find_winner(left, right))
    return out

def zipper(x):
    return dict(zip('ABC', x))

def pick(x,y):
    if y == 'X':
        return zipper('ZXY')[x]
    elif y == 'Y':
        return zipper('XYZ')[x]
    elif y == 'Z':
        return zipper('YZX')[x]

def convert_rounds(rounds):
    return [[x, pick(x,y)] for x,y in rounds]

def solve(raw, convert=False):
    rounds = split_rounds(raw)
    if convert:
        rounds = convert_rounds(rounds)
    return sum(score_rounds(rounds))


## Testing
assert solve(test) == 15
assert solve(test, convert=True) == 12


## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve(raw, convert=True)}")
