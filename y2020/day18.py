import shared
from collections import deque
from copy import deepcopy


def clean_raw(raw):
    clean = raw.replace('(', '( ').replace(')', ' )')
    return clean.split(' ')

def group_and_format(clean):
    out = []
    buff = []
    deq = deque(clean)
    count = 0
    while deq:
        i = deq.popleft()
        if not count:
            if i == '(':
                count += 1
            else:
                out.append(i)
        else:
            if i == '(':            
                count += 1
            elif i == ')':
                count -= 1
            if count:
                buff.append(i)
        if buff and not count:
            out.append(group_and_format(buff))
            buff = []
    return deque(out)

def calc(grouped):
    total = 0
    mode = '+'
    while grouped:
        i = grouped.popleft()
        if i in ('+','*'):
            mode = i
            continue
        else:
            if type(i) is deque or type(i) is list:
                num = calc(i)
            elif i.isdigit():
                num = int(i)
            if mode == '+':
                total += num
            elif mode == '*':
                total *= num
    return total

def solve_row(row, add_first=False):
    clean = clean_raw(row)
    grouped = group_and_format(clean)
    if add_first:
        grouped = group_add_first(grouped)
    ttl = calc(grouped)
    return ttl

def group_add_first(grouped):
    out = deque()
    remain = deepcopy(grouped)
    while remain:
        i = remain.popleft()
        if i == '+':
            h = out.pop()
            j = remain.popleft()
            if type(j) is deque:
                j = group_add_first(j)
            out.append(deque([h, i, j]))
        elif type(i) is deque:
            i = group_add_first(i)
            out.append(i)
        else:
            out.append(i)
    return out


# Validate
assert solve_row('2 * 3 + (4 * 5)') == 26
assert solve_row('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 437
assert solve_row('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 12240
assert solve_row('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 13632

# Part 1
raw = shared.read_file('2020/input/day18.txt')
ttl = sum([solve_row(x) for x in raw])
print(f'Part 1: {ttl} is the sum of all instructions')


# Part 2
assert solve_row('1 + (2 * 3) + (4 * (5 + 6))', add_first=True) == 51
assert solve_row('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', add_first=True) == 23340

ttl = sum([solve_row(x, add_first=True) for x in raw])
print(f'Part 2: {ttl} is the sum if addition comes first in OO')
