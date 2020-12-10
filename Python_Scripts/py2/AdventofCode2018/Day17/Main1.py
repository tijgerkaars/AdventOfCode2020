import Periferals as p

from datetime import datetime
start_time = datetime.now()

inputs = ["Test_Input.txt","Input.txt"]
input = "AdventofCode2018\Day17\\" + inputs[1]
with open(input) as file:
    lines = []
    for line in file:
        lines.append(line.rstrip())

print ("clay inputs:", len(lines))
print ("lines", lines)

chart = dict()
chart["x"] = dict()
chart["y"] = dict()

# parse the input into x,y clusters
for i,line in enumerate(lines):
    one,two = line.split(",")
    one = one.split("=")
    trash,two = two.split("=")
    two = two.split("..")
    axis, on_axis_location = one
    if int(one[1]) in chart[one[0]]:
        chart[one[0]][int(one[1])].append([int(two[0]),int(two[1])])
    else:
        chart[one[0]][int(one[1])] = [[int(two[0]),int(two[1])]]
    # chart[one[0]][int(one[1])] = [int(two[0]),int(two[1])]

# add a point for all the spaces between
coords = []
for axis in chart:
    for each in chart[axis]:
        for j,each2 in enumerate(chart[axis][each]):
            x = each2
            temp = []
            for i in range(max(x) - min(x) +1):
                temp.append(min(x) + i)
            if j == 0:
                chart[axis][each] = [temp]
            else:
                chart[axis][each].append(temp)

# change the coords from a dict[y][x] into list[(y,x),(y,x)]
for axis in chart:
    for row in chart[axis]:
        for chunk in chart[axis][row]:
            for each in chunk:
                if axis == "y":
                    coords.append((row,each))
                else:
                    coords.append((each,row))

print ("chart:", chart)
print (len(coords), "coords:", coords)

# the starting point for the flow
well = [0,500]
print (datetime.now() - start_time, "starting to draw map")
# create the map
water_map = p.ground(coords,well)
print (datetime.now() - start_time, "Finished drawing map")


print (datetime.now() - start_time, "Starting water flow")
# flow the water till de depthfirst search Finished all branches
# while true/break because the starting condition is also the ending condition
while True:
    water_map.create_water()
    # print water_map
    if water_map.water_head == water_map.well_cube:
        break
print (datetime.now() - start_time, "Finished flowing water")

print (water_map.reachable())
print (water_map)
# checks the amount of tiles that have had water in the "|" and that have setteled water "~"
# and the total
print (water_map.reachable())
# between 10199 / 27334
# not 27189
