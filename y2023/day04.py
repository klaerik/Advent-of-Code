import y2023.shared as shared
from dataclasses import dataclass, field


## Data
raw = shared.read_file("day04.txt")
test = shared.read_file("day04-test.txt")


## Functions
def parse_card(card: str) -> list[list[int], list[int]]:
    win_nums, have_nums = card.split(":")[1].split("|")
    win_nums = [int(x) for x in win_nums.split(" ") if x]
    have_nums = [int(x) for x in have_nums.split(" ") if x]
    return win_nums, have_nums


def score_card(win_nums, have_nums):
    score = 0
    matches = 0
    win_nums = set(win_nums)
    for num in have_nums:
        if num in win_nums:
            matches += 1
            score = score * 2 if score else 1
    return score, matches


def solve(raw):
    return sum([score_card(*parse_card(card))[0] for card in raw])


def solve2(raw):
    counts = [1] * len(raw)
    for i, card in enumerate(raw):
        nums = parse_card(card)
        _, matches = score_card(*nums)
        for j in range(1, matches + 1):
            if i + j < len(counts):
                counts[i + j] += 1 * counts[i]
    return sum(counts)


## Testing
assert solve(test) == 13
assert solve2(test) == 30


## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve2(raw)}")
