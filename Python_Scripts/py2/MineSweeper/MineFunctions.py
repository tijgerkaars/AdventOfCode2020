import Setting as s

def numbersIntoLists(game):
    height = game.height
    width = game.width
    raster = game.storage
    grid = []
    for y in range(height):
        grid. append([])
        for x in raster[y]:
            grid[y].append(x.number)
    return grid

def winFunction(game):
    open_needed = game.width*game.height-game.bombs
    open_squares = 0
    for y in range(len(game.storage)):
        for x in range(len(game.storage[y])):
            if game.storage[y][x].state == "open" and game.storage[y][x].number >=0:
                open_squares += 1
            elif game.storage[y][x].state == "open" and  game.storage[y][x].number < 0:
                s.lost = True
                break
        if s.lost == True:
            break
    if s.lost:
        print "you lost"
        return True
    elif open_squares == open_needed:
        print "you win"
        return True
    else:
        return False

def callback(event):
    print "test"
    s.canvas.update()
    if winFunction(s.raster):
        s.temp = True

def mark(event):
    print "test"
    print dir(event)
    print "widget:", event.widget.winfo_x()
    if event.widget.cget("image"):
        event.widget.config(image="")
    else:
        event.widget.config(image=s.photo)
    print event.widget.cget("image")
    s.canvas.update()
