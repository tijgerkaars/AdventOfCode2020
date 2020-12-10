with open("C:\Users\Jobber\Documents\Python Scripts\AdventofCode2018\Day10\Test_Input.txt") as file:
    lines = []
    for line in file:
        # The rstrip method gets rid of the "\n" at the end of each line
        lines.append(line.rstrip().split(">"))
    lights = []
    for point in lines:
        trash,pos = point[0].split("<")
        x,y = pos.split(", ")
        trash,vel = point[1].split("<")
        x1,y1 = vel.split(", ")
        lights.append([int(x),int(y),(int(x1),int(y1))])
print lights


if True:
    with open("C:\Users\Jobber\Documents\Python Scripts\AdventofCode2018\Day10\Input.txt") as file:
        lines = []
        for line in file:
            # The rstrip method gets rid of the "\n" at the end of each line
            lines.append(line.rstrip().split(">"))
        lights = []
        for point in lines:
            trash,pos = point[0].split("<")
            x,y = pos.split(", ")
            trash,vel = point[1].split("<")
            x1,y1 = vel.split(", ")
            lights.append([int(x),int(y),(int(x1),int(y1))])
    print lights


def findSize(lights, extra = False):
    x_range = 0
    y_range = 0
    x_small = 0
    x_large = 0
    y_small = 0
    y_large = 0
    for each in lights:
        if each[0] > x_large:
            x_large = each[0]
        elif each[0] < x_small:
            x_small = each[0]
        if each[1] > y_large:
            y_large = each[1]
        elif each[1] < y_small:
            y_small = each[1]
    x_range = abs(x_large-x_small)
    y_range = abs(y_large-y_small)
    if not extra:
        return x_range, y_range
    else:
        return x_range, y_range, x_small ,y_small


def pprint(lights):
    width,heigth,x_small,y_small = findSize(lights,True)
    width += 1
    heigth += 1
    temp = []
    for each in lights:
        temp.append([each[0]+abs(x_small),each[1]+abs(y_small)])
    str = ""
    for y in range(heigth):
        for x in range(width):
            if [x,y] in temp:
                str += "#"
            else:
                str += "."
        str += "\n"
    print str



x,y = findSize(lights)
time = 0
while True:
    for i in range(len(lights)):
        lights[i][0] = lights[i][0] + lights[i][2][0]
        lights[i][1] = lights[i][1] + lights[i][2][1]
    x1,y1 = findSize(lights)
    time += 1
    if time > 10000:
        print time
    if x < x1 or y < y1:
        break
    x,y = x1,y1


for each in lights:
    each[0] = each[0] - each[2][0]
    each[1] = each[1] - each[2][1]


pprint(lights)
print time
