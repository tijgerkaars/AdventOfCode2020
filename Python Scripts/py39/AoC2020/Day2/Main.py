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
        l = lambda s : (list(map(int, s[0].split('-'))), s[1][:-1], s[2])
        lines = [ l(line.strip().split(' ')) for line in f.readlines()]
    return lines

@ Timer
def part1(inp, valid=0, *arg, **args):
    for (lb, ub), target, code in inp:
        n = 0
        for l in code:
            if l == target:
                n+=1
                if n > ub:
                    break
        if lb <= n <= ub:
            valid += 1
    return valid

@ Timer
def part2(inp, valid=0, *arg, **args):
    for indici, target, code in inp:
        if sum( [code[i-1] == target for i in indici] ) == 1:
            valid += 1
    return valid


if __name__ == "__main__":
    t0 = time()
    day = 2; test = 0; prnt = test != 0
    inp = parse(day,test, prnt=prnt)
    part1(inp, prnt=True)
    part2(inp, prnt=True)