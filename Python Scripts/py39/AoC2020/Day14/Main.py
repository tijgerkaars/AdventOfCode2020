from time import time

def get_mask(mask):
    _,mask = mask.split(' = ')
    return {int(i):int(c) for i,c in enumerate(reversed(mask)) if c !='X'}

def get_floating_mask(mask):
    from itertools import combinations
    _,mask = mask.split(' = ')
    floating = [i for i,each in enumerate(mask) if each == 'X']
    mask=int(mask.replace('X', '0'),2)
    for i in range(len(floating)):
        for comb in combinations(floating,i):
            diff = 0
            for each in comb:
                diff += 2**each
            yield mask + diff

def set_bit(value, bit_index):
    return value | (1 << bit_index)

def clear_bit(value, bit_index):
    return value & ~(1 << bit_index)

def Timer(func):
    def Timer_wrapper(*arg, rtrn:bool=True, prnt:bool=False, **args):
        """ rtrn: return the result if true
            prnt: print -- {the function that is being timed}: {result} -- {time it took}
            *arg and **args contain unnamed and named variables respectably to be passed to the function to be timed"""
        t0 = time()
        out = func(*arg, **args)
        if prnt == True:
            print( f"{str(func)}: {out}  -- {time()-t0}" )
        if rtrn:
            return out
    return Timer_wrapper

@ Timer
def parse(day:int,test:int, *arg, **args):
    """ imports input file from "AoC2020\Day{day}\{f}"  """
    f = f"{f'test_{test}_' if test > 0 else ''}input.txt"
    with open(rf"AoC2020\Day{day}\{f}") as f:
        lines = [line for line in f.read().strip().splitlines()]
    return lines

@ Timer
def part1(inp, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""

    mask = {}
    mem  = {}
    for instr in inp:
        if 'mask' in instr:
            mask = get_mask(instr)
            continue
        index,write=instr.split('] = ')
        index = int(index[4:])
        write = int(write)
        # print(write, index)
        for mask_index,mask_value in mask.items():
            # print(repr(mask_index),repr(mask_value))
            if   mask_value == 1:
                write = set_bit(write, mask_index)
            elif mask_value == 0:
                write = clear_bit(write, mask_index)
            # print(write)
        mem[index] = write
    return sum(mem.values())

@ Timer
def part2(inp, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    i = 0; m = 0
    mam = {}
    print(inp)
    return
    for instr in inp:
        if 'mask' in each:
            m = max(m, instr.count('X'))
            masks = list(get_floating_mask(instr))
            break
        else:
            for mask in masks:
                try:
                    mem[mask] = 

    # print(f"{i=}, {2**m=}, max_opp = {35*i*2**m}")
    pass

if __name__ == "__main__":
    """ files needed
        - input.txt
        - test_{x}_input.txt, with x the test number"""
    t0 = time()
    day = 14; test = 0; prnt = test != 0
    inp = parse(day,test, prnt=prnt)
    part1(inp, prnt=True) # 17765746710228
    part2(inp, prnt=True)
    print(f"Total time: {time()-t0}")




"""
101101X00011110111010X1XX011X0110001
111X0000001X110X1101X01XX100000X1XX1
X1000X100100110111011X10100XX1100000
11100010X0X1110X0X000010X0X00000110X
"""