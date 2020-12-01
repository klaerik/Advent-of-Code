
def run_prog(prog, pos=0):
    for i in range(0, len(prog), 4):
        if prog[i] == 99:
            break
        op, a, b, tgt = prog[i:i+4]
        #print(op, a, b, tgt, prog)
        if op == 1:
            prog[tgt] = prog[a] + prog[b]
        elif op == 2:
            prog[tgt] = prog[a] * prog[b]

    return prog[pos]

assert run_prog([1,9,10,3,2,3,11,0,99,30,40,50]) == 3500
assert run_prog([1,0,0,0,99]) == 2


raw = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,10,1,19,1,6,19,23,1,23,13,27,2,6,27,31,1,5,31,35,2,10,35,39,1,6,39,43,1,13,43,47,2,47,6,51,1,51,5,55,1,55,6,59,2,59,10,63,1,63,6,67,2,67,10,71,1,71,9,75,2,75,10,79,1,79,5,83,2,10,83,87,1,87,6,91,2,9,91,95,1,95,5,99,1,5,99,103,1,103,10,107,1,9,107,111,1,6,111,115,1,115,5,119,1,10,119,123,2,6,123,127,2,127,6,131,1,131,2,135,1,10,135,0,99,2,0,14,0]

def prep_data(in_data, noun=12, verb=2):
    out_data = in_data.copy()
    out_data[1] = noun
    out_data[2] = verb
    return out_data

part_1 = prep_data(raw)
print(f"Part 1 answer: {run_prog(part_1)}")


gen_nounverb = ((noun,verb) for noun in range(100) for verb in range(100))

noun, verb = 0, 0
for noun,verb in gen_nounverb:
    #print(f"Testing {noun} and {verb}...")
    test = prep_data(raw, noun, verb)
    out = run_prog(test)
    #print(f"\tFound {out}")
    if out == 19690720:
        print(f"Found it! {noun} {verb}")
        break
    
print(f"Part 2 answer: {100 * noun + verb}")












