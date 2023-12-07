import y2023.shared as shared
from dataclasses import dataclass, field
import re

## Data
raw = shared.read_file("day05.txt")
test = shared.read_file("day05-test.txt")


## Functions
@dataclass
class Almanac:
    raw: list[str]
    seeds: list[int] | None = None
    maps: dict | None = None
    map_order: dict | None = None
    reversed: bool = False

    def __post_init__(self):
        self.parse_raw()
        if self.reversed:
            self.seeds_to_ranges()
            self.reverse_map()

    def seeds_to_ranges(self):
        seeds = self.seeds.copy()
        self.seeds = []
        while seeds:
            length, start = seeds.pop(), seeds.pop()
            self.seeds.append((start, start + length))
        self.seeds.sort()

    def reverse_map(self):
        out_map = {}
        for typ, mappings in self.maps.items():
            new_typ = self.map_order.get(typ)
            out_map[new_typ] = []
            for mapping in mappings:
                src_start, src_end, dest_start, range_length = mapping
                out_map[new_typ].append(
                    (
                        dest_start,
                        dest_start + range_length - 1,
                        src_start,
                        range_length,
                    )
                )
        self.maps = out_map
        self.map_order = {v: k for k, v in self.map_order.items()}

    def str_to_ints(self, raw_str: str) -> list[int]:
        return [int(x) for x in raw_str.split(" ") if x]

    def parse_raw(self):
        self.maps = {}
        self.map_order = {}
        for row in self.raw:
            if row.startswith("seeds"):
                self.seeds = self.str_to_ints(row.split(":")[1])

            elif m := re.match(r"(\w+)-to-(\w+) map", row):
                src = m.group(1)
                dest = m.group(2)
                self.map_order[src] = dest
                self.maps[src] = []

            elif src and row and row[0].isnumeric():
                dest_start, src_start, range_length = self.str_to_ints(row)
                src_end = src_start + range_length - 1
                self.maps[src].append((src_start, src_end, dest_start, range_length))

            else:
                src = None
                dest = None
            # print(src, dest)

        for typ in self.maps:
            self.maps[typ].sort()

    def translate_number(self, typ: str, num: int) -> tuple[str, int | None]:
        out_num = None
        for src_start, src_end, dest_start, _ in self.maps[typ]:
            if src_start <= num <= src_end:
                out_num = num - src_start + dest_start
                break
        if not out_num:
            out_num = num
        out_typ = self.map_order.get(typ, None)
        return (out_typ, out_num)

    def traverse_mapping(self, num: int, start_typ: str = "seed") -> int:
        typ = start_typ
        while self.map_order.get(typ):
            typ, num = self.translate_number(typ, num)
        return num

    def get_locations(self) -> list[int]:
        return [self.traverse_mapping(seed_num) for seed_num in self.seeds]

    def get_min_location_brute(self) -> int:
        out = float("inf")
        for start, length in zip(self.seeds[0::2], self.seeds[1::2]):
            print(f"Range: {start, length}...", flush=True)
            for i in range(start, start + length):
                new_num = self.traverse_mapping(i)
                out = min(out, new_num)
        return out

    def get_min_seed(self) -> int:
        for i in range(999999999):
            seed_num = self.traverse_mapping(i, start_typ="location")
            for start, end in self.seeds:
                if start <= seed_num <= end:
                    return i
        return None


def solve(raw):
    almanac = Almanac(raw)
    return min(almanac.get_locations())


def solve2(raw):
    almanac = Almanac(raw, reversed=True)
    return almanac.get_min_seed()


## Testing
assert solve(test) == 35
assert solve2(test) == 46


## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve2(raw)}")
