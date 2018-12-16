import re

def read_file(file):
    raw = []
    with open(file) as file:
        for line in file:
            raw.append(line.rstrip('\n'))
    return raw

def parse_rules(rules):
    out = {'.': [], '#': []}
    for rule in rules:
        src, tgt = rule.split(' => ')
        if tgt == '#':
            out[tgt].append(src)
    for tgt in out:
        patterns = out[tgt]
        src = r'(?=(' + '|'.join(patterns).replace('.', '\.') + '))'
        if patterns:
            regex = re.compile(src)
        else:
            regex = None
        out[tgt] = regex
    return out

def next_row(plants, rules):
    last = plants[-1]
    row = []
    positions = set()
    for tgt, regex in rules.items():
        if regex is None:
            continue
        found = re.finditer(regex, last)
        for match in found:
            position = match.start()
            position += 2
            positions.add(position)
    for i in range(len(last)):
        if i in positions:
            row.append('#')
        else:
            row.append('.')
    return ''.join(row)

def calculate_score(row, padding):
    score = 0
    for i,plant in enumerate(row):
        if plant == '#':
            score += i - padding
    return score

def solve_puzzle(file, generations, cutoff=2000):
    raw = read_file(file)
    padding = min(generations, cutoff) * 2
    plants = [padding * '.' + raw[0].split()[2] + padding * '.',] 
    rules = parse_rules(raw[2:])
#    print(rules)
    solution = []
    for i in range(min(generations, cutoff)):
        plants.append(next_row(plants, rules))
    if generations < cutoff:
        solution = calculate_score(plants[-1], padding)
    else:
        last = calculate_score(plants[-2], padding)
        curr = calculate_score(plants[-1], padding)
        growth = curr - last
        generation = len(plants) - 1
        print(f"Growth: {growth}")
        solution = curr + (generations - generation) * growth
    print(f"Found solution: {solution}")
    return solution


assert solve_puzzle('input/day12-start.txt', 20) == 325

input_file = 'input/day12.txt'
solution = solve_puzzle(input_file, 20) 
print(f"Solution 1: {solution}")

assert solve_puzzle(input_file, 20) == 3738

assert solve_puzzle(input_file, 5000, 2000) == solve_puzzle(input_file, 5000, 5001) 

solution2 = solve_puzzle(input_file, 50000000000) 
print(f"Solution 2: {solution2}")
