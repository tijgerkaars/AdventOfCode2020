import game

game = game.game[2]
# prep possibility's
start = [1,2,3,4,5,6,7,8,9]
possibility = []
for i in range(9):
    possibility.append([])
    for j in range(9):
        possibility[i].append(start[:])
# remove possibility's for filled in squares
for i in range(len(game)):
    for j in range(len(game[i])):
        if game[i][j] != 0:
            possibility[i][j] = [-1]
print "\n"

# remove x from list y
def clear(x, y):
    # print "x", x, "y", y
    for i in range(len(y)):
        # print "square", i, y[i]
        lenght = len(y[i])
        for j in range(lenght):
            k = (lenght-1) - j
            if y[i][k] == x and len(y[i]) != 1:
                y[i].pop(k)

# fill y into x
def fill(x,y):
    # print "x", x
    # print "y", y, "\n"
    for i in range(len(y)):
        # print y[i]
        for j in range(len(y[i])):
            # print y[i][j]
            if len(y[i][j]) == 1 and y[i][j][0] != -1:
                x[i][j] = y[i][j][0]
        # print "\n"

# print the sudoku
for i in game:
    print i
print "\n"

# <<<<<< start of alghoritem
# remove possibility's and insert certainties for x loops
past = 0
for loops in range(20):
    # store newest sudoke
    temp = []
    for i in game:
        temp.append(i[:])
    #
    # remove probability's via row's
    #
    # for row in game, i == row
    for i in range(len(game)):
        # for square in, j == square
        for j in range(len(game[i])):
            # clear the number on square (i,j) from the possibility's for that row
            clear(game[i][j], possibility[i])
            total = []
            for k in range(len(possibility[i])):
                for l in possibility[i][k]:
                    if l != -1:
                        total.append(l)
            # see of any number between 1 and 9 occurs only once
        total = []
        for j in range(len(possibility[i])):
            for k in possibility[i][j]:
                if k != -1:
                    total.append(k)
        for k in start:
            if total.count(k) == 1:
                for each in possibility[i]:
                    if k in each and len(each) != 1:
                        lenght = len(each)
                        for l in range(lenght):
                            m = lenght-1-l
                            if each[m] != k:
                                each.pop(m)
                        break
    #
    # remove probability's via columns
    #
    # for column in game, i == columns
    for i in range(len(game[0])):
        column = []
        total = []
        # for square in column, j == square
        for j in range(len(game)):
            # collect referencesses for the column possibility's in a list
            column.append(possibility[j][i])
        # remove the number in the column from probability's
        for j in range(len(game)):
            clear(game[j][i], column)
        for j in column:
            for k in j:
                if k != -1:
                    total.append(k)
        for j in start:
            for k in column:
                if total.count(j) == 1 and len(k) != 1 and j in k:
                    lenght = len(k)
                    for l in range(lenght):
                        m = lenght-1-l
                        if k[m] != j:
                            k.pop(m)
    for i in possibility:
        print i
    print "\n"
    #
    # remove probability's via block
    #
    # for blocks in column
    for m in range(len(game)/3):
        # for blocks in row
        for k in range(len(game[m])/3):
            block = []
            probBlock = []
            # for suares in block <<<
            for i in range(3):
                # >>>
                for j in range(3):
                    # creat list from squares in a block
                    block.append(game[k*3+i][m*3+j])
                    # creat list of reference to possibility's in the block
                    probBlock.append(possibility[k*3+i][m*3+j])
            # remove the number in the block from the possibility's
            for i in block:
                if i != 0:
                    clear(i, probBlock)
            # see if there remains only 1 square for all numbers, <<<
            total = []
            # add all the probability's in the block to 1 list if not -1
            for i in probBlock:
                for j in i:
                    if j != -1:
                        total.append(j)
            # check numbers 1 through 9
            for i in start:
                for j in range(len(probBlock)):
                    # if the number (i) occurs only once and the number is in the probability for the square
                    if total.count(i) == 1 and (i in probBlock[j]):
                        lenght = len(probBlock[j])
                        # remove all the probability's from that square but the only possible number
                        for k in range(lenght):
                            l = lenght-1-k
                            if probBlock[j][l] != i:
                                probBlock[j].pop(l)
                        # can only be in 1 square so break to save time
                        break
            # >>>
    #
    fill(game,possibility)
    #
    # if no new squares were filled in break
    if temp == game:
        # print how many loops were done before breaking
        print "loops:", loops
        for i in possibility:
            print i
        print "\n"
        break
# >>>>>> end of alghoritem

print "\n"
for i in game:
    print i
print "\n"

"""
print "\n"
for i in range(len(possibility)):
    # print i+1
    print possibility[i]
    for j in range(len(possibility[i])):
        t = 0
        # print  possibility[i][j]
    # print "\n"
"""
"""
for i in game:
    print i
"""
