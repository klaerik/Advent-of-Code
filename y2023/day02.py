import y2023.shared as shared
from dataclasses import dataclass, field

## Data
raw = shared.read_file("day02.txt")
test = shared.read_file("day02-test.txt")
bag_part1 = {'red': 12, 'green': 13, 'blue': 14}

## Functions
def parse_color(num_color: str) -> tuple:
    # print(num_color)
    num, color = num_color.strip().split(' ')
    num = int(num)
    return (color, num)

def parse_hand(hand: str) -> dict:
    colors = hand.split(',')
    color_cnts = [parse_color(color) for color in colors]
    color_dict = dict(color_cnts)
    return color_dict

def split_game_to_hands(game: str) -> list:
    hands = game.split(':')[-1].split(';')
    return [parse_hand(hand) for hand in hands]

def is_valid_hand(hand: dict, bag: dict) -> bool:
    for k,v in hand.items():
        if v > bag.get(k, 0):
            return False
    return True

def get_max_color_values(hands: list[dict]) -> dict:
    maxes = None
    for hand in hands:
        if not maxes:
            maxes = hand
        else:
            for k,v in hand.items():
                maxes[k] = max(maxes.get(k, 0), v)
    return maxes

def get_power(colors: dict) -> int:
    out = 1
    for val in colors.values():
        out *= val
    return out


def is_possible_game(game: str, bag: dict) -> bool:
    hands = split_game_to_hands(game)
    for hand in hands:
        valid = is_valid_hand(hand, bag)
        if not valid:
            # print(f"Game not possible: {game}")
            return False
    return True


def solve(raw, bag):
    out = 0
    for i,game in enumerate(raw, start=1):
        if is_possible_game(game, bag):
            out += i
    return out


def solve2(raw):
    game_color_maxes = [get_max_color_values(split_game_to_hands(game)) for game in raw]
    game_powers = [get_power(color_maxes) for color_maxes in game_color_maxes]
    return sum(game_powers)



## Testing
assert parse_color('3 blue') == ('blue', 3)
assert solve(test, bag_part1) == 8
assert solve2(test) == 2286

## Solutions
print(f"Solution to part 1: {solve(raw, bag_part1)}")
print(f"Solution to part 2: {solve2(raw)}")
