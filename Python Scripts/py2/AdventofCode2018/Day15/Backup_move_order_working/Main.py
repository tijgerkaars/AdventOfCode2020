import Classes as c

with open("C:\Users\Jobber\Documents\Python Scripts\AdventofCode2018\Day15\Test_Input_Move2.txt") as file:
    lines = []
    for line in file:
        # The rstrip method gets rid of the "\n" at the end of each line
        if line.rstrip().split(",") != ['']:
            lines.append(line.rstrip().split(","))
    for i in range(len(lines)):
        lines[i] = lines[i][0]

dungeon = []
g = 1
e = 1
for i in range(len(lines)):
    lines[i] = lines[i].split(" ")[0]
    dungeon.append([])
    for each in lines[i]:
        if each in ["e","E"]:
            temp = c.entity(each)
            temp.number = str(e)
            dungeon[i].append(temp)
            e += 1
        elif each in ["g","G"]:
            temp = c.entity(each)
            temp.number = str(g)
            dungeon[i].append(temp)
            g += 1
        elif each == "#":
            dungeon[i].append(c.entity(each))

        else:
            dungeon[i].append(c.entity())

dungeon = c.dungeon(dungeon)

view = 3
for i in range(view):
    print "round " + str(i+1)
    if i+1 == view:
        dungeon.debug = True
    dungeon.round()
    print dungeon
    print "______________"
