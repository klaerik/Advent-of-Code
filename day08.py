with open('input/day08.txt') as f:
    raw = f.readline().strip()

h = 6
w = 25
layers = [raw[i:i+h*w] for i in range(0, len(raw), h*w)]
counts = [l.count('0') for l in layers]
lowest = counts.index(min(counts))
answer = layers[lowest].count('1') * layers[lowest].count('2')
print(f'Part 1 answer: {answer}')

# part 2
visible = [0,] * h * w
for i in range(len(visible)):
    for layer in layers:
        val = layer[i]
        if val == '2':
            continue
        elif val == '1':
            visible[i] = '#'
            break
        elif val == '0':
            visible[i] = ' '
            break

formatted = [visible[i:i+w] for i in range(0, len(visible), w)]
output = '\n'.join([''.join(x) for x in formatted])
print(f"Part 2 answer:\n{output}")
