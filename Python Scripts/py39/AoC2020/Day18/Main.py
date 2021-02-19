from time import time

import re

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
        # Parsing goes here
        lines = [line.strip().replace(' ', '') for line in f.readlines()]
        print(f"longest string: {max(map(len, lines))}")
    return lines

def eval_eq(eq,resolve_func):
    while any([each in eq for each in '()']):
        eq = parse_eq(eq, resolve_func)
    return resolve_func(eq)

def parse_eq(eq, resolve_func):
    cb  = eq.index(')')
    ob  = len(eq[:cb])-''.join(reversed(eq[:cb])).index('(')-1
    obi = eq[ob:cb].count('(')
    preamble = eq[:ob]
    tail     = eq[cb+1:]
    return preamble + str(resolve_func(eq[ob+obi:cb])) + tail

def resolve_eq_1(eq):
    eq = re.split('([\*+])', eq)
    total = eq[0]
    for i in range(2,len(eq),2):
        total = eval(f"{total}{eq[i-1]}{eq[i]}")
    return total

def resolve_eq_2(eq):
    eq = re.split('([\*+])', eq)
    total = eq[0]
    for _ in range(eq.count('+')):
        for i,each in enumerate(eq):
            if each == '+':
                break
        try:
            a = eq[:i-1]
        except IndexError:
            a = []
        try: 
            b = [str(eval(''.join(eq[i-1:i+2])))]
        except IndexError:
            b = []
        try:
            c = eq[i+2:]
        except IndexError:
            c = []
        eq = a+b+c
    return eval(''.join(eq))

@ Timer
def part1(inp, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    print('\n')
    sumval = 0
    for eq in inp:
        sumval += eval_eq(eq, resolve_eq_1)
    return sumval



@ Timer
def part2(inp, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    print('\n')
    sumval = 0
    for i,eq in enumerate(inp):
        sumval += eval_eq(eq, resolve_eq_2)
    return sumval
if __name__ == "__main__":
    """ files needed
        - input.txt
        - test_{x}_input.txt, with x the test number"""
    t0 = time()
    day = 18; test = 0; prnt = test != 0
    inp = parse(day,test, prnt=prnt)
    part1(inp, prnt=True)
    part2(inp, prnt=True)
    print(f"Total time: {time()-t0}")