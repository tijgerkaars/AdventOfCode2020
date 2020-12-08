from Tkinter import *
import Settings
import Attempt2Functions as f


root = Tk()
root.title('Sudoku')

width = 450
height = 450
buttonWidth = width/9
if buttonWidth < 60:
    buttonWidth = 60
buttonHeight = height/9
margin = 5
fontSize = height/20
canvas = Canvas(root, width = width, height = height + buttonHeight)
for i in range(9):
    if (i+1)%3 == 0 and i != 8:
        canvas.create_line((i+1)*(height/9),0 ,(i+1)*(height/9), width, width = margin)
        canvas.create_line(0,(i+1)*(width/9),height,(i+1)*(width/9), width = margin)
canvas.pack()

def end():
    global running
    running = False

def getGame():
    global width
    global height
    global buttonWidth
    global buttonHeight
    global margin
    global fontSize
    global running
    fields = []
    entrys = [Entry(canvas, font = (_, fontSize), justify = "center") for _ in range(81)]
    for i in range(9):
        for j in range(9):
            fields.append(canvas.create_rectangle(i*(height/9),j*(width/9),i*(height/9)+(height/9),j*(width/9)+(width/9)))
            entry = entrys[i*9+j]
            entry.pack()
            entrys[i*9+j] = entry
            canvas.create_window((j+0.5)*(width/9),(i+0.5)*(height/9),window = entry, height = height/9-margin, width = width/9-margin, tag = "box")
            bs = 0
    length = len(fields)
    running = True
    temp = Button(canvas, text = "calculate", command = end)
    canvas.create_window(buttonWidth/2 + 5, height+buttonHeight/2, window = temp, height = buttonHeight - margin, width = buttonWidth - margin, tag = "button")
    canvas.pack()
    canvas.update()
    while running:
        root.after(100)
        canvas.update()
    canvas.delete("box")
    canvas.delete("button")
    canvas.create_text(buttonWidth/2 + 5, height+buttonHeight/2, text = "calculating...", tag = "indicator")
    canvas.update()
    return entrys

def showResult(style = False):
    global width
    global height
    global buttonWidth
    global buttonHeight
    global margin
    global fontSize
    global running
    temp = Button(canvas, text = "Show Process", command = end)
    canvas.create_window(buttonWidth/2 + 10, height+buttonHeight/2, window = temp, height = buttonHeight - margin, width = buttonWidth*2 - margin, tag = "button")
    canvas.delete("indicator")
    canvas.pack()
    canvas.update()
    running = True
    while running:
        root.after(100)
        canvas.update()
    canvas.delete("button")
    canvas.update()
    path = Settings.path
    for each in path:
        each = f.stringToList(each)
        addResult(each)
    if style:
        addResult(style)
    running = True
    temp = Button(canvas, text = "Exit", command = end)
    canvas.create_window(buttonWidth/2 + 5, height+buttonHeight/2, window = temp, height = buttonHeight - margin, width = buttonWidth - margin, tag = "button")
    canvas.pack()
    canvas.update()
    while running:
        root.after(100)
        canvas.update()

def addResult(raster):
    global width
    global height
    global buttonWidth
    global buttonHeight
    global margin
    global fontSize
    global running
    canvas.delete("numbers")
    for y in range(len(raster)):
        for x in range(len(raster[y])):
            if len(raster[y][x]) == 1:
                canvas.create_text((x+0.5)*(width/9),(y+0.5)*(height/9), text = raster[y][x][0], tag = "numbers", font = ("Ariel", fontSize/len(raster[y][x])), fill = "#000000")
            elif len(raster[y][x]) > 1 and len(raster[y][x]) <= 3:
                for xi in range(3):
                    if len(raster[y][x]) == xi:
                        break
                    canvas.create_text((x+(xi+1)*0.25)*(width/9),(y+0.5)*(height/9), text = raster[y][x][xi], tag = "numbers", font = ("Ariel", int(round(fontSize/1.5))), fill = "#808080")
            elif len(raster[y][x]) > 3 and len(raster[y][x]) <= 6:
                for yi in range(2):
                    for xi in range(3):
                        if len(raster[y][x]) == yi*3+xi:
                            break
                        canvas.create_text((x+(xi+1)*0.25)*(width/9),(y+(yi+1)*0.3)*(height/9), text = raster[y][x][yi*3+xi], tag = "numbers", font = ("Ariel", int(round(fontSize/1.8))), fill = "#808080")
                    if len(raster[y][x]) == yi*3+xi:
                        break
            elif len(raster[y][x]) > 6:
                for yi in range(3):
                    for xi in range(3):
                        if len(raster[y][x]) == yi*3+xi:
                            break
                        canvas.create_text((x+(xi+1)*0.25)*(width/9),(y+(yi+1)*0.25)*(height/9), text = raster[y][x][yi*3+xi], tag = "numbers", font = ("Ariel", int(round(fontSize/2.5))), fill = "#d3d3d3")
                    if len(raster[y][x]) == yi*3+xi:
                        break
    canvas.update()

def delay():
    root.after(10)
