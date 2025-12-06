from dataclasses import dataclass
import pyperclip
import y2025.shared as shared

## Data
raw = shared.read_file("day05.txt")
test = shared.read_file("day05-test.txt")


## Functions
@dataclass
class Inventory:
    raw: list[str]

    def __post_init__(self):
        self.parse()
        self.build_lookup()

    def parse(self):
        ranges = []
        values = []
        for rec in self.raw:
            if "-" in rec:
                start, stop = rec.split("-")
                ranges.append((int(start), int(stop)))
            else:
                values.append(int(rec))
        ranges.sort()
        self.ingredients = values
        self.ranges = ranges

    def build_lookup(self):
        lookup = dict(enumerate(self.ranges))
        self.lookup = lookup
        self.low = sorted([(v[0], k) for k, v in lookup.items()])
        self.high = sorted([(v[1], k) for k, v in lookup.items()])

    def find_ranges(self, ingredient: int) -> list:
        possible_low = set()
        possible_high = set()
        for val, idx in self.low:
            if ingredient >= val:
                possible_low.add(idx)
            else:
                break
        for val, idx in self.high[::-1]:
            if ingredient <= val:
                possible_high.add(idx)
        return possible_low.intersection(possible_high)

    def is_fresh(self, ingredient: int) -> bool:
        return bool(self.find_ranges(ingredient))

    def count_fresh(self) -> int:
        fresh = [x for x in self.ingredients if self.is_fresh(x)]
        return len(fresh)

    def combine_range(self, range_id: int) -> bool:
        low, high = self.lookup[range_id]
        combine = self.find_ranges(low)
        combine.update(self.find_ranges(high))
        if not len(combine) > 1:
            return False
        new_low = min([self.lookup[x][0] for x in combine])
        new_high = max([self.lookup[x][1] for x in combine])
        for i in combine:
            del self.lookup[i]
        self.lookup[i] = (new_low, new_high)
        self.ranges = list(self.lookup.values())
        self.build_lookup()
        return True

    def combine_all_ranges(self):
        fresh = True
        while fresh:
            fresh = False
            for i in self.lookup:
                if self.combine_range(i):
                    fresh = True
                    break

    def count_all_fresh(self) -> int:
        count = 0
        for start, stop in self.lookup.values():
            count += stop - start + 1
        return count


def solve(test):
    inv = Inventory(test)
    return inv.count_fresh()


def solve2(test):
    inv = Inventory(test)
    inv.combine_all_ranges()
    return inv.count_all_fresh()


## Testing
assert solve(test) == 3
assert solve2(test) == 14


## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve2(raw)}")
