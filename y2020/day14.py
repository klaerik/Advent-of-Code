import shared
import re



def apply_mask(num, mask):
    bnum = bin(num)[2:].rjust(len(mask), '0')
    out = [i if j == 'X' else j for i,j in in zip(bnum, mask)]
    return int(''.join(out), base=2)

def process_instructions(raw):
    mem = {}
    mask = 36 * '0'
    for rec in raw:
        if rec.startswith('mask'):
            mask = rec.split(' = ')[1]
        else:
            match = re.match(r'.*\[(\d+)\] = (\d+)', rec)
            addr = int(match.group(1))
            num = int(match.group(2))
            mem[addr] = apply_mask(num, mask)
    return mem

def apply_mask2(num, mask):
    bnum = bin(num)[2:].rjust(len(mask), '0')
    temp = [i if j == '0' else j for i,j in zip(bnum, mask)]
    out = [[]]
    for i in temp:
        if i in ('0','1'):
            for sublist in out:
                sublist.append(i)
        else:
            out2 = [x[:] for x in out]
            for sublist in out:
                sublist.append('0')
            for sublist in out2:
                sublist.append('1')
            out.extend(out2)
    return [int(''.join(x), base=2) for x in out]

def process_instructions2(raw):
    mem = {}
    mask = 36 * '0'
    for rec in raw:
        if rec.startswith('mask'):
            mask = rec.split(' = ')[1]
        else:
            match = re.match(r'.*\[(\d+)\] = (\d+)', rec)
            addr = int(match.group(1))
            num = int(match.group(2))
            addrs = apply_mask2(addr, mask)
            for i in addrs:
                mem[i] = num
    return mem


# Solve puzzle
raw = shared.read_file('2020/input/day14.txt')

mem = process_instructions(raw)
print(f'Part 1: {sum(mem.values())} is the total in memory')

mem2 = process_instructions2(raw)
print(f'Part 2: {sum(mem2.values())} is the total for decoder version 2')