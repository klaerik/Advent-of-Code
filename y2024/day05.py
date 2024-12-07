from dataclasses import dataclass

import y2024.shared as shared

## Data
raw = shared.read_file("day05.txt")
test = shared.read_file("day05-test.txt")


## Functions
@dataclass
class Pages:
    raw: list[str]

    def __post_init__(self):
        self.rules, self.pages = self.parse_raw()
        self.order = self.get_order()

    def parse_raw(self):
        out = [[], []]
        for row in self.raw:
            if "|" in row:
                parsed = [int(x) for x in row.split("|")]
                out[0].append(tuple(parsed))
            else:
                parsed = [int(x) for x in row.split(",")]
                out[1].append(tuple(parsed))
        return out

    def get_order(self):
        lookup_left = {}
        lookup_right = {}
        for left, right in self.rules:
            if left not in lookup_left:
                lookup_left[left] = set()
            if right not in lookup_right:
                lookup_right[right] = set()
            lookup_left[left].add(right)
            lookup_right[right].add(left)
        all_rights = set()
        for rights in lookup_left.values():
            all_rights.update(rights)
        start = lookup_left.keys() - all_rights
        if len(start) > 1:
            raise LookupError("Too many starts!")
        start = start.pop()
        del lookup_left[start]
        end = all_rights - lookup_left.keys()
        out = [
            start,
        ]
        while lookup_left:
            all_rights = set()
            for rights in lookup_left.values():
                all_rights.update(rights)
            next_key = (lookup_left.keys() - all_rights).pop()
            out.append(next_key)
            del lookup_left[next_key]
        out.append(end.pop())
        return out

    def is_ordered(self, page: tuple) -> bool:
        ordered_page = sorted(page, key=self.order.index)
        return True if page == tuple(ordered_page) else False

    def get_middle_numbers(self):
        out = 0
        for page in self.pages:
            print(page)
            if self.is_ordered(page):
                middle = len(page) // 2
                out += page[middle]
                print(middle, page[middle])
        return out


pages = Pages(raw)
pages.rules
pages.pages
page = pages.pages[0]
pages.order
sorted(page, key=pages.order.index)
[pages.is_ordered(x) for x in pages.pages]


def solve(test):
    pages = Pages(test)
    return pages.get_middle_numbers()


def solve2(test):
    pass


## Testing
assert solve(test) == 143
assert solve2(test) == None


## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve2(raw)}")
