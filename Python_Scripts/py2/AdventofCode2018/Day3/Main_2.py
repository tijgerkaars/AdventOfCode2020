with open("C:\Users\Jobber\Documents\Python Scripts\AdventofCode2018\Day3\input.txt") as file:
    lines = []
    for line in file:
        # The rstrip method gets rid of the "\n" at the end of each line
        lines.append(line.rstrip().split("."))
#lines = [["#1 @ 1,3: 4x4"],["#2 @ 3,1: 4x4"],["#3 @ 5,5: 2x2"],["#4 @ 6,6: 3x3"], ["#4 @ 0,0: 2x2"]]
print lines
claims = []
counter = 0
for each in lines:
    counter += 1
    trash,temp = each[0].split("@ ")
    pos,dim = temp.split(": ")
    x,y = pos.split(",")
    width,heigth = dim.split("x")
    claims.append([[int(x),int(y)],[int(heigth),int(width)]])
    if counter == -1:
        break
print "topcornerX: claim[0][0], topcornerY: claim[0][1], claimHeigth: claim[1][0], claimWidth: claim[1][1]"

fabric = []
for i in range(1000):
    fabric.append([])
    for j in range(1000):
        fabric[i].append(0)

print "\nstarting cutting"

for claim in claims:
    x  = claim[0][1]
    y = claim[0][0]
    for claimY in range(claim[1][1]):
        for claimX in range(claim[1][0]):
            fabric[y+claimY][x+claimX] += 1

perfectSlice = []

for claim in claims:
    undamaged = True
    x  = claim[0][1]
    y = claim[0][0]
    for claimY in range(claim[1][1]):
        for claimX in range(claim[1][0]):
            if fabric[y+claimY][x+claimX] > 1:
                undamaged = False
    if undamaged:
        perfectSlice.append(claim)
print "perfectSlice:", perfectSlice

for each in perfectSlice:
    print "each:", each, "\n"
    #slice = str(claims[i][0][0]) + "," + str(claims[i][0][1]) + ": " + str(claims[i][1][1]) + "x" + str(claims[i][1][0])
    for i in range(len(claims)):
        if claims[i] == each:
            print "claim: #", i+1, claims[i]
        #temp = str(claims[i][0][0]) + "," + str(claims[i][0][1]) + ": " + str(claims[i][1][1]) + "x" + str(claims[i][1][0])
