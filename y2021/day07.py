import shared
from collections import Counter

## Data
raw = shared.read_file('2021/input/day07.txt')[0]

test = '16,1,2,0,4,2,7,1,2,14'

## Functions
def map_crabs(raw):
    positions = [int(x) for x in raw.split(',')]
    return Counter(positions)

def calc_fuel(crabs):
    positions = max(crabs.keys()) + 1
    left_crabs = 0 
    right_crabs = sum(crabs.values())
    current_fuel = sum([0 if position == 0 else count * position for position,count in crabs.items()])
    fuel_usage = [current_fuel]
    for i in range(positions):
        left_crabs += crabs.get(i,0)
        right_crabs -= crabs.get(i,0)
        current_fuel += left_crabs
        current_fuel -= right_crabs
        fuel_usage.append(current_fuel)
    return fuel_usage

def calc_fuel_nonconstant(crabs):
    positions = max(crabs.keys())
    fuel_usage = [0] * positions
    for i in crabs:
        crab_count = crabs[i]
        for direction in (range(i, positions), range(i, -1, -1)):
            total = 0
            mult = 0
            for j in direction:
                if j == i:
                    continue
                else:
                    mult += 1
                    total += mult * crab_count
                    fuel_usage[j] += total
    return fuel_usage     

def solve(raw, constant_fuel=True):
    crabs = map_crabs(raw)
    fuel = calc_fuel(crabs) if constant_fuel else calc_fuel_nonconstant(crabs)
    #best_position = min([(value,position) for position,value in enumerate(fuel)])[1]
    return min(fuel)

## Testing
assert solve(test) == 37
assert solve(test, constant_fuel=False) == 168

## Solutions
print(f'Part 1: the minimum fuel consumption is {solve(raw)}')
print(f'Part 2: with non-constant fuel use the min fuel is {solve(raw, constant_fuel=False)}')



