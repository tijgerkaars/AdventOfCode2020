with open("C:\Users\Jobber\Documents\Python Scripts\AdventofCode2018\Day3\input.txt") as file:
    lines = []
    for line in file:
        # The rstrip method gets rid of the "\n" at the end of each line
        lines.append(line.rstrip().split("."))
# lines = [["#1 @ 1,3: 4x4"],["#2 @ 3,1: 4x4"],["#3 @ 5,5: 2x2"]]
print lines
claims = []
counter = 0
for each in lines:
    counter += 1
    trash,temp = each[0].split("@ ")
    pos,dim = temp.split(": ")
    x,y = pos.split(",")
    width,heigth = dim.split("x")
    claims.append([[int(x),int(y)],[int(width),int(heigth)]])
print "claims:", claims

fabric = []
for i in range(1000):
    fabric.append([])
    for j in range(1000):
        fabric[i].append(0)

for claim in claims:
    for x in range(claim[1][0]):
        for y in range(claim[1][1]):
            fabric[y+claim[0][1]][x+claim[0][0]] += 1
print "done cutting"
overClaimed = 0
for each in fabric:
    for inch in each:
        if inch > 1:
            overClaimed += 1
print "overClaimed:", overClaimed
