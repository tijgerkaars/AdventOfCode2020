def format(l):
    two_d_grid = []
    for y,row in enumerate(l):
        two_d_grid.append([])
        for x,square in enumerate(l[y]):
            two_d_grid[y].append(square)
    return two_d_grid


class forrest():
    def __init__(self,starting_state):
        self.starting_state = starting_state
        self.heigth = len(starting_state)
        self.width = len(starting_state[0])
        self.top_down = []
        for y,row in enumerate(starting_state):
            self.top_down.append([])
            for x,square in enumerate(row):
                self.top_down[y].append(tile((y,x),starting_state[y][x]))
        self.find_neigbours()
        self.minutes = 0

        self.open_tiles = 0
        self.tree_tiles = 0
        self.yard_tiles = 0
        self.last_score = self.score()

    def update(self):
        self.minutes += 1
        # for each tile
        # check the surroundings/neigbours
        # determine the next rounds state
        # update all the squares
        for y,row in enumerate(self.top_down):
            for x,tile in enumerate(row):
                neigbours = [str(each) for each in tile.set_neigbours()]
                temp = ""
                for each in neigbours:
                    if each != "None":
                        temp += each
                neigbours = temp
                if tile.state == ".":
                    if neigbours.count("|") >= 3:
                        tile.next_state = "|"
                elif tile.state == "|":
                    if neigbours.count("#") >= 3:
                        tile.next_state = "#"
                elif tile.state == "#":
                    if neigbours.count("#") >= 1 and neigbours.count("|") >= 1:
                        tile.next_state = "#"
                    else:
                        tile.next_state = "."
                else:
                    print("we donne fucked up")

        for y,row in enumerate(self.top_down):
            for x,tile in enumerate(row):
                if tile.next_state:
                    tile.state = tile.next_state
                tile.next_state = None

    def score(self):
        self.open_tiles = 0
        self.tree_tiles = 0
        self.yard_tiles = 0
        for y,row in enumerate(self.top_down):
            for x,tile in enumerate(row):
                if tile.state == ".":
                    self.open_tiles += 1
                elif tile.state == "|":
                    self.tree_tiles += 1
                elif tile.state == "#":
                    self.yard_tiles += 1
        return self.open_tiles, self.tree_tiles , self.yard_tiles



    def find_neigbours(self):
        for y,row in enumerate(self.top_down):
            for x,tile in enumerate(row):
                if y-1 >= 0:
                    tile.N = self.top_down[y-1][x]
                    if x-1 >= 0:
                        tile.NW = self.top_down[y-1][x-1]
                    if x+1 < self.width:
                        tile.NE = self.top_down[y-1][x+1]
                if y+1 < self.heigth:
                    tile.S = self.top_down[y+1][x]
                    if x-1 >= 0:
                        tile.SW = self.top_down[y+1][x-1]
                    if x+1 < self.width:
                        tile.SE = self.top_down[y+1][x+1]
                if x-1 >= 0:
                    tile.W = self.top_down[y][x-1]
                if x+1 < self.width:
                    tile.E = self.top_down[y][x+1]

    def __str__(self):
        print ("\n" + str(self.minutes))
        string = "\n"
        for y,row in enumerate(self.top_down):
            for x,square in enumerate(row):
                string += str(square)
            string += "\n"
        string += "\n"
        return string





class tile():
    def __init__(self,coords,state):
        self.coords = coords
        self.state = state
        self.next_state = None
        self.N = None
        self.NE = None
        self.E = None
        self.SE = None
        self.S = None
        self.SW = None
        self.W = None
        self.NW = None
        self.neigbours = None

    def set_neigbours(self):
        return [
        self.N, self.NE,
        self.E, self.SE,
        self.S, self.SW,
        self.W, self.NW
        ]

    def __str__(self):
        return self.state
