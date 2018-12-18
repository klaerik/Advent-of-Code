from collections import defaultdict, Counter
import re


raw = []
with open('input/day4.txt') as file:
    for line in file:
        raw.append(line.rstrip('\n'))
raw.sort()


times = {}
for line in raw:
    regex = re.match('^\[(.*) (\d+):(\d+)\] (\w+) #?(\w+) ?(.*)$', line)
#    print(regex)
    typ = regex[4]
#    print(typ)
    time = int(regex[3])
    if typ == 'Guard':
        guard = regex[5]
    elif typ == 'falls':
        asleep = time
    elif typ == 'wakes':
        up = time
        minutes = []
        for i in range(asleep, up):
            minutes.append(i)
#        print(minutes)
        times.setdefault(guard,[]).extend(minutes)

times

laziest = '0',0,0
laziest2 = '0',0
for guard,time in times.items():
    asleep_ttl = len(time)
    worst_minute, worst_ttl = Counter(time).most_common(1)[0]
    if asleep_ttl > laziest[1]:
        laziest = guard, asleep_ttl, worst_minute
    if worst_ttl > laziest2[1]:
        laziest2 = guard, worst_ttl, worst_minute
    

print(f"Laziest guard,ttl_minutes: {laziest}")
guard_id = laziest[0]
solution = int(guard_id) * laziest[2]
print(f"Best time: {best_minute}")
print(f"Strategy 1 solution: {solution}")

print(f"Strategy 2 laziest: {laziest2}")
solution2 = int(laziest2[0]) * laziest2[2]
print(f"Strategy 2 solution: {solution2}")
    