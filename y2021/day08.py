import shared

## Data
raw = shared.read_file('2021/input/day08.txt')

test = '''be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce'''.split('\n')


## Functions
def process_input(raw):
    out = []
    for line in raw:
        signal,output = line.split(' | ')
        signal = tuple([sort(x) for x in signal.split()])
        output = tuple([sort(x) for x in output.split()])
        out.append((signal, output))
    return out

def count_easy(displays):
    out = 0
    for _,output in displays:
        out += len([x for x in output if len(x) in (2,3,4,7)])
    return out

def solve(raw):
    displays = process_input(raw)
    count = count_easy(displays)
    return count

def map_values(display):
    possible = {alpha:set() for alpha in ('abcdefg')}
    mapped = {}
    orig = {'abcefg':0, 'cf':1, 'acdeg':2, 'acdfg':3, 'bcdf':4, 'abdfg':5, 'abdefg':6, 'acf':7, 'abcdefg':8, 'abcdfg':9}
    len_map = {}
    for combo in orig:
        len_map.setdefault(len(combo), set()).add(combo)
    #uniq_lengths = {2:'cf', 4:'bcdf', 3:'acf', 7:'abcdefg'}
    out = {}
    output = display[1]
    nums = set(display[0] + display[1])
    # Numbers
    for num in nums:






## Testing
assert solve(test) == 26

## Solution for part 1
print(f'Part 1: digits 1,4,7,8 appear {solve(raw)} times')


## Solution for part 2