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

def pprint(grid):
    string = ''
    for row in grid:
        for square in row:
            if square == 0:
                string += 'L'
            elif square == 1 :
                string += '#'
            elif square == -1:
                string += '.'
            else:
                string += str(square)
        string += '\n'
    print(string)

def copy(grid):
    return [row[:] for row in grid]



def count_occupied(grid):
    out = 0
    for row in grid:
        for square in row:
            if square == 1:
                out +=1
    return out
@ Timer
def parse(day:int,test:int, *arg, **args):
    """ imports input file from "AoC2020\Day{day}\{f}"  """
    f = f"{f'test_{test}_' if test > 0 else ''}input.txt"
    with open(rf"AoC2020\Day{day}\{f}") as f:
        # Parsing goes here
        lines = [[0 if each == 'L' else -1 for each in line.strip()] for line in f.readlines()]
        # pprint(lines)
    return lines

@ Timer
def part1(inp, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    def neigbours(x,y,grid, n=0):
        by,bx = (len(grid), len(grid[0]))
        for dx,dy in (
                        (1,1),(1,0),(1,-1),
                        (0,1),(0,-1),
                        (-1,1),(-1,0),(-1,-1)
                    ):
            if by > y+dy >= 0 and bx > x+dx >= 0:
                if grid[y+dy][x+dx] == 1:
                    n+=1
        return n
    new = copy(inp)
    old = []
    i = 0
    while old != new:
        i+=1
        old = copy(new)
        for y,row in enumerate(old):
            for x,square in enumerate(row):
                if square == -1:
                    continue
                n = neigbours(x,y,old)
                if n == 0 and square == 0:
                    new[y][x] = 1
                elif n>=4 and square == 1:
                    new[y][x] = 0
        # print(i)
    return count_occupied(new)


@ Timer
def part2(inp, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    directions = ( (1,1),(1,0),(1,-1),(0,1),(0,-1),(-1,1),(-1,0),(-1,-1))
    by,bx = (len(inp), len(inp[0]))
    bm = max(by,bx)


    def neigbours(x,y,grid, debug=False):
        n = 0
        for dx,dy in directions:                        # for the x/y of all 8 directions
            for _ in range(1,bm):                       #   for the max length of the field
                dx+=1;dy+=1                             #       i steps along the direction
                if by > y+dy >= 0 and bx > x+dx >= 0:   #       if still on the board
                    if grid[y+dy][x+dx] == 1:           #           if the square is occupied
                        n +=1                           #               you see a occupied chair
                        break                           #               don't look in this direction
                    elif grid[y+dy][x+dx] == 0:         #            if the square is a chair but unoccupied
                        break                           #               don't look in this direction
                else:                                   #       you have passed beyond the border
                    break                               #           stop looking here
        return n
    

    new = copy(inp)                                     # don't mutate the input        
    old = copy(inp) 
    old[0][0] = -2                                      # make an empty copy 
    i = 0
    while old != new:                 # While the updated grid is different than the reference grid
        i+=1
        for y,row in enumerate(old):
            for x,square in enumerate(row):
                if square == -1:
                    continue
                n = neigbours(x,y,old)
                if n == 0 and square == 0:
                    new[y][x] = 1
                elif n>=5 and square == 1:
                    new[y][x] = 0
        t   = new
        new = old
        old = t
    print(i)
    return count_occupied(new)


        



if __name__ == "__main__":
    """ files needed
        - input.txt
        - test_{x}_input.txt, with x the test number"""
    t0 = time()
    day = 11; test = 0; prnt = test != 0
    inp = parse(day,test, prnt=prnt)
    part1(inp, prnt=True)
    part2(inp, prnt=True) # and > 2168
    print(f"Total time: {time()-t0}")