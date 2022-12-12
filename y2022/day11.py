import y2022.shared as shared
from dataclasses import dataclass, field
from collections import deque
from typing import Callable, Deque, List
import re

## Data
raw = shared.read_file("day11.txt")
test = shared.read_file("day11-test.txt")

## Functions
def get_nums(text: str):
    return [int(x) for x in re.findall(r'\d+', text)]

@dataclass
class Item:
    """Something stolen by the monkeys."""
    worry: int
    prior_worry: int = None

    def set_worry(self, worry):
        self.prior_worry = self.worry
        self.worry = worry

@dataclass
class Monkey:
    """A stinky, annoying monkey."""
    label: int = None
    items: Deque[Item] = None
    operation: str = None
    test: str = None
    monkey_true: "Monkey" = None
    monkey_false: "Monkey" = None
    inspect_count: int = 0
    relief: bool = True
    lcm: int = 0

    def inspect(self):
        self.inspect_count += 1
        item = self.items.popleft()
        new = eval(self.operation, {'old': item.worry})
        if self.relief is True:
            new //= 3
        else:
            new %= self.lcm
        item.set_worry(new)
        if self.decide(new):
            self.monkey_true.items.append(item)
        else:
            self.monkey_false.items.append(item)

    def decide(self, val: int):
        return val % self.test == 0

    def take_turn(self):
        while self.items:
            self.inspect()
    
    def get_all_nums(self) -> set:
        nums = set()
        nums.update(set(get_nums(self.operation)))
        nums.add(self.test)
        return nums

@dataclass
class Horde:
    """A horrible, thieving, horde of monkeys."""
    definition: List[str]
    monkeys: List["Monkey"] = None
    lcm: int = 0

    def parser(self, relief=True):
        monkeys = []
        for row in self.definition:
            if row.startswith('Monkey'):
                monkeys.append([Monkey(relief=relief)])
            monkeys[-1].append(row)

        for i in monkeys:
            monkey = i[0]
            monkey.label = get_nums(i[1])[0]
            monkey.items = deque([Item(x) for x in get_nums(i[2])])
            monkey.operation = re.search(r'= (.*)', i[3]).groups(1)[0]
            monkey.test = get_nums(i[4])[0]
            monkey.monkey_true = monkeys[get_nums(i[5])[0]][0]
            monkey.monkey_false = monkeys[get_nums(i[6])[0]][0]
        self.monkeys = [x[0] for x in monkeys]
        self.calc_lcm()
        for monkey in self.monkeys:
            monkey.lcm = self.lcm

    def calc_lcm(self):
        nums = set()
        for monkey in self.monkeys:
            nums.update(monkey.get_all_nums())
        out = 1
        for num in nums:
            out *= num
        self.lcm = out

    def calc_monkey_business(self):
        scores = [monkey.inspect_count for monkey in self.monkeys]
        scores.sort()
        a,b = scores[-2:]
        return a * b

    def round(self):
        for monkey in self.monkeys:
            monkey.take_turn()


def solve(raw, rounds=20, relief=True):
    horde = Horde(definition=raw)
    horde.parser(relief=relief)

    for i in range(rounds):
        if i % 1000 == 0:
            print(f"Round: {i}", flush=True)
        horde.round()

    return horde.calc_monkey_business()

## Testing
assert solve(test) == 10605
assert solve(test, rounds=10000, relief=False) == 2713310158

## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve(raw, rounds=10000, relief=False)}")
