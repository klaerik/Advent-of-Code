import shared
import re
from math import prod


def parse_notes(notes):
    out = {}
    rule = re.compile(r'^([\w\s]+):\s+(\d+)-(\d+).*?(\d+)-(\d+)')
    mode = 'rule'
    for rec in notes:
        if rule.match(rec):
            match = rule.search(rec)
            desc = match.group(1)
            range1 = set(range(int(match.group(2)), int(match.group(3))+1))
            range2 = set(range(int(match.group(4)), int(match.group(5))+1))
            out[desc] = range1.union(range2)
        elif rec.startswith('your ticket'):
            mode = 'your ticket'
        elif rec.startswith('nearby tickets'):
            mode = 'nearby tickets'
        elif mode == 'your ticket':
            out[mode] = tuple(int(x) for x in rec.split(','))
        elif mode == 'nearby tickets':
            out.setdefault(mode, []).append(tuple(int(x) for x in rec.split(',')))
    out['all rules'] = set()
    for k,v in out.items():
        if 'ticket' not in k:
            out['all rules'].update(v)
    return out

def find_invalid_values(notes):
    invalid = []
    for nearby in notes['nearby tickets']:
        for i in nearby:
            if i not in notes['all rules']:
                invalid.append(i)
    return invalid

def assign_valid_fields(notes):
    invalid = set(find_invalid_values(notes))
    nearby = []
    fields = {k:v for k,v in notes.items() if k not in ('all rules','nearby tickets','your ticket')}
    for ticket in notes['nearby tickets']:
        check = all([x not in invalid for x in ticket])
        if check:
            nearby.append(ticket)
    out = {}
    for i in range(len(nearby[0])):
        vals =  set(x[i] for x in nearby)
        for field,members in fields.items():
            remain = vals - members
            if not remain:
                out.setdefault(i, set()).add(field)
    singles = {y for x in out.values() for y in x if len(x) == 1}
    while max([len(x) for x in out.values()]) > 1:
        for field,vals in out.items():
            if len(vals) == 1:
                continue
            else:
                vals -= singles
                if len(vals) == 1:
                    singles.add(list(vals)[0])
    return [out[k].pop() for k in sorted(out.keys())]


# Validate logic
raw = shared.read_file('2020/input/day16_demo.txt')
notes = parse_notes(raw)
assert sum(find_invalid_values(notes)) == 71

# Solve puzzle - Part 1
raw = shared.read_file('2020/input/day16.txt')
notes = parse_notes(raw)
invalid = find_invalid_values(notes)
print(f'Part 1: {sum(invalid)} is the sum of the invalid entries')

# Part 2 - Fields in valid tickets
fields = assign_valid_fields(notes)
mult = prod([v for k,v in zip(fields, notes['your ticket']) if k.startswith('departure')])
print(f'Part 2 {mult} is the product of the departure fields on my ticket')