import y2022.shared as shared

## Data
raw = shared.read_file("day04.txt")
test = shared.read_file("day04-test.txt")

## Functions
def assign_ranges(raw):
    out = []
    for pair in raw:
        assignments = []
        for elf in pair.split(","):
            start, stop = elf.split("-")
            assignments.append((int(start), int(stop)))
        out.append(assignments)
    return out


def is_contained(pair):
    (start1, stop1), (start2, stop2) = pair
    contained = (start1 <= start2 and stop1 >= stop2) or (
        start2 <= start1 and stop2 >= stop1
    )
    return contained


def has_overlap(pair):
    (start1, stop1), (start2, stop2) = pair
    return stop1 >= start2 and start1 <= stop2


def solve(raw, func=is_contained):
    return len([x for x in assign_ranges(raw) if func(x)])


## Testing
assert solve(test) == 2
assert solve(test, has_overlap) == 4

## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve(raw, has_overlap)}")
