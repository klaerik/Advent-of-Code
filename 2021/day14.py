import shared
from collections import defaultdict, Counter

## Data
raw = shared.read_file('2021/input/day14.txt')

test = '''NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C'''.split('\n')

## Functions
def process_input(raw):
    start = Counter([a + b for a,b in zip(raw[0], raw[0][1:])])
    rules = build_mapping(raw[1:])
    return start, rules

def build_mapping(raw_rules):
    out = {}
    for rule in raw_rules:
        if not rule:
            continue
        start = rule[:2]
        target = rule[-1]
        out[start] = target
    return out

def insert_pairs(polymer, rules):
    changes = defaultdict(int)
    for pair in polymer:
        if pair in rules:
            new = rules[pair]
            count = polymer[pair]
            changes[pair] -= count
            changes[pair[0] + new] += count
            changes[new + pair[1]] += count
    for pair,count in changes.items():
        polymer[pair] += count
    return polymer

def take_steps(polymer, rules, steps):
    for _ in range(steps):
        polymer = insert_pairs(polymer, rules)
    return polymer

def calc_elements(polymer):
    counts = Counter()
    for k,v in polymer.items():
        counts[k[0]] += v / 2
        counts[k[1]] += v / 2
    for k in counts.keys():
        if counts[k] % 1:
            counts[k] += 0.5
    counts = counts.most_common()
    most = counts[0][1]
    least = counts[-1][1]
    return round(most - least)

def solve(raw, steps=10):
    polymer, rules = process_input(raw)
    polymer = take_steps(polymer, rules, steps)
    return calc_elements(polymer)

## Testing
#assert process_input(test)[0] == Counter('NNCB')
assert process_input(test)[1]['NC'] == 'B'
assert solve(test) == 1588
assert solve(test, 40) == 2188189693529

## Solutions
print(f'Part 1: after 10 rounds, the element calculation is {solve(raw)}')
print(f'Part 2: after 40 rounds, the element calculation is {solve(raw, 40)}')
