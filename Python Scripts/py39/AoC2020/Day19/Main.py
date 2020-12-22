from time import time
import re 


def Timer(func):
    def Timer_wrapper(*arg, rtrn:bool=True, prnt:bool=False, **args):
        """ rtrn: return the result if true
            prnt: print -- {the function that is being timed}: {result} -- {time it took}
            *arg and **args contain unnamed and named variables respectably to be passed to the function to be timed"""
        t0 = time()
        out = func(*arg, **args)
        if prnt == True:
            print( f"{str(func)}: {out}  -- {time()-t0}\n" )
        if rtrn:
            return out
    return Timer_wrapper

@ Timer
def parse(day:int,test:int, *arg, **args):
    """ imports input file from "AoC2020\Day{day}\{f}"  """
    f = f"{f'test_{test}_' if test > 0 else ''}input.txt"
    with open(rf"AoC2020\Day{day}\{f}") as f:
        # Parsing goes here
        rules, inputs = f.read().split('\n\n')
        rules  = [rule.strip().replace('"', '') for rule in rules.split('\n')]
        inputs = [inp.strip()  for inp in inputs.split('\n')]
    return rules, inputs

def rules_builder(rules, rule_dict):
    
    print( {each.split(': ')[0] : each.split(': ')[1] for each in rules}  )
    for each in rules:
        key,value = each.split(': ')
        if not '|' in value:
            value = lambda v=value.split(' '), r = rule_dict : ''.join([r[each]() if each.isdigit() else each for each in v])
        else:
            value=value.split(' | ')
            l1 = lambda v=value[0].split(' '), r = rule_dict : ''.join([r[each]() if each.isdigit() else each for each in v])
            l2 = lambda v=value[1].split(' '), r = rule_dict : ''.join([r[each]() if each.isdigit() else each for each in v])
            value = lambda v=value, l1=l1,l2=l2 : f"({l1()}|{l2()})"
        rule_dict[key] = value
    return rule_dict['0']()
        




@ Timer
def part1(rules, inputs, rule_dict, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    rules = rules_builder(rules, rule_dict)
    print(rules)
    return sum(re.match(f"^{rules}$", each) != None for each in inputs)


@ Timer
def part2(rules, inputs, rule_dict, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    rule_dict['8' ] = lambda r=rule_dict : f"{r['42']()}+"
    rule_dict['11'] = lambda r=rule_dict : f"({'|'.join([ r['42']()*i + r['31']()*i for i in range(1,15) ])})"
    rules = rule_dict['0']()
    # print(rules)
    return sum(re.match(f"^{rules}$", each) != None for each in inputs)

if __name__ == "__main__":
    """ files needed
        - input.txt
        - test_{x}_input.txt, with x the test number"""
    t0 = time()
    day = 19; test = 0; prnt = test != 0
    rules, inputs = parse(day,test, prnt=prnt)
    rule_dict = {}
    part1(rules, inputs, rule_dict, prnt=True)
    part2(rules, inputs, rule_dict, prnt=True)
    print(f"Total time: {time()-t0}")