with open("C:\Users\Jobber\Documents\Python Scripts\AdventofCode2018\Day6\input.txt") as file:
    lines = []
    for line in file:
        # The rstrip method gets rid of the "\n" at the end of each line
        lines.append(line.rstrip().split("."))
    marks = []
    for coord in lines:
        print coord
        for each in coord:
            x,y = each.split(", ")
            x = int(x)
            y = int(y)
            marks.append([x,y])
print marks

marks = [
[1, 1],
[1, 6],
[8, 3],
[3, 4],
[5, 5],
[8, 9]
]
#----------------------------------------------------------------------------------------
# get dimensions of input
heigth = 0
width = 0

for i in range(len(marks)):
    print marks[i]
    if marks[i][0] > width:
        width = marks[i][0] + 1
    if marks[i][1] > heigth:
        heigth = marks[i][1] + 1

print "heigth:", heigth, "width:", width
#----------------------------------------------------------------------------------------
# creat a map for the coordinates
# and a newMap to see if coords are eqidistant
map = []
newMap = []
for y in range(heigth):
    map.append([])
    newMap.append([])
    for x in range(width):
        map[y].append([0])
        newMap[y].append([0])
#----------------------------------------------------------------------------------------
# adding the coordinates on the map
for i in range(len(marks)):
    map   [marks[i][1]] [marks[i][0]] = [i+1]
    newMap[marks[i][1]] [marks[i][0]] = [i+1]

#----------------------------------------------------------------------------------------
# mark all coords closesed to the coordinates
for i in range(5):
    newMap = []
    for y in range(heigth):
        newMap.append([])
        for x in range(width):
            newMap[y].append([])
            for each in map[y][x]:
                newMap[y][x].append(each)
    # create a list to store the updates in while keeping the og as reference

    for y in range(heigth):
        for x in range(width):
            # resolve the square above
            if y-1 >= 0:
                if map[y][x][0] != 0 and newMap[y-1][x][0] == 0:
                    newMap[y-1][x] = [map[y][x][0]]
                if map[y][x][0] != 0 and map[y-1][x][0] == 0 and newMap[y-1][x][0] != 0 and map[y][x][0] not in newMap[y-1][x]:
                    for each in map[y][x]:
                        newMap[y-1][x].append(each)
            # resolve the square below
            if y+1 < heigth:
                if map[y][x][0] != 0 and newMap[y+1][x][0] == 0:
                    newMap[y+1][x] = [map[y][x][0]]
                if map[y][x][0] != 0 and map[y+1][x][0] == 0 and newMap[y+1][x][0] != 0 and map[y][x][0] not in newMap[y+1][x]:
                    for each in map[y][x]:
                        newMap[y+1][x].append(each)
            # resolve the sqaure to the left
            if x-1 >= 0:
                if map[y][x][0] != 0 and newMap[y][x-1][0] == 0:
                    newMap[y][x-1][0] = map[y][x][0]
                if map[y][x][0] != 0 and map[y][x-1][0] == 0 and newMap[y][x-1][0] != 0 and map[y][x][0] not in newMap[y][x-1]:
                    for each in map[y][x]:
                        newMap[y][x-1].append(each)
            # resolve the sqaure to the rigth
            if x+1 < width:
                if map[y][x][0] != 0 and newMap[y][x+1][0] == 0:
                    newMap[y][x+1][0] = map[y][x][0]
                if map[y][x][0] != 0 and map[y][x+1][0] == 0 and newMap[y][x+1][0] != 0 and map[y][x][0] not in newMap[y][x+1]:
                    for each in map[y][x]:
                        newMap[y][x+1].append(each)

    for i in range(len(map)):
        """
        print map[i], "    ", newMap[i]
        """
        temp = ""
        for each in map[i]:
            if len(each) == 1:
                temp = temp + " " + str(each[0])
            else:
                temp = temp + " " + "."
        temp = temp + "       "
        for each in newMap[i]:
            if len(each) == 1:
                temp = temp + " " + str(each[0])
            else:
                temp = temp + " " + "."
        print temp
    print "\n"

    map = newMap
