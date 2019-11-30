from typing import NamedTuple
import re

class Operation(NamedTuple):
    opcode: int
    a: int
    b: int
    c: int

def import_file(file):
    raw = []
    with open(file) as file:
        for line in file:
            raw.append(line.rstrip('\n'))
    puzzle = []
    group = {}
    for line in raw:
        start_stop = re.search(r'^(Before|After):\s+\[([\d, ]+)\]$', line)
        if start_stop:
            registers = [int(i) for i in start_stop[2].split(', ')]
            state = start_stop[1].lower()
            if state == 'before':
                group = {}
            group[state] = registers
            if state == 'after':
                puzzle.append(group)
        elif re.search(r'^\d', line):
            op = [int(i) for i in line.split()]
            group['op'] = op
    return puzzle
        

def addr(reg, a, b, c):
    reg[c] = reg[a] + reg[b]
    return reg

def addi(reg, a, b, c):
    reg[c] = reg[a] + b
    return reg

def mulr(reg, a, b, c):
    reg[c] = reg[a] * reg[b]
    return reg

def muli(reg, a, b, c):
    reg[c] = reg[a] * b
    return reg
   
def banr(reg, a, b, c):
    reg[c] = reg[a] & reg[b]
    return reg

def bani(reg, a, b, c):
    reg[c] = reg[a] & b
    return reg

def borr(reg, a, b, c):
    reg[c] = reg[a] | reg[b]
    return reg

def bori(reg, a, b, c):
    reg[c] = reg[a] | b
    return reg

def setr(reg, a, b, c):
    reg[c] = reg[a]
    return reg

def seti(reg, a, b, c):
    reg[c] = a
    return reg

def gtir(reg, a, b, c):
    reg[c] = 1 if a > reg[b] else 0
    return reg

def gtri(reg, a, b, c):
    reg[c] = 1 if reg[a] > b else 0
    return reg

def gtrr(reg, a, b, c):
    reg[c] = 1 if reg[a] > reg[b] else 0
    return reg

def eqir(reg, a, b, c):
    reg[c] = 1 if a == reg[b] else 0
    return reg

def eqri(reg, a, b, c):
    reg[c] = 1 if reg[a] == b else 0
    return reg

def eqrr(reg, a, b, c):
    reg[c] = 1 if reg[a] == reg[b] else 0
    return reg

def compare(puzzle, log=False):
    calcs = [addr, addi, mulr, muli, 
         banr, bani, borr, bori, 
         setr, seti, gtir, gtri,
         gtrr, eqir, eqri, eqrr]
    mapped = {}
    for i in range(16):
        mapped[i] = set(calcs)
    out = []
    for group in puzzle:
        reg = group['before']
        op = group['op']
        after = group['after']
        op_cnt = 0
        good_calc = set()
        for calc in calcs:
            result = calc(reg[:], *op[1:])
            if log:
                print(reg, op, result, after, calc.__name__, result == after)
            if result == after:
                op_cnt += 1
                good_calc.add(calc)
        out.append(op_cnt)
        mapped[op[0]] &= good_calc
#    mapped = {k: v.pop() for k,v in mapped.items()}
    for i in range(len(mapped)):
        singletons = {list(v)[0] for v in mapped.values() if len(v) == 1}
#        print(i,singletons)
        if len(singletons) == len(mapped):
            break
        for k,v in mapped.items():
            if len(v) == 1:
#                print(k,v)
                continue
            else:
                mapped[k] -= singletons
    mapped = {k: list(v)[0] for k,v in mapped.items()}
    return out, mapped

def solve(file):
    puzzle = import_file(file)
    results = compare(puzzle)[0]
    solution = len([x for x in results if x >= 3])
    return solution


test = import_file('input/day16-test.txt')
results = compare(test)
assert results[0] == [3,]
assert solve('input/day16-test.txt') == 1
assert mulr([3, 2, 1, 1], 2, 1, 1)

file = 'input/day16-part1.txt'
solution1 = solve('input/day16-part1.txt')
print(f"Solution 1: {solution1}")

# Solve part 2
puzzle = import_file('input/day16-part1.txt')
mapped = compare(puzzle)[1]

puzzle2 = []
with open('input/day16-part2.txt') as f:
    for line in f:
        puzzle2.append([int(i) for i in line.rstrip('\n').split()])
registers = [0, 0, 0, 0]
for op in puzzle2:
    calc = mapped[op[0]]
    registers = calc(registers, *op[1:])
print(f"Part 2, registers: {registers}\n\tSolution: {registers[0]}")





