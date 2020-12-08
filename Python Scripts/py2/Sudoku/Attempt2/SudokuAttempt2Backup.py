import game as imput
import Queue
import Attempt2Functions as f


SelectedGame = 7
# Solved: 0,1,3,4,5,6
# Remaining: 2,7
numbers = [1,2,3,4,5,6,7,8,9]

#-------------------------
# Basic game setup:
#   - making a list of lists
# each square contains the possible numbers:
#   - squares containing only 1 number are certain squares/numbers

game = imput.game[SelectedGame]
f.pprint(game)

for i in range(9):
    for j in range(9):
        if game[i][j] == 0:
            game[i][j] = numbers[:]
        else:
            game[i][j] = [game[i][j]]
f.pprint(game)

for i in range(10):
    f.complete(game, i+1)
    if f.done(game):
        print "Loops:", i
        break

queue = Queue.PriorityQueue()
queue.put((0, game))
if f.valid(game, True) and not f.done(game):
    # while not queue.empty():
    for i in range(1):
        if queue.qsize()%100 == 0:
            print queue.qsize()
        trash, current = queue.get()
        print "trash:", trash
        print "current:", current
        trash = 0
        f.display(current)
        children = f.children(current)
        solutions = []
        for each in children:
            counter = 0
            start = ""
            end = "start"
            while start != end:
                start = str(each)
                f.complete(each, i, True)
                counter += 1
                end = str(each)
            if f.valid(each, True):
                if f.done(each):
                    print "Done Through BruteForce"
                    f.display(each)
                    # break
                    # remove brake if multiple solutions seem likely
                    solutions.append(each)
                    break
                else:
                    queue.put((f.score2(each), each))
        if len(solutions) > 0:
            break

test = dict()
if len(solutions) > 0:
    print len(solutions)
    for each in solutions:
        if str(each) in test:
            test[str(each)] += 1
        else:
            test[str(each)] = 1
    print test
"""
if False:
    f.display (game, True)
    f.pprint  (game, "row")
    f.pprint  (game, "column")
    f.pprint  (game, "block")
"""
