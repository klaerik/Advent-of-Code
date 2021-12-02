import re
import shared
from copy import deepcopy

def split_raw(raw):
    rules = {}
    messages = []
    for line in raw:
        if line.isalpha():
            messages.append(line)
        else:
            key,val = line.split(':')
            rules[key] = val.strip().strip('"')
    return rules, messages


def resolve_rules(key, rules, max_depth, depth=0):
    depth += 1
    print(depth)
    if depth > max_depth:
        return set()
    rule = rules[key]
    if rule.isalpha():
        return set((rule))
    out = []
    for group in rule.split('|'):
        subout = ('',)
        for lookup in group.strip().split():
            children = resolve_rules(lookup, rules, max_depth, depth=depth) #tuple of strings
            if children:
                subout = tuple([a + b  for a in subout for b in children if len(a + b) < max_depth])
        if len(subout[0]):
            out.append(subout)
    return set([child for parent in out for child in parent where len(child) < max_depth])

def count_matches(rules, messages, key='0'):
    max_depth = max([len(m) for m in messages])
    resolved = resolve_rules(key, rules, max_depth)
    return len([m for m in messages if m in resolved])


# Part 1
# Validate 
raw_demo = shared.read_file('2020/input/day19_demo.txt')
rules, messages = split_raw(raw_demo)
assert count_matches(rules, messages)



# Solve
rules, messages = split_raw(shared.read_file('2020/input/day19.txt'))
print(f"Part 1: {count_matches(rules, messages)} matches found for rule 0")

# Part 2
def update_rules(rules, messages):
    change = '8: 42 | 42 8','11: 42 31 | 42 11 31'
    change, _ = split_raw(change)
    for c in change:
        vals = change[c]
        single,recursive = [x.strip() for x in vals.split('|')]
        temp = [single]
        for _ in range(2):
            temp.append(re.sub(c, temp[-1], recursive))
        change[c] = ' | '.join(temp)
    for k,v in change.items():
        rules[k] = v
    return rules

raw_demo = shared.read_file('2020/input/day19_demo2.txt')
rules, messages = split_raw(raw_demo)
rules = update_rules(rules, messages)
assert count_matches(rules, messages) == 12

rules['8']
rules['11']
rules['31']

change = '8: 42 | 42 8','11: 42 31 | 42 11 31'
change, _ = split_raw(change)
