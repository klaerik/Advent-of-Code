import shared

def cluster_groups(raw):
    groups = ' '.join([x if x else ',' for x in raw]).split(',')
    groups = [x.strip().split() for x in groups if x]
    return groups

def any_yes_per_group(group):
    out = set()
    for member in group:
        out = out.union(set(member))
    return out

def all_yes_per_group(group):
    out = set(list(group[0]))
    for member in group[1:]:
        out = out.intersection(set(member))
    return out


# Solve puzzle for day 6
raw = shared.read_file('input/day06.txt', include_blank_lines=True)
clean = cluster_groups(raw)

part1 = sum([len(any_yes_per_group(group)) for group in clean])
print(f'Part 1: Found {part1} total response counts in groups')

part2 = sum([len(all_yes_per_group(group)) for group in clean])
print(f'Part 2: Found {part2} unanimous response counts in groups')

