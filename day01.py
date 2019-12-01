# Advent of code - day 1

from math import floor

def fuel(mass):
    return floor(mass / 3) - 2

assert fuel(12) == 2
assert fuel(14) == 2
assert fuel(1969) == 654
assert fuel(100756) == 33583

reqs = []
with open('input/day1.txt') as f:
    for line in f:
        reqs.append(line.strip())

out = []
for i in reqs:
    out.append(fuel(int(i)))

final_fuel = sum(out)
print(f'Fuel for part 1 is: {final_fuel}')



# part 2
i = 0
zeros = 0
while zeros < len(reqs):
    f = out[i]
    f_next = fuel(f)
    if f_next <= 0:
        zeros += 1
        out.append(0)
    elif zeros > 0:
        zeros -= 1
        out.append(f_next)
    else:
        out.append(f_next)
    #print(zeros, flush=True)
    i += 1

really_final_fuel = sum(out)
print(f'OK, really it is actually {really_final_fuel}')
    
