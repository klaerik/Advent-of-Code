import shared
from collections import deque

def valid_xmas_num(num, group):
    for i in group:
        check = num - i
        if check in group and check != i:
            return True
    return False

def find_invalid_xmas(group, preamble=25):
    for i in range(preamble, len(group)):
        num = group[i]
        pre = set(group[i-preamble:i])
        check = valid_xmas_num(num, pre)
        if not check:
            return num
    return None

def find_contiguous_sum(target, group):
    nums = deque()
    total = 0
    i = 0
    while total != target:
        if total < target:
            new = group[i]
            nums.append(new)
            total += new
            i += 1
        elif total > target:
            total -= nums.popleft()
    return list(nums)

def find_xmas_weakness(target, group):
    nums = find_contiguous_sum(target, group)
    return sum([min(nums), max(nums)])


# Solve puzzle
raw = shared.read_file('2020/input/day09.txt')
clean = [int(x) for x in raw if x]

# Part 1
part1 = find_invalid_xmas(clean)
print(f'Part 1: {part1} is the first number to fail xmas cipher')

# Part 2
part2 = find_xmas_weakness(part1, clean)
print(f'Part 2: {part2} is the encryption weakness in xmas cipher')