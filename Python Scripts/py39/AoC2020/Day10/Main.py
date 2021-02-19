from time import time

def Timer(func):
    def Timer_wrapper(*arg, rtrn = True, prnt = False, **args):
        t0 = time()
        out = func(*arg, **args)
        if prnt == True:
            print( f"{str(func)}: {out}  -- {time()-t0}" )
        if rtrn:
            return out
    return Timer_wrapper

@ Timer
def parse(day,test, *arg, **args):
    f = rf"{f'test_{test}_' if test > 0 else ''}input.txt"
    with open(rf"AoC2020\Day{day}\{f}") as f:
        lines = sorted(map(int, (i for i in f.readlines())))
    return lines

@ Timer
def part1(inp, debug=False, **args):
    diff = [inp[i]-inp[i-1] for i in range(1,len(inp))]
    if debug: print(diff)
    return diff, Counter(diff)

@ Timer
def part2(inp, diff, debug=False, **args):
    knots = [0]+[i+1 for i,each in enumerate(diff) if each == 3]
    parts = list(map(len, [inp[knots[i-1]:knots[i]] for i in range(1,len(knots))]))
    if debug: print(parts)
    out = 1
    for p in parts:
        if p == 3:
            out *= 2
        elif p == 4:
            out *= 4
        elif p == 5:
            out *= 7
    return out

if __name__ == "__main__":
    """ files needed
        - input.txt
        - test_{x}_input.txt, with x the test number"""
    from collections import Counter

    t0 = time()
    day = 10; test = 0; prnt = test != 0
    inp = parse(day,test, prnt=prnt)
    inp = [0] + inp + [inp[-1]+3]
    diff,_ =part1(inp, prnt=True)
    part2(inp, diff, prnt=True)
    print(f"Total time: {time()-t0}")