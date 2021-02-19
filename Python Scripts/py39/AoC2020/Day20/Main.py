import numpy as np
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
        lines = [tile_piece.strip().replace(':', '').splitlines() for tile_piece in f.read().split('\n\n')]
        tiles = { int(tile[0].split(' ')[1]) : tile[1:] for tile in lines}
        for tile in tiles:
            tiles[tile] = Tile(tile, tiles[tile])
    return tiles

class Tile:
    def __init__(self, id, layout):
        self.id     = id
        self.layout = np.array( [list(map(tile_str_2_bool, each)) for each in layout] )
        self.set_all_current_sides()

        self.connected = {}
    
    def set_all_current_sides(self):
        self.sides  = np.array( 
                       (self.layout[0],
                        self.layout[:,-1],
                        np.fromiter(reversed(self.layout[-1]), dtype=int),
                        np.fromiter(reversed(self.layout[:,0]), dtype=int)   )
        )
        self.reversed_sides = np.array(
            [np.fromiter(reversed(each), dtype=int) for each in self.sides]
        )

    def __repr__(self):
        return str(self.id)

    def intersect(self, other):
        for i,this in enumerate(self.sides):
            for j,that in enumerate(other.sides):
                if (this == that).all():
                    print(f'matches unflipped')
                    return i,j,0
            for j,that in enumerate(other.reversed_sides):
                if (this == that).all():
                    print('matches a flipped')
                    return i,j,1
            

        

def tile_str_2_bool(t):
    return 1 if t =='#' else 0

@ Timer
def part1(inp, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""

    for each in inp.values():
        for other in inp.values():
            if each != other:
                print(each.intersect(other))
                print()
                print( each.layout)
                print()
                print(other.layout)
                return

@ Timer
def part2(inp, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    pass

if __name__ == "__main__":
    """ files needed
        - input.txt
        - test_{x}_input.txt, with x the test number"""
    t0 = time()
    day = 20; test = 1; prnt = test != 0
    inp = parse(day,test, prnt=prnt)
    part1(inp, prnt=True)
    # part2(inp, prnt=True)
    print(f"Total time: {time()-t0}")