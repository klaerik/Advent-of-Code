raw = []
with open('input/day05.txt') as f:
    raw = f.readline().strip().split(',')

def lookup(pos, lst):
    return int(lst[pos]) if 0 <= pos < len(lst) else 0

def run_prog(prog, input_ins=-99, pos=0, debug=False):
    i = 0
    prog = prog.copy()
    out = None
    while i < len(prog):
        op_parms = prog[i].zfill(5)
        op = op_parms[-2:]
        if op == '99':
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
            prog[a] = str(input_ins)
            step = 2
        elif op == '04':
            out = a_val
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
    return out


test = '3,0,4,0,99'.split(',')
run_prog(test, 1, debug=0)

test = '1002,4,3,4,33'.split(',')
run_prog(test, debug=True)

test = '1101,100,-1,4,0'.split(',')
run_prog(test, debug=True)

test = '3,9,8,9,10,9,4,9,99,-1,8'.split(',')
assert run_prog(test, 1, debug=False) == 0
assert run_prog(test, 8, debug=False) == 1

test = '3,9,7,9,10,9,4,9,99,-1,8'.split(',')
assert run_prog(test, 1) == 1
assert run_prog(test, 8) == 0

test = '3,3,1108,-1,8,3,4,3,99'.split(',')
assert run_prog(test, 1) == 0
assert run_prog(test, 8) == 1



test = '3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9'.split(',')
assert run_prog(test, 1) == 1
assert run_prog(test, 0) == 0

test = '3,3,1105,-1,9,1101,0,0,12,4,12,99,1'.split(',')
assert run_prog(test, 1) == 1
assert run_prog(test, 0) == 0

test = [x.strip() for x in '''3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
    1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
    999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99'''.split(',')]
assert run_prog(test, 1) == 999
assert run_prog(test, 8) == 1000
assert run_prog(test, 9) == 1001



print(f'Part 1 output:')
run_prog(raw, 1, debug=False)

print(f'Part 2 output:')
run_prog(raw, 5)