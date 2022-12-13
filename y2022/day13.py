import y2022.shared as shared
from dataclasses import dataclass,field
from typing import List

## Data
raw = shared.read_file("day13.txt")
test = shared.read_file("day13-test.txt")
 
## Functions
@dataclass
class PacketDecoder:
    raw: List[str]
    pairs: List = field(default_factory=list)

    def preprocess(self):
        pass

    def str_to_packet(self, text:str):
        out = here = []
        stack = []
        last = ''
        for i in text:
            if i.isdigit() and last.isdigit():
                last += i
            elif last.isdigit():
                here.append(int(last))
                last = ''
            elif i.isdigit():
                last = i

            if i == '[':
                new = []
                here.append(new)
                here = here[-1]
                stack.append(new)
            elif i == ']':
                _ = stack.pop()
                here = stack[-1]

        return out[0]
            
            






def solve(raw):
    pass


def solve2(raw):
    pass


## Testing
assert solve(test) == 13
assert solve2(test) == None


## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve2(raw)}")
