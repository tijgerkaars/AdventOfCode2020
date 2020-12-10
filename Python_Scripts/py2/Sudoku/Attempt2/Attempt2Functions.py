import Vizualize as v
import Settings


counter = 0
numbers = [1,2,3,4,5,6,7,8,9]

def pprint(raster, orientation = "row"):
    print "\n----"
    global counter
    counter += 1
    temp = []
    print "print counter:", counter
    if orientation == "row":
        print "rows"
        for i in range(len(raster)):
            temp.append(raster[i])
    if orientation == "column":
        print "columns"
        for x in range(len(raster[0])):
            temp.append([])
            for y in range(len(raster)):
                temp[x].append(raster[y][x])
    if orientation == "block":
        print "blocks"
        for y in range(len(raster)/3):
            for x in range(len(raster[y])/3):
                temp.append([])
                for yi in range(3):
                    for xi in range(3):
                        temp[y*3+x].append(raster[y*3+yi][x*3+xi])
    for i in range(len(temp)):
        print temp[i]
    print "---"

def display(raster, extra = False):
    print "______________"
    temp = ["\n"]
    occurrenses = dict()
    for y in range(len(raster)):
        for x in range(len(raster[y])):
            if len(raster[y][x]) == 1:
                temp.append(" ")
                temp.append(str(raster[y][x][0]))
                temp.append(" ")
                if raster[y][x][0] in occurrenses:
                    occurrenses[raster[y][x][0]] += 1
                else:
                    occurrenses[raster[y][x][0]] = 1
            else:
                temp.append(" _ ")
            if (x+1)%3 == 0 and x != 0:
                temp.append("|")
        if (y+1)%3 == 0 and y != (0 or 8):
            temp.append("\n............................")
        temp.append("\n")
    temp = ''.join(temp)
    print temp
    if extra:
        for each in occurrenses:
            print each, ":", occurrenses[each]
    print "______________"

# Check if the game is copmleted correctly
def done(raster):
    # check the rows
    for y in range(len(raster)):
        row = []
        # for each square in the row
        for x in range(len(raster[0])):
            # for each possibility in that square
            for each in raster[y][x]:
                row.append(each)
        # for each number 1,2,3,4,5,6,7,8,9
        for i in range(1,10):
            # if it apears more than once
            if row.count(i) != 1:
                # tell the bruteforce the game is not complete yet
                return False
    # for each column in the raster
    for x in range(len(raster[0])):
        # store the possibility's here
        column = []
        # for each square in the column
        for y in range(len(raster)):
            # for each possibility in that sqaure
            for each in raster[y][x]:
                column.append(each)
        # if a number occurs more than once tell the bruteforce to keep going
        for i in range(1,10):
            if column.count(i) != 1:
                return False
    # denotes the dimensions of the sqaure block
    blocksize = 3
    # for each row of blocks
    for y in range(len(raster)/blocksize):
        # for each block in that row
        for x in range(len(raster[y])/blocksize):
            # store the block info here
            block = []
            # for each row inside the block
            for y2 in range(blocksize):
                # for each sqaure inside that row of 3
                for x2 in range(blocksize):
                    # for each possibility in that sqaure
                    for each in raster[y*blocksize + y2][x*blocksize + x2]:
                        block.append(each)
            # if a number occures more than once, tell the bruteforce to keep going
            for i in range(1,10):
                if block.count(i) != 1:
                    return False
    # if a number occures only once in each row, column, and block, tell the bruteforce that the game is complete
    return True

# check if the current game is still valid
def valid(raster, debug = False):
    for y in range(len(raster)):
        row = []
        possibilities = []
        for x in range(len(raster[y])):
            if len(raster[y][x]) == 1:
                row.append(raster[y][x][0])
            for each in raster[y][x]:
                possibilities.append(each)
        for i in range(1,10):
            if row.count(i) > 1:
                if debug:
                    print "(row) double numbers", i
                    print "row:", row
                return False
            elif possibilities.count(i) == 0:
                if debug:
                    print "Missing number:", i
                return False
    for x in range(len(raster[0])):
        column = []
        possibilities = []
        for y in range(len(raster)):
            if len(raster[y][x]) == 1:
                column.append(raster[y][x][0])
            for each in raster[y][x]:
                possibilities.append(each)
        for i in range(1,10):
            if column.count(i) > 1:
                if debug:
                    print "double numbers (column)", i
                return False
            elif possibilities.count(i) == 0:
                if debug:
                    print "Missing number:", i
                return False
    # denotes the dimensions of the sqaure block
    blocksize = 3
    for y in range(len(raster)/blocksize):
        # for each block in that row
        for x in range(len(raster[y])/blocksize):
            # store the block info here
            block = []
            possibilities = []
            # for each row inside the block
            for y2 in range(blocksize):
                # for each sqaure inside that row of 3
                for x2 in range(blocksize):
                    if len(raster[y*blocksize + y2][x*blocksize + x2]) == 1:
                        block.append(raster[y*blocksize + y2][x*blocksize + x2])
                    for each in raster[y*blocksize + y2][x*blocksize + x2]:
                        possibilities.append(each)
        for i in range(1,10):
            if column.count(i) > 1:
                if debug:
                    print "double numbers (block)", i
                return False
            elif possibilities.count(i) == 0:
                if debug:
                    print "Missing number:", i
                return False
    return True

def score(raster):
    NumberCountAll = 0
    NumberCountSmallestRow = 0
    NumberCountSmallestColumn = 0
    NumberCountSmallestBlock = 0
    for y in range(len(raster)):
        for x in range(len(raster[0])):
            NumberCountAll += len(raster[y][x])
    # rows
    NumberCountSmallestRow = NumberCountAll
    for y in range(len(raster)):
        RowNumberCounter = 0
        for x in range(len(raster[y])):
            RowNumberCounter += len(raster[y][x])
        if NumberCountSmallestRow > RowNumberCounter:
            NumberCountSmallestRow = RowNumberCounter
    # columns
    NumberCountSmallestColumn = NumberCountAll
    for x in range(len(raster[0])):
        ColumnNumberCounter = 0
        for y in range(len(raster)):
            ColumnNumberCounter += len(raster[y][x])
        if NumberCountSmallestColumn > ColumnNumberCounter:
            NumberCountSmallestColumn = ColumnNumberCounter
    # blocks
    NumberCountSmallestBlock = NumberCountAll
    for y1 in range(3):
        for x1 in range(3):
            BlockNumberCounter = 0
            for y2 in range(len(raster)/3):
                for x2 in range(len(raster[y])/3):
                    BlockNumberCounter += len(raster[y1*3 + y2][x1*3 + x2])
            if NumberCountSmallestBlock > BlockNumberCounter:
                NumberCountSmallestBlock = BlockNumberCounter
    score = NumberCountAll - (NumberCountSmallestRow + NumberCountSmallestBlock + NumberCountSmallestColumn)
    score = NumberCountSmallestRow + NumberCountSmallestBlock + NumberCountSmallestColumn
    if score < 0:
        score = 0
    return score

def score2(raster):
    score = 0
    for y in range(len(raster)):
        for x in range(len(raster[y])):
            for each in raster[y][x]:
                score += 1
    return score

def CompleteByRemoval(raster, mark = True):
    loop = 0
    start = "start"
    end = "end"
    while start != end:
    # for test in range(marker):
        # Check rows
        start = str(raster)
        # for each row
        removed = 0
        for y in range(len(raster)):
            # Check and track each square for defined numbers
            DefinedNumbers = []
            # For each square
            for x in range(len(raster[0])):
                if len(raster[y][x]) == 1:
                    DefinedNumbers.append(raster[y][x][0])
            for x in range(len(raster[0])):
                temp = DefinedNumbers[:]
                placeHolder = raster[y][x][:]
                for each in temp:
                    if each in placeHolder and len(placeHolder) != 1:
                        placeHolder.remove(each)
                        removed += 1
                raster[y][x] = placeHolder
                if mark and Settings.path[-1] != str(raster):
                    Settings.path.append(str(raster))

        removed = 0
        for x in range(len(raster[0])):
            DefinedNumbers = []
            for y in range(len(raster)):
                if len(raster[y][x]) == 1:
                    DefinedNumbers.append(raster[y][x][0])
            for y in range(len(raster)):
                temp = DefinedNumbers[:]
                placeHolder = raster[y][x][:]
                for each in temp:
                    if each in placeHolder and len(placeHolder) != 1:
                        placeHolder.remove(each)
                        removed += 1
                raster[y][x] = placeHolder[:]
                if mark and Settings.path[-1] != str(raster):
                    Settings.path.append(str(raster))

        removed = 0
        for y in range(len(raster)/3):
            for x in range(len(raster[0])/3):
                DefinedNumbers = []
                for yi in range(3):
                    for xi in range(3):
                        if len(raster[y*3 + yi][x*3 + xi]) == 1:
                            DefinedNumbers.append(raster[y*3 + yi][x*3 + xi][0])
                for yi in range(3):
                    for xi in range(3):
                        temp = DefinedNumbers[:]
                        placeHolder = raster[y*3 + yi][x*3 + xi][:]
                        for each in temp:
                            if each in placeHolder and len(placeHolder) != 1:
                                placeHolder.remove(each)
                                removed += 1
                        if mark and Settings.path[-1] != str(raster):
                            Settings.path.append(str(raster))
                        raster[y*3 + yi][x*3 + xi] = placeHolder[:]
        end = str(raster)
        loop += 1
        # print "loop:", loop

def CompleteByRemainders(raster, mark = True):
    # rows
    if True:
        for y in range(len(raster)):
            CompleteByRemoval(raster)
            PossibleNumbers = []
            for x in range(len(raster[y])):
                for each in raster[y][x]:
                    PossibleNumbers.append(each)
            numberCount = dict()
            for i in range(1,10):
                if PossibleNumbers.count(i) in numberCount:
                    numberCount[PossibleNumbers.count(i)].append(i)
                else:
                    numberCount[PossibleNumbers.count(i)] = [i]
            for i in numberCount:
                if i == 1:
                    for x in range(len(raster)):
                        if any(elem in raster[y][x]  for elem in numberCount[i]) and len(raster[y][x]) != 1:
                            placeHolder = raster[y][x][:]
                            for each in placeHolder:
                                if each not in numberCount[i]:
                                    placeHolder.remove(each)
                            if mark and Settings.path[-1] != str(raster):
                                Settings.path.append(str(raster))
                            raster[y][x] = placeHolder[:]
                if i > 1:
                    matches = 0
                    for x in range(len(raster)):
                        if any(elem in raster[y][x] for elem in numberCount[i]):
                            matches += 1
                    if matches == len(numberCount[i]) and len(numberCount[i]) == i:
                        for x in range(len(raster)):
                            if all(elem in raster[y][x]  for elem in numberCount[i]):
                                placeHolder = raster[y][x][:]
                                for each in placeHolder:
                                    if each not in numberCount[i]:
                                        placeHolder.remove(each)
                                if mark and Settings.path[-1] != str(raster):
                                    Settings.path.append(str(raster))
                                raster[y][x] = placeHolder[:]
    # Column
    if True:
        for x in range(len(raster[0])):
            CompleteByRemoval(raster)
            column = []
            PossibleNumbers = []
            for y in range(len(raster)):
                column.append( raster[y][x])
                for each in raster[y][x]:
                    PossibleNumbers.append(each)
            numberCount = dict()
            for i in range(1,10):
                if PossibleNumbers.count(i) in numberCount:
                    numberCount[PossibleNumbers.count(i)].append(i)
                else:
                    numberCount[PossibleNumbers.count(i)] = [i]
            for i in numberCount:
                if i == 1:
                    for y in range(len(raster)):
                        if any(elem in raster[y][x]  for elem in numberCount[i]) and len(raster[y][x]) != 1:
                            placeHolder = raster[y][x][:]
                            for each in placeHolder:
                                if each not in numberCount[i]:
                                    placeHolder.remove(each)
                            if mark and Settings.path[-1] != str(raster):
                                Settings.path.append(str(raster))
                            raster[y][x][:] = placeHolder[:]
                if i > 1:
                    matches = 0
                    for y in range(len(raster)):
                        if any(elem in raster[y][x] for elem in numberCount[i]):
                            matches += 1
                    if matches == len(numberCount[i]) and len(numberCount[i]) == i:
                        for y in range(len(raster)):
                            if all(elem in raster[y][x]  for elem in numberCount[i]):
                                placeHolder = raster[y][x][:]
                                for each in placeHolder:
                                    if each not in numberCount[i]:
                                        placeHolder.remove(each)
                                if mark and Settings.path[-1] != str(raster):
                                    Settings.path.append(str(raster))
                                raster[y][x][:] = placeHolder[:]
    # Blocks
    if True:
        for y in range(len(raster)/3):
            for x in range(len(raster[y])/3):
                CompleteByRemoval(raster)
                PossibleNumbers = []
                for yi in range(3):
                    for xi in range(3):
                        for each in raster[y*3 + yi][x*3 + xi]:
                            PossibleNumbers.append(each)
                numberCount = dict()
                for i in range(1,10):
                    if PossibleNumbers.count(i) in numberCount:
                        numberCount[PossibleNumbers.count(i)].append(i)
                    else:
                        numberCount[PossibleNumbers.count(i)] = [i]
                for i in numberCount:
                    if i == 1:
                        for yi in range(3):
                            for xi in range(3):
                                if any(elem in raster[y*3 + yi][x*3 + xi]  for elem in numberCount[i]) and len(raster[y*3 + yi][x*3 + xi]) != 1:
                                    placeHolder = raster[y*3 + yi][x*3 + xi][:]
                                    for each in placeHolder:
                                        if each not in numberCount[i]:
                                            placeHolder.remove(each)
                                    if mark and Settings.path[-1] != str(raster):
                                        Settings.path.append(str(raster))
                                    raster[y*3 + yi][x*3 + xi] = placeHolder[:]
                    if i > 1:
                        matches = 0
                        for yi in range(3):
                            for xi in range(3):
                                if any(elem in raster[y*3 + yi][x*3 + xi] for elem in numberCount[i]):
                                    matches += 1
                        if matches == len(numberCount[i]) and len(numberCount[i]) == i:
                            for yi in range(3):
                                for xi in range(3):
                                    if all(elem in raster[y*3 + yi][x*3 + xi]  for elem in numberCount[i]):
                                        placeHolder = raster[y*3 + yi][x*3 + xi][:]
                                        for each in placeHolder:
                                            if each not in numberCount[i]:
                                                placeHolder.remove(each)
                                        if mark and Settings.path[-1] != str(raster):
                                            Settings.path.append(str(raster))
                                        raster[y*3 + yi][x*3 + xi] = placeHolder[:]

def CompleteBySets(raster, mark = True):
    # Rows
    if True:
        for y in range(len(raster)):
            row = []
            for x in range(len(raster[y])):
                row.append(raster[y][x][:])
            sets = dict()
            for each in row:
                if row.count(each) in sets and each not in sets[row.count(each)]:
                    sets[row.count(each)].append(each)
                else:
                    sets[row.count(each)] = [each]
            for i in sets:
                for each in sets[i]:
                    if len(each) == i and len(each) != 1:
                        for x in range(len(raster[y])):
                            if raster[y][x] != each and any(elem in raster[y][x]  for elem in each):
                                placeHolder = raster[y][x][:]
                                for number in raster[y][x]:
                                    if number in each:
                                        placeHolder.remove(number)
                                if mark and Settings.path[-1] != str(raster):
                                    Settings.path.append(str(raster))
                                raster[y][x] = placeHolder[:]

    # Column
    for x in range(len(raster[0])):
        column = []
        for y in range(len(raster)):
            column.append(raster[y][x][:])
        sets = dict()
        for each in column:
            if column.count(each) in sets and each not in sets[column.count(each)]:
                sets[column.count(each)].append(each)
            else:
                sets[column.count(each)] = [each]
        for i in sets:
            for each in sets[i]:
                if len(each) == i and len(each) != 1:
                    for y in range(len(raster)):
                        if raster[y][x] != each and any(elem in raster[y][x]  for elem in each):
                            placeHolder = raster[y][x][:]
                            for number in raster[y][x]:
                                if number in each:
                                    placeHolder.remove(number)
                            if mark and Settings.path[-1] != str(raster):
                                Settings.path.append(str(raster))
                            raster[y][x] = placeHolder[:]
    # Block

"""
 _  _  1 | 7  _  8 | _  2  _ |  X needs to be an 1 because the * are
 6  _  4 | 1  _  5 | 8  7  3 |  the only places left in the blocks Suitable for an 1
 _  _  8 | 4  _  _ | 1  _  _ |  so the 1 needs to be removed from the possibilities in the
............................    squares with the #
 4  _  _ | 5  8  2 | _  *  9 |
 9  8  5 | 3  _  1 | 2  4  _ |  - parce the block in 3 1/3 rows ([[1/3],[2/3],[3/3]])
 _  _  2 | 9  _  _ | 5  *  8 |  -!check if a number occurs in only 1 of them (dictionary, as index the numbers, list occurrenses?)
............................    - translate the y*3 + yi to  1 y (y*3 + indexnumber)
 *  *  * | _  5  9 | _  _  #2|  - remove the number from that row
 _  _  3 | _  1  _ | _  _  _ |  -- #2 works
 8  5  9 | _  _  _ | _  #1 X |  -- #1 works aswell, yay
"""
def CompletIndirect(raster, mark = True):
    if True:
        a = -1
        for y in range(len(raster)/3):
            for x in range(len(raster[y])/3):
                CompleteByRemoval(raster)
                # make a list to contain 3 strips
                block = []
                temp = []
                for yi in range(3):
                    # make a list to contain a strip
                    block.append([])
                    temp.append([])
                    # place the numbers that occure in each strip of 3, unless it is a square that was solved already
                    for xi in range(3):
                        temp[yi].append(raster[y*3 + yi][x*3 + xi])
                        for each in raster[y*3 + yi][x*3 + xi]:
                            if each not in block[yi] and len(raster[y*3 + yi][x*3 + xi]) != 1:
                                block[yi].append(each)
                # make a list to remember which numbers should be removed
                toBeRemoved = []
                for i in range(1,10):
                    # check in how many strips the number occurs
                    occured = 0
                    for each in block:
                        if each.count(i) != 0:
                            occured += 1
                    # if it occurs in only 1 remember it to remove later
                    if occured == 1:
                        toBeRemoved.append(i)
                # cycle through the doomed numbers
                for each in toBeRemoved:
                    # for i in range so that i can be used to determine the row later on
                    for i in range(len(block)):
                        # if the number is in this strip then it can be removed from the row the strip is part of
                        if each in block[i]:
                            # the row relative to the block
                            row = y*3 + i
                            # if the block is the middel blocks
                            # -> this will remove it from the left of the block
                            for xR in range(0,(x*3)):
                                if each in raster[row][xR]:
                                    placeHolder = raster[row][xR][:]
                                    placeHolder.remove(each)
                                    raster[row][xR] = placeHolder[:]
                            # -> this will remove it from the right of the block
                            for xR in range(x*3+3, len(raster[row])):
                                if each in raster[row][xR]:
                                    placeHolder = raster[row][xR][:]
                                    placeHolder.remove(each)
                                    raster[row][xR] = placeHolder[:]
                            if mark and Settings.path[-1] != str(raster):
                                Settings.path.append(str(raster))
    if True:
        for y in range(len(raster)/3):
            for x in range(len(raster[y])/3):
                CompleteByRemoval(raster)
                block = []
                temp = []
                for xi in range(3):
                    # make a list to contain a strip
                    block.append([])
                    temp.append([])
                    # place the numbers that occure in each strip of 3, unless it is a square that was solved already
                    for yi in range(3):
                        temp[xi].append(raster[y*3 + yi][x*3 + xi])
                        for each in raster[y*3 + yi][x*3 + xi]:
                            if each not in block[xi] and len(raster[y*3 + yi][x*3 + xi]) != 1:
                                block[xi].append(each)
                toBeRemoved = []
                for i in range(1,10):
                    # check in how many strips the number occurs
                    occured = 0
                    for each in block:
                        if each.count(i) != 0:
                            occured += 1
                    # if it occurs in only 1 remember it to remove later
                    if occured == 1:
                        toBeRemoved.append(i)
                # cycle through the doomed numbers
                for each in toBeRemoved:
                    # for i in range so that i can be used to determine the row later on
                    for i in range(len(block)):
                        # if the number is in this strip then it can be removed from the row the strip is part of
                        if each in block[i]:
                            # the row relative to the block
                            column = x*3 + i
                            # if the block is the middel blocks
                            # -> this will remove it from the left of the block
                            for yR in range(0,(y*3)):
                                if each in raster[yR][column]:
                                    placeHolder = raster[yR][column][:]
                                    placeHolder.remove(each)
                                    raster[yR][column] = placeHolder[:]
                            # -> this will remove it from the right of the block
                            for yR in range(y*3+3, len(raster)):
                                if each in raster[yR][column]:
                                    placeHolder = raster[yR][column][:]
                                    placeHolder.remove(each)
                                    raster[yR][column] = placeHolder[:]
                            if mark and Settings.path[-1] != str(raster):
                                Settings.path.append(str(raster))

def complete(raster, mark = True, debug = False):
    CompleteByRemoval(raster, mark)
    if mark:
        v.addResult(raster)
    if not valid(raster, debug):
        if debug:
            print "Error 1"
        return
    CompleteByRemainders(raster, mark)
    if mark:
        v.addResult(raster)
    if not valid(raster, debug):
        if debug:
            print "Error 2"
        return
    CompleteBySets(raster, mark)
    if mark:
        v.addResult(raster)
    if not valid(raster, debug):
        if debug:
            print "Error 3"
        return
    CompletIndirect(raster, mark)
    if mark:
        v.addResult(raster)
    if not valid(raster, debug):
        if debug:
            print "Error 4"
        return


def children(raster):
    childs = []
    # y is the row
    for y in range(len(raster)):
        # x is the column
        for x in range(len(raster[0])):
            # if there are more than 1 possibility
            if len(raster[y][x]) != 1:
                # create a temporary board
                for each in raster[y][x]:
                    new_board = raster[:]
                    for yi in range(len(new_board)):
                        new_board[yi] = raster[yi][:]
                        for xi in range(len(new_board[yi])):
                            new_board[yi][xi] = raster[yi][xi][:]
                    new_board[y][x] = [each][:]
                    childs.append(new_board)
    return childs

def stringToList(string):
    spliced = []
    spliced = string.split("]")
    splicedIntRaster = []
    for each in spliced:
        splicedInt = []
        for characters in each:
            if characters.isdigit():
                splicedInt.append(int(characters))
        if splicedInt:
            splicedIntRaster.append(splicedInt)
    raster = []
    for y in range(9):
        temp = []
        for x in range(9):
            temp.append(splicedIntRaster[y*9+x])
        raster.append(temp)
    return raster
