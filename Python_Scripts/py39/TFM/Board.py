

class Board:
    tile_codes = {
        'Empty'     : ' .. ',
        'City'      : ' Ci ',
        'Greenery'  : ' Gr ',
        'Ocean'     : ' Oc ',
        'Special'   : ' SP '
    }
    str_m = None
    class Tile:
        owner = None
        def __init__(self, board, x,y, resource=None, reserve=None):
            self.board = board
            self.x, self.y = x,y
            self.resource  = resource
            self.reserve   = reserve
            self.placed    = None

        def __str__(self):
            return '    ' if self.placed is None else self.placed

    def __init__(self,game=None, grid_sid_len=5):
        if game is None and __name__ != '__main__':
            raise ValueError('Board needs a master. masterles initiation is only for debugging')
        self.game = game

        axis_len = grid_sid_len*2-1
        self.grid = [[self.Tile(self, i,j) for i in range(axis_len)] for j in range(axis_len)]
        for y in range(axis_len):
            _x = abs(y-axis_len//2)
            for x in range(_x//2,axis_len-(_x+1)//2):
                self.grid[y][x].placed = self.tile_codes['Empty']

    def __str__(self):
        string = ''
        for i,row in enumerate(self.grid):
            for square in row:
                if self.str_m is None:
                    string += f"{square} "
                elif self.str_m == 'coord':
                    if square.placed is None:
                        string += f"{square} "
                    else:
                        string += f"({square.y},{square.x}) "
            string += '\n'
            string += '\n' if i%2 else '\n  '
        self.str_m = None
        return string
    
    def _board_place_city(self, p ,y, x):
        try:
            t = self.grid[y][x]
            t.placed = self.tile_codes['City']
            t.owner  = p
            return 'Succes', t.resource
        except ValueError as e:
            print('fail point')
            return e, None

    def coord_map(self):
        self.str_m =  'coord'
        print(self)

"""
    b = Board()
    b.coord_map()
    b.grid[0][2].placed = b.tile_codes['City']
    print(b)
    """



if __name__ == '__main__':
    import Main




#