
import Queue
import cProfile
import re
import games
import functions as func

print dir(func)

# d, kolom/rij 1 of 2
# start, [x,y]
# lengte van het veld

testv1 = [[5],[1,1],[1,1],[1,1],[5]]
testh1 = [[5],[1,1],[1,1],[1,1],[5]]

testv2 = [[5],[0],[0],[0],[0]]
testh2 = [[1],[1],[1],[1],[1]]

testv3 = [[1],[1],[0],[1],[1],[0],[1],[1]]
testh3 = [[2,2,2],[0],[0],[0],[0]]

testv4 = [[1],[1],[1],[1],[1]]
testh4 = [[5],[0],[0],[0],[0]]

testv5 = [[6],[0],[0],[0],[0]]
testh5 = [[0],[0],[1],[1],[1],[1],[1],[1],[0],[0]]

testv6 = [[2,2,2],[0],[0],[0],[0]]
testh6 = [[1],[1],[0],[1],[1],[0],[1],[1]]

test = 0

sides = games.game4[1]
top = games.game4[0]

if test == 1:
    sides = testv1
    top = testh1
elif test == 2:
    sides = testv2
    top = testh2
elif test == 3:
    sides = testv3
    top = testh3
elif test == 4:
    sides = testv4
    top = testh4
elif test == 5:
    sides = testv5
    top = testh5
elif test == 6:
    sides = testv6
    top = testh6


width = len(top)
print "sides", sides
height = len(sides)
print "top", top
print "width", width, "height",height

picture = []
for x in range(len(sides)):
    picture.append([x])
    picture[x] = []
    for y in range(len(top)):
        picture[x].append(0)


### picture[y][x]
# picture = -1, definitly not coloured
# picture = 1, coloured field toply
# picture = 2, coloured field sidesly
# print the field: printb(picture)

print "\nTest output\n"
# fill(board, o, positions, x=0, y=0, filler = 1)

def frag(board, o, slot, fragment, totalfraglen, summed, filler = 1, x=0, y=0):
    print "\nfrag"
    if o == "row":
        print slot, fragment, totalfraglen, summed
        # vult alle rijen die compleet gedifineerd zijn
        if totalfraglen == summed:
            for i in range(len(slot)):
                func.fill(board, o, slot[i], x, y, 3)
        elif totalfraglen > 0.5*summed:
            ###### KIJK OF DE FRAGMENTEN MET DE SLOTS MATCHEN
            print summed*0.5
            print round(0.5*summed-0.5)
            for i in slot:
                print i
            kk= 0
    return board

print "\nEnd test\n"

###-------
# fill in all full and empty rows
picture = func.x(top, sides, picture)
# cycle through the rows
print "\nRows"
for i in range(height):
    slots = []
    for j in range(width):
        if func.space(picture,"row",j,i) not in slots:
            slots.append(func.space(picture,"row",j,i))
    # print "row:", i, "slots:", slots, "fragments:", sides[i]
    # print len(slots), len(sides[i])
    summed = 0
    totalfraglen = 0
    for k in slots:
        if k != "empty":
            summed += (k[0]-k[1])+ 1
            if k[0] != len(picture[0])-1:
                summed += 1
        else:
            break

    for h in sides[i]:
        totalfraglen += h + 1
    totalfraglen -= 1
    if totalfraglen > 0.5*summed:
        frag(picture,"row", slots, sides[i], totalfraglen, summed)
    print "\n"


print "\nColumns"
# cycle through the columns
for i in range(width):
    slots = []
    for j in range(height):
        if func.space(picture,"column",i,j) not in slots:
            slots.append(func.space(picture,"column",i,j))
###-------

func.printb(picture)
