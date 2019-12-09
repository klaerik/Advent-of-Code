from itertools import permutations

raw = []
with open('input/day07.txt') as f:
    raw = f.readline().strip().split(',')

def lookup(pos, lst):
    return int(lst[pos]) if 0 <= pos < len(lst) else 0

def run_prog(prog, input_ins=[-99], pos=0, debug=False, verbose=False, final=False):
    i = pos
    prog = prog.copy()
    out = None
    final = False
    while i < len(prog):
        op_parms = prog[i].zfill(5)
        op = op_parms[-2:]
        if op == '99':
            final = True
            break
        
        mode_c, mode_b, mode_a = op_parms[:3]
        a = lookup(i+1, prog)
        b = lookup(i+2, prog) 
        c = lookup(i+3, prog) 
        a_val = lookup(a, prog) if mode_a == '0' else a
        b_val = lookup(b, prog) if mode_b == '0' else b
        c_val = lookup(c, prog) if mode_c == '0' else c
       
        if op == '01':
            prog[c] = str(a_val + b_val)
            step = 4
        elif op == '02':
            prog[c] = str(a_val * b_val)
            step = 4
        elif op == '03':
            if len(input_ins) > 0:
                prog[a] = str(input_ins.pop(0))
            else:
                print("Ran out of stuff!")
                break
            step = 2
        elif op == '04':
            out = a_val
            if verbose:
                print(f'OUTPUT: {out}')
            step = 2
        elif op in ['05','06']:
            if (op == '05' and a_val != 0) or (op == '06' and a_val == 0):
                i = b_val
                step = 0
            else:
                step = 3
        elif op in ['07','08']:
            if (op == '07' and a_val < b_val) or (op == '08' and a_val == b_val):
                prog[c] = '1'
            else:
                prog[c] = '0'
            step = 4
        i += step
        if debug:
            print('step', step, 'next', prog[i], 'opparms', op_parms, op, 'mode', mode_a, mode_b, mode_c, 'parms', a, b, c, 'vals', a_val, b_val, c_val)
            print(prog)
    return {'prog':prog, 'out':out, 'pos':i, 'final':final, 'input_ins':input_ins}


def amplifier_circuit(prog, phase_sequence):
    amps = [{'prog':prog.copy(), 'input_ins':[x], 'final':False} for x in phase_sequence]
    prior_amp = False
    while not amps[-1]['final']:
        for i in range(len(amps)):
            print(i)
            amp = amps[i]
            if prior_amp:
                pao = prior_amp['out']
                if pao is not None:
                    amp['input_ins'].append(prior_amp['out'])
            else:
                amp['input_ins'].append(0)
            amp = run_prog(**amp)
            print(amp['out'])
            #print(amp)
            prior_amp = amp
    return amps[-1]['out']


def find_best_sequence(prog):
    best_phase_sequence = None
    best_result = 0
    for seq in permutations([0, 1, 2, 3, 4]):
        result = amplifier_circuit(prog, seq)
        if result > best_result:
            best_result = result
            best_phase_sequence = seq
    return best_phase_sequence, best_result


test = '3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0'.split(',')
phase = (4,3,2,1,0)
run_prog(test, [phase[0], 0])
assert amplifier_circuit(test, phase) == 43210
assert find_best_sequence(test)[0] == phase

test = '3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0'.split(',')
phase = (0,1,2,3,4)
signal = 54321
assert amplifier_circuit(test, phase) == signal
assert find_best_sequence(test)[0] == phase
assert find_best_sequence(test)[1] == signal

test = '3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0'.split(',')
phase = (1,0,4,3,2)
assert amplifier_circuit(test, phase) == 65210
assert find_best_sequence(test)
assert find_best_sequence(test)[0] == phase
    
print(f'Max signal for part 1: {find_best_sequence(raw)[1]}')
    

