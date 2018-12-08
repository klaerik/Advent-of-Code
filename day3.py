from collections import defaultdict

puzzle = 'input/day3.txt'

raw = []
with open(puzzle) as file:
    for line in file:
        raw.append(line.rstrip('\n'))

#print(raw)

coordinates = defaultdict(int)
claims = {}
for claim in raw:
#claim = '#123 @ 3,2: 5x4'
    id, _, start, finish = claim.split()
    x,y = [int(i) for i in start.rstrip(':').split(',')]
    w,h = [int(i) for i in finish.split('x')]
    points = set()
#    print(x, y, w, h)
    for x_i in range(x, x + w):
        for y_i in range(y, y + h):
            coordinates[(x_i, y_i)] += 1
            points.add((x_i, y_i))
    claims[id] = points

    
multi_claims = sum([1 for v in coordinates.values() if v > 1])            
print(f"Overlap: {multi_claims}")

safe_coordinates = {k for k,v in coordinates.items() if v == 1}

for k,v in claims.items():
    if safe_coordinates.issuperset(v):
       print(f"Safe: {k}")
       break