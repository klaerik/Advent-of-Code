import y2022.shared as shared
from dataclasses import dataclass, field
from typing import Union, List
from collections import deque

## Data
raw = shared.read_file("day10.txt")
test = shared.read_file("day10-test.txt")

## Functions
@dataclass
class Signal:
    instructions: List[str]
    queue: deque = None
    register: int = 1
    cycle: int = 0
    signal_strength: List[int] = field(default_factory=list)
    crt: List[List[str]] = None

    def __post_init__(self):
        if self.queue is None:
            self.queue = deque([])
        self.crt = [[' '] * 40 for _ in range(6)]

    def read_instruction(self, instruction):
        if instruction == 'noop':
            cmd = instruction
            ops = [0]
        else:
            cmd,val = instruction.split()
            ops = [0, int(val)]
        self.queue.extend(ops)
    
    def process_cycle(self):
        self.cycle += 1
        self.write_crt()
        if self.cycle % 40 == 20:
            print(self.cycle, self.register, self.queue)
            self.signal_strength.append(self.cycle * self.register)
        self.register += self.queue.popleft()
        
    def resolve_signal(self):
        for instruction in self.instructions:
            self.read_instruction(instruction)
            self.process_cycle()
        while self.queue:
            self.process_cycle()
    
    def interesting_signals(self):
        return sum(self.signal_strength[:6])

    def write_crt(self):
        row, col = divmod(self.cycle - 1, 40)
        if col in (self.register-1, self.register, self.register+1):
            self.crt[row][col] = "#"

    def read_crt(self) -> str:
        return '\n'.join([''.join(row) for row in self.crt])



def solve(raw):
    signal = Signal(raw.copy())
    signal.resolve_signal()
    return signal.interesting_signals()

def solve2(raw):
    signal = Signal(raw.copy())
    signal.resolve_signal()
    return signal.read_crt()

## Testing
assert solve(test) == 13140

## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2:\n{solve2(raw)}")
