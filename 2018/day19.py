# From day 16
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

###########################333

from typing import NamedTuple

class Operation(NamedTuple):
    opcode: object
    a: int
    b: int
    c: int

lookup = {'addr': addr,
    'addi': addi,
    'mulr': mulr,
    'muli': muli,
    'banr': banr,
    'bani': bani,
    'borr': borr,
    'bori': bori,
    'setr': setr,
    'seti': seti,
    'gtir': gtir,
    'gtri': gtri,
    'gtrr': gtrr,
    'eqir': eqir,
    'eqri': eqri,
    'eqrr': eqrr}

def import_file(file):
    raw = []
    with open(file) as f:
        for line in f:
            raw.append(line.rstrip('\n'))
    
    ip = int(raw[0].split(' ')[1])
    ops = []
    for operation in raw[1:]:
        i = operation.split()
        ops.append(Operation(lookup[i[0]], int(i[1]), int(i[2]), int(i[3])))
    return ip, ops


def solve(file, reg0 = 0, store = None):
#    file = 'input/day19-test.txt'
#   reg0 = 1
    ip, ops = import_file(file)
    reg = [reg0, 0, 0, 0, 0, 0]
    i = 0
    while 0 <= reg[ip] < len(ops):
#    for x in range(1000):
        op = ops[reg[ip]]
        if op == Operation(addi, 2, 1, 2) and reg[1] > reg[2]:
            op = Operation(setr, 1, 0, 2)
            print(f"Override!")
        print(f"Registers: {reg}\tExecuting: {op}")
        instruction = op.opcode
        reg = instruction(reg, *op[1:])
#        print(f"Registers: {reg}")
        reg[ip] += 1
        i += 1
        if isinstance(store, list) and reg[ip] == 3:
            store.append(reg)
            print(reg)
    reg[ip] -= 1    
    print(f"Final registers: {reg} (Rounds: {i - 1})")
    return reg, store


test = solve('input/day19-test.txt')
assert test[0] == [6, 5, 6, 0, 0, 9]

file = 'input/day19.txt'
solution = solve(file)
print(f"Solution 1: {solution[0][0]}")


file = 'input/day19.txt'
solution = solve(file, reg0 = 1, store = [])



store = solution[1]
store[:100]
store[-100:]

#solution = solve('input/day19.txt', reg0=1)
#print(f"Solution 2: {solution[0]}")





