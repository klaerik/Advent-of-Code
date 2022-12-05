import y2022.shared as shared

## Data
raw = shared.read_file('day05.txt', strip=False)
test = shared.read_file('day05-test.txt', strip=False)

## Functions
def split_crates_and_proc(raw):
    raw_crates = []
    raw_proc = []
    for i in raw:
        if i.startswith('move'):
            raw_proc.append(i)
        else:
            raw_crates.append(i)
    return raw_crates, raw_proc

def init_crates(raw_crates):
    out = {}
    positions = {}
    for row in raw_crates[::-1]:
        if not out:
            for i,val in enumerate(row):
                if val.isdigit():
                    out[int(val)] = []
                    positions[int(val)] = i
        else:
            for k,v in positions.items():
                crate = row[v]
                if crate.isalpha():
                    out[k].append(crate)
    return out

def init_proc(raw_proc):
    out = []
    for i in raw_proc:
        step = [int(x) for x in i.split(' ') if x.strip().isdigit()]
        out.append(step)
    return out

def init_warehouse(crates, proc):
    return init_crates(crates), init_proc(proc)

def process_step(step, crates, multi_move=False):
    count,start,stop = step
    if multi_move is False:
        for _ in range(count):
            crates[stop].append(crates[start].pop())
    else:
        crates[stop].extend(crates[start][-count:])
        del crates[start][-count:]

def process_proc(proc, crates, multi_move):
    for step in proc:
        process_step(step, crates, multi_move)
    return crates

def solve(raw, multi_move=False):
    raw_crates, raw_proc = split_crates_and_proc(raw)
    crates, proc = init_warehouse(raw_crates, raw_proc)
    crates = process_proc(proc, crates, multi_move)
    out = ''
    for k in sorted(crates.keys()):
        out += crates[k][-1]
    return out

## Testing
assert solve(test) == 'CMZ'
assert solve(test, multi_move=True) == 'MCD'

## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve(raw, multi_move=True)}")
