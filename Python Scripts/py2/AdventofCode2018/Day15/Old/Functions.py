class dungeon():
    def __init__ (self,input):
        print "input:", input
        self.grid = []
        for y in range(len(input)):
            self.grid.append([])
            for x in range(len(input[y])):
                new_square = self.square()
                new_square.position = (y,x)
                new_square.state = str(input[y][x])
                self.grid[y].append(new_square)
    def __str__ (self):
        string = ""
        for row in self.grid:
            for tile in row:
                string += tile.state
            string += "\n"
        return string


class square(dungeon):
    def __init__ (self):
        self.position = None
        self.state = None

        self.North = None
        self.East = None
        self.South = None
        self.West = None

    def find_enemys(self):
        print self.grid
