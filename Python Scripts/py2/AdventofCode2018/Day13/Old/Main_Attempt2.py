import imput
import challenge
from Tkinter import *

class cart():
    def __init__(self):
        self.crossing = "l"
        self.direction = ""

class tracks():
    def __init__(self,number,elves = False,test = False):
        if test:
            game = imput.game[number]
        else:
            game = challenge.game
        self.directionOrder = ("l", "s", "r")
        self.orientations = ("v", ">", "<", "^")
        self.elves = elves
        self.test = test
        self.repair = []
        self.carts = []
        self.rails = []
        self.raster = []
        self.newRaster = []
        print len(game)
        print len(game[0])
        for y in range(len(game)):
            self.raster.append([])
            self.rails.append([])
            self.repair.append([])
            for x in range(len(game[y])):
                if game[y][x] == ">" or game[y][x] == "<" or game[y][x] == "v" or game[y][x] == "^":
                    if game[y][x] == ">" or game[y][x] == "<":
                        self.rails[y].append("-")
                        self.repair[y].append("-")
                    elif game[y][x] == "v" or game[y][x] == "^":
                        self.rails[y].append("|")
                        self.repair[y].append("|")
                    self.carts.append((y,x))
                    self.raster[y].append(cart())
                    self.raster[y][x].direction = game[y][x][:]
                else:
                    self.rails[y].append(game[y][x][:])
                    self.repair[y].append(game[y][x][:])
                    self.raster[y].append(game[y][x][:])
        self.anim = True
        if self.anim:
            self.root = Tk()
            self.root.title('Minetracks')
            self.running = True
            self.scale = 4.5
            self.speed = 10
            self.stepwise = False
            self.canvas = Canvas(self.root, height = (self.scale * len(self.raster)) + 30, width = (self.scale * len(self.raster[0])))
            self.drawMap()
            self.updateMap()
            self.canvas.pack()
        if test:
            self.startTest(40)
            if self.anim:
                self.button("close window")
        else:
            self.start()

    def start(self):
        while not self.end():
            self.tick()
        self.pprint()

    def startTest(self,temp):
        for i in range(temp):
            self.pprint()
            self.tick()
        self.pprint()

    def buttonEnd(self):
        self.running = False


    def tick(self):
        self.newRaster = []
        self.carts = []
        for y in range(len(self.raster)):
            self.newRaster.append([])
            for x in range(len(self.raster[y])):
                self.newRaster[y].append(self.rails[y][x][:])
        for y in range(len(self.rails)):
            for x in range(len(self.rails[y])):
                if type(self.raster[y][x]) == type(cart()):
                    if self.raster[y][x].direction == "v" and self.repair[y+1][x] != " ":
                        self.moveD(y,x)
                        self.carts.append([y+1,x])
                    elif self.raster[y][x].direction == "<" and self.repair[y][x-1] != " ":
                        self.moveL(y,x)
                        self.carts.append([y,x-1])
                    elif self.raster[y][x].direction == "^" and self.repair[y-1][x] != " ":
                        self.moveU(y,x)
                        self.carts.append([y-1,x])
                    elif self.raster[y][x].direction == ">" and self.repair[y][x+1] != " ":
                        self.moveR(y,x)
                        self.carts.append([y,x+1])
                    elif self.raster[y][x].direction == "X":
                        self.newRaster[y][x] = cart()
                        self.newRaster[y][x].direction = "X"
        if self.elves:
            for y in range(len(self.rails)):
                for x in range(len(self.rails[y])):
                    if self.rails[y][x] == "X":
                        self.fixTrack(y,x)
        self.raster = self.newRaster
        if self.anim:
            if self.test:
                self.button("after move")
            self.updateMap()
            if self.stepwise:
                self.button("next slide")
            self.canvas.update()
            self.canvas.after(self.speed)

    def button(self,text = ""):
        self.running = True
        temp = Button(self.canvas, text = text, command = self.buttonEnd)
        self.canvas.create_window(20, (self.scale * len(self.raster) + 10), anchor = "w", window = temp, height = 20, width = 200, tag = "button")
        self.canvas.pack()
        self.canvas.update()
        while self.running:
            self.root.after(100)
            self.canvas.update()
        self.canvas.delete("button")


    def updateMap(self):
        self.canvas.delete("cart")
        for each in self.carts:
            y,x = each
            self.canvas.create_rectangle((x+0.3)*self.scale,(y+0.3)*self.scale,(x+0.7)*self.scale,(y+0.7)*self.scale, fill = "red", tag = "cart")
            self.canvas.create_text((x+0.5)*self.scale,(y+0.5)*self.scale, fill = "grey", tag = "cart")
            if self.test and self.stepwise:
                self.button()

    def moveR(self,y,x):
        if type(self.newRaster[y][x+1]) == type(cart()) or type(self.raster[y][x+1]) == type(cart()):
            self.raster[y][x].direction = "X"
            self.raster[y][x+1] = self.rails[y][x]
            self.rails[y][x+1] = "X"
        else:
            if self.rails[y][x+1] == "-":
                self.raster[y][x].direction = ">"
            elif self.rails[y][x+1] == "\\":
                self.raster[y][x].direction = "v"
            elif self.rails[y][x+1] == "/":
                self.raster[y][x].direction = "^"
            elif self.rails[y][x+1] == "+":
                self.moveC(y,x)
        self.newRaster[y][x+1] = self.raster[y][x]
        self.newRaster[y][x] = self.rails[y][x][:]

    def moveL(self,y,x):
        if type(self.newRaster[y][x-1]) == type(cart()):
            self.raster[y][x].direction = "X"
            self.newRaster[y][x-1].direction = "X"
            self.rails[y][x-1] = "X"
        else:
            if self.rails[y][x-1] == "-":
                self.raster[y][x].direction = "<"
            elif self.rails[y][x-1] == "\\":
                self.raster[y][x].direction = "^"
            elif self.rails[y][x-1] == "/":
                self.raster[y][x].direction = "v"
            elif self.rails[y][x-1] == "+":
                self.moveC(y,x)
            self.newRaster[y][x-1] = self.raster[y][x]
            self.newRaster[y][x] = self.rails[y][x][:]

    def moveD(self,y,x):
        if type(self.raster[y+1][x]) == type(cart()):
            self.raster[y][x].direction = "X"
            self.raster[y+1][x].direction = "X"
            self.rails[y+1][x] = "X"
        else:
            if self.rails[y+1][x] == "|":
                self.raster[y][x].direction = "v"
            elif self.rails[y+1][x] == "/":
                self.raster[y][x].direction = "<"
            elif self.rails[y+1][x] == "\\":
                self.raster[y][x].direction = ">"
            elif self.rails[y+1][x] == "+":
                self.moveC(y,x)
        self.newRaster[y+1][x] = self.raster[y][x]
        self.newRaster[y][x] = self.rails[y][x][:]

    def moveU(self,y,x):
        if type(self.newRaster[y-1][x]) == type(cart()):
            self.raster[y][x].direction = "X"
            self.newRaster[y-1][x].direction = "X"
            self.rails[y-1][x] = "X"
        else:
            if self.rails[y-1][x] == "|":
                self.raster[y][x].direction = "^"
            elif self.rails[y-1][x] == "/":
                self.raster[y][x].direction = ">"
            elif self.rails[y-1][x] == "\\":
                self.raster[y][x].direction = "<"
            elif self.rails[y-1][x] == "+":
                self.moveC(y,x)
        self.newRaster[y-1][x] = self.raster[y][x]
        self.newRaster[y][x] = self.rails[y][x][:]

    def moveC(self,y,x):
        if self.raster[y][x].direction == ">":
            if self.raster[y][x].crossing == "l":
                self.raster[y][x].direction = "^"
                self.itir(y,x)
            elif self.raster[y][x].crossing == "s":
                self.raster[y][x].direction = ">"
                self.itir(y,x)
            elif self.raster[y][x].crossing == "r":
                self.raster[y][x].direction = "v"
                self.itir(y,x)
        elif self.raster[y][x].direction == "^":
            if self.raster[y][x].crossing == "l":
                self.raster[y][x].direction = "<"
                self.itir(y,x)
            elif self.raster[y][x].crossing == "s":
                self.raster[y][x].direction = "^"
                self.itir(y,x)
            elif self.raster[y][x].crossing == "r":
                self.raster[y][x].direction = ">"
                self.itir(y,x)
        elif self.raster[y][x].direction == "v":
            if self.raster[y][x].crossing == "l":
                self.raster[y][x].direction = ">"
                self.itir(y,x)
            elif self.raster[y][x].crossing == "s":
                self.raster[y][x].direction = "v"
                self.itir(y,x)
            elif self.raster[y][x].crossing == "r":
                self.raster[y][x].direction = "<"
                self.itir(y,x)
        elif self.raster[y][x].direction == "<":
            if self.raster[y][x].crossing == "l":
                self.raster[y][x].direction = "v"
                self.itir(y,x)
            elif self.raster[y][x].crossing == "s":
                self.raster[y][x].direction = "<"
                self.itir(y,x)
            elif self.raster[y][x].crossing == "r":
                self.raster[y][x].direction = "^"
                self.itir(y,x)

    def itir(self,y,x):
        for i in range(len(self.directionOrder)):
            if self.directionOrder[i] == self.raster[y][x].crossing:
                if i+1 >= len(self.directionOrder):
                    self.raster[y][x].crossing = self.directionOrder[0]
                else:
                    self.raster[y][x].crossing = self.directionOrder[i+1]
                break

    def fixTrack(self,y,x):
        self.newRaster[y][x] = self.repair[y][x][:]
        self.raster[y][x] = self.repair[y][x][:]
        self.rails[y][x] = self.repair[y][x][:]


    def drawMap(self):
        for each in self.repair:
            print each
        for y in range(len(self.repair)):
            for x in range(len(self.repair[0])):
                # self.canvas.create_rectangle(x*self.scale,y*self.scale,(x+1)*self.scale,(y+1)*self.scale, tag = "line", tag = "backGrid")
                if self.repair[y][x] == "|":
                    self.canvas.create_line((x+0.5)*self.scale,y*self.scale,(x+0.5)*self.scale,(y+1)*self.scale, fill = "grey", tag = "line")
                elif self.repair[y][x] == "-":
                    self.canvas.create_line(x*self.scale,(y+0.5)*self.scale,(x+1)*self.scale,(y+0.5)*self.scale, fill = "grey", tag = "line")
                elif self.repair[y][x] == "+":
                    self.canvas.create_line((x+0.5)*self.scale,y*self.scale,(x+0.5)*self.scale,(y+1)*self.scale, fill = "grey", tag = "line")
                    self.canvas.create_line(x*self.scale,(y+0.5)*self.scale,(x+1)*self.scale,(y+0.5)*self.scale, fill = "grey", tag = "line")
                    self.canvas.create_line((x)*self.scale,(y+0.5)*self.scale,(x+0.5)*self.scale,(y+1)*self.scale, fill = "grey", tag = "line")
                    self.canvas.create_line(x*self.scale,(y+0.5)*self.scale,(x+0.5)*self.scale,(y)*self.scale, fill = "grey", tag = "line")
                    self.canvas.create_line((x+0.5)*self.scale,(y+1)*self.scale,(x+1)*self.scale,(y+0.5)*self.scale, fill = "grey", tag = "line")
                    self.canvas.create_line((x+0.5)*self.scale,(y)*self.scale,(x+1)*self.scale,(y+0.5)*self.scale, fill = "grey", tag = "line")
                elif self.repair[y][x] == "/":
                    if y-1 >= 0 and x-1 >= 0:
                        if self.repair[y-1][x] in ("|","+","\\","/") and self.repair[y][x-1] in ("-","+","\\","/"):
                            self.canvas.create_line(x*self.scale,(y+0.5)*self.scale,(x+0.5)*self.scale,(y)*self.scale, fill = "grey", tag = "line")
                    if y+1 < len(self.repair) and x+1 < len(self.repair[y]):
                        if self.repair[y+1][x] in ("|","+","\\","/")and self.repair[y][x+1] in ("-","+","\\","/"):
                            self.canvas.create_line((x+0.5)*self.scale,(y+1)*self.scale,(x+1)*self.scale,(y+0.5)*self.scale, fill = "grey", tag = "line")
                elif self.repair[y][x] == "\\":
                    if y-1 >= 0 and x+1 < len(self.repair[y]):
                        if self.repair[y-1][x] in ("|","+","\\","/") and self.repair[y][x+1] in ("-","+","\\","/"):
                            self.canvas.create_line((x+0.5)*self.scale,(y)*self.scale,(x+1)*self.scale,(y+0.5)*self.scale, fill = "grey", tag = "line")
                    if y+1 < len(self.repair) and  x-1 >= 0:
                        if self.repair[y+1][x] in ("|","+","\\","/") and self.repair[y][x-1] in ("-","+","\\","/"):
                            self.canvas.create_line((x)*self.scale,(y+0.5)*self.scale,(x+0.5)*self.scale,(y+1)*self.scale, fill = "grey", tag = "line")

    def crash(self):
        for y in range(len(self.rails)):
            for x in range(len(self.rails[y])):
                if self.rails[y][x] == "X":
                    print "crash:", x,y
                    return True
        return False

    def survivor(self):
        bestCart = []
        for y in range(len(self.raster)):
            for x in range(len(self.raster[y])):
                if type(self.raster[y][x]) == type(cart()):
                    bestCart.append((x,y))
        if len(bestCart) == 1:
            print "bestcart:", bestCart[0]
            return True
        elif len(bestCart) == 0:
            print "All carts destroyed"
            return True
        else:
            print "Remaining carts:", len(bestCart)
            return False

    def end(self):
        if self.elves:
            return self.survivor()
        else:
            return self.crash()

    def pprint(self,rails = False):
        print "____________________"
        for y in range(len(self.raster)):
            temp = ""
            for x in range(len(self.raster[y])):
                if type(self.raster[y][x]) != type(cart()):
                    temp += self.raster[y][x]
                else:
                    temp += self.raster[y][x].direction
            print temp
        print "\n"
        if rails:
            for y in range(len(self.rails)):
                temp = ""
                for x in range(len(self.rails[y])):
                    temp += self.rails[y][x]
                print temp

game = tracks(1,True,False)
