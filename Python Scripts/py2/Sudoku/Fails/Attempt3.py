import game as imput
import Attempt3Functions as f
import Queue


SelectedGame = 3
numbers = [1,2,3,4,5,6,7,8,9]

game = imput.game[SelectedGame]
f.pprint(game)

for i in range(9):
    for j in range(9):
        if game[i][j] == 0:
            game[i][j] = numbers[:]
        else:
            game[i][j] = [game[i][j]]
f.pprint(game)

f.clear(game)
