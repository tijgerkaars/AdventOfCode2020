import game as imput
import Queue
import Attempt2Functions as f
import Vizualize as v
import Settings


SelectedGame = 2
# Solved: 0,1,2,3,4,5,6,8,9
# BruteForced: 2
# Remaining: 7
numbers = [1,2,3,4,5,6,7,8,9]
Settings.init()

#-------------------------
# Basic game setup:
#   - making a list of lists
# each square contains the possible numbers:
#   - squares containing only 1 number are certain squares/numbers

game = imput.game[SelectedGame]
f.pprint(game)

entrys = v.getGame()

print "entrys:", entrys

imput = []
for y in range(9):
    imput.append([])
    for x in range(9):
        each = entrys[y*9+x].get()
        if each:
            each = int(each)
        else:
            each = 0
        imput[y].append(each)

f.pprint(imput)

print game

userImput = False
for y in range(len(imput)):
    for x in range(len(imput[y])):
        if imput[y][x] != 0:
            userImput = True
            game = imput
            break
    if userImput:
        break

print game

for i in range(9):
    for j in range(9):
        if game[i][j] == 0:
            game[i][j] = numbers[:]
        else:
            game[i][j] = [game[i][j]]
f.pprint(game)

Settings.path.append(str(game))

for i in range(10):
    hold = str(game)
    f.complete(game)
    if f.done(game):
        print "Loops:", i
        f.display(game)
        break
    if hold == str(game):
        break

if f.complete(game):
    print "for loop completed"
    v.showResult()

if f.valid(game, True) and not f.done(game):
    print "start BruteForce"
    archive = False
    queue = Queue.PriorityQueue()
    queue.put((0, game))
    discarded = set()
    counter = 0
    # loop till a solution is found
    while not queue.empty():
        counter += 1
        if counter%1000 == 0:
            print counter
        # get the game from the queue
        trash, game = queue.get()
        # create child games
        children = f.children(game)
        for child in children:
            childHolder = str(child)
            # try and solve the guess human like
            v.addResult(child)
            f.complete(child, False)
            # if the game is solved
            if f.done(child):
                # place the solution in an archive
                print "done with BruteForce"
                archive = True
                f.complete(f.stringToList(childHolder))
                # f.
                v.showResult()
                break
            elif f.valid(child):
                if str(child) not in discarded:
                    discarded.add(str(child))
                    if str(child) == childHolder:
                        v.addResult(child)
                    queue.put((f.score(child), child))
        if archive:
            print "solution found"
            break

for each in Settings.path:
    each = f.stringToList(each)
    if f.done(each):
        f.display(each)

print "\n"
