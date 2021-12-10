import shared

## Data
raw = shared.read_file('2021/input/day10.txt')

test = '''[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]'''.split('\n')

## Functions
def validate_chunk(chunk):
    points = {
        ')': 3,
        ']': 57, 
        '}': 1197,
        '>': 25137,}        
    parens = {'(':')', '[':']', '{':'}', '<':'>'}
    stack = []
    for char in chunk:
        if char in parens:
            stack.append(parens[char])
        else:
            expected = stack.pop()
            if expected != char:
                return points[char],[]
    return 0,''.join(reversed(stack))

def get_corrupted_score(chunks):
    out = 0
    for chunk in chunks:
        out += validate_chunk(chunk)[0]
    return out

def calc_points(chunk):
    autocomplete_points = {')':1, ']':2, '}':3, '>':4}
    score = 0
    for char in chunk:
        points = autocomplete_points[char]
        score *= 5
        score += points
    return score

def get_middle_score(chunks):
    scores = []
    for chunk in chunks:
        stderr,incomplete = validate_chunk(chunk)
        if stderr == 0:
            scores.append(calc_points(incomplete))
    middle = len(scores) // 2
    scores.sort()
    return scores[middle]

## Testing
assert validate_chunk('{([(<{}[<>[]}>{[]{[(<()>')[0] == 1197
assert validate_chunk('[({(<(())[]>[[{[]{<()<>>')[1] == '}}]])})]'
assert calc_points('])}>') == 294
assert get_corrupted_score(test) == 26397
assert get_middle_score(test) == 288957

## Solutions
print(f'Part 1: Navigation system corrupted chunk score is {get_corrupted_score(raw)}')
print(f'Part 2: Navigation middle incomplete score is {get_middle_score(raw)}')