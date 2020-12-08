pprintCounter = 0
test = True
numbers = [1,2,3,4,5,6,7,8,9]

def pprint(raster):
    print "\n----"
    global pprintCounter
    pprintCounter += 1
    print "print counter:", pprintCounter
    for i in range(len(raster)):
        print raster[i]
    print "---"

def display(raster):
    print "______________"
    temp = ["\n"]
    for y in range(len(raster)):
        for x in range(len(raster[y])):
            if len(raster[y][x]) == 1:
                temp.append(" ")
                temp.append(str(raster[y][x][0]))
                temp.append(" ")
            else:
                temp.append(" _ ")
            if (x+1)%3 == 0 and x != 0:
                temp.append("|")
        if (y+1)%3 == 0 and y != (0 or 8):
            temp.append("\n............................")
        temp.append("\n")
    temp = ''.join(temp)
    print temp
    print "______________"

def checkRow(raster, y):
    global test
    global numbers
    rowCount = dict()
    rowPossibilities = []
    for x in range(len(raster[y])):
        print raster[y][x]
        for each in raster[y][x]:
            rowPossibilities.append(each)
    if test:
        print "rowPossibilities:", rowPossibilities
    for i in numbers:
        if rowPossibilities.count(i) in rowCount:
            rowCount[rowPossibilities.count(i)].append(i)
        else:
            rowCount[rowPossibilities.count(i)] = [i]
    if test:
        print "rowCount:", rowCount


def clear(raster):
    print "test"
    for y in range(len(raster)):
        checkRow(raster, y)
        break
