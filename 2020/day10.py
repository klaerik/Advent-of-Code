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
        for next_num in clean[i+1:]:
            if next_num <= num + 3:
                out[next_num] += out[num]
            else:
                break
    return out[clean[-1]]

print(f'Part 2: {count_adapter_combos(clean)} possible adapter combos')
