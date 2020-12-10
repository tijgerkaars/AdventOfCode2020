#---------------------------------------------------------------------------
"""
test inputs
09 players; last marble is worth 0025 points: high score is 0032
10 players; last marble is worth 1618 points: high score is 8317
13 players; last marble is worth 7999 points: high score is 146373
17 players; last marble is worth 1104 points: high score is 2764
21 players; last marble is worth 6111 points: high score is 54718
30 players; last marble is worth 5807 points: high score is 37305
"""
"""
puzzel input
412 players; last marble is worth 71646 points
"""

circle = [0,2,1]
elves = 412
gamelength = 71646*100
players = dict()

for i in range(elves):
    players[i] = 0

print players

active = 1

for marble in range(3,gamelength+1):
    if marble%1000 == 0:
        print marble, "of", gamelength, "; remaining:", gamelength-marble 
    # print "player:", marble%elves, "marble:", marble
    if marble%23:
        if (active+2)%len(circle) == 0:
            circle.append(marble)
        else:
            circle = circle[:(active+2)%len(circle)] + [marble] + circle[(active+2)%len(circle):]
        for i in range(len(circle)):
            if circle[i] == marble:
                active = i
    elif marble%23 == 0 and marble != 0:
        score = marble
        active = active-7
        if active < 0:
            active = len(circle)+active
        score += circle[active]
        players[marble%elves] += score
        circle = circle[:active] + circle[active+1:]

largest = 0
bestPlayer = 0
for each in players:
    print each, players[each]
    if players[each] > largest:
        largest = players[each]
        bestPlayer = each
print "winner", bestPlayer, largest
