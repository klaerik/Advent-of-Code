import shared
import copy


def parse_instructions(raw):
    instructions = []
    for i in raw:
        cmd,num = i.split(' ')
        num = int(num)
        instructions.append((cmd, num))
    return instructions

class Console():
    def __init__(self, instructions, start_pos=0):
        self.instructions = instructions
        self.acc = 0
        self.seen = set()
        self.pos = start_pos 
    
    def step(self):
        pos = self.pos
        ins, val = self.instructions[pos] 
        if ins == 'acc':
            self.acc += val
            pos += 1
        elif ins == 'jmp':
            pos += val
        elif ins == 'nop':
            pos += 1
        self.pos = pos

    def calc(self):
        while self.pos not in self.seen:
            self.seen.add(self.pos)
            self.step()
            if self.pos == len(self.instructions):
                return True
            elif self.pos > len(self.instructions):
                return False
        return False
    


# Solve puzzle - Part 1
raw = shared.read_file('2020/input/day08.txt')
instructions = parse_instructions(raw)
console = Console(instructions)
console.calc() 
print(f'Part 1: accumulator == {console.acc} before second pass')

# Part 2 - find command that needs to be switched
check = list(console.seen)
while check:
    pos = check.pop()
    ins, val = instructions[pos]
    if ins in ('jmp','nop'):
        base = Console(instructions.copy())
        base.instructions[pos] = ('jmp', val) if ins == 'nop' else ('nop', val)
        result = base.calc()
        if result:
            print(f'Part 2: acc == {base.acc} if position {pos} is changed')
            break





