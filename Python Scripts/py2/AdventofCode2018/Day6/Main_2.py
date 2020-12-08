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

#----------------------------------------------------------------------------------------
# test case


# marks = [[1, 1],[1, 6],[8, 3],[3, 4],[5, 5],[8, 9]]


#----------------------------------------------------------------------------------------
# get dimensions of input
heigth = 0
width = 0

for i in range(len(marks)):
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
        map[y].append(".")
        newMap[y].append(".")
#----------------------------------------------------------------------------------------
# get all the distances
for y in range(heigth):
    for x in range(width):
        distances = []
        for each in marks:
            distance = abs(y-each[1]) + abs(x-each[0])
            distances.append(distance)
        total = sum(distances)
        if total < 10000:
            map[y][x] = "#"
#----------------------------------------------------------------------------------------
# find the amount of spaces that are within range
inRange = 0

for y in range(heigth):
    for x in range(width):
        if map[y][x] == "#":
            inRange += 1

print inRange

# result = 39398
