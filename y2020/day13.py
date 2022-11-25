import shared


raw = shared.read_file('2020/input/day13.txt')

ticket = int(raw[0])

buses = [int(x) for x in raw[1].split(',') if x != 'x']
buses.sort()

def find_first_bus(start, buses):
    time = start
    first = False
    while not first:
        for bus in buses:
            if time % bus == 0:
                first = bus
                return {'bus': first, 'time': time}
        time += 1

first_bus = find_first_bus(ticket, buses)
part1 = first_bus['bus'] * (first_bus['time'] - ticket)
print(f'Part 1: {part1} is the first bus seen')


vals = []
count = 0
for i in raw[1].split(','):
    if i.isdigit():
        vals.append((int(i), count))
    count += 1
vals.sort(reverse=True)
vals

max_val, max_diff = vals[0]
count = 100000000000000
while count % max_val != 0:
    count += 1
count -= max_diff
match = False
track = 0
while not match:
    count += max_val
    match = True
    for val,diff in vals[1:]:
        if (count + diff) % val != 0:
            match = False
            break
    if track == 10000000:
        print(count, flush=True)
    track += 1
print(count)


from numpy import lcm
lcm(647, 557)




