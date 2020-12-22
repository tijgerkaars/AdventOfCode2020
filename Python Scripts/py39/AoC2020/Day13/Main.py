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
        t_first, busses = [line.strip() for line in f.readlines()]
        t_first = int(t_first); busses = [int(each)  if each != 'x' else 0 for each in busses.split(',')]
    return t_first, busses

@ Timer
def part1(inp, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    t_first, busses = inp
    shortest_wait = 2^63 - 2; out = 0
    for each in busses:
        if each == 0:
            continue
        temp = each-t_first%each
        if temp < shortest_wait:
            shortest_wait = temp
            out = temp*each
    return out

@ Timer
def part2(inp, start_stamp=100_000_000_000_000, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    """ Chinese Remainder Theorem: https://www.youtube.com/watch?v=zIFehsBHB8o 
        remainder_mod_pairs needed -i for some reason, didn't really figure out why, but it worked """
    _, busses = inp
    # busses = [17,0,13,19]
    remainder_mod_pairs = []; N = 1
    for i,each in enumerate(busses):
        if each != 0:
            remainder_mod_pairs.append((-i,each))
            N *= each
    # remainder_mod_pairs = [(3,5),(1,7),(6,8)]; N = 5*7*8
    t = 0
    for bi,mod in remainder_mod_pairs:
        ni = N//mod
        xi = ni%mod
        i = 0
        while True:
            temp = (xi*i)%mod
            if temp == 1:
                xi = i
                break
            i += 1
        t = (t + bi*ni*xi) % N
    return t


if __name__ == "__main__":
    """ files needed
        - input.txt
        - test_{x}_input.txt, with x the test number"""
    t0 = time()
    day = 13; test = 0; prnt = test != 0
    inp = parse(day,test, prnt=prnt)
    part1(inp, prnt=True)
    part2(inp, prnt=True)
    print(f"Total time: {time()-t0}")