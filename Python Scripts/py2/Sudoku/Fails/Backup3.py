import game as g
import math
import Queue
from Tkinter import *

"""
Functions
"""
#####################################################
# print the array fancy like
def pprint(array, pos = False):
    for y in range(len(array)):
        temp = []
        for x in range(len(array[y])):
            if len(array[y][x]) == 1:
                if pos:
                    temp.append(array[y][x])
                else:
                    temp.append(array[y][x][0])
            else:
                if pos:
                    temp.append(array[y][x])
                else:
                    temp.append(0)
            if x%3 == 2 and x < 8:
                temp.append("-")
        print temp
        if y%3 ==  2 and y < 8:
            print ""
    print "\n"

# place the array into a new array so altering it doesnt fuck shit up
# returns the coppied list
def copy(list):
    temp = []
    for each in list:
        if type(each) == type([]):
            temp.append(copy(each))
        else:
            temp.append(each)
    return temp

# checks if the rows are valid
# returns boolian
def check(array):
    # if check returns 'True', the row is valid
    valid = True
    numbers = [1,2,3,4,5,6,7,8,9]
    # copy the game into an unlinked array to prefent faults
    temp = copy(array)
    # for each row
    for y in range(len(temp)):
        # for each space in the row
        for x in range(len(temp[y])):
            # if that space has more than 1 number in it
            if len(temp[y][x]) != 1:
                temp[y][x] = [0]
        row = []
        for x in range(len(temp[y])):
            for each in temp[y][x]:
                row.append(each)
        for number in numbers:
            if row.count(number) > 1:
                valid = False
    for x in range(len(temp[0])):
        column = []
        for y in range(len(temp)):
            column.append(temp[y][x])
        for number in numbers:
            if column.count(number) > 1:
                valid = False
    for y in range(len(temp)/3):
        for x in range(len(temp[y])/3):
            block = []
            for y2 in range(3):
                for x2 in range(3):
                    block.append(temp[y*3+y2][x*3+x2])
            for number in numbers:
                if row.count(number) > 1:
                    valid = False
    return valid

def done(array):
    valid = True
    numbers = [1,2,3,4,5,6,7,8,9]
    for y in range(len(array)):
        row = []
        for x in range(len(array[y])):
            for each in array[y][x]:
                row.append(each)
        for i in range(len(numbers)):
            if row.count(i) != 1:
                valid = False
    for x in range(len(array[0])):
        column = []
        for y in range(len(array)):
            for each in array[y][x]:
                column.append(each)
        for i in range(len(numbers)):
            if column.count(i) != 1:
                valid = False
    for x1 in range(3):
        for y1 in range(3):
            block = []
            for x2 in range(3):
                for y2 in range(3):
                    block.append(array[y1*3+y2][x1*3+x2])
            for i in range(len(numbers)):
                if block.count(i) != 1:
                    valid = False
    return not valid

def remove(list,steps):
    solid = []
    for each in list:
        if len(each) == 1:
            solid.append(each[0])
    for each in solid:
        for square in list:
            if each in square and len(square) != 1:
                for x in range(len(square)):
                    if each == square[x] and square > 1:
                        square.pop(x)
                        break
            if len(square) == 1 and square not in solid:
                if square[0] not in solid:
                    solid.append(square[0])

def single(list,steps):
    all = []
    for square in list:
        if len(square) != 1:
            for each in square:
                all.append(each)
    for i in numbers:
        if all.count(i) == 1:
            for square in list:
                if i in square and len(square) > 1:
                    while square:
                        square.pop()
                    square.append(i)

def sets(list,steps):
    temp = []
    for each in list:
        if list.count(each) == len(each) and len(each) != 1 and each != temp:
            temp = each
            for number in each:
                for square in list:
                    if square != each and number in square:
                        for x in range(len(square)):
                            if square[x] == number and len(square) > 1:
                                square.pop(x)
                                # important
                                break

def stick(steps, array):
    last = steps[-1][:]
    new = last[:]
    for y in range(len(last)):
        if last[y] != array[y]:
            new[y] = last[y][:]
            for x in range(len(last[y])):
                if array[y][x] != new[y][x]:
                    new[y][x] = array[y][x][:]
                    if new != steps[-1]:
                        steps.append(new)

def clean(game):
    array = game[0]
    steps = game[1]
    # check rows
    for row in range(len(array)):
        remove(array[row],74)
        if steps[-1] != array:
            stick(steps, array)
        single(array[row],steps)
        if steps[-1] != array:
            stick(steps, array)
        sets(array[row],steps)
        if steps[-1] != array:
            stick(steps, array)
    # check Column
    for y in range(len(array[0])):
        column = []
        for x in range(len(array)):
            column.append(array[x][y])
        remove(column,steps)
        if steps[-1] != array:
            stick(steps, array)
        single(column,steps)
        if steps[-1] != array:
            stick(steps, array)
        sets(column,steps)
        if steps[-1] != array:
            stick(steps, array)
    # check blocks
    for y1 in range(len(array)/3):
        for x1 in range(len(array[y])/3):
            block = []
            for y2 in range(3):
                for x2 in range(3):
                    block.append(array[y1*3+y2][x1*3+x2])
            remove(block,steps)
            if steps[-1] != array:
                stick(steps, array)
            single(block,steps)
            if steps[-1] != array:
                stick(steps, array)
            sets(block,steps)
            if steps[-1] != array:
                stick(steps, array)
    return [array,steps]


# command to exit a while loop by button on canvas
def end():
    global running
    running = False

def ref(list,y,x):
    new = list[:]
    new[y] = list[y][:]
    new[y][x] = list[y][x][:]
    return new


#####################################################


#@@@@@@@@

# setting up for the interactive canvas
root = Tk()
root.title('Sudoku')
# height and width of the canvas, and other margins/borders
width = 450
height = 450
buttonWidth = width/9
if buttonWidth < 60:
    buttonWidth = 60
buttonHeight = height/9
margin = 5
fontSize = height/20
canvas = Canvas(root, width = width, height = height + buttonHeight)
canvas.pack()
fields = []
# create entry boxes for input from the user
entrys = [Entry(canvas, font = (_, fontSize), justify = "center") for _ in range(81)]
# for each row/column
for i in range(9):
    # create lines to mark the 3x3 squares
    if (i+1)%3 == 0 and i != 8:
        canvas.create_line((i+1)*(height/9),0 ,(i+1)*(height/9), width, width = margin)
        canvas.create_line(0,(i+1)*(width/9),height,(i+1)*(width/9), width = margin)
    # create the grid and place the entry boxes
    for j in range(9):
        # create the grid lines
        fields.append(canvas.create_rectangle(i*(height/9),j*(width/9),i*(height/9)+(height/9),j*(width/9)+(width/9), tag = "grid"))
        # create the entry boxes
        entry = entrys[i*9+j]
        entry.pack()
        entrys[i*9+j] = entry
        canvas.create_window((j+0.5)*(width/9),(i+0.5)*(height/9),window = entry, height = height/9-margin, width = width/9-margin, tag = "box")

running = True

# creat a button to end input face
temp = Button(canvas, text = "calculate", command = end)
canvas.create_window(buttonWidth/2 + 5, height+buttonHeight/2, window = temp, height = buttonHeight - margin, width = buttonWidth - margin, tag = "button")
canvas.update()
while running:
    root.after(100)
    canvas.update()
running = True, canvas.delete("box"), canvas.delete("button"), canvas.update()
# place the input in a array and proper formatting for legacy code
temp = []
for y in range(9):
    temp.append([])
    for x in range(9):
        each = entrys[y*9+x].get()
        if each:
            each = int(each)
        else:
            each = 0
        temp[y].append(each)

empty = True
for i in temp:
    for j in i:
        if j != 0:
            empty = False
# if the user gave no imput, load the test game indicated above
if empty:
    temp = g.game[3]

solutions = []
game = []
steps = []
numbers = [1,2,3,4,5,6,7,8,9]
for y in range(len(temp)):
    game.append([])
    for x in range(len(temp[y])):
        if temp[y][x] != 0:
            game[y].append([temp[y][x]])
        elif temp[y][x] == 0:
            game[y].append(numbers[:])
print check(game)
game = [game,[copy(game)]]
temp = 0
for i in range(20):
    game = clean(game)
    if temp == len(game[1]):
        break
    temp = len(game[1])
#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$
last = []
counter = 0
for each in game[1]:
    counter += 1
    if last == each:
        print "wut?"
    last = copy(each)
    last = []
    for y in range(len(each)):
        for x in range(len(each[y])):
            if len(each[y][x]) == 1:
                canvas.create_text((x+0.5)*(width/9),(y+0.5)*(height/9), text = each[y][x], tag = "numbers", font = (_, fontSize/(len(each[y][x]))), fill = "#000000")
            elif len(each[y][x]) > 1 and len(each[y][x]) <= 3:
                for i in range(len(each[y][x])):
                    canvas.create_text((x+0.5)*(width/9),(y+0.5)*(height/9), text = each[y][x], tag = "new", font = (_, fontSize/(len(each[y][x]))), fill = "#868686")
            elif len(each[y][x]) > 3 and len(each[y][x]) <= 6:
                for i in range(3):
                    canvas.create_text((x+(i+1)*0.25)*(width/9), (y+0.30)*(height/9), text = each[y][x][i], tag = "new", font = (_, fontSize/3), fill = "#858585")
                    if i+3 < len(each[y][x]):
                        canvas.create_text((x+(i+1)*0.25)*(width/9), (y+0.70)*(height/9), text = each[y][x][3+i], tag = "new", font = (_, fontSize/3), fill = "#858585")
            else:
                for i in range(3):
                    canvas.create_text((x+(i+1)*0.25)*(width/9), (y+0.25)*(height/9), text = each[y][x][i], tag = "new", font = (_, fontSize/3), fill = "#858585")
                    canvas.create_text((x+(i+1)*0.25)*(width/9), (y+0.50)*(height/9), text = each[y][x][3+i], tag = "new", font = (_, fontSize/3), fill = "#858585")
                    if i+6 < len(each[y][x]):
                        canvas.create_text((x+(i+1)*0.25)*(width/9), (y+0.75)*(height/9), text = each[y][x][6+i], tag = "new", font = (_, fontSize/3), fill = "#858585")
    """
    canvas.update()
    root.after(1)
    canvas.delete("new")
    """
#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$

"""
# Bruteforce
"""
queue = Queue.Queue()
queue.put(game)
counter = 0
breaking = False
children = []
result = []
print "Start Bruteforce"
while not queue.empty():
    current = queue.get()
    if counter%10 == 0:
        print "counter:", counter, ", queue.qsize():", queue.qsize()
        pprint(current[0])
    counter += 1
    if not done(current[0]):
        print "done"
        result = copy(current[0])
        break
    for y in range(len(current[0])):
        # print "row:", current[0][y]
        for x in range(len(current[0][y])):
            # print "square:", current[0][y][x]
            if len(current[0][y][x]) > 1:
                for pos in current[0][y][x]:
                    new = copy(current[0])
                    new[y][x] = [pos][:]
                    for i in range(3):
                        clean([new,current[1]])
                    if done(new):
                        print "done2"
                        result = new
                        breaking = True
                    if not check(new):
                        children.append(new)
                    else:
                        queue.put([new,current[1]])
                    if breaking == True:
                        break
            if breaking == True:
                break
        if breaking == True:
            break
    if breaking == True:
        break

print "Bruteforce done"

pprint(result)

canvas.delete("new")
for y in range(len(result)):
    for x in range(len(result[y])):
        if len(result[y][x]) == 1:
            canvas.create_text((x+0.5)*(width/9),(y+0.5)*(height/9), text = result[y][x], font = (_, fontSize), tag = "numbers", fill = "#000000")
            canvas.update()
            root.after(100)

temp = Button(canvas, text = "Exit", command = end)
canvas.create_window(buttonWidth/2 + 5, height+buttonHeight/2, window = temp, height = buttonHeight - margin, width = buttonWidth - margin, tag = "button")
canvas.update()
while running:
    root.after(100)
    canvas.update()
