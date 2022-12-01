import shared
from collections import deque

## Data
raw = '''Player 1 starting position: 6
Player 2 starting position: 3'''.split('\n')

test = '''Player 1 starting position: 4
Player 2 starting position: 8'''.split('\n')

## Functions
def process_input(raw):
    p1 = raw[0][-1]
    p2 = raw[1][-1]
    return int(p1), int(p2)

def play_game(p1, p2):
    die = deque(range(1,101))
    positions = [p1, p2]
    scores = [0, 0]
    die_rolls = 0
    while max(scores) < 1000:
        for player in range(len(positions)):
            pos = positions[player]
            roll = 0
            for _ in range(3):
                roll += die[0]
                die.rotate(-1)
                die_rolls += 1
            pos += roll
            while pos > 10:
                pos -= 10
            scores[player] += pos
            positions[player] = pos
            if scores[player] >= 1000:
                print(scores, die_rolls)
                break
    return die_rolls * min(scores)

def solve(raw):
    p1, p2 = process_input(raw)
    return play_game(p1, p2)

def play_dirac_game(p1, p2):
    p1_scores = [((p1, 0)), ((p2, 0))]



## Testing
p1, p2 = process_input(test)
assert play_game(p1, p2) == 739785
assert solve(test) == 739785

## Solutions
print(f'Part 1: Game ends after {solve(raw)}')