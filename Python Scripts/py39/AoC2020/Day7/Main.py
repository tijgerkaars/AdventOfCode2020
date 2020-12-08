

class Bag:
    """ node like doubly linked list """
    def __init__(self, name):
        self.name     = name # str
        self.parents  = {}   # str : Bag obj
        self.children = {}   # str : tuple(Bag obj, count)
    
    def __repr__(self):
        """ human readable prints """
        return f"{list(self.parents.keys())} > {self.name} > {list(self.children.keys())}"
    def __str__(self):
        return self.name

class BagPile:
    """ hold regulations: a querry tree allowing both upwards and downwards navigation """
    def __init__(self, instructions):
        self.bags = {} # str : Bag obj
        for instr in instructions:
            self.insert(instr)
    def __str__(self):
        """ human readable prints """
        string = ''
        for bag in self.bags.items():
            string += f"{repr(bag)}\n"
        return string
    def insert(self, instr):
        """ format and inset regulations into tree """
        parent, children = instr.split(' contain ')
        parent = self.get_bag(parent)
        for child in children.split(', '):
            n, t = child.split(' ', 1)
            try:
                n = int(n)
            except ValueError:
                n = 0
                t = child
            child = self.get_bag(t)
            parent.children[t] = (child, n)
            child.parents[parent.name] = parent
        
    def get_bag(self, bag: str):
        """ ensures each bag type gets created only once and thus proper linking in the tree """
        try:
            b = self.bags[bag]
        except KeyError:
            b = self.bags[bag] = Bag(bag)
        return b
    
    def querry_parent(self, bag, querried = None):
        """ querries upward to find any starting nodes that are upstream from the target 
            Path doesn't matter so a set is used
            returns amound of starting nodes"""
        querried = querried if querried != None else set()
        if not bag in self.bags.keys(): # check for user error
            raise KeyError(f"{bag} not in pile, try: {self.bags.keys()}")
        q = self.get_bag(bag)
        for name in q.parents.keys():
            if name not in querried: # new step in path
                querried.add(name)
                self.querry_parent(name, querried)
        return len(querried)

    def querry_contained(self, bag , count = 0):
        """ moves down tree and returns sums of bags inside the querried bag """
        if not bag in self.bags.keys():
            raise KeyError(f"{bag} not in pile, try: {self.bags.keys()}")
        q = self.get_bag(bag)
        for child, inf in q.children.items():
            count += inf[1] * (1 + self.querry_contained(child)) # 'amound of the bag contained' * (that bag + it's content)
        return count




if __name__ == "__main__":
    from time import time
    t0 = time()
    test = 0
    f = f"{f'test{test}' if test > 0 else ''}Input.txt"

    t4 = time()
    with open(rf"Python Scripts\py39\AoC2020\Day7\{f}") as f:
        # again, learning regex might be good :S
        instructions = [line.replace(' bags','').replace(' bag','').replace('\n','').replace('.','') for line in f]
    print("input parce:", time()- t4)
    t3 = time(); pile = BagPile(instructions); print("tree building:", time()-t3)
    t1 = time(); print(f"part 1: {pile.querry_parent('shiny gold')} -- {time()-t1}")
    t2 = time(); print(f"part 2: {pile.querry_contained('shiny gold')} -- {time()-t2}")

    print("total:", time()-t0)
