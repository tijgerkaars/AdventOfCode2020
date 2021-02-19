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
        lines = [(each[0], int(each[1:])) for each in f.readlines()[0].split()]
        print(lines)
    return lines

@ Timer
def part1(inp, direct = {'N':0, 'E':1, 'S':2, 'W':3}, coords = (0,0), **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    current_dir = 1
    for instr, n in inp:
        if instr == 'F':
            instr = current_dir
        elif instr in 'RL':
            if instr == 'R':
                current_dir += n//90
            else:
                current_dir -= n//90
            current_dir %= 4
            continue
        else:
            instr = direct[instr]
        x,y = coords
        if instr == 0:
            coords = (x,y+n)
        elif instr == 1:
            coords = (x+n,y)
        elif instr == 2:
            coords = (x,y-n)
        elif instr == 3:
            coords = (x-n,y)
    return sum(abs(each) for each in coords)

@ Timer
def part2(inp, direct = {'N':0, 'E':1, 'S':2, 'W':3}, coords = (0,0), waypoint =(10,1), **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    import math
    for i,n in inp:
        if   i=='F':        # if the instruction is F, move ntimes towards waypoint
            x,y   = coords
            dx,dy = waypoint
            dx*=n;dy*=n
            coords = (x+dx, y+dy)
            continue
        elif i in ('R', 'L'): # if the instruction is R or L rotate the waypoint around the boat
            if i == 'L':
                n *= -1
            x,y = waypoint
            radians = n*(math.pi/180)
            xx = x * math.cos(radians) + y * math.sin(radians) 
            yy = -x * math.sin(radians) + y * math.cos(radians)      
            waypoint = tuple(math.floor(each) if each%1<0.5 else math.ceil(each) for each in (xx,yy))
            continue
        else:               # move the waypoint in the direction of the instruction
            i = direct[i]
            x,y = waypoint
            if   i==0:
                waypoint = (x,y+n)
            elif i==1:
                waypoint = (x+n,y)
            elif i==2:
                waypoint = (x,y-n)
            elif i==3:
                waypoint = (x-n,y)
    return sum(abs(each) for each in coords)






if __name__ == "__main__":
    """ files needed
        - input.txt
        - test_{x}_input.txt, with x the test number"""
    t0 = time()
    day = 12; test = 0; prnt = test != 0
    inp = parse(day,test, prnt=prnt)
    part1(inp, prnt=True)
    part2(inp, prnt=True)
    print(f"Total time: {time()-t0}")