import y2022.shared as shared

## Data
raw = shared.read_file('day03.txt')
test = shared.read_file('day03-test.txt')

## Functions
def compartmentalize(raw):
    out = []
    for rucksack in raw:
        midpoint = len(rucksack) // 2
        out.append((rucksack[:midpoint], rucksack[midpoint:]))
    return out

def get_priority(item: str):
    if item.islower():
        return ord(item) - ord('a') + 1
    else:
        return ord(item) - ord('A') + 27

def find_dups(left, right):
    return (set(left) & set(right)).pop()

def score_rucksack(left, right):
    shared = find_dups(left, right)
    return get_priority(shared)

def score_rucksacks(rucksacks):
    return [score_rucksack(left, right) for left,right in rucksacks]

def solve(raw):
    rucksacks = compartmentalize(raw)
    scores = score_rucksacks(rucksacks)
    return sum(scores)

# part 2
def split_by_group(raw):
    out = []
    for i in range(0,len(raw),3):
        rucksacks = raw[i:i+3]
        out.append(rucksacks)
    return out

def find_badge(group):
    remain = set.intersection(*[set(x) for x in group])
    return remain.pop()

def solve2(raw):
    score = 0
    for group in split_by_group(raw):
        badge = find_badge(group)
        score += get_priority(badge)
    return score

## Testing
assert solve(test) == 157
assert solve2(test) == 70

## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve2(raw)}")
