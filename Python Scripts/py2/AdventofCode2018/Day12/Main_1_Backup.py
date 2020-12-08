with open("C:\Users\Jobber\Documents\Python Scripts\AdventofCode2018\Day12\Test_Input.txt") as file:
    lines = []
    for line in file:
        # The rstrip method gets rid of the "\n" at the end of each line
        if line.rstrip().split(",") != ['']:
            lines.append(line.rstrip().split(","))
    for i in range(len(lines)):
        lines[i] = lines[i][0]
print lines
start = None
grow_conditions = []
other_conditions = []

class pot():
    def __init__(self,plant,id):
        self.plant = plant
        self.id = id

# split the input into the initial state and the grow_conditions
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

print grow_conditions
print other_conditions
conditions = (grow_conditions,other_conditions)
import Main_1_Functions as f

start = f.pad(start)
print len(start), start, "\n"

state = start
for i in range(20):
    print state
    state = f.grow(state,conditions)
    state = f.pad(state)
print "test:", state

state = state[4:]
print "test:", state
plants = 0
for i in range(len(state)):
    if state[i] == "#":
        plants += (i-2)
print plants

fail = [3149]
if plants in fail:
    print "you fucked it"
else:
    print "might be it"
#----------------------------------------------------------
"""
 0: ...#..#.#..##......###...###...........
 1: ...#...#....#.....#..#..#..#...........
 2: ...##..##...##....#..#..#..##..........
 3: ..#.#...#..#.#....#..#..#...#..........
 4: ...#.#..#...#.#...#..#..##..##.........
 5: ....#...##...#.#..#..#...#...#.........
 6: ....##.#.#....#...#..##..##..##........
 7: ...#..###.#...##..#...#...#...#........
 8: ...#....##.#.#.#..##..##..##..##.......
 9: ...##..#..#####....#...#...#...#.......
10: ..#.#..#...#.##....##..##..##..##......
11: ...#...##...#.#...#.#...#...#...#......
12: ...##.#.#....#.#...#.#..##..##..##.....
13: ..#..###.#....#.#...#....#...#...#.....
14: ..#....##.#....#.#..##...##..##..##....
15: ..##..#..#.#....#....#..#.#...#...#....
16: .#.#..#...#.#...##...#...#.#..##..##...
17: ..#...##...#.#.#.#...##...#....#...#...
18: ..##.#.#....#####.#.#.#...##...##..##..
19: .#..###.#..#.#.#######.#.#.#..#.#...#..
20: .#....##....#####...#######....#.#..##.
    .#....##....#####...#######....#.#..##...
"""
"""
....##.##..###.##.#..#..#####..#.##.#.#.....##.##..#..#....#..#....##.##.##.#.#..##.###.#..#..###..###.#.#...
...#

"""
