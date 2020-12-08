import MineFunctions as f
import MineVizualize as v
import random
import Setting as s
import Tkinter as tk
from PIL import Image, ImageTk
from Tkinter import *

s.init()

class square():
    def __init__(self, position, probability = 0, bomb = False):
        self.number = 0
        self.button = 0
        self._widget = None
        self.state = "covered" # "covered"/"flagged"/"open"
        if type(position) == type(()):
            self.position = position
        else:
            print "square(position, "", "") must be tuple"
        if probability >= 100 or probability >= 0:
            self.probability = probability
        else:
            print "square("", probability, "") must be between 0 and 100"
        if type (bomb) == type(True):
            self.bomb = bomb
            if bomb:
                self.number = -1
        else:
            print "square("", "", bomb) must be boolean"
    def info(self,spec = "all"):
        if spec == "position" or spec == "all":
            print "position:", self.position
        if spec == "probability" or spec == "all":
            print "probability:", self.probability
        if spec == "bomb" or spec == "all":
            print "bomb:", self.bomb
        if spec == "number" or spec == "all":
            print "number:", self.number

    def __str__(self):
        string = str(self.number)
        return string


class grid():
    def __init__(self,width,height,bombs):
        self.height = height
        self.width = width
        self.bombs = bombs
        self.storage = []
        self.print_style = 1
        mineLocations = []
        temp = 0
        while len(mineLocations) != bombs and temp < 1000:
            temp += 1
            x = random.randint(0, self.height*self.width-1)
            if x not in mineLocations:
                mineLocations.append(x)
        mineLocations.sort()
        # mineLocations =  [30, 5, 17, 11,20, 29]
        # mineLocations = [2,5,7,8,9,12]
        print "TEST mineLocations:", len(mineLocations), mineLocations
        for y in range(height):
            self.storage.append([])
            for x in range(width):
                if y*self.width + x in mineLocations:
                    self.storage[y].append(square((y,x),100, True))
                else:
                    self.storage[y].append(square((y,x), 0, False))
        self.markMines()
        #-end init-

    def info(self,y,x):
        return self.storage[y][x].info()
    def markMines(self):
        h = 0
        raster = f.numbersIntoLists(self)
        for y in range(self.height):
            for x in range(self.width):
                if self.storage[y][x].number == -1:
                    # boven
                    if y-1 >= 0 and self.storage[y-1][x].number != -1 and True:
                        self.storage[y-1][x].number += 1
                    # links boven
                    if y-1 >= 0 and x-1 >= 0 and self.storage[y-1][x-1].number != -1 and True:
                        self.storage[y-1][x-1].number += 1
                    # rechts boven
                    if y-1 >= 0 and x+1 < self.width and self.storage[y-1][x+1].number != -1 and True:
                        self.storage[y-1][x+1].number += 1
                    # links
                    if x-1 >= 0 and self.storage[y][x-1].number != -1 and True:
                        self.storage[y][x-1].number += 1
                    # rechts
                    if x+1 < self.width and self.storage[y][x+1].number != -1 and True:
                        self.storage[y][x+1].number += 1
                    # links onder
                    if x-1 >= 0 and y+1 < self.height and self.storage[y+1][x-1].number != -1 and True:
                        self.storage[y+1][x-1].number += 1
                    # onder
                    if y+1 < self.height and self.storage[y+1][x].number != -1 and True:
                        self.storage[y+1][x].number += 1
                    # rechts onder
                    if x+1 < self.width and y+1 < self.height and self.storage[y+1][x+1].number != -1 and True:
                        self.storage[y+1][x+1].number += 1
        print "\n"

    def __str__(self):
        string = ""
        if self.print_style == 1:
            for y in range(len(self.storage)):
                for x in range(len(self.storage[y])):
                    if len(str(self.storage[y][x])) < 2:
                        string += " "
                    string += " " + str(self.storage[y][x])
                string += "\n"
            return string
        elif self.print_style == 2:
            for y in range(len(self.storage)):
                for x in range(len(self.storage[y])):
                    if self.storage[y][x].state == "covered":
                        string += "  #"
                    elif self.storage[y][x].state == "open":
                        if len(str(self.storage[y][x])) < 2:
                            string += " "
                        string += " " + str(self.storage[y][x])
                string += "\n"
            return string
        else:
            print "That is not a valid style"
            return None

def play():
    # get from imput:
    imput = (30 ,20 , 90)
    #imput = None
    if not imput:
        imput = v.getImput()

    raster = grid(imput[0],imput[1],imput[2])
    s.raster = raster

    s.canvas = v.startGame(s.raster)
    s.canvas.bind("<Button-1>", f.callback)
    s.canvas.pack()
    i = 0
    while True:
        print i
        i+=1
        s.canvas.update()
        s.canvas.after(100)
        if f.winFunction(s.raster):
            break
        if i > 10000:
            break
    s.canvas.after(1000)
    s.canvas.delete("all")
    s.canvas.after(1000)
    s.root.destroy()

    # print "test:", game.info(1,1)
    v.test(raster)
