import Classes as c

with open("C:\Users\Jobber\Documents\Python Scripts\AdventofCode2018\Day15\Input.txt") as file:
    lines = []
    for line in file:
        # The rstrip method gets rid of the "\n" at the end of each line
        if line.rstrip().split(",") != ['']:
            lines.append(line.rstrip().split(","))
    for i in range(len(lines)):
        lines[i] = lines[i][0]

dungeon = c.dungeon(lines)
print "starting state:"
print dungeon
print "--------"
result = dungeon.play()
print "end score:", result
print dungeon
