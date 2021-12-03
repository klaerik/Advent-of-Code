import shared

## Data
raw = shared.read_file('2021/input/day03.txt')
test = [
    '00100',
    '11110',
    '10110',
    '10111',
    '10101',
    '01111',
    '00111',
    '11100',
    '10000',
    '11001',
    '00010',
    '01010',
    ]

## Functions
def get_gamma_rate(report):
    counts = [[0, 0] for _ in report[0]]
    for num in report:
        for i,value in enumerate(num):
            counts[i][int(value)] += 1
    out = ''.join(['0' if count[0] > count[1] else '1' for count in counts])
    return out

def get_epsilon_rate(report):
    gamma = get_gamma_rate(report)
    return swap_vals(gamma)

def swap_vals(num):
    remap = {'1': '0', '0': '1'}
    return ''.join([remap[x] for x in num])

def solve_puzzle(report, func1=get_gamma_rate, func2=get_epsilon_rate):
    return int(func1(report), 2) * int(func2(report), 2)

def get_ratings(report, rating_type):
    selection = report
    for i in range(len(report[0])):
        if len(selection) == 1:
            break
        found = [[], []]
        for num in selection:
            val = num[i]
            found[int(val)].append(num)
        zeros, ones = [len(x) for x in found]
        if (rating_type == 'o2' and zeros > ones) or (rating_type == 'co2' and zeros <= ones):
            selection = found[0]
        else:
            selection = found[1]
    return selection[0]

def get_o2_gen_rating(report):
    return get_ratings(report, 'o2')

def get_co2_scrubber_rating(report):
    return get_ratings(report, 'co2')


## Testing
assert get_gamma_rate(test) == '10110'
assert get_epsilon_rate(test) == '01001'
assert int(get_gamma_rate(test), 2) == 22
assert solve_puzzle(test) == 198
assert get_o2_gen_rating(test) == '10111'
assert get_co2_scrubber_rating(test) == '01010'
assert solve_puzzle(test, get_o2_gen_rating, get_co2_scrubber_rating) == 230

## Solution for part 1
print(f'Part 1: Submarine power consumption is {solve_puzzle(raw)}')

## Solution for part 2
print(f'Part 2: Submarine life support rating is {solve_puzzle(raw, get_o2_gen_rating, get_co2_scrubber_rating)}')