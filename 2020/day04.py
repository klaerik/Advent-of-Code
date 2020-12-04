import shared
import re

def has_all_fields(passport, fields = {'byr','iyr','eyr','hgt','hcl','ecl','pid','cid'}):
    present = set(passport.keys())
    remain = fields - present
    if not remain or remain == {'cid'}:
        return True
    else:
        return False

def has_valid_values(passport):
    if all([re.match(r'^(19[2-9][0-9]|200[0-2])$', passport['byr']),
           re.match(r'^(201[0-9]|2020)$', passport['iyr']),
           re.match(r'^(202[0-9]|2030)$', passport['eyr']),
           re.match(r'^((59|6[0-9]|7[0-6])in|(1[5-8][0-9]|19[0-3])cm)', passport['hgt']),
           re.match(r'#[0-9a-f]{6}$', passport['hcl']),
           passport['ecl'] in {'amb','blu','brn','gry','grn','hzl','oth'},
           re.match(r'^\d{9}$', passport['pid'])
           ]):
        return True
    else:
        return False

def extract_passport(rec):
    passport = {}
    for field in rec.split(' '):
        if field:
            k,v = field.split(':')
            passport[k] = v
    return passport


# Solve day 4
file = 'input/day04.txt'
raw = shared.read_file(file, include_blank_lines=True)
clean = ' '.join([x if x else ',' for x in raw]).split(',')
passports = [extract_passport(rec) for rec in clean if rec]

valid = [x for x in passports if has_all_fields(x)]
print(f'Part 1: {len(valid)} passports are valid')

valid2 = [x for x in passports if has_all_fields(x) and has_valid_values(x)]        
print(f'Part 2: {len(valid2)} passports with tighter rules')