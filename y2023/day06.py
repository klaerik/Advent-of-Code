import y2023.shared as shared
import math

## Data
raw = shared.read_file("day06.txt")
test = shared.read_file("day06-test.txt")

## Functions
# distance = button_time * (race_time - button_time)
# distance = button_time * race_time - button_time **2
# quadratic equation!!


def parse_races(raw: list[str]) -> list[tuple]:
    time = [int(x) for x in raw[0].split(":")[1].split(" ") if x.isdecimal()]
    distance = [int(x) for x in raw[1].split(":")[1].split(" ") if x.isdecimal()]
    return list(zip(time, distance))


def combine_races(races: list[tuple]) -> tuple:
    time = ""
    distance = ""
    for t, d in races:
        time += str(t)
        distance += str(d)
    return int(time), int(distance)


def complete_the_square(race_time: int, distance: int) -> tuple[int, int]:
    plus_minus = math.sqrt(0.25 * race_time**2 - distance)
    constant = 0.5 * race_time
    return -plus_minus + constant, plus_minus + constant


def distance_traveled(button_time: int, race_time: int):
    return button_time * (race_time - button_time)


def ways_to_win(race_time: int, distance: int) -> int:
    smallest, biggest = complete_the_square(race_time, distance)
    start = math.ceil(smallest)
    if math.isclose(start, smallest):
        start += 1
    finish = math.floor(biggest)
    if math.isclose(finish, biggest):
        finish -= 1
    return finish - start + 1


def solve(test):
    races = parse_races(test)
    return math.prod([ways_to_win(time, distance) for time, distance in races])


def solve2(test):
    time, distance = combine_races(parse_races(test))
    return ways_to_win(time, distance)


## Testing
assert ways_to_win(7, 9) == 4
assert ways_to_win(15, 40) == 8
assert ways_to_win(30, 200) == 9

assert solve(test) == 288
assert solve2(test) == 71503


## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve2(raw)}")
