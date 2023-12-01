import y2023.shared as shared
from dataclasses import dataclass, field
import re

## Data
raw = shared.read_file("day01.txt")
test = shared.read_file("day01-test.txt")
test2 = shared.read_file("day01-test2.txt")

## Functions
words = ('one','two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine') 
digit_mapping = {word: str(i) for i,word in enumerate(words, start=1)}

def resolve_digits(num: str) -> str:
    return digit_mapping.get(num, num)

def get_digits(line: str, include_words = False) -> int:
    if include_words:
        word_regex = r"|" + r"|".join(words)
    else:
        word_regex = ""
    first = re.search(r"([0-9]" + word_regex + r")", line).group(1)
    last = re.search(r".*(\d" + word_regex + r")", line).group(1)
    return int(resolve_digits(first)+resolve_digits(last))

def solve(raw, include_words=False):
    return sum([get_digits(line, include_words) for line in raw])


## Testing
assert solve(test) == 142
assert solve(test2, include_words=True) == 281


## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve(raw, include_words=True)}")
