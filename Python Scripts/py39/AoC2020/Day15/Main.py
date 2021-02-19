from time import time

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
        lines = [line.strip() for line in f.readlines()]
        lines = [int(i) for each in lines for i in each.split(',')]
    return lines

@ Timer
def part1(inp, N=2020, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    # 0 3 6 0 3 3 1 0 4 0    
    spoken_dict = {each:i for i,each in enumerate(inp[:-1])}
    current = inp[-1]
    n = len(inp[:-1])
    while n < N-1:
        if current not in spoken_dict.keys():
            spoken_dict[current] = n
            current = 0
        else:
            last = spoken_dict[current]
            spoken_dict[current] = n
            current = n-last
        # print(spoken_dict)
        n += 1
    return current


@ Timer
def part2(inp, N, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    return part1(inp, N=N)

if __name__ == "__main__":
    """ files needed
        - input.txt
        - test_{x}_input.txt, with x the test number"""
    t0 = time()
    day = 15; test = 0; prnt = test != 0
    inp = parse(day,test, prnt=prnt)
    part1(inp, N=2020    , prnt=True)
    part2(inp, N=30000000, prnt=True)
    print(f"\nTotal time: {time()-t0}")