#---------------------------------------------------------------------------
"""
09 players; last marble is worth 0025 points: high score is 0032
10 players; last marble is worth 1618 points: high score is 8317
13 players; last marble is worth 7999 points: high score is 146373
17 players; last marble is worth 1104 points: high score is 2764
21 players; last marble is worth 6111 points: high score is 54718
30 players; last marble is worth 5807 points: high score is 37305
"""
circle = []
elves = 9
gamelength = 25
players = dict()

for i in range(elves):
    players[i+1] = 0

print "-"
circle = [0,1]
active = 1
for i in range(len(circle),gamelength+1):
    if i%23 != 0:
        if active+2 <= len(circle):
            circle = circle[:active+2] + [i] + circle[active+2:]
        else:
            circle = circle[:(active+2)%len(circle)] + [i] + circle[(active+2)%len(circle):]

        for j in range(len(circle)):
            if circle[j] == i:
                active = j
    else:
        if i%elves != 0:
            players[i%elves+1] = i +circle[(active-7)%len(circle):][:1][0]
        else:
            players[elves] = i +circle[(active-7)%len(circle):][:1][0]
        score = circle[(active-7)%len(circle):][:1][0]
        for j in range(len(circle)):
            if circle[j] == score:
                circle.remove(score)
                active = j
                break
    print "Marbel:", i, "player:", i%elves+1, circle[:active], [circle[active]], circle[active+1:]


for each in players:
    print each, players[each]
