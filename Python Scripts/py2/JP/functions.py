# fill the picture with coordinates
def debugpic(z):
    for i in range(height):
        for j in range(width):
            if i == j and j == 0:
                z[i][j] = ["x,y"]
            else:
                z[i][j] = [j,i]
    return z

# clears a picture
def clear(z):
    for i in range(height):
        for j in range(width):
            z[i][j] = 0
    return z

def printb(z):
    print "field"
    for i in range(len(z)):
        print z[i]
    print "field end"

# find the available spaces for a row
# (column to be implemented)
def space(board, o, x = 0, y = 0):
    width = len(board[0])
    height = len(board)
    # check row, x = 0, y = row to check
    start = -1
    started = False
    end = -1
    # checks lenghtes of the available slots for fragments
    if o == "row":
        for i in range(width):
            if board[y][i] >= 0 and started == False:
                start = i
                started = True
                # for a single fragment at the end of the row
                if i == width - 1:
                    return i, i
            elif board[y][i] < 0 and started == True:
                end = i-1
                started = False
                if i > x:
                    started = False
                    break
            elif i == width-1 and started == True:
                end = i
                started = False
        if end == -1 or start == -1:
            return "empty"
        else:
            return end, start
    elif o == "column":
        for i in range(height):
            if board[i][x] >=0 and started == False:
                start = i
                started = True
                if i == height-1:
                    return i,i
            elif board[i][x] < 0 and started == True:
                end = i-1
                started = False
                if i > y:
                    break
            elif i == height-1 and started == True:
                end = i
                started = False
        if end == start and start == -1:
            return "empty"
        else:
            return end, start

# fills a designated portion of the picture
# insert the picture, row/column, (end. start), the column, the row, what number is placed on the picture
def fill(board, o, positions, x=0, y=0, filler = 1):
    if positions == "empty":
        return
    if o == "row":
        for i in range(positions[1], positions[0] + 1):
            #if board[y][i] == 0:
                board[y][i] = filler
    elif o == "column":
        for i in range(positions[1], positions[0] + 1):
            #if board[i][x] == 0:
                board[i][x] = filler
    return board

def x(top, sides, board):
    for i in range(len(sides)):
        if sides[i][0] == len(top):
            fill(board, "row", ((len(top)-1),0), 0, i, 1)
    for i in range(len(sides)):
        if sides[i][0] == 0:
            fill(board, "row", ((len(top)-1),0), 0, i,-1)
    for i in range(len(top)):
        if top[i][0] == len(sides):
            fill(board, "column", ((len(sides)-1),0), i, 0, 2)
    for i in range(len(top)):
        if top[i][0] == 0:
            fill(board, "column", ((len(sides)-1),0), i, 0,-2)
    return board

def frag(board, o, slot, fragment, x=0, y=0, filler = 1):
    if o == "row":
        end = slot[0]
        start = slot[1]
        print "(", end, start, ")", fragment
        if (end - start) == fragment:
            board = fill(board, o, slot, x, y, filler)
        elif 0.5*(end-start) < fragment:
            start2 = end - fragment + 1
            end2 = start + fragment - 1
            board = fill(board, o, (end2,start2), x, y, filler)
        return board



""""
picture = [
[0, 0,-1, 0, 0],
[0,-1,-1, 0,-1],
[-1, 0,-1, 0,-1],
[0, 0,-1, 0, 0],
[0, 0,-1, 0,-1],
[0, 0,-1, 0, 0],
[0, 0,-1, 0, 0],
[0, 0,-1, 0,-1],
[0,-1,-1, 0,-1],
[0, 0,-1, 0, 0]]


picture = [
[0, 0, -10, 0, 0, 0, 0, 0, 0, 0],
[0, -1, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, -1, 0, 0, 0, 0],
[0, 0, -1, 0, 0, 0, 0, 0,-1, 0],
[0, 0, -1, 0, -1, 0, 0, 0,-1, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[0,-1,-1,-1,-1,-1,-1,-1,-1,-1]]

"""
