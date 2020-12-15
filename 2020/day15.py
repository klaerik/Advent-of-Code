import shared


def initialize_lookup(turns):
    lookup = {}
    for i,val in enumerate(turns, start=1):
        lookup[val] = lookup.get(val, ())[-1:] + (i,)
    return lookup

def take_turn(turn_number, last_val, lookup):
    if len(lookup[last_val]) == 1:
        return 0
    else:
        a,b = lookup[last_val]
        return b - a

def play_game(initial, stop=2020):
    lookup = initialize_lookup(initial)
    turns = initial[:]
    i = len(turns)
    while i < stop:
        i += 1
        num = take_turn(i, turns[-1], lookup)
        lookup[num] = lookup.get(num, ())[-1:] + (i,)
        turns.append(num)
    return turns


assert play_game([0,3,6])[-1] == 436
assert play_game([1,3,2])[-1] == 1
assert play_game([2,1,3])[-1] == 10
assert play_game([3,1,2])[-1] == 1836

initial = [9,3,1,0,8,4]
turns = play_game(initial)
print(f'Part 1: {turns[-1]} is the number spoken on turn 2020')

assert play_game([0,3,6], stop=30000000)[-1] == 175594

turns = play_game(initial, stop=30000000)
print(f'Part 2: {turns[-1]} is the number spoken on turn 30000000')

