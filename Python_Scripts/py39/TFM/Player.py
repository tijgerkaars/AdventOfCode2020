class Player:
    def __init__(self, game, name:str='None'):
        self.game = game
        self.name = name
        self.hand = []
        self.cities     = 0
        self.greeneries = 0
        self.tiles      = 0
        self.resources  = { r:0 for r in game.resources }
        self.production = { r:0 for r in game.resources }

    def _player_raise_temp(self):
        if self.resources['heat'] >= 8:
            self.game._raise_temperature(self)
            return True
        return False

    def __str__(self):
        string  = f'Player: {self.name}\n'
        string += '\nResources:\n'  + ' - '.join( [ f'{r[:2]}: {v}' for r,v in self.resources.items()  ] ) + '\n'
        string += '\nProduction:\n' + ' - '.join( [ f'{r[:2]}: {v}' for r,v in self.production.items() ] ) + '\n'
        
        return string + self.game.devider










        
if __name__ == "__main__":
    import Main