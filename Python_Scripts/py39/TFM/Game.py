from Player import Player
from Board  import Board

class Game:
    tages   = { 'Space',
                'Power',
                'Science',
                'Jovian',
                'Earth',
                'Plant',
                'Microbe',
                'Animal',
                'City',
                'Event'
            }
 
    resources   = ('Gold', 'Steel', 'Titanium', 'Plant', 'Energy', 'Heat')
    devider     = '\n' + '-#-#' * 50 + '-\n'
    turn        = 0
    milestone   = 0

    milestone_goals = {
        'base_terraformer'  : 35,
        'base_mayor'         : 3,
        'base_greenery'      : 3,
        'base_builder'       : 8,
        'base_tactician'     : 16

    }

    milestone_challenge= {
        'base' : {
            'base_terraformer'  : lambda p, m=milestone_goals : p.score            >= m['base_terraformer'],
            'base_mayor'        : lambda p, m=milestone_goals : p.cities           >= m['base_mayor'],
            'base_greenery'     : lambda p, m=milestone_goals : p.greeneries       >= m['base_greenery'],
            'base_builder'      : lambda p, m=milestone_goals : p.tages['builder'] >= m['base_builder'],
            'base_tactician'    : lambda p, m=milestone_goals : len(p.hand)        >= m['base_tactician'],
        }
    }
    awards      = 0
    award_price = (8,14,20)
    #board setup
    # board = board_setup_func(radius?) #NOTE map function, include position: resources, oceans, vulcano(s), cit(y)/(ies)
                                        #       file/json/etc...
    # temp setup
    temperature = 0
    temperature_range   = tuple(i for i in range(-30,8+1,2))
    temperature_range_l = len(temperature_range)
    temperature_events  = {
        -24: lambda p : p.increase_heat_production,
        -20: lambda p : p.increase_heat_production,
         0 : lambda p : p._place_tile(p, 'ocean') # TODO decidce whethere to put in player or in game
    }
    # oxygen setup
    oxygen = 0
    oxygen_range   = tuple(i for i in range(0,14+1,1))
    oxygen_range_l = len(temperature_range)
    oxygen_events  = {
        8 : lambda p : p.increase_temperature
    }
    # ocean setup
    oceans      = 0
    oceans_max  = 9
    ocean_pos   = { # NOTE place_holders till coordinate system is decided
        (1,1),
        (2,2),
        (3,3)
    }

    tile_placing = {
        'Greenery'  : lambda b, p, y,x : b._board_place_greenery(p ,y, x),
        'Ocean'     : lambda b, p, y,x : b._board_place_ocean(   p ,y, x),
        'City'      : lambda b, p, y,x : b._board_place_city(    p ,y, x)
    }
    def __init__(self, players=2):
        self.players = [Player(self, str(i)) for i in range(players)]
        [print(p) for p in self.players]
        self.board = Board(self)
        print(self.board)

        for player in self.players:
            self._game_place_city(player, 0,2)
            print(self.board)
            

            break

    def _raise_temperature(self, player):
        if self.temperature >= self.temperature_range_l:
            return False
        self.temperature += 1
        player.score     += 1
        if self.temperature_range[self.temperature] in self.temperature_events.keys():
            self.temperature_events[ self.temperature_range[self.temperature] ](player)
        return True
    
    def _raise_oxygen(self, player):
        if self.temperature >= self.oxygen_range_l:
            return False
        self.oxygen  += 1
        player.score += 1
        if self.oxygen_range[self.oxygen] in self.oxygen_events.keys():
            self.oxygen_events[ self.oxygen_range[self.oxygen] ](player)
    
    def _game_place_tile(self, player, y,x, tile='None'):
        try:
            code, resource = self.tile_placing[tile](self.board, player, y,x)
            if code == 'ERROR VALUE':
                raise InterruptedError(f'Error {code} in _game_place_tile {tile} ')
            return code, resource
        except:
            raise ValueError(f'{tile} is an unknown tile, known tiles are: {self.tile_placing.keys()}')
    
    def _game_place_city(self, player, y,x):
        try:
            code, resource = self._game_place_tile(player, y,x, 'City')
            player.cities += 1
        except:
            raise NotImplementedError
    
    def _game_place_greenery(self, player, y,x):
        self._raise_oxygen(player)
        raise NotImplementedError

    def _game_place_ocean(self, player, y,x):
        raise NotImplementedError








if __name__ == '__main__':
    import Main