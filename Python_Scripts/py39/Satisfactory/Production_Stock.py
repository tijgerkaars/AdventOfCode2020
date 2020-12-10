test = 'Test'

import numpy as np
import re

a = """
    1 Iron Ore -{2s}> 1 Iron Ingot
    3 Iron Ingot -> 2 Iron Plate
    10 Iron Ingot + 4 Plastic -{1s}> 15 Iron Plate
    1 Iron Ingot -{2s}> 1 Iron Rod
    1 Iron Rod -{2s}> 4 Screw
    6 Iron Plate + 12 Screw -{1m}> 1 Reinforced Iron Plate
    3000 Crude Oil -{3s}> 2 plastic + 2000 Heavy Oil Residue
    """

# iron_plate = 3*iron_ingot = 3*iron_ore


class Recipie:
    def __init__(self, inp, name = None):
        comp,t, prod = re.split(r"\s*-|>\s*",inp)
        # self.comp = {a[1] : int(a[0]) for each in comp.split('+') for a in ([(each.strip().split(' ',1))]) }
        self.t = t
        self.comp = {part : n for part,n in self.parse_formula_side(comp)}
        self.prod = {part : n for part,n in self.parse_formula_side(prod)}
        self.name = name if name != None else 'Unknown name'
        print(self)
    
    def parse_formula_side(self, f):
        for each in f.split('+'):
            each   = each.strip()
            n,part = each.split(' ',1)
            yield part, int(n) 
    
    def __repr__(self):
        comp_string = ' + '.join((f"({n}) {comp}" for comp, n in self.comp.items()))
        return comp_string
    
    def __str__(self, *arg, **args):
        comp_string = ' + '.join((f"({n}) {comp}" for comp, n in self.comp.items()))
        prod_string = ' + '.join((f"({n}) {prod}" for prod, n in self.prod.items()))
        return f"{comp_string} -{self.t}> {prod_string}"



# print(a)
class RecipieBook:
    node_products = {'Iron Ore', 'Copper Ore', 'Caterium Ore', 'S.A.M. Ore', 'Limestone', 'Coal', 'Raw Quartz', 'Sulfur', 'Uranium', 'Bauxite', 'Crude Oil'}
    def __init__(self, recipies):
        self.recipies = {}
        recipies = [recipie.strip() for recipie in recipies.strip().splitlines()]
        for recipie in recipies:
            recipie = Recipie(recipie)
            for each in recipie.prod.keys():
                try:
                    self.recipies[each].append( recipie )
                except KeyError:
                    self.recipies[each] = []
                    self.recipies[each].append( recipie )
    
    def querry(self, prod:str, target:list, amount:float = 1.0, prefered_recipies:list = None):
        if amount == 0:
            return 0
        print(self.recipies[prod])
        return
        for component in self.recipies[prod]:           # for each of the things needed to craft the desired item
            for each in component.comp.keys():
                if each in target:
                    return component.comp[each]
        
if __name__ == "__main__":
    book = RecipieBook(a)
    book.querry('Iron Plate', ['Iron Ore'])
