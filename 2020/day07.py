import shared
import re
from math import prod

def parse_bags(raw):
    lookup = {}
    for rec in raw:
        key = re.search(r'^([\w ]+?) bag', rec).group(1)
        _ = lookup.setdefault(key, {})
        contents = rec.split('contain')[1].split(',')
        for item in contents:
            parsed = re.search(r'^\s*(\d+) ([\w ]+) bag', item)
            if parsed:
                bag = parsed.group(2)
                count = int(parsed.group(1))
                lookup[key][bag] = count
    return lookup

def find_all_parent_bags(bag_lookup, child_bag = 'shiny gold'):
    found = -1
    total_found = 0
    remain = set(bag_lookup.keys())
    desired = {child_bag,}
    while found:
        found = set()
        for i in remain:
            for j in bag_lookup[i]:
                if j in desired:
                    found.add(i)
        desired |= found
        remain -= found
        total_found += len(found)
    return total_found


def find_all_child_bags(bag_lookup, parent_bag = 'shiny gold'):
    bag_counts = 0
    for child,cnt in bag_lookup[parent_bag].items():
        child_cnt = find_all_child_bags(bag_lookup, parent_bag=child)
        bag_counts += cnt
        bag_counts += cnt * child_cnt
    return bag_counts


# Solve puzzle
raw = shared.read_file('2020/input/day07.txt')
bags = parse_bags(raw)

count = find_all_parent_bags(bags, child_bag = 'shiny gold')
print(f'Part 1: {count} bags can hold shiny gold bags')

children = find_all_child_bags(bags, parent_bag = 'shiny gold')
print(f'Part 2: {children} total bags are needed for 1 shiny gold bag')

