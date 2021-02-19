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
        lines = set(int(line.strip()) for line in f.readlines())
    return lines

@ Timer
def part1(nums, *arg, **args):
    for num in nums:
        if 2020-num in nums:
            return (2020-num) * num

@ Timer
def part2(nums, *arg, **args):
    for num in nums:
        for other in nums:
            if num != other and 2020-(num+other) in nums:
                return (2020-(num+other)) * other * num
if __name__ == "__main__":
    t0 = time()
    day = 1; test = 0
    inp = parse(day,test)
    part1(inp, prnt=True)
    part2(inp, prnt=True)
    print(f'Total: {time()-t0}')