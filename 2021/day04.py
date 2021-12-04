import shared

## Data
raw = shared.read_file('2021/input/day04.txt')

test = '''7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
'''
test = test.split('\n')

## Functions

def process_input(raw):
    draws = [int(x) for x in raw[0].strip().split(',')]
    puzzles = [Puzzle(puzzle_list) for puzzle_list in extract_puzzles(raw[1:])]
    return {'draws': draws, 'puzzles': puzzles}

def extract_puzzles(puzzle_list):
    puzzles = []
    for row in puzzle_list:
        puzzles.append([int(x) for x in row.split()])
    out = [[]]
    puzzle_size = len(puzzles[0])
    for row in puzzles:
        if not row:
            continue
        if len(out[-1]) == puzzle_size:
            out.append([])
        out[-1].append(row)
    return out

class Puzzle():
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.map_puzzle()
        self.found = [[0] * len(puzzle[0]), [0] * len(puzzle)]
        self.solved = False

    def map_puzzle(self):
        mapping = {}
        for y,row in enumerate(self.puzzle):
            for x,val in enumerate(row):
                point = (x,y)
                mapping.setdefault(val, set())
                mapping[val].add(point)
        self.mapping = mapping

    def calc_puzzle(self, ball):
        out = 0
        for row in self.puzzle:
            for val in row:
                if val != 'X':
                    out += val
        return out * ball

    def draw(self, ball):
        for entry in self.mapping.get(ball, []):
            x,y = entry
            self.puzzle[y][x] = 'X'
            self.found[0][x] += 1
            self.found[1][y] += 1
            if self.found[0][x] == len(self.puzzle[0]) or self.found[1][y] == len(self.puzzle):
                self.solved = True
        if self.solved:
            return self.calc_puzzle(ball)
        return None
    
    def __str__(self):
        out = ['#' * len(self.puzzle)]
        for row in self.puzzle:
            out.append(''.join([('  '+str(x))[-3:] for x in row]))
        return '\n'.join(out)
        
def solve(raw, pick_last=False):
    bingo = process_input(raw)
    remain = len(bingo['puzzles'])
    last = None
    for ball in bingo['draws']:
        for puzzle in bingo['puzzles']:
            if puzzle.solved:
                continue
            result = puzzle.draw(ball)
            if result:
                last = result
                remain -= 1
                if (pick_last and remain == 0) or not pick_last:
                    return result
    return last


## Testing
assert process_input(test)['draws'] == [int(x) for x in '7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1'.split(',')]
assert len(process_input(test)['puzzles']) == 3
assert solve(test) == 4512
assert solve(test, pick_last=True) == 1924

## Solution for part 1
print(f'Part 1: Final bingo score is {solve(raw)}')

## Solution for part 2
print(f'Part 2: Playing it safe, the score is: {solve(raw, pick_last=True)}')