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

def sum_calories(inventories, top_n=1):
    sums = [sum(elf) for elf in inventories]
    return sum(sorted(sums)[-top_n:])

def solve(raw, n):
    invs = split_elf_inventories(raw)
    return sum_calories(invs, n)

## Testing
assert solve(test, 1) == 24000
assert solve(test, 3) == 45000

## Solutions
print(f"Solution to part 1: {solve(raw, 1)}")
print(f"Solution to part 2: {solve(raw, 3)}")
