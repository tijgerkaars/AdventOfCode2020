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
        lines = f.readlines()
    return lines

@ Timer
def part1(inp, **args):
    pass

@ Timer
def part2(inp, **args):
    pass

if __name__ == "__main__":
    t0 = time()
    day = -1; test = 1; prnt = not test
    inp = parse(day,test, prnt=prnt)
    # part1(inp, prnt=True)
    # part2(inp, prnt=True)
    print(f"Total time: {time()-t0}")