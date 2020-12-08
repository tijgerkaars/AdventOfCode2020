from time import time

def Timer(func):
    def Timer_wrapper(*arg, rtrn = True, prnt = False, **args):
        """ Function Timing decorator """
        t0 = time()
        out = func(*arg, **args)
        if prnt == True:
            print( f"{str(func)}: {out}  -- {time()-t0}" )
        if rtrn:
            return out
    return Timer_wrapper

@ Timer
def parse(day,test, *arg, **args):
    """ parse the input """
    f = f"{f'test_{test}_' if test > 0 else ''}input.txt"
    with open(rf"Python Scripts\py39\AoC2020\Day{day}\{f}") as f:
        lines = [ line.strip().split(' ') for line in f.readlines() ]
        lines = [(line[0], int(line[1])) for line in lines]
    return lines

class Console:
    def __init__(self, instructions):
        """ another opp code like thing :S 
            holds the instructions and the operations"""
        self.accumulator   = 0
        self.index         = 0
        self.instructions  = instructions
        self.visited = set()
        self.operations = {
            'nop' : self.nop,
            'acc' : self.acc,
            'jmp' : self.jmp
        }
        self.repair = {
            'nop' : 'jmp',
            'jmp' : 'nop'
        }

    def nop(self, n):
        """ increments index """
        self.index       += 1
        return True
    def acc(self, n):
        """ increments index by 1 and accumulator by n"""
        self.index       += 1
        self.accumulator += n
        return True
    def jmp(self,  n):
        """ jumps index by n """
        self.index += n
        return True

    @ Timer
    def part1(self, repair_index = None, **args):
        """ executes instructions till it starts repeating or till it exits. 
            Can take a repair_index that will swap instructions at that index acording to self.repair dict
            Then returns tuple: (acc, exit) 
            - With acc:  The accumulator
            - with exit: True if exit was normal or False if instruction index repeated """
        self.accumulator = 0
        self.index   = 0
        self.visited = set()
        while self.index not in self. visited and len(self.instructions) > self.index:
            self.visited.add(self.index)
            instr = self.instructions[self.index]
            instr, num = instr
            if self.index == repair_index:
                instr = self.repair[instr]
            self.operations[instr](num)
        return self.accumulator, self.index >= len(self.instructions)


    @ Timer
    def part2(self, inp, **args):
        """ Looks through the instructions till it finds a possibly broken instruction and tells the console to execute (part1 func for now) while 'repairing' said index """
        for i, (instr, _) in enumerate(inp):
            if instr in ['nop', 'jmp']:
                acc, truety = self.part1(repair_index=i)
                if truety:
                    return acc

if __name__ == "__main__":
    t0 = time()
    day = 8; test = 0; prnt = test != 0
    inp = parse(day,test, prnt=prnt)
    console = Console(inp)
    console.part1(prnt=True)
    console.part2(inp, prnt=True)
    print(f"Total time: {time()-t0}")