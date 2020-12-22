from time import time
import itertools


def produce_neigbours(x,y,z):
    for xi in range(-1,2):
        for yi in range(-1,2):
            for zi in range(-1,2):
                if not 0==xi==yi==zi:
                    yield (x+xi, y+yi, z+zi)

def loop_gen(r,d=None, _f=True):
    """ takes a list of ranges: r. produces all indexes of a nested loop of dept len(r) """

    if _f: # automatinc dimension check?
        if d == None:
            d = len(r) 
        elif len(r) != d:
            raise IndexError( f"{'Not enough' if len(r) < d else 'To many'} ranges ({len(r)}) provided for nesting depth ({d})" )
    if d>0:
        for i in range(*r[-d]): # loop bakcward so output indexi match input order of ranges pylint: disable=invalid-unary-operand-type
            a = [i] # add this index 
            for each in loop_gen(r,d-1, _f=False):
                yield a + each # add all other indexes left after it
    else: # start with an empty list
        yield []

def produce_N_neigbours(pos):
    N = len(pos) 
    for a in loop_gen( tuple((-1,2) for _ in range( N )) ):
        if a == [0]*N:
            continue
        yield tuple(map(sum,zip(pos,a)))

def evolve_dimension(pocket, cycles=6, activate=(3,), tolerate=(2,3)):
    for cycle in range(cycles):
        print(cycle)
        pocket_ref = pocket.copy()
        pocket = set()
        active_neigbouring = {}
        for each in pocket_ref:
            for other in produce_N_neigbours(each):
                try:
                    active_neigbouring[other] +=1
                except:
                    active_neigbouring[other] = 1
        for square, neigbours in active_neigbouring.items():
            if square in pocket_ref and neigbours in tolerate:
                pocket.add(square)
            elif square not in pocket_ref and neigbours in activate:
                pocket.add(square)
    return pocket
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
        lines = [each.strip() for each in f.readlines()]
    return lines

@ Timer
def part1(inp, cycles=6, activate=(3,), tolerate=(2,3), dimension = 4, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    pocket = { tuple([x,y] +[0]*(dimension-2)) for y,row in enumerate(inp) for x,state in enumerate(row) if state == '#'}
    pocket = evolve_dimension(pocket,  cycles=cycles, activate=activate, tolerate=tolerate)
    return len(pocket)

@ Timer
def part2(inp, cycles=6, activate=(3,), tolerate=(2,3), dimension = 4, **args):
    if dimension < 2:
        raise IndexError('To little dimensions, need to be 2d or higher')
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    pocket = { tuple([x,y] +[0]*(dimension-2)) for y,row in enumerate(inp) for x,state in enumerate(row) if state == '#'}
    pocket = evolve_dimension(pocket,  cycles=cycles, activate=activate, tolerate=tolerate)
    return len(pocket)

if __name__ == "__main__":
    """ files needed
        - input.txt
        - test_{x}_input.txt, with x the test number"""
    t0 = time()
    day = 17; test = 0; prnt = test != 0
    inp = parse(day,test, prnt=prnt)
    part1(inp, dimension = 3, prnt=True)
    part2(inp, dimension = 4, prnt=True)

    for i in range(5,8):
        part2(inp, dimension = i, prnt=True)
    print(f"Total time: {time()-t0}")