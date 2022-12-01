import y2022.shared as shared

## Data
raw = shared.read_file("day01.txt", include_blank_lines=True)
test = shared.read_file("day01-test.txt", include_blank_lines=True)


## Functions
def split_elf_inventories(raw):
    out = [[]]
    for val in raw:
        if not val:
            out.append([])
        else:
            out[-1].append(int(val))
    return out

def find_max_calories(inventories):
    return max([sum(elf) for elf in inventories])

def sum_calories(inventories, top_n=3):
    sums = [sum(elf) for elf in inventories]
    return sum(sorted(sums)[-top_n:])

def solve(raw):
    invs = split_elf_inventories(raw)
    return find_max_calories(invs)

def solve2(raw):
    invs = split_elf_inventories(raw)
    return sum_calories(invs)


## Testing
assert solve(test) == 24000
assert solve2(test) == 45000


## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve2(raw)}")
