import shared
from collections import Counter

## Data
raw = shared.read_file('2021/input/day06.txt')[0]

test = "3,4,3,1,2"

## Functions
def preprocess(raw):
    return [int(num) for num in raw.split(',')]

def get_fish_counts(fish):
    return Counter(fish)

def update_fish_lineage(day, fish):
    if day in fish:
        parents = fish[day]
        fish[day] = 0
        fish[day + 7] += parents
        fish[day + 9] += parents
    return fish

def track_fish_births(days, fish):
    for i in range(days):
        #print(i, sum(fish.values()), sorted([(k-i,v) for k,v in fish.items() if v != 0]))
        fish = update_fish_lineage(i, fish)
    return fish

def solve(raw, days=80):
    fish = get_fish_counts(preprocess(raw))
    fish = track_fish_births(days, fish)
    return sum(fish.values())

## Testing
assert preprocess(test) == [3,4,3,1,2]
test_fish = get_fish_counts(preprocess(test))
#assert update_fish_lineage(1, test_fish) 
assert solve(test) == 5934
assert solve(test, 256) == 26984457539

## Solution for part 1
print(f'Part 1: {solve(raw)} fish remain')

## Solution for part 2
print(f'Part 2: {solve(raw, 256)} fish remain after 256 days')
