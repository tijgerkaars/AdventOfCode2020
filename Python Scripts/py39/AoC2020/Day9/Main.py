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
    f = f"{f'test_{test}_' if test > 0 else ''}input.txt"
    with open(rf"Python Scripts\py39\AoC2020\Day{day}\{f}") as f:
        lines = [int(line.strip()) for line in f.readlines()]
    return lines

@ Timer
def part1(inp, preamble, **args):
    """ takes preamble length slices from the input, checks if a sum from slice elements is the next value 
        returns first value that doesn't match preamble""" 
    for i in range(preamble,len(inp)):
        sub = inp[i-preamble:i]
        if not any( inp[i] - each in sub for each in sub ):
            return inp[i]
@ Timer
def part2(inp, p1, **args):
    """ checks the sum of increasingly long slices for value of part1
        returns min + max of that slice """
    inp_len = len(inp)
    for l in range(2, inp_len):
        for i in range(l, inp_len):
            sub = inp[i-l:i]
            if sum( sub ) == p1:
                return min(sub) + max(sub)


if __name__ == "__main__":
    t0 = time()
    day = 9; test = 0; prnt = test != 0
    preamble = [25,5]
    inp = parse(day,test, prnt=prnt)
    p1 = part1(inp, preamble[test], prnt=True)
    part2(inp, p1, prnt=True)
    print(f"Total time: {time()-t0}")