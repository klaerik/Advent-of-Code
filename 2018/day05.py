import string

raw = ''
with open('input/day5.txt') as file:
    for line in file:
        raw = line.rstrip('\n')

polymer = list(raw)

def react(polymer):        
    fully_reacted = False
    while not fully_reacted:
        fully_reacted = True
        last = ''
        start = 0
        for i in range(start, len(polymer)):
            unit = polymer[i]
            if unit != last and unit.upper() == last.upper():
                #print(last, unit)
                del polymer[i-1:i+1]
                fully_reacted = False
                start = i - 1
                break
            else:
                last = unit
    return ''.join(polymer)

#Problem 1
final = react(polymer)
solution = len(final)
print(f"Solution: {solution} units remain")


improved_polymers = {}
for typ in string.ascii_lowercase:
    filtered = [x for x in polymer if x.lower() != typ]
    improved_polymers[typ] = react(filtered)

improved_lengths = []
for k,v in improved_polymers.items():
    polymer_length = len(v)
    print(f"\t{k} length - {polymer_length}")
    improved_lengths.append(polymer_length)

solution2 = min(improved_lengths)
print(f"Solution 2 - min improved length: {solution2}")



    