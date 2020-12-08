import Queue
import cProfile
import re
import games
import vizualize
import time
from Tkinter import *

markers = False

# moves one item in a list to a higher index, here the blocks through rows or columns
def move(parts, pos):
    temp = parts[:]
    store = temp[pos]
    temp[pos] = 0
    temp[pos+1] = store
    return temp

# moves all possible blocks right/down in the row/column
def children(parts):
    if markers == True:
        print "children start:"
    count = 0
    aList = []
    for j in range(len(parts)):
        if j+1 < len(parts) and j+2 < len(parts) and parts[j] > 0:
            if parts[j+1] == 0 and parts[j+2] == 0:
                if move(parts,j) not in aList:
                    aList.append(move(parts,j))
                    count += 1
        elif j+1 < len(parts) and j+2 == len(parts) and parts[j] > 0:
            if parts[j+1] == 0:
                if move(parts,j) not in aList:
                    aList.append(move(parts,j))
                    count += 1
    if markers == True:
        if count > 1:
            print count, "Children made.\n"
        if count == 1:
            print count, "Child made.\n"
        if count == 0:
            print "No children made"
    return aList

# nice way to print the picture
def pp(pic):
    for i in range(len(pic)):
        print pic[i]
    print "\n"
# inserts "empty blocks" into the list equal to the space left by the given blocks
def prep(parts, size):
    emptys = size
    lengte = len(parts)
    for j in range(lengte):
        emptys -= parts[j]
    temp = 0
    for j in range(lengte):
        k = ((lengte-1) - j)
        if k != 0:
            temp += 1
            parts.insert(k,0)
    emptys -= temp
    for j in range(emptys):
        parts.append(0)
    return parts

# finds all the combinations of a row/column
def permutate(raw):
    # list to store the combinations
    perms = []
    # archive to prevent doubles
    archive = set()
    archive.add(str(raw))
    queue = Queue.Queue()
    queue.put(raw)
    perms.append(raw)
    counter = 0
    while not queue.empty():
        counter += 1
        if markers == True:
            print "counter:", counter
        # haal een combinatie uit de que en maak daar alle volgende combinaties van
        for each in children(queue.get()):
            # als de nieuwe combinatie nog niet eerder gevonden was,...
            if not str(each) in archive:
                #...zet hem in het archief
                archive.add(str(each))
                #...zet hem in de lijst van combinaties
                perms.append(each)
                #... zet hem in de queue om te kijken deze verder ontwikkeld kan worden
                queue.put(each)
                if len(perms) % 5000 == 0:
                    print "len(perms):", len(perms), "queue.qsize():", queue.qsize(), "counter:", counter
        if markers == True:
            print "\n"
    # change all the blocks into several blocks of length 1
    for i in perms:
        lengte = len(i)
        for j in range(lengte):
            k = lengte - 1 - j
            if i[k] > 1:
                temp = i[k]
                i[k] = 1
                for l in range(temp-1):
                    i.insert(k,1)
    return perms

# fills all the pixels in the picture that are certain
def fill(picture,board,ori):
    width = len(board[0])
    height= len(board[1])
    # fill all the certain pixels in the rows
    if ori == "row":
        # cycle through the rows
        for i in range(height):
            # cycle over a row
            for j in range(width):
                # check if the pixel is the same in all combinations
                certain = 0
                for each in board[1][i]:
                    # if the pixel is empty in this combination, prepare a negative
                    if each[j] == 0 and certain == 0:
                        certain = -1
                    # if the pixel should be full according to this combination, prepare a positive
                    elif each[j] == 1 and certain == 0:
                        certain = 1
                    # if the combinations don't match, stop checking the combinations for that pixel
                    elif (each[j] == 0 and certain != -1) or (each[j] == 1 and certain != 1):
                        certain = "uncertain"
                        break
                # if all combinations agree on a positive/negative, put a positive/negative
                if certain == 1 or certain == -1:
                    picture[i][j] = certain
    elif ori == "column":
        # cycle through the columns
        for i in range(width):
            # cycle over a column
            for j in range(height):
                # check if the pixel is the same in all combinations
                certain = 0
                for each in board[0][i]:
                    # if the pixel is empty in this combination, prepare a negative
                    if each[j] == 0 and certain == 0:
                        certain = -1
                    # if the pixel should be full according to this combination, prepare a positive
                    elif each[j] == 1 and certain == 0:
                        certain = 1
                    # if the combinations don't match, stop checking the combinations for that pixel
                    elif (each[j] == 0 and certain != -1) or (each[j] == 1 and certain != 1):
                        certain = "uncertain"
                        break
                # if all combinations agree on a positive/negative, put a positive/negative
                if certain == 1 or certain == -1:
                    picture[j][i] = certain
                    #1,1,1,1,0,1,0,1,0,0
    return pic

# check if the combinations are still valid
def check(picture,board,ori):
    width = len(board[0])
    height= len(board[1])
    if ori == "row":
        # cycle through the rows
        for i in range(height):
            # if ther is only 1 combination skip the rest of the loop
            if len(board[1][i]) == 1:
                continue
            # check each pixel in a row
            for j in range(width):
                # make a list to store the index of (in)valid combinations
                aList = []
                # cycle through the combinations for rows
                for each in board[1][i]:
                    # if all other combinations where invalid break the loop
                    count = len(board[1][i])
                    if count == 1:
                        break
                    # if the picture has a certain empty pixel and the combination suggest a coloured pixel,...
                    if picture[i][j] == -1 and each[j] == 1:
                        #... mark the combination as wrong in the index list
                        aList.insert(count,False)
                    # if the picture has a certain full pixel and the combination suggest an empty pixel,...
                    elif picture[i][j] == 1 and each[j] != 1:
                        #... mark the combination as wrong in the index list
                        aList.insert(count,False)
                    # if the combination doesn't contradict the pixel mark it as oke
                    else:
                        aList.insert(count,True)
                    count -= 1
                # if no valid combinations remain
                if not aList:
                    break
                # remove all the invalid combinations
                lengte = len(aList)
                for k in range(lengte):
                    l = lengte - 1 - k
                    if not aList[l]:
                        board[1][i].pop(l)
    if ori == "column":
        # cycle through the columns
        for i in range(width):
            # creat a list for the (in)valid combinations
            bList = []
            # cycle through the combinations for columns
            for each in board[0][i]:
                # creat a list to place the column in
                column = []
                # creat a list of (in)valid pixels
                aList = []
                # place the column in the list
                for j in range(height):
                    column.insert(j,picture[j][i])
                count = 0
                # cycle over the column
                for j in range(height):
                    # if the combination doesnt match the pixel
                    if column[j] == 1 and each[j] != 1:
                        aList.insert(count, False)
                        break
                    elif column[j] == -1 and each[j] == 1:
                        aList.insert(count,False)
                        break
                    # if combination is compatible with all the certain pixels
                    else:
                        aList.insert(count,True)
                    count += 1
                # if one of the certain pixels didn't match a combination,...
                if False in aList:
                    #... place the combination in bList
                    bList.append(each)
            # remove all the invalid combinations
            for k in bList:
                board[0][i].pop(board[0][i].index(k))
    # return the remaining combinations
    return board

#############################
#############################
# choose the game to solve
game = games.game12
index = games.game12[:]
for i in range(len(game)):
    index[i]=game[i][:]
    for j in range(len(game[i])):
        index[i][j] = game[i][j][:]
# the items in game[0] match the number of columns, game[1] matches the rows
width = len(game[0])
height= len(game[1])

# construct an empty canvas
pic = []
count = 0
for i in range(height):
    pic.append([])
    for j in range(width):
        pic[i].append(count)

print "width:", width, "height", height
print game
#############################
#############################

TopBlocks = 0
SideBlocks = 0

for i in game[0]:
    if len(i) > TopBlocks:
        TopBlocks = len(i)
for i in game[1]:
    if len(i) > SideBlocks:
        SideBlocks = len(i)

print TopBlocks, SideBlocks

print "permutations"
# find the combinations for the rows and replace the input with them
for i in range(len(game[0])):
    print "permutate top:", i+1
    game[0][i] = permutate(prep(game[0][i],height))
# find the combinations for the columns and replace the input with them
for i in range(len(game[1])):
    print "permutate sides:", i+1
    game[1][i] = permutate(prep(game[1][i],width))
print "permutations done"

# creat a list to store each layer
layers = []
print "pic:", pic
# add a list to store the first layer in
layers.append([])
for j in range(len(pic)):
    layers[0].insert(j,pic[j][:])
# creat 100 layers, if necesairy
for i in range(100):
    # creat a list to store this cycles first layer
    temp = []
    # place this cycles first layer in the list
    for j in pic:
        temp.append(j[:])
    print "draw:", i
    # fill all the certain pixels
    pic = fill(pic,game,"row")
    print i*2+1, pic
    # store this newly created layer <<<
    # i*2 as 2 layers are made per cycle, and + 1 because the empty layer is on index 0
    layers.insert((i*2+1), [])
    for j in range(len(pic)):
        layers[i*2+1].insert(j,pic[j][:])
    #>>>
    # use the new certain pixels to eliminate combinations for the columns
    game = check(pic,game,"column")
    print i*2+1, pic
    # check the remaining combinations to find new certain pixels
    pic = fill(pic,game,"column")
    # store this newly created layer <<<
    layers.insert((i*2+2), [])
    for j in range(len(pic)):
        layers[i*2+2].insert(j,pic[j][:])
    #>>>
    # use the new certain pixels to eliminate combinations for the rows
    game = check(pic,game,"row")
    # if no changes were made this cyle perform no more cycles
    if temp == pic:
        print "done"
        break

for i in range(len(layers)):
    print layers[i]
# remove any accidental double layers <<<
lengte = len(layers)
for i in range(lengte):
    j = lengte - i - 1
    if j != 0 and layers[j] == layers[j-1]:
        layers.pop(j)
#>>>
print "\n"

# cycle through the draw stages/layers
for i in range(len(layers)):
    # cycle through the rows of a stage
    for j in range(len(layers[i])):
        # if this row differs from the previous
        if layers[i][j] != layers[i-1][j]:
            # cycle through each pixel in this row
            for k in range(len(layers[i][j])):
                # if the pixel was empty on the previous layer but has been solved now,...
                if layers[i-1][j][k] == 0 and layers[i-1][j][k] != layers[i][j][k]:
                    #... if that pixel is now filled:---
                    if layers[i][j][k] > 0:
                        #--- mark that pixel with the layer it was filled in
                        layers[i][j][k] = i
                    #... if that pixel is now certainly empty:---
                    elif layers[i][j][k] < 0:
                        #--- mark that pixel with the layer it was filled in
                        layers[i][j][k] = -i
                # ensure the previous markings get carried over <<<
                # if the pixel was not empty on the previous layer,...
                elif layers[i-1][j][k] != 0 and layers[i-1][j][k] != layers[i][j][k]:
                    #... and filled in,---
                    if layers[i][j][k] > 0:
                        #--- mark it as the last layer
                        layers[i][j][k] = i - 1
                    #... and is now certainly empty,---
                    elif layers[i][j][k] < 0:
                        #--- mark it as the last layer
                        layers[i][j][k] = -(i-1)
                #>>>
print "\n\n\ntest:"

### JUMP ###

resize = 15
if width + SideBlocks < 30 and height + TopBlocks < 30:
    resize = 25
border = round(resize/20)
if border < 3:
    border = 3
SquaresVertical = (width + SideBlocks) * resize
SquaresHorizontal = (height + TopBlocks) * resize
SideBlocks = SideBlocks * resize
TopBlocks = TopBlocks * resize
print SideBlocks, TopBlocks
print SquaresVertical/resize, SquaresHorizontal/resize

master = Tk()
render = Canvas(master, height = SquaresHorizontal, width = SquaresVertical)

x1, y1, x2, y2 = 0, 0, SideBlocks, TopBlocks
# draw spaces for top markers
for i in range(width):
    for j in range(TopBlocks/resize):
        render.create_rectangle(SideBlocks+i*resize, y1+j*resize, SideBlocks+(i+1)*resize, y1+(j+1)*resize)
# draw spaces for side markers
for j in range(SideBlocks/resize):
    for i in range(height):
        render.create_rectangle((x1+(j*resize)), y2+i*resize, (x1+(j+1)*resize), (y2+1)*resize)
# draw the drawing spaces
for i in range(width):
    for j in range(height):
        render.create_rectangle(SideBlocks + i*resize, TopBlocks + j*resize, SideBlocks + (i+1)*resize, TopBlocks + (j+1)*resize)
# draw horizontal segmentation lines
for i in range(height):
    if (i)%5 == 0:
        render.create_line(0, TopBlocks+(i)*resize, SquaresVertical, TopBlocks+(i)*resize, width = 3)
# draw vertical segmentation lines
for i in range(width):
    if (i)%5 == 0:
        render.create_line(SideBlocks+(i)*resize, 0, SideBlocks+(i)*resize, SquaresHorizontal, width = 3)
# draw boudary
render.create_rectangle(3, 3, SquaresVertical, SquaresHorizontal, width = 3)

# place the marks at the top
for i in range(len(index[0])):
    for j in range(len(index[0][i])):
        k = (len(index[0][i])-j)-1
        render.create_text(SideBlocks + (i+0.5)*resize, TopBlocks-(j+0.5)*resize, text = index[0][i][k])

for i in range(len(index[1])):
    for j in range(len(index[1][i])):
        k = (len(index[1][i])-j)-1
        render.create_text(SideBlocks-(0.5+j)*resize, TopBlocks+(i+0.5)*resize, text = index[1][i][k])

render.pack()
master.update()

#layers
for i in range(len(layers)):
    # i is the layer
    for j in range(len(layers[i])):
        # j is the row
        for k in range(len(layers[i][j])):
            # k is the pixel
            if layers[i][j][k] == i and i != 0:
                render.create_rectangle((x2+(k*resize)+border),(y2+(j*resize)+border),(x2+((k+1)*resize)-border),(y2+((j+1)*resize)-border), fill = "black")
                render.pack()
                master.update()
    time.sleep(1)

time.sleep(50)
print "test end"


# game is horizontal and vertical permutated
# print game
# game[x]: x=0 -> vertical, x=1 -> horizontal
# print game[0]
# game[x][y]: x=0,y(0->width) zijn de kolomen, x=1,y(0->height) zijn de rijen
# print game[0][0]
# game[x][y][z]: z zijn de permutaties
# print game[0][0][0]
