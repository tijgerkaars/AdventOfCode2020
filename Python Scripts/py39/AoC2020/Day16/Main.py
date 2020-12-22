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
        fields, ticket, others = [line for line in f.read().split('\n\n')]
        ticket = [list(map(int, other.split(','))) for other in ticket.split('\n')[1:]][0]
        others = [list(map(int, other.split(','))) for other in others.split('\n')[1:]]
    fields_dict = {}
    for field in fields.split('\n'):
        field, rules = field.split( ': ' )
        l = []
        for rule in rules.split(' or '):
            a,b = map(int, rule.split('-'))
            l.append( lambda x,a=a,b=b : bool(a<=x<=b) )
        fields_dict[field] = lambda x, l=l : any([each(x) for each in l])

    return fields_dict, ticket, others

@ Timer
def part1(fields, others, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    
    summed = 0; removed = []
    for i, other in enumerate(others):
        for each in other:
            if not any(lamb(each) for lamb in fields.values()):
                summed += each
                removed.append(i)
    for i in reversed(removed):
        others.pop(i)
    return summed



@ Timer
def part2(fields, ticket, others, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    possible_fields = [set(fields.keys()) for _ in ticket]
    print(possible_fields)

    for other_ticket in others:
        for i, each in enumerate(other_ticket):
            for field, test in fields.items():
                if not test(each):
                    # print(f"{other_ticket=}: {field} ({i}-{each})= {test(each)=}")
                    try:
                        possible_fields[i].remove(field)
                    except:
                        pass
                    # [print(j, each) for j,each in enumerate(possible_fields)]
        print('\n')
    
    ref_list = []; i = 0
    while ref_list != possible_fields and i < 10000:
        i+= 1
        ref_list = [each.copy() for each in possible_fields]
        for each in possible_fields:
            if len(each) == 1:
                for other in possible_fields:
                    if each != other:
                        other -= each
    [print(j, each) for j,each in enumerate(possible_fields)]
    x = 1
    for i,each in enumerate(possible_fields):
        each = list(each)[0]
        if 'departure' in each:
            x *= ticket[i]
    return x

if __name__ == "__main__":
    """ files needed
        - input.txt
        - test_{x}_input.txt, with x the test number"""
    t0 = time()
    day = 16; test = 0; prnt = test != 0
    fields, ticket, others = parse(day,test, prnt=prnt)
    part1(fields, others, prnt=True)
    part2(fields, ticket, others, prnt=True)
    print(f"Total time: {time()-t0}")