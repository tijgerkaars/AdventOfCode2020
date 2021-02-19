class Player:
    def __init__(self, game, name:str='None'):
        self.game = game
        self.name = name
        self.hand = []
        self.resources  = { r:0 for r in game.resources }
        self.production = { r:0 for r in game.resources }

    def __str__(self):
        string  = f'Player: {self.name}\n'
        string += '\nResources:\n'  + ' - '.join( [ f'{r[:2]}: {v}' for r,v in self.resources.items()  ] ) + '\n'
        string += '\nProduction:\n' + ' - '.join( [ f'{r[:2]}: {v}' for r,v in self.production.items() ] ) + '\n'
        
        return string + self.game.devider










        
if __name__ == "__main__":
    import Main