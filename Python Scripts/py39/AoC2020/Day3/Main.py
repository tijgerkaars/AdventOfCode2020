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
        lines = [line.strip() for line in f.readlines()]
    return lines

@ Timer
def part1(inp, df, pos=(0,0), hits = 0, **args):
    x,y,dx,dy = *pos, *df
    w,h = len(inp[0]), len(inp)
    while True:
        x += dx; y += dy
        if y >= h:
            break
        x %= w
        if inp[y][x] == '#':
            hits += 1
    return hits

@ Timer
def part2(inp, dfs = [(1,1),(3,1),(5,1),(7,1),(1,2)], **args):
    total = 1
    for df in dfs:
        total *= part1(inp, df)
    return total

if __name__ == "__main__":
    t0 = time()
    day = 3; test = 0; prnt = test != 0
    inp = parse(day,test, prnt=prnt)
    part1(inp, (3,1), prnt=True)
    part2(inp, prnt=True)
    print(f"Total time: {time()-t0}")