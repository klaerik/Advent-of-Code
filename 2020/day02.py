import shared
import re


def parse_password(rec):
    rgx = re.compile(r'^(\d+)-(\d+) ([a-z]): ([a-z]+)')
    matches = rgx.search(rec)
    start, stop = int(matches.group(1)), int(matches.group(2))
    letter, password = matches.group(3), matches.group(4)
    return start, stop, letter, password

def is_valid(start, stop, letter, password):
    count = password.count(letter)
    if start <= count <= stop:
        return True
    else:
        return False

def is_valid2(a, b, letter, password):
    pos1 = password[a-1] == letter
    pos2 = password[b-1] == letter
    if pos1 and not pos2 or pos2 and not pos1:
        return True
    else:
        return False


# Check validity
file = 'input/day02.txt'
raw = shared.read_file(file)

valid = valid2 = 0
for rec in raw:
    vals = parse_password(rec)
    if is_valid(*vals):
        valid += 1
    if is_valid2(*vals):
        valid2 += 1

print(f'Part 1 answer: {valid} valid passwords')

print(f'Part 2 answer: {valid2} valid passwords')
