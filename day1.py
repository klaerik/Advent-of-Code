file = 'input/day1.txt'
nums = []
with open(file) as file:
    for line in file:
        line = line.rstrip('\n')
        sign = line[0]
        num = int(line[1:])
        num = num if sign == '+' else num * -1
        nums.append(num)

freq = 0
log = {freq,}
iterations = 0
repeat = False
while not repeat:
    for num in nums:
        freq += num 
        if freq in log and not repeat:
            print(f"Repeat {freq}")
            repeat = True
        log.add(freq)
    if iterations == 0:
        print(f"Final {freq}")
    iterations += 1