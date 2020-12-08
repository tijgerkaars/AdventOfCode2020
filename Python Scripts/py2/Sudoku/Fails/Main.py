import game as g
import math
import Queue
from Tkinter import *

"""
Functions
"""
###################################
# copy's all list's within a list
def copy(list):
    global counter
    counter += 1
    temp = []
    for each in list:
        if type(each) == type([]):
            temp.append(copy(each))
            print counter, each
        else:
            temp.append(each)
    return temp
###################################

# the game that is solved if no input is given by users
testGame = 3
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

# command to exit a while loop by button on canvas
def end():
    global running
    running = False

# creat a button to end input face
temp = Button(canvas, text = "calculate", command = end)
canvas.create_window(buttonWidth/2 + 5, height+buttonHeight/2, window = temp, height = buttonHeight - margin, width = buttonWidth - margin, tag = "button")
canvas.update()
while running:
    root.after(100)
    canvas.update()
# place the input in a array and proper formatting for legacy code
game = []
for y in range(9):
    game.append([])
    for x in range(9):
        each = entrys[y*9+x].get()
        if each:
            each = int(each)
        else:
            each = 0
        game[y].append(each)

# show the user that the answer is being calculated
canvas.delete("box")
canvas.delete("button")
canvas.create_text(buttonWidth/2 + 5, height+buttonHeight/2, text = "calculating...", tag = "indicator")
canvas.update()
# check if the user gave input
empty = True
for i in game:
    for j in i:
        print j, empty
        if j != 0:
            empty = False
# if the user gave no imput, load the test game indicated above
if empty:
    game = g.game[testGame]

anti = []
empty = [1,2,3,4,5,6,7,8,9]

for row in range(len(game)):
    print game[row]
    anti.append([])
    for square in game[row]:
        if square != 0:
            anti[row].append([square])
        else:
            anti[row].append(empty[:])

print "\n"
for i in anti:
    print i
print "\n"

def pprint(array):
    temp = copy(array)
    array = temp
    for y in range(len(array)):
        row = []
        for x in range(len(array[y])):
            if len(array[y][x]) != 1:
                array[y][x] = [0]
            row.append(array[y][x])
            if x%3 == 2 and (x != 8):
                row.append("-")
        print row
        if (y+1)%3 == 0 and y != len(array)-1:
            temp = []
            for i in range(len(row)):
                temp.append("-")
            print temp
    print "\n"


# remove number from lists in list
def remove(number, list):
    for each in list:
        if len(each) != 1 and number in each:
            for poss in range(len(each)):
                if each[poss] == number:
                    each.pop(poss)
                    break

def removePro(list):
    test = False
    if test == True:
        print list
    solid = []
    liquid = []
    for x in range(len(list)):
        if len(list[x]) == 1:
            solid.append(list[x][0])
        elif len(list[x]) > 1:
            liquid.append(list[x])
    if test == True:
        print "solid:", solid
        print "liquid:", liquid
    temp = []
    while temp != list:
        temp = []
        for each in list:
            temp.append(each[:])
        if test == True:
            print "temp:", temp
            print "list:", list
        for number in solid:
            remove(number,list)
        for x in range(len(list)):
            if len(list[x]) == 1:
                solid.append(list[x][0])
        if test == True:
            print list


def singles(list, test = 0):
    if test == 1:
        test = True
    else:
        test = False
    freq = []
    if test == True:
        print "\ntest function singles:-"
        print "list:", list
    # removePro(list)
    for each in list:
        if len(each) != 1:
            for number in each:
                freq.append(number)
    for i in empty:
        if freq.count(i) == 1:
            for each in range(len(list)):
                if i in list[each]:
                    # suck it references problems
                    for j in range(len(list[each])):
                        list[each].pop()
                    list[each].append(i)
    if test == True:
        print "Test end\n"

def copy(list):
    test = False
    step = []
    if test == True:
        print "step whole:", step
        print "list:", list
    for i in range(len(list)):
        step.append([])
        if test == True:
            print "step row:", step
            print "i:", list[i]
        for j in range(len(list[i])):
            step[i].append([])
            if test == True:
                print "step square:", step
                print "j:", list[i][j]
            for k in list[i][j]:
                step[i][j].append(k)
    return step

def sets(list):
    test = False
    if test == True:
        print "test\n"
    for square in list:
        if test == True:
            print "square:", square, "len:", len(square), "count:", list.count(square)
        if len(square) == list.count(square) and len(square) != 1:
            if test == True:
                print "square 2:", square
                print "list 1:", list
            for number in square:
                for each in list:
                    if each != square:
                        for poss in range(len(each)):
                            if each[poss] == number:
                                each.pop(poss)
                                break
            if test == True:
                print "list 2:", list
    if test == True:
        print "end test"

def check(list, part = "all"):
    test = False
    testR = False
    testC = False
    testB = False
    testEndR = False
    testEndC = False
    TestEndB = False
    if test == True:
        print "test"
        print list
    if part == "row" or part == "all":
        for row in range(len(list)):
            if testR == True:
                print "row:", list[row]
            filled = []
            for square in range(len(list[row])):
                if testR == True:
                    print "square:", list[row][square]
                if len(list[row][square]) == 1:
                    filled.append(list[row][square][0])
            for i in empty:
                if filled.count(i) > 1:
                    if testEndR == True:
                        print "row filled:", filled
                    return False
    if part == "column" or part == "all":
        for column in range(len(list[0])):
            filled = []
            for square in range(len(list)):
                if len(list[square][column]) == 1:
                    filled.append(list[square][column][0])
            if testC == True:
                print "column:", filled
            for i in empty:
                if filled.count(i) > 1:
                    if testEndC == True:
                        print "column filled:", filled
                    return False
    if part == "block" or part == "all":
        for BlockRows in range((len(list)/3)):
            for BlockColumns in range(len(list[0])/3):
                filled = []
                for j in range(3):
                    for i in range(3):
                        if len(list[BlockRows*3 + i][BlockColumns*3 + j]) == 1:
                            filled.append(list[BlockRows*3 + i][BlockColumns*3 + j][0])
                if testB == True:
                    print "block:", block
                for i in empty:
                    if filled.count(i) > 1:
                        if TestEndB == True:
                            print "column filled:", filled
                        return False
    return True

def done(array, test = 0):
    if test:
        print"start testing done"
    won = True
    for y in array:
        for x in y:
            if len(x) != 1:
                won = False
    c = check(array)
    if won and c:
        return True
    elif won and not c:
        return False
    elif not won and c:
        return False
    else:
        return False

print "starting cleaner"
steps = []
steps.append(copy(anti))
controle = []
controle.append(copy(anti))
test = False
# solve in so many cycles
for loop in range(30):
    change = False
    # loop over the rows and remove inpossible numbers
    print "checking rows:", loop
    for row in range(len(anti)):
        for square in range(len(anti[row])):
            if len(anti[row][square]) == 1:
                removePro(anti[row])
        steps.append(copy(anti))
        singles(anti[row],0)
        steps.append(copy(anti))
        sets(anti[row])
        steps.append(copy(anti))
    if controle[len(controle)-1] != anti:
        controle.append(copy(anti))
        change = True
        if not check(anti):
            print "invalid alteration in row on loop:", loop
            for x in anti:
                print x
            break
    # loop over the columns and remove inpossible numbers
    print "checking columns:", loop
    for column in range(len(anti[0])):
        ColumnList = []
        for square in range(len(anti)):
            ColumnList.append(anti[square][column])
        for square in range(len(ColumnList)):
            if len(ColumnList[square]) == 1:
                removePro(ColumnList)
        steps.append(copy(anti))
        singles(ColumnList, 0)
        steps.append(copy(anti))
        sets(ColumnList)
        steps.append(copy(anti))
    if controle[len(controle)-1] != anti:
        controle.append(copy(anti))
        change = True
        if not check(anti):
            print "invalid alteration in column on loop:", loop
            for y in range(len(anti)):
                for x in range(len(anti[y])):
                    if len(anti[y][x]) > 1:
                        anti[y][x] = [0]
            for x in anti:
                print x
            break
    # Loop over the blocks and remove inpossible numbers
    print "checking blocks:", loop
    for BlockRows in range((len(anti)/3)):
        for BlockColumns in range(len(anti[0])/3):
            block = []
            for j in range(3):
                for i in range(3):
                    block.append(anti[BlockRows*3 + i][BlockColumns*3 + j])
            for square in block:
                if len(square) == 1:
                    removePro(block)
            steps.append(copy(anti))
            singles(block,0)
            steps.append(copy(anti))
            sets(block)
            steps.append(copy(anti))
    if controle[len(controle)-1] != anti:
        controle.append(copy(anti))
        change = True
        if not check(anti):
            print "invalid alteration in block on loop:", loop
            for x in anti:
                print x
            break
    #stop the looping if no changes are made
    if change == False:
        print "no more change\n"
        break
print "done looping\n"

last = steps.pop()
path = []
temp = []
length = len(steps)
for i in range(length):
    temp = steps.pop()
    if temp != last:
        path.append(last)
        last = temp

length = len(path)
for i in range(length):
    last = path.pop()
    steps.append(last)

for row in range(len(last)):
    for square in range(len(last[row])):
        if len(last[row][square]) == 1:
            game[row][square] = last[row][square]
        else:
            game[row][square] = last[row][square]

total = 1
for i in game:
    for j in i:
        total *= len(j)
print "total possibility's left:", total

forced = False

if not done(game):
    print "Starting BruteForce"
    forced = True
    # do something with a queue here, place all options in a queue and remove once invalid
    queue = Queue.Queue()
    queue.put(game)
    test = False
    loop = 0
    counter = 0
    while not queue.empty():
        loop +=1
        canvas.delete("numbers")
        breaking = False
        current = queue.get()
        if loop%10000 == 0:
            print "loop:", loop, "counter:", counter, "queue length:", queue.qsize()
            for y in range(len(current)):
                for x in range(len(current[y])):
                    if len(current[y][x]) == 1:
                        canvas.create_text((x+0.5)*(width/9),(y+0.5)*(height/9), text = current[y][x], tag = "numbers", font = (_, fontSize), fill = "#000000")
            canvas.create_text(width-50,height+(height/9)/2, text = counter , tag = "counter")
            canvas.update()
            canvas.delete("counter")
        if test == True:
            pprint(current)
        for i in empty:
            for row in range(len(current)):
                if test == True:
                    print "row:", current[row]
                for square in range(len(current[row])):
                    if test == True:
                        print "square:", current[row][square], "length:", len(current[row][square])
                    if len(current[row][square]) > 1 and len(current[row][square]) == i:
                        pos = current[row][square][:]
                        for each in pos:
                            temp = []
                            current[row][square] = [each]
                            counter += 1
                            if check(current):
                                temp = copy(current)
                                queue.put(temp)
                                steps.append(temp)
                                breaking = True
                    if breaking == True:
                        break
                if breaking == True:
                    break
            if breaking == True:
                break
elif total > 500000000000000:
    print "To many possibility's"
else:
    print "Sudoku solved"

print "Begin showing solution"
running = True
temp = Button(canvas, text = "Start solution", command = end)
canvas.delete("indicator")
canvas.create_window(buttonWidth/2 + margin*2, height+buttonHeight/2, window = temp, height = buttonHeight - margin, width = buttonWidth*2 - margin, tag = "button")
canvas.update()
while running:
    root.after(100)
    canvas.update()
canvas.delete("button")

counter = -1
temp = []
for each in steps:
    canvas.delete("numbers")
    for y in range(len(each)):
        for x in range(len(each[y])):
            if len(each[y][x]) == 1:
                if counter < length:
                    canvas.create_text((x+0.5)*(width/9),(y+0.5)*(height/9), text = each[y][x], tag = "numbers", font = (_, fontSize/(len(each[y][x]))), fill = "#000000")
                else:
                    if each[y][x] == last[y][x]:
                        canvas.create_text((x+0.5)*(width/9),(y+0.5)*(height/9), text = each[y][x], tag = "numbers", font = (_, fontSize/(len(each[y][x]))), fill = "#000000")
                    else:
                        canvas.create_text((x+0.5)*(width/9),(y+0.5)*(height/9), text = each[y][x], tag = "numbers", font = (_, fontSize/(len(each[y][x]))), fill = "red")
            elif len(each[y][x]) > 1 and len(each[y][x]) <= 3:
                canvas.create_text((x+0.5)*(width/9),(y+0.5)*(height/9), text = each[y][x], tag = "numbers", font = (_, fontSize/(len(each[y][x]))), fill = "#858585")
            elif len(each[y][x]) > 3 and len(each[y][x]) <= 6:
                for i in range(3):
                    canvas.create_text((x+(i+1)*0.25)*(width/9), (y+0.30)*(height/9), text = each[y][x][i], tag = "numbers", font = (_, fontSize/3), fill = "#858585")
                    if i+3 < len(each[y][x]):
                        canvas.create_text((x+(i+1)*0.25)*(width/9), (y+0.70)*(height/9), text = each[y][x][3+i], tag = "numbers", font = (_, fontSize/3), fill = "#858585")
            else:
                for i in range(3):
                    canvas.create_text((x+(i+1)*0.25)*(width/9), (y+0.25)*(height/9), text = each[y][x][i], tag = "numbers", font = (_, fontSize/3), fill = "#858585")
                    canvas.create_text((x+(i+1)*0.25)*(width/9), (y+0.50)*(height/9), text = each[y][x][3+i], tag = "numbers", font = (_, fontSize/3), fill = "#858585")
                    if i+6 < len(each[y][x]):
                        canvas.create_text((x+(i+1)*0.25)*(width/9), (y+0.75)*(height/9), text = each[y][x][6+i], tag = "numbers", font = (_, fontSize/3), fill = "#858585")
        temp = each
    canvas.update()
    counter += 1
    x = 250
    if counter < length:
        canvas.after(x)
    elif forced == True:
        canvas.after(5)
    else:
        canvas.after(x/5)
canvas.delete("text")
canvas.create_text(buttonWidth/2 + 5, height+buttonHeight/2, text = "Job Done :)", tag = "text")
canvas.update()
canvas.after(1000)
canvas.delete("text")
canvas.update()

running = True
temp = Button(canvas, text = "Exit", command = end)
canvas.create_window(buttonWidth/2 + 5, height+buttonHeight/2, window = temp, height = buttonHeight - margin, width = buttonWidth - margin, tag = "button")
canvas.update()
while running:
    root.after(100)
    canvas.update()
