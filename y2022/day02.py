import y2022.shared as shared

## Data
raw = shared.read_file("day02.txt")
test = shared.read_file("day02-test.txt")

## Functions
def split_rounds(raw):
    return [x.split() for x in raw]


def zipper(x):
    return dict(zip("ABC", x))


win = zipper("YZX")
loss = zipper("ZXY")
draw = zipper("XYZ")
hand = {"X": 1, "Y": 2, "Z": 3}
plays = dict(zip("XYZ", (loss, draw, win)))


def score_round(left, right):
    score = hand[right]
    if win[left] == right:
        score += 6
    elif draw[left] == right:
        score += 3
    return score


def score_rounds(rounds):
    return [score_round(*round) for round in rounds]


def pick_play(left, right):
    return plays[right][left]


def convert_rounds(rounds):
    return [[x, pick_play(x, y)] for x, y in rounds]


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
