import Main_1_Functions as f

with open("C:\Users\Jobber\Documents\Python Scripts\AdventofCode2018\Day12\Input.txt") as file:
    lines = []
    for line in file:
        # The rstrip method gets rid of the "\n" at the end of each line
        if line.rstrip().split(",") != ['']:
            lines.append(line.rstrip().split(","))
    for i in range(len(lines)):
        lines[i] = lines[i][0]
print lines

# split the input
grow_conditions = []
other_conditions = []

for each in lines:
    if "initial" in each:
        trash, start = each.split(": ")
    elif "=>" in each:
        if "=> #" in each:
            temp,trash = each.split(" =>")
            grow_conditions.append(temp)
        else:
            temp,trash = each.split(" =>")
            other_conditions.append(temp)

# create the pots
pots = f.row()
pots.plants = start
pots.grow_conditions = grow_conditions
pots.other_conditions = other_conditions

# grow the pots
i = 0
while i < 1001:
    i += 1
    pots.grow()
    if i % 1000 == 0:
        print pots
        print pots.score()

print 67000 * 50000000000/1000
