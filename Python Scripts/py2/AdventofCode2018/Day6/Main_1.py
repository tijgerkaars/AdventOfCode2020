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

# marks = [[1, 1],[1, 6],[8, 3],[3, 4],[5, 5],[8, 9]]
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
while True:
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
            for each in map[y][x]:
                # resolve the square above
                if y-1 >= 0:
                    if each != 0 and newMap[y-1][x][0] == 0:
                        newMap[y-1][x] = [each]
                    if each != 0 and map[y-1][x][0] == 0 and newMap[y-1][x][0] != 0 and each not in newMap[y-1][x]:
                        newMap[y-1][x].append(each)
                # resolve the square below
                if y+1 < heigth:
                    if each != 0 and newMap[y+1][x][0] == 0:
                        newMap[y+1][x] = [each]
                    if each != 0 and map[y+1][x][0] == 0 and newMap[y+1][x][0] != 0 and each not in newMap[y+1][x]:
                        newMap[y+1][x].append(each)
                # resolve the sqaure to the left
                if x-1 >= 0:
                    if each != 0 and newMap[y][x-1][0] == 0:
                        newMap[y][x-1] = [each]
                    if each != 0 and map[y][x-1][0] == 0 and newMap[y][x-1][0] != 0 and each not in newMap[y][x-1]:
                        newMap[y][x-1].append(each)
                # resolve the sqaure to the rigth
                if x+1 < width:
                    if each != 0 and newMap[y][x+1][0] == 0:
                        newMap[y][x+1] = [each]
                    if each != 0 and map[y][x+1][0] == 0 and newMap[y][x+1][0] != 0 and each not in newMap[y][x+1]:
                        newMap[y][x+1].append(each)
    # print the thing nicely to see the changes made this pass
    """
    for i in range(len(map)):
        print map[i], "    ", newMap[i]
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
    """
    # save the changes for the next pass
    if newMap == map:
        break
    else:
        map = newMap
#----------------------------------------------------------------------------------------
# inspect the map to find the infinite fields

infinite = []
# for al the squares along the left and right
for y in range(heigth):
    if len(map[y][0]) == 1 and map[y][0][0] not in infinite:
        infinite.append(map[y][0][0])
    if len(map[y][width-1]) == 1 and map[y][width-1][0] not in infinite:
        infinite.append(map[y][width-1][0])
for x in range(width):
    if len(map[0][x]) == 1 and map[0][x][0] not in infinite:
        infinite.append(map[0][x][0])
    if len(map[heigth-1][x]) == 0 and map[heigth-1][x][0] not in infinite:
        infinite.append(map[heigth-1][x][0])
print infinite

#----------------------------------------------------------------------------------------
# inspect the map to find the size of the convined fields
sizes = dict()
for y in range(heigth):
    for x in range(width):
        if len(map[y][x]) == 1 and map[y][x][0] not in infinite:
            if map[y][x][0] not in sizes:
                sizes[map[y][x][0]] = 1
            else:
                sizes[map[y][x][0]] += 1
print sizes
#----------------------------------------------------------------------------------------
# check the found convined fields and find the largest
largest = -1

for each in sizes:
    if sizes[each] > largest:
        largest = sizes[each]
print largest


#----------------------------------------------------------------------------------------
# show the result


for i in range(len(map)):
    temp = ""
    for each in map[i]:
        if len(each) == 1:
            temp = temp + " " + str(each[0])
        else:
            temp = temp + " " + "."
    print temp
print "\n"
