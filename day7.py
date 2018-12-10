#!/usr/bin/env python3

raw = []
with open('input/day7.txt') as file:
    for line in file:
        raw.append(line.rstrip('\n'))


steps = {}
possible = set()
for line in raw:
    step = line.split()
    upstream = step[1]
    downstream = step[7]
    steps.setdefault(upstream, dict()).setdefault('down',set()).add(downstream)
    for i in downstream:
        steps.setdefault(downstream, dict()).setdefault('up',set()).add(upstream)

steps

done = []
queue = []
up = set(steps.keys())
down = {j for i in steps.values() for j in i.get('down',[])}
possible = up | down
buffer = list(up - down)

len({1,} - {1,})

while len(possible) > len(done):
    buffer.sort()
    
    # Pick first node in buffer with satisfied dependencies
    ready = None
    for i,val in enumerate(buffer):
        upstream = steps[val].get('up',set())
        if len(upstream - set(done)) == 0:
            ready = i
            break
    #print(f"{buffer} {ready} START")
    active = buffer.pop(ready)
    #print(buffer)
    downstream = steps[active].get('down',set()) - set(done) - set(buffer)
    buffer.extend(list(downstream))
    done.append(active)
    #print(buffer, i, active)
    #print(done)

solution = ''.join(done)
print(f"Solution: {solution}")
    

