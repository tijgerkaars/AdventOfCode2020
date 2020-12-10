import Game as g
import Setting as s
import MineVizualize as v
import random

s.init()


# ---------------------------------------------------------------
# create a game
game = g.grid(5,5,3)
game.print_style = 2
s.raster = game
print game


#---------------------------------------------------------------------
# if no logical next step can be made find a random number
def random_square():
    covered_square = []
    for y in range(len(game.storage)):
        for x in range(len(game.storage[y])):
            if game.storage[y][x].state == "covered":
                covered_square.append((y,x))
    square = random.choice(covered_square)
    return square

def solve(field):
    # make the field available to all files
    s.raster = field
    # make sure that the first square that is chosen is not a bomb
    while True:
        start_Y,start_X = random_square()
        print start_Y,start_X
        if s.raster.storage[start_Y][start_X].number >= 0:
            break
        else:
            print s.raster.storage[start_Y][start_X].number
    # create the game in Tkinter
    # at this point mostly to satisfy dependebilitties
    v.startGame(s.raster)
    # uncover the starting square
    v.uncover(None,start_Y,start_X)
    print s.raster
    print s.raster.storage
    for y in range(len(s.raster.storage)):
        for x in range(len(s.raster.storage[y])):
            if s.raster.storage[y][x].state == "open" and s.raster.storage[y][x].number != 0:
                print x,y, "number:", s.raster.storage[y][x].number
                cue = []
                for y1 in range(3):
                    cue.append([])
                    for x1 in range(3):
                        cue[y1].append([])

                cue[1][1] = s.raster.storage[y][x]
                if y-1 >= 0 and x-1 >= 0:
                    cue[0][0] = s.raster.storage[y-1][x-1]
                else:
                    cue[0][0] = "#"
                if y-1 >= 0:
                    cue[0][1] = s.raster.storage[y-1][x]
                else:
                    cue[0][1] = "#"
                if y-1 >= 0 and x+1 < len(s.raster.storage[y]):
                    cue[0][2] = s.raster.storage[y-1][x+1]
                else:
                    cue[0][2] = "#"
                if x-1 >= 0:
                    cue[1][0] = s.raster.storage[y][x-1]
                else:
                    cue[1][0] = "#"
                if x+1 < len(s.raster.storage[y]):
                    cue[1][2] = s.raster.storage[y][x+1]
                else:
                    cue[1][2] = "#"
                if x-1 >= 0 and y+1 < len(s.raster.storage):
                    cue[2][0] = s.raster.storage[y+1][x-1]
                else:
                    cue[2][0] = "#"
                if y+1 < len(s.raster.storage):
                    cue[2][1] = s.raster.storage[y+1][x]
                else:
                    cue[2][1] = "#"
                if y+1 < len(s.raster.storage) and x+1 < len(s.raster.storage[y]):
                    cue[2][2]= s.raster.storage[y+1][x+1]
                else:
                    cue[2][2] = "#"

                for y in range(len(cue)):
                    for x in range(len(cue[y])):
                        if type(cue[y][x]) != type(""):
                            if cue[y][x].state == "open":
                                cue[y][x] = cue[y][x].number
                            else:
                                cue[y][x] = "@"

                for each in cue:
                    print each
                break
            print "\n"

solve(game)

g.play()



#________________________________________________________________________________________________
#----------------------------------------------------------------------------------------------------

#    #   1   #   #   #      1/5  1  1/5  #   #
#    #   #   #   #   #      1/5 1/5 1/5  #   #
#    #   #   #   #   #       #   #   #   #   #
#    #   #   #   #   #       #   #   #   #   #
#    #   #   #   #   #       #   #   #   #   #


#    1/2  2   2   1  #       #   #   2   #   #
#    1/2 1/1 1/2 1/2 #       #   #   2   #   #
#     #   #   #   #  #       #   #   #   #   #
#     #   #   #   #  #       #   #   #   #   #
#     #   #   #   #  #       #   #   #   #   #
