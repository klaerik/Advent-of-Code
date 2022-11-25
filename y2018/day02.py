from collections import Counter

infile = 'input/day2.txt'

raw = []
with open(infile) as file:
    for line in file:
        raw.append(line.rstrip('\n'))

groups = []
for box in raw:
    counts = {x for x in Counter(box).values() if x in {2,3}}
    str(counts)
    groups.extend(counts)

totals = Counter(groups)
checksum = totals[2] * totals[3]

print(checksum)    



while raw:
    box = raw.pop()
    for box2 in raw:
        common = []
        for a,b in zip(box, box2):
            if a == b:
                common.append(a)
        if len(box) == len(common) + 1:
            print(''.join(common))
            break

