import Setting as s
import Tkinter as tk
import MineFunctions as f
from Tkinter import *
from PIL import Image, ImageTk

s.init()

def test(game):
    height = game.height
    width = game.width
    raster = game.storage
    grid = []
    for y in range(height):
        grid. append([])
        for x in raster[y]:
            grid[y].append(x.number)
    for each in grid:
        print each

def end():
    s.running = False

def close():
    end()
    s.canvas.destroy()


def getImput():
    s.root = tk.Tk()
    root = s.root
    root.title('Minesweeper')
    canvas = tk.Canvas(root, width = s.canvasWidth, height = s.canvasHeight)
    canvas.pack()
    x, y = s.canvasTextMargin, s.canvasTextMargin
    userImput = []
    canvas.create_text(2*x,y , text = "Width")
    imputWidth = tk.Entry(canvas, justify = "left")
    canvas.create_window(4*x,y, anchor = "w", window = imputWidth, tag = "box")
    canvas.create_text(2*x,2*y, text = "Height")
    imputHeigth = tk.Entry(canvas, justify = "left")
    canvas.create_window(4*x,2*y, anchor = "w", window = imputHeigth, tag = "box")
    canvas.create_text(2*x,3*y, text = "Bombs")
    imputBombs = tk.Entry(canvas, justify = "left")
    canvas.create_window(4*x,3*y, anchor = "w", window = imputBombs, tag = "box")
    startButton = tk.Button(canvas, text = "start", command = end)
    canvas.create_window(s.canvasWidth, s.canvasHeight,anchor = "se", window = startButton, height = s.buttonHeight, width = s.buttonWidth, tag = "button")
    canvas.pack()
    canvas.update()
    valid = False
    s.running = True
    text,temp = False, False
    while s.running or not valid:
        root.after(100)
        canvas.update()
        if not imputBombs.get().isdigit() and imputBombs.get() or not imputHeigth.get().isdigit() and imputHeigth.get() or not imputWidth.get().isdigit() and imputWidth.get():
            if not text:
                canvas.delete("imputWarning")
                text = canvas.create_text(2*x,4*y, text = "Only numbers please", anchor = "w", tag = "imputWarning")
                print text, "test"
        elif text:
            # should be easier :#
            if not imputBombs.get() and not imputHeigth.get() and not imputWidth.get() or imputBombs.get().isdigit() and not imputHeigth.get() and not imputWidth.get() or imputBombs.get().isdigit() and imputHeigth.get().isdigit() and not imputWidth.get() or imputBombs.get().isdigit() and not imputHeigth.get() and imputWidth.get().isdigit() or not imputBombs.get() and imputHeigth.get().isdigit() and not imputWidth.get() or not imputBombs.get() and imputHeigth.get().isdigit() and imputWidth.get().isdigit() or not imputBombs.get() and not imputHeigth.get() and imputWidth.get().isdigit():
                canvas.delete("imputWarning")
                text = False
        if imputBombs.get().isdigit() and len(imputBombs.get()) != 0 and imputHeigth.get().isdigit() and imputWidth.get().isdigit() and len(imputHeigth.get()) != 0 and len(imputWidth.get()) != 0:
            valid = True
        if s.running == False and not text:
            text = canvas.create_text(2*x,4*y, text = "please fill out all fields", anchor = "w", tag = "imputWarning")
        if s.running == False:
            if int(imputBombs.get()) > int(imputHeigth.get()) * int(imputWidth.get()):
                canvas.delete("imputWarning")
                text = canvas.create_text(2*x,4*y, text = "That ammount of mines is ludicrous", anchor = "w", tag = "imputWarning")
                text = canvas.create_text(2*x,5*y, text = "Don't you want any empty spaces?", anchor = "w", tag = "imputWarning")
                s.running = True
        if not valid:
            s.running = True
    s.width = int(imputWidth.get())
    s.height = int(imputHeigth.get())
    s.bombs = int(imputBombs.get())
    return int(imputWidth.get()), int(imputHeigth.get()), int(imputBombs.get())

def uncover(text = None,row = None,column = None):
    if s.canvas:
        if s.raster.storage[row][column]._widget.cget("image"):
            return
    s.canvas.delete(text)
    s.raster.storage[row][column].state = "open"
    if s.raster.storage[row][column].number == 0:
        # if the square to the left is not a bomb and is still covered
        if row-1 >= 0 and s.raster.storage[row-1][column].number >= 0 and s.raster.storage[row-1][column].state == "covered" and True:
            uncover(s.raster.storage[row-1][column].button, row-1, column)
        # if the square to the right is not a bomb and still covered
        if row+1 < s.raster.height and s.raster.storage[row+1][column].number >= 0 and s.raster.storage[row+1][column].state == "covered" and True:
            uncover(s.raster.storage[row+1][column].button, row+1, column)
        # if the square above is not a bomb and still covered
        if column-1 >= 0 and s.raster.storage[row][column-1].number >= 0 and s.raster.storage[row][column-1].state == "covered" and True:
            uncover(s.raster.storage[row][column-1].button, row, column-1)
        # if the square below is not a bomb and still covered
        if column+1 < s.raster.width and s.raster.storage[row][column+1].number >= 0 and s.raster.storage[row][column+1].state == "covered" and True:
            uncover(s.raster.storage[row][column+1].button, row, column+1)
        # corners
        # if the square above and left is not a bomb and is still covered
        if column-1 >= 0 and row-1 >= 0 and s.raster.storage[row-1][column-1].number >= 0 and s.raster.storage[row-1][column-1].state == "covered" and True:
            uncover(s.raster.storage[row-1][column-1].button, row-1, column-1)
        # if the square above to the right is not a bomb and is still covered
        if column+1 < s.raster.width and row-1 >= 0 and s.raster.storage[row-1][column+1].number >= 0 and s.raster.storage[row-1][column+1].state == "covered" and True:
            uncover(s.raster.storage[row-1][column+1].button, row-1, column+1)
        # if the square below to the left is not a bomb and is still covered
        if column-1 >= 0 and row+1 < s.raster.height and s.raster.storage[row][column].number >= 0 and s.raster.storage[row+1][column-1].state == "covered" and True:
            uncover(s.raster.storage[row+1][column-1].button, row+1, column-1)
        # if the square below to the right is not a bomb and is still covered
        if column+1 < s.raster.width and row+1 < s.raster.height and s.raster.storage[row+1][column+1].number >= 0 and s.raster.storage[row+1][column+1].state == "covered" and True:
            uncover(s.raster.storage[row+1][column+1].button, row+1, column+1)

def lost():
    pass

def startGame(raster):
    if s.root:
        s.root.destroy()
    s.canvasWidth, s.canvasHeight = raster.width * s.squareScaling, raster.height * s.squareScaling
    s.root = tk.Tk()
    root = s.root

    my_image = Image.open("C:\Users\Jobber\Documents\Python Scripts\MineSweeper\\flag.jpg")

    s.photo = ImageTk.PhotoImage(my_image)
    root.title('Minesweeper')
    canvas = tk.Canvas(root, width = s.canvasWidth + 2* s.canvasMargin, height = s.canvasHeight + 2* s.canvasMargin + s. buttonHeight)
    s.canvas = canvas
    canvas.pack()
    buttons = []
    for rows in range(raster.height):
        for squares in range(raster.width):
            number = rows*raster.width + squares
            text = "Button" + str(number+1)
            raster.storage[rows][squares].button = text
            squareButton = tk.Button(canvas, relief = "groove", command = lambda text = text, row = rows, column = squares : uncover(text, row, column), bg = 'grey', image = None)
            squareButton.bind("<Button-3>", f.mark)
            s.raster.storage[rows][squares]._widget = squareButton
            buttons.append(squareButton)
            canvas.create_window(s.canvasMargin + s.squareScaling*squares, s.canvasMargin + s.squareScaling*rows, anchor = "nw", window = squareButton, height = s.squareScaling, width = s.squareScaling, tag = text)
            if int(raster.storage[rows][squares].number) != 0:
                canvas.create_text(s.canvasMargin + s.squareScaling*(0.4 + squares), s.canvasMargin + s.squareScaling*(0.25 + rows), anchor = "nw", text = str(raster.storage[rows][squares].number))
    return canvas
