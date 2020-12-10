import Input
import Challenge
# import challenge as i
import Tkinter as tk
import Vizualize as v

game = Input.game[4]
game = Challenge.game

class cart():
    def __init__(self):
        self.crossing = "l"
        self.direction = None
        self.track = None
        self.position = None

    def __str__(self):
        return str(self.direction)

    def move(self):
        # print self.position, "cart move:", self.direction
        if self.direction == ">":
            # rotate the cart
            if self.track.E.type == "/":
                self.direction = "^"
            elif self.track.E.type == "\\":
                self.direction = "v"
            elif self.track.E.type == "+":
                self.moveC()
            else:
                pass
            # remove the cart from this track
            self.track.carts.remove(self)
            # move it to the next track
            self.track.E.carts.append(self)
            # store  the marker to the new track
            self.track = self.track.E
            # change the cars position
            self.position = self.track.position
        elif self.direction == "v":
            if self.track.S.type == "/":
                self.direction = "<"
            elif self.track.S.type == "\\":
                self.direction = ">"
            elif self.track.S.type == "+":
                self.moveC()
            else:
                pass
            self.track.carts.remove(self)
            self.track.S.carts.append(self)
            self.track = self.track.S
            self.position = self.track.position
        elif self.direction == "<" and len(self.track.carts) < 2:
            if self.track.W.type == "/":
                self.direction = "v"
            elif self.track.W.type == "\\":
                self.direction = "^"
            elif self.track.W.type == "+":
                self.moveC()
            else:
                pass
            self.track.carts.remove(self)
            self.track.W.carts.append(self)
            self.track = self.track.W
            self.position = self.track.position
        elif self.direction == "^" and len(self.track.carts) < 2:
            if self.track.N.type == "/":
                self.direction = ">"
            elif self.track.N.type == "\\":
                self.direction = "<"
            elif self.track.N.type == "+":
                self.moveC()
            else:
                pass
            self.track.carts.remove(self)
            self.track.N.carts.append(self)
            self.track = self.track.N
            self.position = self.track.position
        return self.position

    def moveC(self):
        if self.crossing == "l":
            self.crossing = "s"
            if self.direction == ">":
                self.direction = "^"
            elif self.direction == "^":
                self.direction = "<"
            elif self.direction == "<":
                self.direction = "v"
            elif self.direction == "v":
                self.direction = ">"
        elif self.crossing == "s":
            self.crossing = "r"
        elif self.crossing == "r":
            self.crossing = "l"
            if self.direction == ">":
                self.direction = "v"
            elif self.direction == "v":
                self.direction = "<"
            elif self.direction == "<":
                self.direction = "^"
            elif self.direction == "^":
                self.direction = ">"



class rail_track():
    def __init__(self):
        self.parent = None
        self.position = None
        self.type = None
        self.carts = []
        self.N = None
        self.E = None
        self.S = None
        self.W = None

    def __str__(self):
        string = ""
        if len(self.carts) == 0:
            return str(self.type)
        elif len(self.carts) > 1:
            return "X"
        else:
            return str(self.carts[0])

class plan():
    def __init__(self,raster = None):
        tracks,rails = self.construct(raster)
        self.elves = elves
        # contains the map
        self.tracks = tracks
        # contains indivitual rail pieces
        self.rails = rails
        self.carts = self.cart_maker(raster)
        print self.carts

    def remove_crashes(self):
        temp = self.carts.keys()
        temp.sort()
        for each in temp:
            if len(self.carts[each].track.carts) > 1:
                self.carts[each].track.carts = []
                self.carts.pop(each)

    def update(self):
        order = self.carts.keys()
        order.sort()
        new_dict = dict()
        for i in range(len(order)):
            coord = self.carts[order[i]].move()
            new_dict[coord] = self.carts[order[i]]
        self.carts = new_dict

    def construct(self,raster):
        print raster
        temp = []
        for y in range(len(raster)):
            temp.append([])
            for x in range(len(raster[0])):
                if raster[y][x] != " ":
                    temp[y].append(rail_track())
                    temp[y][x].position = (y,x)
                    if raster[y][x] in ("^", "v", "|"):
                        temp[y][x].type = "|"
                    elif raster[y][x] in ("<", ">", "-"):
                        temp[y][x].type = "-"
                    elif raster[y][x] == "\\":
                        temp[y][x].type = "\\"
                    elif raster[y][x] == "/":
                        temp[y][x].type = "/"
                    elif raster[y][x] == "+":
                        temp[y][x].type ="+"
                    temp[y][x].parent = self
                else:
                    temp[y].append(raster[y][x])
        #reverence
        rev = rail_track()
        # for every rail element
        for y in range(len(raster)):
            for x in range(len(raster[0])):
                # if the current position is a track
                if type(temp[y][x]) == type(rail_track()):
                    # if the track is X
                    if temp[y][x].type == "|":
                        # if the positions along y are in bounds
                        if y-1 >= 0 and y+1 < len(raster):
                            # if the position North is a track that connects
                            if type(temp[y-1][x]) == type(rev) and temp[y-1][x].type != "-" and type(temp[y+1][x]) == type(rev) and temp[y+1][x].type != "-":
                                # the pointer North is now that track
                                temp[y][x].N = temp[y-1][x]
                                # the pointer South is now that track
                                temp[y][x].S = temp[y+1][x]
                    elif temp[y][x].type == "-":
                        if x-1 >= 0 and x+1 < len(raster[y]):
                            if type(temp[y][x-1]) == type(rev) and temp[y][x-1].type != "|" and type(temp[y][x+1]) == type(rev) and temp[y][x+1].type != "|":
                                temp[y][x].W = temp[y][x-1]
                                temp[y][x].E = temp[y][x+1]
                    elif temp[y][x].type == "/":
                        if x-1 >= 0 and y-1 >= 0:
                            if type(temp[y-1][x]) == type(rev) and type(temp[y][x-1]) == type(rev) and temp[y-1][x].type != "-" and temp[y][x-1].type != "|":
                                temp[y][x].N = temp[y-1][x]
                                temp[y][x].W = temp[y][x-1]
                        if x+1 < len(raster[y]) and y+1 < len(raster):
                            if type(temp[y+1][x]) == type(rev) and type(temp[y][x+1]) == type(rev) and temp[y+1][x].type != "-" and temp[y][x+1].type != "|":
                                temp[y][x].S = temp[y+1][x]
                                temp[y][x].E = temp[y][x+1]
                    elif temp[y][x].type == "\\":
                        if x-1 >= 0 and y+1 < len(raster):
                            if type(temp[y+1][x]) == type(rev) and type(temp[y][x-1]) == type(rev) and temp[y+1][x].type != "-" and temp[y][x-1].type != "|":
                                temp[y][x].S = temp[y+1][x]
                                temp[y][x].W = temp[y][x-1]
                        if x+1 < len(raster[y]) and y-1 >= 0:
                            if type(temp[y-1][x]) == type(rev) and type(temp[y][x+1]) == type(rev) and temp[y-1][x].type != "-" and temp[y][x+1].type != "|":
                                temp[y][x].N = temp[y-1][x]
                                temp[y][x].E = temp[y][x+1]
                    elif temp[y][x].type == "+":
                        if x-1 >= 0 and y+1 >= 0 and x+1 < len(raster[y]) and y-1 < len(raster):
                            if type(temp[y-1][x]) == type(rev) and type(temp[y+1][x]) == type(rev) and type(temp[y][x-1]) == type(rev) and type(temp[y][x+1]) == type(rev) and "-" not in (temp[y-1][x].type,temp[y+1][x].type) and "|" not in (temp[y][x-1].type,temp[y][x+1].type):
                                temp[y][x].N = temp[y-1][x]
                                temp[y][x].S = temp[y+1][x]
                                temp[y][x].W = temp[y][x-1]
                                temp[y][x].E = temp[y][x+1]
                    else:
                        print "a track points to a wrong point at:", x,y
        new_tracks = []
        for y in range(len(temp)):
            for x in range(len(temp[y])):
                if type(temp[y][x]) == type(rev):
                    new_tracks.append(temp[y][x])
                    # print "type:", temp[y][x].type, "N:", temp[y][x].N,"S:", temp[y][x].S,"E:", temp[y][x].E,"W:", temp[y][x].W
        return temp, new_tracks

    def cart_maker(self,raster):
        new_carts = dict()
        rev = rail_track()
        for y in range(len(raster)):
            for x in range(len(raster[y])):
                if raster[y][x] in ("v", ">", "<", "^"):
                    new_cart = cart()
                    new_cart.position = self.tracks[y][x].position
                    new_cart.track = self.tracks[y][x]
                    self.tracks[y][x].carts.append(new_cart)
                    if raster[y][x] == "v":
                        new_cart.direction = "v"
                    elif raster[y][x] == ">":
                        new_cart.direction = ">"
                    elif raster[y][x] == "^":
                        new_cart.direction = "^"
                    elif raster[y][x] == "<":
                        new_cart.direction = "<"
                    new_carts[new_cart.position] = new_cart
        return new_carts

    def __str__(self):
        raster = self.tracks
        string = "\n"
        for y in range(len(raster)):
            for x in range(len(raster[y])):
                string += str(raster[y][x])
            string += "\n"
        return string







#-------------------------------------------------
elves = True
q = plan(game)
i = 1
print "step:", i-1
# sim = v.simulation(q)
while True:
    q.update()
    if elves:
        q.remove_crashes()
        if len(q.carts) <= 1:
            temp = q.carts.keys()
            temp = (temp[0][1], temp[0][0])
            print temp, "testp:", i
            break
    if i%10000 == 0 and False:
        print len(q.carts)
        print "step:", i
    i += 1

temp = []
temp.append(str(q))

"""
print "TESTS"

test = plan(Input.game[5])
print test
for i in range(7):
    test.update()
    print "update"
    test.remove_crashes()
print test
test.update()
print "update"
test.remove_crashes()
print test
t = test.carts.keys()
print t, test
"""


# ans = 92,42
