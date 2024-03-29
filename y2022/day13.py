from collections import deque
from dataclasses import dataclass, field
from typing import List

import y2022.shared as shared

## Data
raw = shared.read_file("day13.txt")
test = shared.read_file("day13-test.txt")
 
## Functions
@dataclass
class PacketDecoder:
    raw: List[str]
    pairs: List = field(default_factory=list)
    full: List = field(default_factory=list)
    dividers: list = None

    def __post_init__(self):
        self.generate_pairs()
        self.dividers = [[[2]], [[6]]]
        self.generate_full_list()

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
            # print(i, last, here, stack)

            if i == '[':
                new = list()
                here.append(new)
                here = new
                stack.append(new)
            elif i == ']':
                if len(stack) == 1:
                    here = stack.pop()
                else:
                    _ = stack.pop()
                    here = stack[-1]

        return out.pop()

    def generate_pairs(self):
        pair = []
        for text in self.raw:
            packet = self.str_to_packet(text)
            if pair:
                pair.append(packet)
                self.pairs.append(pair)
                pair = []
            else:
                pair.append(packet)
    
    def is_sorted(self, left: list, right: list) -> bool:
        """Is the pair sorted?"""
        sublist_status = None
        for i in range(max([len(left), len(right)])):
            if len(left) > i:
                a = left[i]
            else:
                return True
            if len(right) > i:
                b = right[i]
            else:
                return False
            if type(a) == int and type(b) == int:
                if a < b:
                    return True
                elif a > b:
                    return False
            else:
                a = [a] if type(a) == int else a
                b = [b] if type(b) == int else b
                sublist_status = self.is_sorted(a, b)
            if sublist_status is not None:
                return sublist_status
        return None

    def sum_sorted_indices(self):
        out = 0
        for i,pair in enumerate(self.pairs, start=1):
            if self.is_sorted(*pair):
                out += i
            # print(i, out, self.is_sorted(*pair), pair)
        return out

    def generate_full_list(self):
        for pair in self.pairs:
            for packet in pair:
                self.full.append(packet)
        for divider in self.dividers:
            self.full.append(divider)

    def sort(self):
        is_sorted = False
        round = 0
        while not is_sorted:
            if round % 100 == 0:
                print(f"Sort iteration: {round}")
            round += 1
            is_sorted = True
            for i in range(len(self.full)-1):
                left, right = self.full[i], self.full[i+1]
                if not self.is_sorted(left, right):
                    is_sorted = False
                    self.full[i], self.full[i+1] = right, left
    
    def get_decoder_key(self):
        key = 1
        for i,packet in enumerate(self.full, start=1):
            if packet in self.dividers:
                # print(i,packet)
                key *= i
        return key


def solve(raw):
    return PacketDecoder(raw).sum_sorted_indices()

def solve2(raw):
    decoder = PacketDecoder(raw)
    decoder.sort()
    return decoder.get_decoder_key()


## Testing
assert solve(test) == 13
assert solve2(test) == 140


## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve2(raw)}")
