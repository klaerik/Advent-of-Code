from collections import Counter

raw = '146810-612564'
start,stop = [int(i) for i in raw.split('-')]


def is_valid(num, start=start, stop=stop, triple_check=False):
    snum = str(num)
    len_ok = len(snum) == 6
    range_ok = start <= num <= stop
    counts = Counter(snum)
    if triple_check:
        double_ok = any([x == 2 for x in counts.values()])
    else:
        double_ok = any([x > 1 for x in counts.values()])
    last = snum[0]
    inc_ok = True
    for i in snum[1:]:
        if i < last:
            inc_ok = False
            break
        else:
            last = i
    checks = [len_ok, range_ok, double_ok, inc_ok]
    #print(checks)
    return all(checks)

def check_range(start, stop, triple_check=False):
    out = []
    for i in range(start, stop+1):
        if is_valid(i, start=start, stop=stop, triple_check=triple_check):
            out.append(i)
    return out

assert is_valid(111111, start=111111, stop=222222)
assert not is_valid(123444, start=123443, stop=123445, triple_check=True)
assert is_valid(111122, start=111122, stop=111123, triple_check=True)

print(f'First answer: {len(check_range(start, stop))}')
print(f'Second answer: {len(check_range(start, stop, triple_check=True))}')