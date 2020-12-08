import imput

class cart():
    def __init__(self):
        self.crossing = "l"
        self.direction = ""

class tracks():
    def __init__(self,number):
        game = imput.game[number]
        self.directionOrder = ("l", "s", "r")
        self.orientations = ("v", ">", "<", "^")
        self.raster = []
        self.newRaster = []
        for y in range(len(game)):
            self.raster.append([])
            print game[y]
            for x in range(len(game[y])):
                if game[y][x] == ">" or game[y][x] == "<" or game[y][x] == "v" or game[y][x] == "^":
                    self.raster[y].append(cart())
                    self.raster[y][x].direction = game[y][x][:]
                else:
                    self.raster[y].append(game[y][x])

    def tick(self):
        self.newRaster = []
        for y in range(len(self.raster)):
            self.newRaster.append([])
            for x in range(len(self.raster[y])):
                self.newRaster[y].append(self.raster[y][x])
                if type(self.raster[y][x]) == type(cart()):
                    self.raster[y][x] = self.raster[y][x].direction
        for y in range(len(self.raster)):
            for x in range(len(self.raster[y])):
                if self.raster[y][x] == ">":
                    self.moveR(y,x)
                elif self.raster[y][x] == "^":
                    self.moveU(y,x)
                elif self.raster[y][x] == "<":
                    self.moveL(y,x)
                elif self.raster[y][x] == "v":
                    self.moveD(y,x)
        self.raster = self.newRaster[:]


    def moveD(self,y,x):
        if self.raster[y+1][x] == "|":
            self.newRaster[y+1][x] = self.newRaster[y][x]
            self.newRaster[y][x] = "|"
        elif self.raster[y+1][x] == "\\":
            self.newRaster[y][x].direction = ">"
            if type(self.newRaster[y+1][x+1]) == type(cart()):
                self.newRaster[y][x].direction = "X"
            self.newRaster[y+1][x+1] = self.newRaster[y][x]
            self.newRaster[y][x] = "|"
        elif self.raster[y+1][x] == "/":
            self.newRaster[y][x].direction = "<"
            if type(self.newRaster[y+1][x-1]) == type(cart()):
                self.newRaster[y][x].direction = "X"
            self.newRaster[y+1][x-1] = self.newRaster[y][x]
            self.newRaster[y][x] = "|"
        elif self.raster[y+1][x] == "+":
            self.moveC(y,x)

    def moveL(self,y,x):
        if self.raster[y][x-1] == "-":
            self.newRaster[y][x-1] = self.newRaster[y][x]
            self.newRaster[y][x] = "-"
        elif self.raster[y][x-1] == "/":
            self.newRaster[y][x].direction = "v"
            if type(self.newRaster[y+1][x-1]) == type(cart()):
                self.newRaster[y][x].direction = "X"
            self.newRaster[y+1][x-1] = self.newRaster[y][x]
            self.newRaster[y][x] = "-"
        elif self.raster[y][x-1] == "\\":
            self.newRaster[y][x].direction = "^"
            if type(self.newRaster[y-1][x-1]) == type(cart()):
                self.newRaster[y][x].direction = "X"
            self.newRaster[y-1][x-1] = self.newRaster[y][x]
            self.newRaster[y][x] = "-"
        elif type(self.raster[y][x-1]) == type(cart()):
            self.newRaster[y][x].direction = "X"
        elif self.raster[y][x-1] == "+":
            self.moveC(y,x)


    def moveU(self,y,x):
        if self.raster[y-1][x] == "|":
            self.newRaster[y-1][x] = self.newRaster[y][x]
            self.newRaster[y][x] = "|"
        elif self.raster[y-1][x] == "\\":
            self.newRaster[y][x].direction = "<"
            if type(self.newRaster[y-1][x-1]) == type(cart()):
                self.newRaster[y][x].direction = "X"
            self.newRaster[y-1][x-1] = self.newRaster[y][x]
            self.newRaster[y][x] = "|"
        elif self.raster[y-1][x] == "/":
            self.newRaster[y][x].direction = ">"
            if type(self.newRaster[y-1][x+1]) == type(cart()):
                self.newRaster[y][x].direction = "X"
            self.newRaster[y-1][x+1] = self.newRaster[y][x]
            self.newRaster[y][x] = "|"
        elif self.raster[y-1][x] == "+":
            self.moveC(y,x)

    def moveR(self,y,x):
        if self.raster[y][x+1] == "-":
            self.newRaster[y][x+1] = self.newRaster[y][x]
            self.newRaster[y][x] = "-"
        elif self.raster[y][x+1] == "/":
            self.newRaster[y][x].direction = "^"
            if type(self.newRaster[y-1][x+1]) == type(cart()):
                self.newRaster[y][x].direction = "X"
            self.newRaster[y-1][x+1] = self.newRaster[y][x]
            self.newRaster[y][x] = "-"
        elif self.raster[y][x+1] == "\\":
            self.newRaster[y][x].direction = "v"
            if type(self.newRaster[y+1][x+1]) == type(cart()):
                self.newRaster[y][x].direction = "X"
            self.newRaster[y+1][x+1] = self.newRaster[y][x]
            self.newRaster[y][x] = "-"
        elif self.raster[y][x+1] == ">":
            self.newRaster[y][x].direction = "X"
            self.newRaster[y][x+1] = self.newRaster[y][x]
            self.newRaster[y][x] = "-"
        elif self.raster[y][x+1] == "X":
            self.newRaster[y][x].direction = "X"
            self.newRaster[y][x+1] = self.newRaster[y][x]
            self.newRaster[y][x] = "-"
        elif self.raster[y][x+1] == "+":
            self.moveC(y,x)

    def moveC(self,y,x):
        print "moveC test"
        print "crossing", self.newRaster[y][x].crossing
        print "direction:", self.newRaster[y][x].direction
        if self.raster[y][x] == ">":
            if self.newRaster[y][x].crossing == "l":
                self.itir(y,x)
                self.newRaster[y][x].direction = "^"
                self.newRaster[y-1][x+1] = self.newRaster[y][x]
                self.newRaster[y][x] = "-"
            elif self.newRaster[y][x].crossing == "s":
                self.itir(y,x)
                self.newRaster[y][x+2] = self.newRaster[y][x]
                self.newRaster[y][x] = "-"
            elif self.newRaster[y][x].crossing == "r":
                self.itir(y,x)
                self.newRaster[y][x].direction = "v"
                self.newRaster[y+1][x+1] = self.newRaster[y][x]
                self.newRaster[y][x] = "-"
        if self.raster[y][x] == "^":
            if self.newRaster[y][x].crossing == "l":
                self.itir(y,x)
                self.newRaster[y][x].direction = "<"
                self.newRaster[y+1][x-1] = self.newRaster[y][x]
                self.newRaster[y][x] = "-"
            elif self.newRaster[y][x].crossing == "s":

            elif self.newRaster[y][x].crossing == "r":

    def itir(self,y,x):
        print "itir test 1:", self.newRaster[y][x].crossing
        for i in range(len(self.directionOrder)):
            if self.newRaster[y][x].crossing == self.directionOrder[i]:
                if i+1 >= len(self.directionOrder):
                    self.newRaster[y][x].crossing = self.directionOrder[0]
                else:
                    self.newRaster[y][x].crossing = self.directionOrder[i+1]
                break
        print "itir test 2:", self.newRaster[y][x].crossing

    def pprint(self):
        print "\n"
        for y in range(len(self.raster)):
            temp = ""
            for x in range(len(self.raster[y])):
                if type(self.raster[y][x]) != type(cart()):
                    temp += self.raster[y][x]
                else:
                    temp += self.raster[y][x].direction
            print temp
        pass






game = tracks(2)
for i in range(3):
    game.tick()
    game.pprint()
