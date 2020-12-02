 from itertools import combinations

file = '2020/input/day01.txt'
report = []
with open(file) as f:
    for line in f:
        num = line.strip()
        if num:
            report.append(int(num))

# Part 1
combos = combinations(report, 2)
valid = [combo for combo in combos if sum(combo) == 2020][0]

print(f'Answer 1: {valid[0] * valid[1]}')


# Part 2
combos = combinations(report, 3)
valid = [combo for combo in combos if sum(combo) == 2020][0]

print(f'Answer 2: {valid[0] * valid[1] * valid[2]}')
