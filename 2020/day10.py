import shared

# Data prep
raw = shared.read_file('2020/input/day10.txt')
clean = [int(x) for x in raw]
clean.append(0)
clean.append(max(clean) + 3)
clean.sort()

# Part 1
out = {}
last = None
for num in clean:
    if last is not None:
        diff = num - last
        out[diff] = out.get(diff, 0) + 1
    last = num
print(f'Part 1: {out[1] * out[3]} adapter multiplier')

# Part 2
def count_adapter_combos(adapters):
    clean = sorted(adapters)
    out = {x:0 for x in clean}
    out[0] = 1
    for i,num in enumerate(clean):
        if i == len(clean)-1:
            break
        j = i + 1
        check = clean[j]
        while check <= num + 3 and j < len(clean):
            out[check] += out[num]
            j += 1
            if j < len(clean):
                check = clean[j]
    return out[clean[-1]]

print(f'Part 2: {count_adapter_combos(clean)} possible adapter combos')
